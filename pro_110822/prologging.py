import logging
import time
import inspect
import os

logging.getLogger().setLevel(logging.NOTSET)

class Log:
  def __init__(self, fileNameLength) -> None:
    self.file_name = inspect.stack()[1].filename
    self.file_name = self.file_name.split('\\')[-1]
    self.logger = logging.getLogger(self.file_name)


    logFormat = logging.Formatter(f'%(asctime)s | %(name){fileNameLength}s | %(levelname)8s | %(message)s')


    c_handler = logging.StreamHandler()

    logFileName = time.strftime("%Y%m%d-%H_%M_%S") + '.log'
    logFileDirectory = self._create_log_directory(inspect.stack()[1].filename)

    f_handler = logging.FileHandler(logFileDirectory + "\\" + logFileName)
    c_handler.setFormatter(logFormat)
    f_handler.setFormatter(logFormat)

    self.logger.addHandler(c_handler)
    self.logger.addHandler(f_handler)

  def _create_log_directory(self, path):
    pathList = path.split('\\')[:-1]
    logDirectory = "\\".join(pathList)
    logDirectory = logDirectory + "\\logs"
    try:
      os.mkdir(logDirectory) 
    except FileExistsError:
      pass
    return logDirectory


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

