from fastapi import FastAPI
from api.models.api_request import ApiRequest
from api.modules import handle_s1_vh_mask, handle_s2_ndwi_mask, handle_s2_mndwi_mask, handle_grid_ndwi, handle_grid_mndwi

app = FastAPI()

@app.post("/get-s1-vh-mask")
async def get_s1_vh_mask(request: ApiRequest):
    return await handle_s1_vh_mask(request)

@app.post("/get-s2-ndwi-mask")
async def get_s2_ndwi_mask(request: ApiRequest):
    return await handle_s2_ndwi_mask(request)

@app.post("/get-s2-mndwi-mask")
async def get_s2_mndwi_mask(request: ApiRequest):
    return await handle_s2_mndwi_mask(request)

@app.post("/get-grid-ndwi")
async def get_grid_ndwi(request: ApiRequest):
    return await handle_grid_ndwi(request)

@app.post("/get-grid-mndwi")
async def process_mndwi_grid(request: ApiRequest):
    """
    Process the area as a grid using MNDWI water detection
    """
    return await handle_grid_mndwi(request)
