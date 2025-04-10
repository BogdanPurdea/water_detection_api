import ee
from api.modules.data_retrievers import get_sentinel1_collection, get_sentinel2_collection

def detect_water_from_satellite(coordinates, start_date, end_date, source, bands=None, index_name=None, threshold=0):
    """
    Detect water bodies using either optical (Sentinel-2) or radar (Sentinel-1) satellite imagery.

    Args:
        coordinates (list): List of coordinates defining the ROI
        start_date (str): Start date in 'YYYY-MM-DD' format
        end_date (str): End date in 'YYYY-MM-DD' format
        source (str): Data source ('S2' for Sentinel-2, 'S1' for Sentinel-1)
        bands (tuple): Sentinel-2 bands for indices (e.g., ('B3', 'B8') for NDWI)
        index_name (str): Name of the water index ('NDWI', 'MNDWI', or 'VH')
        threshold (float): Threshold for water classification

    Returns:
        tuple: (index_mean, water_mask)
            - index_mean: Mean values of the water index
            - water_mask: Binary water mask (1 = water, 0 = non-water)
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

        # Improved VH processing for water detection
        vh_backscatter = sentinel1.select('VH').map(
            lambda image: ee.Image(10).multiply(image.log10())
                .rename('VH_dB')
                # Apply speckle filter
                .focal_median(radius=30, units='meters')
                # Additional smoothing
                .focal_mean(radius=30, units='meters')
        )

        # Take temporal mean
        vh_mean = vh_backscatter.mean()

        # Resample to 30m and clip to ROI
        vh_resampled = vh_mean.reproject(crs='EPSG:4326', scale=30).clip(roi)
        
        # Create water mask using improved threshold
        # Water typically has very low backscatter in VH (usually below -20 dB)
        water_mask = vh_resampled.lt(-20).rename("VH_filtered_water_mask")

        index_mean = vh_resampled
    else:
        raise ValueError("Invalid source. Choose 'S2' for Sentinel-2 or 'S1' for Sentinel-1.")

    return index_mean, water_mask

def detect_water_ndwi(coordinates, start_date, end_date, ndwi_threshold=0.3):
    """
    Detect water bodies using Normalized Difference Water Index (NDWI) from Sentinel-2.
    NDWI uses green and NIR bands and is better for detecting open water bodies.
    
    Args:
        coordinates: Area coordinates defining region of interest
        start_date: Start date in 'YYYY-MM-DD' format
        end_date: End date in 'YYYY-MM-DD' format
        ndwi_threshold: NDWI threshold (default: 0.3)
            - Values > 0.3 typically indicate water
            - Higher values = more confident water detection
            - Range: -1 to 1
    
    Returns:
        tuple: (ndwi_mean, water_mask)
            - ndwi_mean: Mean NDWI values over time period
            - water_mask: Binary water mask (1 = water, 0 = non-water)
    """
    return detect_water_from_satellite(
        coordinates=coordinates,
        start_date=start_date,
        end_date=end_date,
        source="S2",
        bands=('B3', 'B8'),  # B3=green (0.56µm), B8=NIR (0.84µm)
        index_name="NDWI",
        threshold=ndwi_threshold
    )

def detect_water_mndwi(coordinates, start_date, end_date, mndwi_threshold=0.2):
    """
    Detect water bodies using Modified NDWI (MNDWI) from Sentinel-2.
    MNDWI uses green and SWIR bands and is better for turbid water and built-up areas.
    
    Args:
        coordinates: Area coordinates defining region of interest
        start_date: Start date in 'YYYY-MM-DD' format
        end_date: End date in 'YYYY-MM-DD' format
        mndwi_threshold: MNDWI threshold (default: 0.2)
            - Values > 0.2 typically indicate water
            - Higher values = more confident water detection
            - Range: -1 to 1
    
    Returns:
        tuple: (mndwi_mean, water_mask)
            - mndwi_mean: Mean MNDWI values over time period
            - water_mask: Binary water mask (1 = water, 0 = non-water)
    """
    return detect_water_from_satellite(
        coordinates=coordinates,
        start_date=start_date,
        end_date=end_date,
        source="S2",
        bands=('B3', 'B11'),  # B3=green (0.56µm), B11=SWIR (1.61µm)
        index_name="MNDWI",
        threshold=mndwi_threshold
    )

def detect_water_radar(coordinates, start_date, end_date, vh_threshold=-20):
    """
    Detect water bodies using VH polarization from Sentinel-1 radar.
    Radar detection works through clouds but may have noise in urban areas.
    
    Args:
        coordinates: Area coordinates defining region of interest
        start_date: Start date in 'YYYY-MM-DD' format
        end_date: End date in 'YYYY-MM-DD' format
        vh_threshold: VH backscatter threshold in dB (default: -20)
            - Values < -20 dB typically indicate water
            - Lower values = more confident water detection
            - Typical range: -25 to -15 dB for water
    
    Returns:
        tuple: (vh_backscatter, water_mask)
            - vh_backscatter: Mean VH backscatter values in dB
            - water_mask: Binary water mask (1 = water, 0 = non-water)
    """
    return detect_water_from_satellite(
        coordinates=coordinates,
        start_date=start_date,
        end_date=end_date,
        source="S1",
        threshold=vh_threshold
    )
