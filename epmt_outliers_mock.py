from logging import getLogger, basicConfig, DEBUG, ERROR, INFO, WARNING
logger = getLogger(__name__)  # you can use other name
basicConfig(level=DEBUG)

def detect_outlier_jobs():
    return ''