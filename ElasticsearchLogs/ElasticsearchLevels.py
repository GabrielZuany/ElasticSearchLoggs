import inspect
from .ElasticsearchSender import ElasticsearchSender
from .ElasticsearchConfig import ElasticsearchConfig
import datetime
import uuid

def stack():
        stack = inspect.stack()[4]
        src = stack[1].split("\\")[-1]
        line = stack[2]
        module = stack[3]
        if module == "<module>" or module == "send_log":
            stack = inspect.stack()[-1]
            line = stack[2]
            module = f"{src} file body, line {line}"
    
        stacks_log = dict()
        stacks_log["stack"] = {"file":src, "line": line, "module": module}
        return stacks_log

def log(level: str, message: str, exception: Exception | None) -> str:
    if exception is None:
        logging = str(f'[{level}]::[{datetime.datetime.now()}]::[{message}]')
    else:
        logging = str(f'[{level}]::[{datetime.datetime.now()}]::[{message}]::[{exception}]')
    return logging

def doc(level: str, message: str, exception: Exception | None, user_id: str, callstack: bool, logger:str) -> dict:
    trace = stack()
    source = trace["stack"]["file"]
    if callstack is False:
        trace = None
    logging = log(level, message, exception)
    timestamp = datetime.datetime.now()
    logId = uuid.uuid4()
    doc = {
        "@timestamp": timestamp,
        "Level": level,
        "LogId": logId,
        "Log": logging,
        "Message": message,
        "fields": {
            "UserId": user_id,
            "MessageDetails": {
                "Exception": str(exception),
                "Level": level,
                "Logger": logger,
                "Source": source,
                "Stack": trace
            }
        }
    }
    if exception is None:
        del doc["fields"]["MessageDetails"]["Exception"]
    if callstack is False:
        del doc["fields"]["MessageDetails"]["Stack"]

    return doc

class ElasticsearchError():
    def __init__(
            self, 
            config:ElasticsearchConfig,
            message:str = "ElasticsearchError",
            user_id:str = None,
            exception:Exception = None
        ) -> None:
        self.sender = ElasticsearchSender(config)
        self.doc = doc("ERROR", message, exception, user_id, True, config.logger)
        
    def send(self):
        self.sender.send(self.doc)

class ElasticsearchInfo():
    def __init__(
            self, 
            config:ElasticsearchConfig,
            message:str = "ElasticsearchInfo",
            user_id:str = None,
        ) -> None:
        self.sender = ElasticsearchSender(config)
        self.doc = doc("INFO", message, None, user_id, False, config.logger)

    def send(self):
        self.sender.send(self.doc)

class ElasticsearchWarning():
    def __init__(
            self, 
            config:ElasticsearchConfig,
            message:str = "ElasticsearchWarning",
            user_id:str = None,
        ) -> None:
        self.sender = ElasticsearchSender(config)
        self.doc = doc("WARNING", message, None, user_id, False, config.logger)

    def send(self):
        self.sender.send(self.doc)

class ElasticsearchDebug():
    def __init__(
            self, 
            config:ElasticsearchConfig,
            message:str = "ElasticsearchDebug",
            user_id:str = None,
        ) -> None:
        self.sender = ElasticsearchSender(config)
        self.doc = doc("DEBUG", message, None, user_id, False, config.logger)

    def send(self):
        self.sender.send(self.doc)

class ElasticsearchCritical():
    def __init__(
            self, 
            config:ElasticsearchConfig,
            message:str = "ElasticsearchCritical",
            user_id:str = None,
        ) -> None:
        self.sender = ElasticsearchSender(config)
        self.doc = doc("CRITICAL", message, None, user_id, True, config.logger)

    def send(self):
        self.sender.send(self.doc)