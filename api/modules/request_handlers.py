from fastapi import HTTPException
from api.models.api_request import ApiRequest
from api.modules.processing.water_detection import detect_water_radar, detect_water_ndwi, detect_water_mndwi
from api.modules.processing.geojson_format import convert_radar_water_to_geojson, convert_optical_ndwi_to_geojson, convert_optical_mndwi_to_geojson
from config.init_config import logger
from api.helpers.save_geojson import save_geojson

async def handle_s1_vh_mask(request: ApiRequest):
    try:
        logger.info("Received request: %s", request)

        vh_mean, flood_mask = detect_water_radar(
            coordinates=request.coordinates,
            start_date=request.start_date,
            end_date=request.end_date,
            vh_threshold=request.vh_threshold,
        )

        water_mask_geojson = convert_radar_water_to_geojson(flood_mask, vh_mean, request.coordinates,
                                            request.start_date, request.end_date)
        save_geojson(water_mask_geojson, "./data/s1_vh_water_mask.geojson")
        logger.info("Computed water mask successfully.")
        return water_mask_geojson

    except Exception as e:
        logger.error("An error occurred: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e))

async def handle_s2_ndwi_mask(request: ApiRequest):
    try:
        logger.info("Received request: %s", request)

        ndwi_mean, computed_water_mask = detect_water_ndwi(
            coordinates=request.coordinates,
            start_date=request.start_date,
            end_date=request.end_date,
            ndwi_threshold=request.ndwi_threshold
        )

        water_mask_geojson = convert_optical_ndwi_to_geojson(computed_water_mask, ndwi_mean, request.coordinates, 
                                                request.start_date, request.end_date)
        
        # save_geojson(water_mask_geojson, "./data/ndwi_water_mask.geojson")
        logger.info("Computed water mask successfully.")
        return water_mask_geojson

    except Exception as e:
        logger.error("An error occurred: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e))

async def handle_s2_mndwi_mask(request: ApiRequest):
    try:
        logger.info("Received request: %s", request)

        mndwi_mean, computed_water_mask = detect_water_mndwi(
            coordinates=request.coordinates,
            start_date=request.start_date,
            end_date=request.end_date,
            mndwi_threshold=request.mndwi_threshold
        )

        water_mask_geojson = convert_optical_mndwi_to_geojson(computed_water_mask, mndwi_mean, request.coordinates, 
                                                request.start_date, request.end_date)
        
        # save_geojson(water_mask_geojson, "./data/mndwi_water_mask.geojson")
        logger.info("Computed water mask successfully.")
        return water_mask_geojson

    except Exception as e:
        logger.error("An error occurred: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e))