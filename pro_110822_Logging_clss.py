import logging
import os
import inspect



class Log:
  def __init__(self, fileNameLength) -> None:
    logging.getLogger().setLevel(logging.NOTSET)
    self.file_name = inspect.stack()[1].filename
    self.file_name = self.file_name.split('\\')[-1]
    self.logger = logging.getLogger(self.file_name)

    logFormat = logging.Formatter(f'%(asctime)s | %(name){fileNameLength}s | %(levelname)8s | %(message)s')

    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler('file.log')
    c_handler.setFormatter(logFormat)
    f_handler.setFormatter(logFormat)

    self.logger.addHandler(c_handler)
    self.logger.addHandler(f_handler)

  def _get_call_trace(self)-> str:
    trace_ = ''
    for i in range(2, len(inspect.stack())):
      if (inspect.stack()[i][3] == '<module>'):
        break
      trace_ = trace_ + ' -> ' + inspect.stack()[i][3]

    trace_ = trace_[4:]
    trace_ = trace_ + ': '
    return trace_


  def info(self, message):
    trace_ = self._get_call_trace()
    log = trace_ + message
    self.logger.info(log)


  def debug(self, message):
    trace_ = self._get_call_trace()
    log = trace_ + message
    self.logger.debug(log)


  def warning(self, message):
    trace_ = self._get_call_trace()
    log = trace_ + message
    self.logger.warning(log)


  def error(self, message):
    trace_ = self._get_call_trace()
    log = trace_ + message
    self.logger.error(log)


  def critical(self, message):
    trace_ = self._get_call_trace()
    log = trace_ + message
    self.logger.critical(log)


  def exception(self, message):
    trace_ = self._get_call_trace()
    log = trace_ + message
    self.logger.exception(log)


    




# log = Log(8)

# log.debug('this is debug')
# log.info('this is info')
# log.warning('this is warning')
# log.error('this is error')
# log.critical('this is critical')







  







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