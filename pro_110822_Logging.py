import logging
import os
import inspect





logging.getLogger().setLevel(logging.NOTSET)

# Create a custom logger
file_name = os.path.basename(__file__)

# print( file_name , f'{inspect.stack()[0][3]} | ', f'{inspect.stack()[1][3]} || ', 'RuntimeError (widget already deleted) -> passed')


logger = logging.getLogger(file_name)

# Create handlers
c_handler = logging.StreamHandler()
f_handler = logging.FileHandler('file.log')


_name_length_ = 5
_levelname_length_ = 8

# Create formatters and add it to handlers
format = logging.Formatter(f'%(asctime)s | %(name){_name_length_}s | %(levelname){_levelname_length_}s | %(message)s')
c_handler.setFormatter(format)
f_handler.setFormatter(format)

# Add handlers to the logger
logger.addHandler(c_handler)
logger.addHandler(f_handler)

logger.debug("debug message")
logger.info("info message")
logger.warning("warning message")
logger.error("error message")
logger.critical("critical message")
# name = 'John'
# logger.error(f'{name} raised an error')
# print()
a = 5
b = 0
try:
  c = a / b
except Exception as e:
  logger.exception("Exception occurred")








# c_handler.setLevel(logging.NOTSET)
# f_handler.setLevel(logging.NOTSET)






###################################################
# import logging
# # logging_example.py

# import logging

# # Create a custom logger
# logger = logging.getLogger(__name__)

# # Create handlers
# c_handler = logging.StreamHandler()
# f_handler = logging.FileHandler('file.log')
# c_handler.setLevel(logging.WARNING)
# f_handler.setLevel(logging.ERROR)

# # Create formatters and add it to handlers
# c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
# f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# c_handler.setFormatter(c_format)
# f_handler.setFormatter(f_format)

# # Add handlers to the logger
# logger.addHandler(c_handler)
# logger.addHandler(f_handler)

# logger.warning('This is a warning')
# logger.error('This is an error')
###################################################




###################################################
# import logging

# logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
# logging.basicConfig(format='%(process)d-%(levelname)s-%(message)s')
# logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
# logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
# logging.debug("debug message")
# logging.info("info message")
# logging.warning("warning message")
# logging.error("error message")
# logging.critical("critical message")
# name = 'John'
# logging.error(f'{name} raised an error')
# print()
# a = 5
# b = 0
# try:
#   c = a / b
# except Exception as e:
#   logging.exception("Exception occurred")
###################################################