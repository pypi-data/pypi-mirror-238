import logging as _logging
import logging.handlers as handlers
import os
import socket

from skywalking.trace.context import get_context

from linker_atom.config import settings


class Logger(_logging.Logger):
    
    def __init__(self):
        pass
    
    def init_logger(
            self,
            name,
            log_dir='./logs',
            level=_logging.NOTSET,
            roate='midnight'
    ):
        """
        :param roate: when roate
        :param name: Name of the logger.
        :param log_name: Name of the log file.
        :param log_dir: The directory to save log files.
        :param level: Log level: The lowest level of log.
        :param Rotate: How to rotate log files.
        """
        super().__init__(name, level)
        formatter = _logging.Formatter(
            '%(levelname)s | %(asctime)s | %(pathname)s:%(lineno)d | %(funcName)s | %(message)s'
        )
        
        if not self.handlers:
            console_handler = _logging.StreamHandler()
            self.addHandler(console_handler)
            console_handler.setFormatter(formatter)
            hostname = socket.gethostname()
            logger_dir_path = os.path.join(log_dir, name, hostname)
            logger_file_path = os.path.join(logger_dir_path, 'access.log')
            os.makedirs(logger_dir_path, exist_ok=True)
            
            file_handler = handlers.TimedRotatingFileHandler(
                logger_file_path,
                when=roate,
                backupCount=int(os.getenv('LOG_BACKUP_COUNT', 30)),
                encoding="utf-8",
            )
            file_handler.suffix = "-%Y%m%d.log"
            self.addHandler(file_handler)
            file_handler.setFormatter(formatter)
    
    @property
    def trace_id(self) -> str:
        context = get_context()
        trace_id = str(context.segment.related_traces[0])
        return trace_id
    
    def debug(self, msg, *args, **kwargs) -> None:
        stack_level = kwargs.pop('stacklevel') if kwargs.get('stacklevel') else 2
        super().debug(f'{self.trace_id} | {msg}', stacklevel=stack_level, *args, **kwargs)
    
    def info(self, msg: object, *args, **kwargs) -> None:
        stack_level = kwargs.pop('stacklevel') if kwargs.get('stacklevel') else 2
        super().info(f'{self.trace_id} | {msg}', stacklevel=stack_level, *args, **kwargs)
    
    def warning(self, msg: object, *args, **kwargs) -> None:
        stack_level = kwargs.pop('stacklevel') if kwargs.get('stacklevel') else 2
        super().warning(f'{self.trace_id} | {msg}', stacklevel=stack_level, *args, **kwargs)
    
    def error(self, msg: object, *args, **kwargs) -> None:
        stack_level = kwargs.pop('stacklevel') if kwargs.get('stacklevel') else 2
        super().error(f'{self.trace_id} | {msg}', stacklevel=stack_level, *args, **kwargs)


logger = Logger()
logger.init_logger(settings.log_config.log_dir)
