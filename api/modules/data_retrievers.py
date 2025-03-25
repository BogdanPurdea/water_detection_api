import ee

def get_sentinel2_collection(roi, start_date, end_date):
    """Retrieve Sentinel-2 imagery for the given parameters."""
    return ee.ImageCollection('COPERNICUS/S2_HARMONIZED') \
        .filterBounds(roi) \
        .filterDate(start_date, end_date) \
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 10)) \
        .limit(10)
        
def get_sentinel1_collection(roi, start_date, end_date):
    """Retrieve Sentinel-1 imagery for the given parameters."""
    return ee.ImageCollection('COPERNICUS/S1_GRD') \
        .filterBounds(roi) \
        .filterDate(start_date, end_date) \
        .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VH')) \
        .filter(ee.Filter.eq('instrumentMode', 'IW'))
