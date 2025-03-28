import ee

def calculate_water_coverage(water_mask, aoi):
    """
    Calculate water coverage percentage from a water mask
    
    Parameters:
    - water_mask: Binary water mask (0 or 1) from water detection
    - aoi: Area of interest geometry
    
    Returns:
    - Water coverage percentage
    """
    # Get the name of the band from the water mask
    band_name = water_mask.bandNames().get(0).getInfo()
    
    # Calculate the mean (which gives us the percentage of water pixels)
    water_coverage = water_mask.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=aoi,
        scale=10,  # Sentinel-2 resolution
        maxPixels=1e9
    )
    
    # Get the value using the correct band name
    coverage_value = water_coverage.get(band_name).getInfo()
    
    # Convert to percentage
    return coverage_value * 100 if coverage_value is not None else 0