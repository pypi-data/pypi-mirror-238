from .client import Client
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("started RuKassa")
logger.info("RuKassa - basic donate")