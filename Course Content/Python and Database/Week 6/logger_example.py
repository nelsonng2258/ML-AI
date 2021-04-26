import logging

# custom loggers
file_logger = logging.getLogger("file_logger")
console_logger = logging.getLogger("console_logger")

# custom handlers
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.WARNING)

file_handler = logging.FileHandler('app.log', mode='w')
file_handler.setLevel(logging.ERROR)

# custom formatters and adding them to the handlers
console_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
                                                 datefmt='%d-%b-%Y %H:%M:%S')

console_handler.setFormatter(console_format)
file_handler.setFormatter(file_format)

# adding the handlers to the logger
console_logger.addHandler(console_handler)
file_logger.addHandler(file_handler)