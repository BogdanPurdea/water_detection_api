import ee
import logging

# Initialize GEE
def init_gee():
    ee.Authenticate()
    ee.Initialize(project="flood-detection-assessment")

# Set up logging
def init_logging():
    logging.basicConfig(level=logging.INFO)
    return logging.getLogger(__name__)

logger = init_logging()
