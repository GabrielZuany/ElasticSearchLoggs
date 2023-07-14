from .ElasticsearchConfig import ElasticsearchConfig
from .ElasticsearchLevels import *
from .ElasticsearchConfig import DEFAULT_INDEX
from loguru import logger

class ElasticsearchLogging:
    def __init__(
        self, 
        host:str = 'localhost', 
        port:int = 9200, 
        index:str = DEFAULT_INDEX
    ) -> None:
        self.config = ElasticsearchConfig(host, port, index)

    def error(self, message:str, user_id:str, exception:Exception):
        error = ElasticsearchError(self.config, message, user_id, exception)
        logger.error(message + " -> " + str(exception))
        error.send()

    def info(self, message:str, user_id:str = None):
        info = ElasticsearchInfo(self.config, message, user_id)
        logger.info(message)
        info.send()

    def debug(self, message:str, user_id:str = None):
        debug = ElasticsearchDebug(self.config, message, user_id)
        logger.debug(message)
        debug.send()

    def warning(self, message:str, user_id:str = None):
        warning = ElasticsearchWarning(self.config, message, user_id)
        logger.warning(message)
        warning.send()

    def critical(self, message:str, user_id:str = None):
        critical = ElasticsearchCritical(self.config, message, user_id)
        logger.critical(message)
        critical.send()