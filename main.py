import time
import logging
import ecs_logging
import elasticsearch
import kibana

es = elasticsearch.Elasticsearch(hosts=["http://localhost:9200"])

idx_send = es.index(
    index="test-index",
    id=2,
    document={"TESTE": "data", "timestamp": time.time()}
)

get = es.get(
    index="test-index",
    id=2,
)

print(idx_send)
print(get)


