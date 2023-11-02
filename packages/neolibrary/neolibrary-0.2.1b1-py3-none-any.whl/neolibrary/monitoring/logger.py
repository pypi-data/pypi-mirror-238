import logging
from colorlog import ColoredFormatter
from typing import Any, NoReturn
import os
import arrow

# local imports
from neolibrary.monitoring.config import config
from neolibrary.utils import log_to_dateformat


class NeoLogger(logging.Logger):
    """
    This is a customized logger for NeoMedSys project.

    Parameters
    ----------
    name : str
        Name of the logger.
    level : int, optional
        Logging level. Defaults to logging.NOTSET.
    level_e : int, optional
        Logging level for error messages. Defaults to logging.WARNING.
    rotate_days : int, optional
        Number of days after which the log file is rotated. Defaults to 30.

    Returns
    -------
    logging.Logger
        A customized logger.
    """

    def __init__(self, name: str, level: int = config.LOG_LEVEL, level_e: int = config.LOG_LEVEL_E, rotate_days: int = 30) -> NoReturn:
        """
        This is a customized logger for NeoMedSys project.

        Parameters
        ----------
        name : str
            Name of the logger.
        level : int, optional
            Logging level. Defaults to logging.NOTSET.
        level_e : int, optional
            Logging level for error messages. Defaults to logging.WARNING.
        rotate_days : int, optional
            Number of days after which the log file is rotated. Defaults to 30.

        Returns
        -------
        logging.Logger
            A customized logger.
        """
        super().__init__(name, level)
        self.init_logger() # check and create logs folder if it doesn't exist
        self.name = name
        self.rotate_days = rotate_days
        self.PATH = config.ROOT + '/logs/' + name + '.log'
        logging.addLevelName(config.SUCCESS, 'SUCCESS')
        logging.addLevelName(config.FAIL, 'FAIL')
        logging.addLevelName(config.PIPE, 'PIPE')
        logging.root.setLevel(level)
        self.formatter = ColoredFormatter(
            config.LOGFORMAT,
            log_colors=config.LOG_COLORS,
        )
        self.e_formatter = ColoredFormatter(
            config.LOGFORMAT_ERROR,
            log_colors=config.LOG_COLORS,
        )
        self.stream = logging.StreamHandler()
        self.file_handler = logging.FileHandler(self.PATH)
        self.file_handler.setLevel(level_e)
        self.stream.setFormatter(self.formatter)
        self.file_handler.setFormatter(self.e_formatter)
        self.setLevel(config.LOG_LEVEL)
        if self.hasHandlers():
            self.handlers.clear()
        self.addHandler(self.stream)
        self.addHandler(self.file_handler)

    def success(self, message: str, *args: Any, **kws: Any) -> NoReturn:
        """
        Log 'message % args' with severity 'SUCCESS'.

        Parameters
        ----------
        message : str
            Message to log.
        *args : Any
            Arguments to log.
        **kws : Any
            Keyword arguments to log.

        Returns
        -------
        NoReturn
        """
        self.rotate()
        if self.isEnabledFor(config.SUCCESS):
            self._log(config.SUCCESS, message, args, **kws)

    def fail(self, message: str, *args: Any, **kws: Any) -> NoReturn:
        """
        Log 'message % args' with severity 'FAIL'.

        Parameters
        ----------
        message : str
            Message to log.
        *args : Any
            Arguments to log.
        **kws : Any
            Keyword arguments to log.
        
        Returns
        -------
        NoReturn
        """
        self.rotate()
        if self.isEnabledFor(config.FAIL):
            self._log(config.FAIL, message, args, **kws)

    def pipe(self, message: str, *args: Any, **kws: Any) -> NoReturn:
        """
        Log 'message % args' with severity 'PIPE'.

        Parameters
        ----------
        message : str
            Message to log.
        *args : Any
            Arguments to log.
        **kws : Any
            Keyword arguments to log.

        Returns
        -------
        NoReturn
        """
        self.rotate()
        if self.isEnabledFor(config.PIPE):
            self._log(config.PIPE, message, args, **kws)

    def info(self, message: str, *args: Any, **kws: Any) -> NoReturn:
        """
        log 'message % args' with severity 'INFO'.

        Parameters
        ----------
        message : str
            Message to log.
        *args : Any
            Arguments to log.
        **kws : Any
            Keyword arguments to log.

        Returns
        -------
        NoReturn
        """
        self.rotate()
        if self.isEnabledFor(logging.INFO):
            self._log(logging.INFO, message, args, **kws)

    def debug(self, message: str, *args: Any, **kws: Any) -> NoReturn:
        """
        Log 'message % args' with severity 'DEBUG'.

        Parameters
        ----------
        message : str
            Message to log.
        *args : Any
            Arguments to log.
        **kws : Any
            Keyword arguments to log.

        Returns
        -------
        NoReturn
        """
        self.rotate()
        if self.isEnabledFor(logging.DEBUG):
            self._log(logging.DEBUG, message, args, **kws)

    def warning(self, message: str, *args: Any, **kws: Any) -> NoReturn:
        """
        Log 'message % args' with severity 'WARNING'.

        Parameters
        ----------
        message : str
            Message to log.
        *args : Any
            Arguments to log.
        **kws : Any
            Keyword arguments to log.
        Returns
        -------
        NoReturn
        """
        self.rotate()
        if self.isEnabledFor(logging.WARNING):
            self._log(logging.WARNING, message, args, **kws)

    def error(self, message: str, *args: Any, **kws: Any) -> NoReturn:
        """
        Log 'message % args' with severity 'ERROR'.

        Parameters
        ----------
        message : str
            Message to log.
        *args : Any
            Arguments to log.
        **kws : Any
            Keyword arguments to log.

        Returns
        -------
        None: NoReturn
        """
        self.rotate()
        if self.isEnabledFor(logging.ERROR):
            self._log(logging.ERROR, message, args, **kws)

    def critical(self, message: str, *args: Any, **kws: Any) -> NoReturn:
        """
        Log 'message % args' with severity 'CRITICAL'.

        Parameters
        ----------
        message : str
            Message to log.
        *args : Any
            Arguments to log.
        **kws : Any
            Keyword arguments to log.
        Returns:
            None: NoReturn
        """
        self.rotate()
        if self.isEnabledFor(logging.CRITICAL):
            self._log(logging.CRITICAL, message, args, **kws)

    def init_logger(self) -> NoReturn:
        """
        Initialize the logger by setting up the folder structure if it doesn't exist.

        Parameters
        ----------
        None

        Returns
        -------
        NoReturn
        """
        if not os.path.exists(config.ROOT + '/logs'):
            os.makedirs(config.ROOT + '/logs')

    def rotate(self) -> NoReturn:
        """
        Roatates log files after self.rotate_day days.

        Reads the first line of the log (which is the latest log entry) and compares it with the current date.
        If the difference is greater than self.rotate_days, the log file is deleted.

        Statement from dev: (For some reason it is AIDS to find the creation time of a file on linux)

        Parameters
        ----------
        None

        Returns
        -------
        NoReturn
        """

        now = arrow.now()
        for logfile in os.listdir(config.ROOT + '/logs'):
            if logfile.endswith('.log'):

                with open(config.ROOT + '/logs/' + logfile, 'r') as f:
                    lines = f.readlines()
                    if len(lines) > 0:
                        line = lines[0]
                        date_format = log_to_dateformat(line=line)
                        last_timestamp_arrow = arrow.get(date_format, 'YYYY-MM-DD HH:mm:ss')
                        days_processed = int((now - last_timestamp_arrow).days)
                        if days_processed > self.rotate_days:
                            os.remove(config.ROOT + '/logs/' + logfile)
                            self.info('Removed log file: {}'.format(logfile))
