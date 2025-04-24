# Flood Detection and Alert System - Bottom Layer

A FastAPI-based application that processes satellite data to detect flood events using Google Earth Engine.

## Features

- Water detection using multiple satellite data sources:
  - Sentinel-2 optical imagery (NDWI and MNDWI indices)
  - Sentinel-1 radar data (VH polarization)
- Grid-based analysis for better area coverage
- Multiple API endpoints for different processing needs
- Efficient data processing using Google Earth Engine

## API Endpoints

- `/get-s1-vh-mask` - Get water mask using Sentinel-1 radar data
- `/get-s2-ndwi-mask` - Get water mask using Sentinel-2 NDWI
- `/get-s2-mndwi-mask` - Get water mask using Sentinel-2 MNDWI
- `/get-grid-ndwi` - Get grid-based NDWI analysis
- `/get-grid-mndwi` - Get grid-based MNDWI analysis

## Setup

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Set up Google Earth Engine authentication:
   - Visit [Google Earth Engine](https://earthengine.google.com/) to sign up
   - Initialize Earth Engine authentication
   - Place your credentials in the appropriate location

## Running the Application

Start the server by running:

```bash
cd sat_bottom_layer
python server.py
```

The server will start at `http://127.0.0.1:8000`

## API Documentation

Once the server is running, visit `http://127.0.0.1:8000/docs` for the interactive API documentation.

## Requirements

All dependencies are listed in `requirements.txt`. Install them using pip as shown in the Setup section.
