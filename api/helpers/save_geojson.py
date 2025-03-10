import json

def save_geojson(geojson_data: dict, filename) -> None:
    """Save GeoJSON data to a file.
    
    Args:
        geojson_data: The GeoJSON data to save
        filename: The name of the file to save to
    """
    with open(filename, "w") as f:
        json.dump(geojson_data, f, indent=2)
