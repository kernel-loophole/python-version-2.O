from asyncio.log import logger
import logging 
import logging.config
logging.basicConfig(filename='logging_out.log',level=logging.INFO)

for i in range(0,10):
    logger=logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    ch=logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter=logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # logging.getLogger('simple')
    # logging.config.fileConfig('logging.conf')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    logger.debug("debugging")
    logger.warning("waring")
    logger.info("info")