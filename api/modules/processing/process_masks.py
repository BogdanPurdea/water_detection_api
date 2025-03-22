import ee
from api.modules.data_retrievers import get_sentinel1_collection, get_sentinel2_collection

def calculate_water_mask(coordinates, start_date, end_date, source, bands=None, index_name=None, threshold=0):
    """
    Generalized function to compute a water mask from Sentinel-1 or Sentinel-2 imagery.

    Args:
        coordinates (list): List of coordinates defining the ROI.
        start_date (str): Start date in 'YYYY-MM-DD' format.
        end_date (str): End date in 'YYYY-MM-DD' format.
        source (str): Data source ('S2' for Sentinel-2, 'S1' for Sentinel-1).
        bands (tuple): Sentinel-2 bands for NDWI/MNDWI (e.g., ('B3', 'B8') for NDWI).
        index_name (str): Name of the index ('NDWI', 'MNDWI', or 'VH').
        threshold (float): Threshold for water mask classification.

    Returns:
        ee.Image: Computed water mask.
    """
    # Define ROI
    roi = ee.Geometry.Polygon(coordinates)

    if source == "S2":
        # Load Sentinel-2 imagery
        sentinel2 = get_sentinel2_collection(roi, start_date, end_date)

        if sentinel2.size().getInfo() == 0:
            raise ValueError(f"No Sentinel-2 images found for {index_name} computation in the given date range.")

        # Compute NDWI or MNDWI
        index = sentinel2.map(lambda image: image.normalizedDifference(bands).rename(index_name))
        index_mean = index.mean().clip(roi)

        # Create a binary water mask
        water_mask = index_mean.gt(threshold).rename(f"{index_name}_water_mask")

    elif source == "S1":
        # Load Sentinel-1 data
        sentinel1 = get_sentinel1_collection(roi, start_date, end_date)

        if sentinel1.size().getInfo() == 0:
            raise ValueError("No Sentinel-1 images found for the given date range and coordinates.")
        # Convert VH backscatter to decibels and apply a mean filter
        vh_decibels = sentinel1.select('VH').map(lambda image: ee.Image(10).multiply(image.log10()).rename('VH_dB'))
        print(vh_decibels.getInfo())
        vh_filtered = vh_decibels.map(lambda image: image.focal_mean(radius=3, units='pixels').rename('VH_filtered'))

        # Resample Sentinel-1 to 30m resolution
        vh_resampled = vh_filtered.mean().reproject(crs='EPSG:4326', scale=30)
        
        # Create water mask using Sentinel-1 VH
        water_mask = vh_resampled.lt(threshold).rename("VH_filtered_water_mask")

        index_mean = vh_resampled.clip(roi)
    else:
        raise ValueError("Invalid source. Choose 'S2' for Sentinel-2 or 'S1' for Sentinel-1.")

    return index_mean, water_mask

def s2_ndwi_water_mask(coordinates, start_date, end_date, ndwi_threshold=0):
    """ Wrapper for NDWI water mask computation. """
    return calculate_water_mask(coordinates, start_date, end_date, "S2", ('B3', 'B8'), "NDWI", ndwi_threshold)


def s2_mndwi_water_mask(coordinates, start_date, end_date, mndwi_threshold=0):
    """ Wrapper for MNDWI water mask computation. """
    return calculate_water_mask(coordinates, start_date, end_date, "S2", ('B3', 'B11'), "MNDWI", mndwi_threshold)


def s1_vh_water_mask(coordinates, start_date, end_date, vh_threshold=1.25):
    """ Wrapper for Sentinel-1 VH-based water mask computation. """
    return calculate_water_mask(coordinates, start_date, end_date, "S1", threshold=vh_threshold)
