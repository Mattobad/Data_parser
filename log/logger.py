import logging


def logger(name,log_level):
    # set logger
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    # set format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    #for stream logs
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    # add the stream handler
    logger.addHandler(stream_handler)


    return logger