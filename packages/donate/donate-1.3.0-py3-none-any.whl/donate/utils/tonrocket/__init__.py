from .client import Client
from .types.donate import Donate_init
from .types.user import User
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("started TonRocket")
logger.info("TonRocket - Crypto donate")