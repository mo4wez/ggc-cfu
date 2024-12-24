import logging

def get_logger(name):
    # Create a logger
    logger = logging.getLogger(name)
    
    # Set the logging level (change to DEBUG, INFO, WARNING, ERROR, etc. as needed)
    logger.setLevel(logging.DEBUG)
    
    # Create console handler and set level
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    
    # Create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    
    # Add the handler to the logger if it doesn't already have it
    if not logger.hasHandlers():
        logger.addHandler(ch)
    
    return logger