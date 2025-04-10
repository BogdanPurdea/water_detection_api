import ee
from api.modules.processing.water_detection import detect_water_ndwi
from api.modules.processing.water_coverage import calculate_water_coverage
from api.modules.processing.geojson_format import convert_water_mask_to_geojson

def create_grid_cells(coordinates, cell_size_degrees=0.1):
    """
    Create a grid of cells from the input coordinates.
    
    Args:
        coordinates: List of coordinates defining the area
        cell_size_degrees: Size of each cell in degrees (default: 0.1° ≈ 11km)
    
    Returns:
        List of cell coordinates
    """
    # Get bounding box of input coordinates
    lons = [coord[0] for coord in coordinates]
    lats = [coord[1] for coord in coordinates]
    min_lon, max_lon = min(lons), max(lons)
    min_lat, max_lat = min(lats), max(lats)
    
    # Create grid cells
    cells = []
    current_lon = min_lon
    while current_lon < max_lon:
        current_lat = min_lat
        while current_lat < max_lat:
            cell = [
                [current_lon, current_lat],
                [current_lon + cell_size_degrees, current_lat],
                [current_lon + cell_size_degrees, current_lat + cell_size_degrees],
                [current_lon, current_lat + cell_size_degrees],
                [current_lon, current_lat]
            ]
            cells.append(cell)
            current_lat += cell_size_degrees
        current_lon += cell_size_degrees
    
    return cells

def process_grid_cell(cell_coordinates, start_date, end_date, ndwi_threshold=0.3):
    """
    Process a single grid cell to calculate NDWI mean, water mask, and coverage.
    
    Args:
        cell_coordinates: Coordinates of the cell
        start_date: Start date in 'YYYY-MM-DD' format
        end_date: End date in 'YYYY-MM-DD' format
        ndwi_threshold: NDWI threshold for water detection
    
    Returns:
        Dictionary containing cell data including water mask
    """
    # Calculate NDWI and water mask for the cell
    ndwi_mean, water_mask = detect_water_ndwi(
        coordinates=cell_coordinates,
        start_date=start_date,
        end_date=end_date,
        ndwi_threshold=ndwi_threshold
    )
    
    # Calculate water coverage for the cell
    cell_geometry = ee.Geometry.Polygon(cell_coordinates)
    water_coverage = calculate_water_coverage(water_mask, cell_geometry)
    
    # Get mean NDWI value for the cell
    ndwi_value = ndwi_mean.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=cell_geometry,
        scale=30,
        maxPixels=1e9
    ).get('NDWI').getInfo()
    
    # Convert water mask to GeoJSON
    water_mask_geojson = convert_water_mask_to_geojson(water_mask, ndwi_mean, cell_coordinates, start_date, end_date, "NDWI")
    
    return {
        "type": "Feature",
        "geometry": {
            "type": "Polygon",
            "coordinates": [cell_coordinates]
        },
        "properties": {
            "ndwi_mean": ndwi_value,
            "water_coverage": water_coverage,
            "start_date": start_date,
            "end_date": end_date,
            "water_mask": water_mask_geojson
        }
    }

def process_grid(coordinates, start_date, end_date, cell_size_degrees=0.1, ndwi_threshold=0.3):
    """
    Process the entire area as a grid of cells.
    
    Args:
        coordinates: List of coordinates defining the area
        start_date: Start date in 'YYYY-MM-DD' format
        end_date: End date in 'YYYY-MM-DD' format
        cell_size_degrees: Size of each cell in degrees
        ndwi_threshold: NDWI threshold for water detection
    
    Returns:
        GeoJSON FeatureCollection containing all cells
    """
    # Create grid cells
    cells = create_grid_cells(coordinates, cell_size_degrees)
    
    # Process each cell
    features = []
    for cell in cells:
        try:
            cell_data = process_grid_cell(cell, start_date, end_date, ndwi_threshold)
            features.append(cell_data)
        except Exception as e:
            print(f"Error processing cell: {e}")
            continue
    
    # Create FeatureCollection
    return {
        "type": "FeatureCollection",
        "features": features,
        "properties": {
            "start_date": start_date,
            "end_date": end_date,
            "cell_size_degrees": cell_size_degrees,
            "total_cells": len(features)
        }
    } 