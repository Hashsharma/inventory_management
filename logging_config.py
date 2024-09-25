# your_app_name/logging_config.py

import logging

def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(levelname)s %(asctime)s %(module)s %(message)s',
    )

    logger = logging.getLogger('inventory_mgmt')
    return logger
