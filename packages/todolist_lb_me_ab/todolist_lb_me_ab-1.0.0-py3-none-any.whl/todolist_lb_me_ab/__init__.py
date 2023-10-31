import logging

# Initialize the root logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)  # Set the root logger to the lowest level

# Create debug log handler
debug_handler = logging.FileHandler('debug_logs.txt')
debug_handler.setLevel(logging.DEBUG)
debug_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
debug_handler.setFormatter(debug_format)
logger.addHandler(debug_handler)

# Create error log handler
error_handler = logging.FileHandler('error_logs.txt')
error_handler.setLevel(logging.ERROR)
error_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
error_handler.setFormatter(error_format)
logger.addHandler(error_handler)
