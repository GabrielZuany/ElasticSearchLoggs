import datetime
from loguru import logger
import elasticsearch
import socket

DEFAULT_INDEX = "default-index"

class ElasticsearchConfig:
    def __init__(
            self,
            host:str = 'localhost',
            port:int = 9200, 
            index:str = DEFAULT_INDEX
    ) -> None:
        self.host = host
        self.port = port
        self.index = index
        hostname=socket.gethostname()
        IPAddr=socket.gethostbyname(hostname)

        self.logger = str(IPAddr) + "-" + str(hostname)
        self.es = elasticsearch.Elasticsearch(hosts=[f"http://{host}:{port}"])
        
        if index == DEFAULT_INDEX:
            self.create_current_date_index(index)
    
    def default_mapping(self):
        return {
        "properties": {
            "@timestamp": {
                "type": "date"
            },
            "Level": {
                "type": "text"
            },
            "LogId": {
                "type": "text"
            },
            "Log": {
                "type": "text"
            },
            "Message": {
                "type": "text"
            },
            "fields": {
                "properties": {
                    "UserId": {
                        "type": "text"
                    },
                    "MessageDetails": {
                        "properties":{
                            "Exception": {
                                "type": "text"
                            },
                            "Level": {
                                "type": "text"
                            },
                            "Logger": {
                                "type": "text"
                            },
                            "Source": {
                                "type": "text"
                            },
                            "Stack": {
                                "properties": {
                                    "file": {
                                        "type": "text"
                                    },
                                    "line": {
                                        "type": "text"
                                    },
                                    "module": {
                                        "type": "text"
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    def create_index(
            self, 
            index:str = DEFAULT_INDEX
    ) -> None:
        try:
            self.es.indices.create(index=index, mappings=self.default_mapping())
        except Exception as e:
            logger.error(f"Error creating index: {e}")
        
    def delete_index(
            self, 
            index:str
    ) -> None:
        try:
            self.es.indices.delete(index=index)
        except Exception as e:
            logger.error(f"Error deleting index: {e}")
    
    def create_current_date_index(
            self, 
            index:str = DEFAULT_INDEX
    ) -> None:
        current_month = datetime.datetime.now().strftime("%Y-%m")
        new_index = f"{index}-{current_month}"
        try:
            self.create_index(new_index)
            self.index = new_index
        except Exception as e:
            logger.error(f"Error creating index: {e}")
