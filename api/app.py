from fastapi import FastAPI
from api.models.api_request import ApiRequest
from api.modules import handle_s1_vh_mask, handle_s2_ndwi_mask, handle_s2_mndwi_mask

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
