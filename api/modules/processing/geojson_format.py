import ee
from api.modules.processing.water_coverage import calculate_water_coverage

def convert_water_mask_to_geojson(mask, mean_index, coordinates, start_date, end_date, index_name):
    """
    Convert water detection results to GeoJSON format with water coverage statistics.

    Args:
        mask: Binary water mask image (1 = water, 0 = non-water)
        mean_index: Mean index values (NDWI, MNDWI, or VH backscatter)
        coordinates: List of coordinates defining the area
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)
        index_name: Name of the water index used ('NDWI', 'MNDWI', or 'VH_dB')

    Returns:
        dict: GeoJSON format containing:
            - Water body polygons
            - Mean index values for each polygon
            - Total water coverage percentage
            - Metadata about the detection
    """
    # Create area boundary
    roi = ee.Geometry.Polygon(coordinates)

    # Calculate water coverage percentage
    water_coverage_pct = calculate_water_coverage(mask, roi)

    # Convert the mask to polygons
    vectors = mask.reduceToVectors(
        geometry=roi,
        scale=30,  # Resolution in meters
        geometryType='polygon',
        eightConnected=False,
        labelProperty='value',
        maxPixels=1e13
    )
    # Add the average index value to each polygon
    def add_index_value(feature):
        mean_value = mean_index.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=feature.geometry(),
            scale=30,
            maxPixels=1e13
        ).get(index_name)
        
        return feature.set(f'{index_name.lower()}_mean', mean_value)

    # Apply the calculation to all polygons
    vectors_with_data = vectors.map(add_index_value)

    # Convert to GeoJSON format
    geojson = vectors_with_data.getInfo()

    # Add metadata including water coverage
    geojson["properties"] = {
        "index_name": index_name,
        "start_date": start_date,
        "end_date": end_date,
        "coordinates": coordinates,
        "source": "api",
        "water_coverage_percentage": water_coverage_pct  # Added water coverage
    }

    return geojson

def convert_optical_ndwi_to_geojson(ndwi_mask, ndwi_mean, coordinates, start_date, end_date):
    """
    Convert NDWI-based water detection results to GeoJSON.
    NDWI is better suited for detecting open water bodies.
    """
    return convert_water_mask_to_geojson(
        ndwi_mask, 
        ndwi_mean, 
        coordinates, 
        start_date, 
        end_date, 
        "NDWI"
    )

def convert_optical_mndwi_to_geojson(mndwi_mask, mndwi_mean, coordinates, start_date, end_date):
    """
    Convert MNDWI-based water detection results to GeoJSON.
    MNDWI is better suited for turbid water and built-up areas.
    """
    return convert_water_mask_to_geojson(
        mndwi_mask, 
        mndwi_mean, 
        coordinates, 
        start_date, 
        end_date, 
        "MNDWI"
    )

def convert_radar_water_to_geojson(vh_mask, vh_mean, coordinates, start_date, end_date):
    """
    Convert radar-based (Sentinel-1 VH) water detection results to GeoJSON.
    Radar detection works through clouds but may have noise in urban areas.
    """
    return convert_water_mask_to_geojson(
        vh_mask, 
        vh_mean, 
        coordinates, 
        start_date, 
        end_date, 
        "VH_dB"
    )
