import uuid
import ElasticsearchLogs.ElasticsearchLogging as esl

# Create a logger
logger = esl.ElasticsearchLogging(
    host="localhost",
    port=9200
)

logger.info("Hello World!", uuid.uuid4())

try:
    res = 1 / 0
except Exception as e:
    logger.error("Error", uuid.uuid4(), e)