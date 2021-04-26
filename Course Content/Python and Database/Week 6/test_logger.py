from logger_example import console_logger, file_logger


    
def in_code_logger():
    console_logger.warning("warning test")
    file_logger.error("application test")
    
    
def config_file_logger():
    import logging
    import logging.config
    logging.config.fileConfig('logging_config.ini')
    logger = logging.getLogger('from_config_file')
    
    logger.debug('From config file logger.')
    
if __name__ == "__main__":
    in_code_logger()
    config_file_logger()