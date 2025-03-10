import uvicorn
from fastapi import FastAPI
from api.modules.init_config import init_gee
from api.app import app

# Initialize GEE
init_gee()

# Run the API
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)