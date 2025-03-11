import ee

def convert_mask_to_geojson(mask, mean_index, coordinates, start_date, end_date, index_name):
    """
    Converts a water/flood mask to GeoJSON format using reduceToVectors.

    Args:
        mask (ee.Image): Water or flood mask image.
        mean_index (ee.Image): Mean spectral index image (NDWI, MNDWI, etc.).
        coordinates (list): List of coordinates defining the ROI.
        start_date (str): Start date of analysis (YYYY-MM-DD).
        end_date (str): End date of analysis (YYYY-MM-DD).
        index_name (str): Name of the spectral index used (e.g., 'NDWI', 'MNDWI', 'VH').

    Returns:
        dict: Mask in GeoJSON format with metadata stored in the FeatureCollection.
    """
    # Define ROI
    roi = ee.Geometry.Polygon(coordinates)

    # Convert the mask to vectors (polygons)
    vectors = mask.reduceToVectors(
        geometry=roi,
        scale=30,  # Resolution of the mask
        geometryType='polygon',  # Output as polygons
        eightConnected=False,  # Use 4-connected pixel rule
        labelProperty='value',  # Property to store the pixel value
        maxPixels=1e13  # Increase if needed
    )

    # Function to add the mean index value to each feature
    def add_index_mean(feature):
        index_value = mean_index.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=feature.geometry(),
            scale=30,
            maxPixels=1e13
        ).get(index_name)  # Get the mean index value

        return feature.set(f'{index_name.lower()}_mean', index_value)

    # Apply the function to all vector features
    merged_features = vectors.map(add_index_mean)

    # Convert to GeoJSON
    geojson = merged_features.getInfo()

    # Add metadata to the FeatureCollection level
    geojson["properties"] = {
        "index_name": index_name,
        "start_date": start_date,
        "end_date": end_date,
        "coordinates": coordinates  # Store ROI coordinates for reference
    }

    return geojson

def ndwi_mask_to_geojson(ndwi_mask, ndwi_mean, coordinates, start_date, end_date):
    """Wrapper for NDWI-based water mask conversion to GeoJSON."""
    return convert_mask_to_geojson(ndwi_mask, ndwi_mean, coordinates, start_date, end_date, "NDWI")


def mndwi_mask_to_geojson(mndwi_mask, mndwi_mean, coordinates, start_date, end_date):
    """Wrapper for MNDWI-based water mask conversion to GeoJSON."""
    return convert_mask_to_geojson(mndwi_mask, mndwi_mean, coordinates, start_date, end_date, "MNDWI")


def vh_mask_to_geojson(vh_mask, vh_mean, coordinates, start_date, end_date):
    """Wrapper for VH-based water mask conversion to GeoJSON (Sentinel-1)."""
    return convert_mask_to_geojson(vh_mask, vh_mean, coordinates, start_date, end_date, "VH_filtered")
