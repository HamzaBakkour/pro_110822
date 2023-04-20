import logging
import time
import inspect
import os
from functools import wraps
logging.getLogger().setLevel(logging.NOTSET)


def formatted_log_line(func):
  @wraps(func)
  def wrapper(*args, **kwargs):
    if isinstance(args[1], list):
      log = f'{", ".join(str(x) for x in args[1])}, '
    elif isinstance(args[1], str):
      log = args[1] + ', '
    else:
      raise ValueError(f'{args[1]} is of type: {type(args[1])}. Only str and list are accepted')
    wrapped = func(args[0], log, **kwargs)
    return wrapped
  return wrapper

class Log:
  def __init__(self, mode = '_CONSOLE_', disable = False) -> None:
    self.file_name = inspect.stack()[1].filename
    self.file_name = self.file_name.split('\\')[-1]
    self.logger = logging.getLogger(self.file_name)
    self.disable = disable


    logFormat = logging.Formatter(f'%(asctime)s | %(levelname)8s | {self.file_name[:-3]}, %(message)s')

    c_handler = logging.StreamHandler()

    if (mode == '_FILE_') or (mode == '_CONSOLE_FILE_'):
      logFileName = time.strftime("%Y%m%d-%H_%M_%S") + '.log'
      logFileDirectory = self._create_log_directory(inspect.stack()[1].filename)
      f_handler = logging.FileHandler(logFileDirectory + "\\" + logFileName)
      f_handler.setFormatter(logFormat)

    c_handler.setFormatter(logFormat)

    if mode == '_CONSOLE_':
      self.logger.addHandler(c_handler)
    elif mode == '_CONSOLE_FILE_':
      self.logger.addHandler(c_handler)
      self.logger.addHandler(f_handler)
    elif mode == '_FILE_':
      self.logger.addHandler(f_handler)
    else:
      raise ValueError(f'unknow mdoe -- {mode} --')




  def _create_log_directory(self, path):
    pathList = path.split('\\')[:-1]
    logDirectory = "\\".join(pathList)
    logDirectory = logDirectory + "\\logs"
    try:
      os.mkdir(logDirectory) 
    except FileExistsError:
      pass
    return logDirectory

  @formatted_log_line
  def info(self, where, message = 'NO LOG MESSAGE'):
      if self.disable:
        return
      self.logger.info(where + message + '\n')

  @formatted_log_line
  def debug(self, where, message = 'NO LOG MESSAGE'):
    if self.disable:
      return
    self.logger.debug(where + message + '\n')    

  @formatted_log_line
  def warning(self, where, message = 'NO LOG MESSAGE'):
    if self.disable:
      return
    self.logger.warning(where + message + '\n')  

  @formatted_log_line
  def error(self, where, message = 'NO LOG MESSAGE'):
    if self.disable:
      return
    self.logger.error(where + message + '\n')  

  @formatted_log_line
  def critical(self, where, message = 'NO LOG MESSAGE'):
    if self.disable:
      return
    self.logger.critical(where + message + '\n')  

  @formatted_log_line
  def exception(self, where, message = 'NO LOG MESSAGE'):
    if self.disable:
      return    
    self.logger.exception(where + message + '\n')  

# l = Log()

# l.info(['method 1', 'method 2'], message='rasing exption')

# l.info(['method 1', 'method 2'], message='rasing exption')


  # def info(self, where, message = 'NO LOG MESSAGE', new_line = True):
  # def debug(self, where, message = 'NO LOG MESSAGE', new_line = True):
  # def warning(self, where, message = 'NO LOG MESSAGE', new_line = True):
  # def error(self, where, message = 'NO LOG MESSAGE', new_line = True):
  # def critical(self, where, message = 'NO LOG MESSAGE', new_line = True):
  # def exception(self, where, message = 'NO LOG MESSAGE', new_line = True):

