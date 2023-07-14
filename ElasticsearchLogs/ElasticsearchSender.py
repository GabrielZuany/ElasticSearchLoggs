from .ElasticsearchConfig import ElasticsearchConfig

class ElasticsearchSender:
    def __init__(self, config:ElasticsearchConfig) -> None:
        self.config = config
        pass
    
    def send(self, doc:dict):
        self.config.es.index(index=self.config.index, id=doc["LogId"], document=doc)