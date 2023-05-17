import sys
import logging
import logging.handlers
from ansimarkup import parse

class ColoredFormatter(logging.Formatter):
    """ Formatter para saída colorida no standard output """

    MAPPING = {
        'DEBUG'   : {'prefix': '<blue>', 'suffix': '</blue>'},
        'INFO'    : {'prefix': '', 'suffix': ''},
        'WARNING' : {'prefix': '<dim><yellow>', 'suffix': '</yellow></dim>'},
        'ERROR'   : {'prefix': '<red>', 'suffix': '</red>'},
        'CRITICAL': {'prefix': '<r,w>', 'suffix': '</r,w>'},
    }

    def format(self, record):
        """ Formata mensagem """
        mapping = self.MAPPING.get(record.levelname)
        prefix = mapping['prefix']
        suffix = mapping['suffix']
        s = super().format(record)
        return parse(f'{prefix}{s}{suffix}')

class AppLogger:
    """ Classe que representa o logger da aplicação """
    _logger = None

    @classmethod
    def setup(cls, log_filename=None, file_mode='w', fmt=u'%(message)s', datefmt=None):
        """
        Retorna instância do logger

        :param log_filename: nome do arquivo de log
        """
        logging.basicConfig()
        logger_name = cls.__module__ + '.' + cls.__name__
        cls._logger = logging.getLogger(logger_name)

        cls._logger.setLevel(logging.DEBUG)
        cls._logger.root.handlers.clear()
        cls._logger.propagate = False

        stream_handler = logging.StreamHandler(sys.stdout)
        #stream_handler.setFormatter(logging.Formatter(fmt=fmt, datefmt=datefmt))
        stream_handler.setFormatter(ColoredFormatter(fmt=fmt, datefmt=datefmt))
        cls._logger.addHandler(stream_handler)

        if log_filename is not None:
            file_handler = logging.FileHandler(log_filename, mode=file_mode, encoding='utf-8')
            file_handler.setFormatter(logging.Formatter(fmt=fmt, datefmt=datefmt))
            file_handler.setLevel(logging.INFO)
            cls._logger.addHandler(file_handler)

        return cls._logger

    @classmethod
    def instance(cls):
        """
        Retorna instância do logger

        :param method: nome do método que se deseja retornar do logger
        """
        if cls._logger is None:
            cls._logger = cls.setup(log_filename=None)

        return cls._logger

class ServiceLogger:
    """ Classe que representa o logger do serviço """
    _logger = None

    @classmethod
    def setup(cls, servicename, level=logging.INFO,
                  log_filename=None, file_mode='a',
                  fmt='%(asctime)s [%(levelname)s]: %(message)s', datefmt=None):
        """
        Retorna instância do logger

        :param log_filename: nome do arquivo de log
        """
        logging.basicConfig()
        logger_name = cls.__module__ + '.' + cls.__name__
        cls._logger = logging.getLogger(logger_name)

        cls._logger.setLevel(level)
        cls._logger.root.handlers.clear()
        cls._logger.propagate = False

        ntevent_handler = logging.handlers.NTEventLogHandler(servicename)
        ntevent_handler.setFormatter(logging.Formatter(fmt='%(message)s', datefmt=None))
        ntevent_handler.setLevel(level)
        cls._logger.addHandler(ntevent_handler)

        if log_filename is not None:
            file_handler = logging.FileHandler(log_filename, mode=file_mode, encoding='utf-8')
            file_handler.setFormatter(logging.Formatter(fmt=fmt, datefmt=datefmt))
            file_handler.setLevel(level)
            cls._logger.addHandler(file_handler)

        return cls._logger

    @classmethod
    def instance(cls):
        """
        Retorna instância do logger

        :param method: nome do método que se deseja retornar do logger
        """
        if cls._logger is None:
            servicename = cls.__module__ + '.' + cls.__name__
            cls._logger = cls.setup(servicename, log_filename=None)

        return cls._logger
