# Flood Detection API

A FastAPI-based application that processes satellite data to detect flood events using Google Earth Engine.

## Setup

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Set up Google Earth Engine authentication
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
