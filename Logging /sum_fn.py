import logging
def sum(x,y):
    
    
    logging.info("return from function")
    return x+y
def mul(x,y):
    logging.info("in mul function")
    return x*y

def sub(x,y):
    logging.info("in sub function")
    return abs(x-y)