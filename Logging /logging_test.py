import logging
import sum_fn
logging.basicConfig(filename='loging.log',encoding='utf-8',level=logging.INFO,format='%(asctime)s %(message)s')
logging.info("starting")
print(sum_fn.sum(10,10))
print(sum_fn.mul(10,9))
print(sum_fn.sub(10,20))
logging.info("ending")
# logging.warning("print on screen ")
# #this line not be printed
# #The INFO message doesn’t appear because the default level is WARNING.

# logging.info("info and not print")
# logging.critical("critical")
# logging.debug("debug")
# logging.error("error")