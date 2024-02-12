from loguru import logger

logger.add("logger/logs.log", format="{time} {message}", level="DEBUG", rotation="2 MB")
