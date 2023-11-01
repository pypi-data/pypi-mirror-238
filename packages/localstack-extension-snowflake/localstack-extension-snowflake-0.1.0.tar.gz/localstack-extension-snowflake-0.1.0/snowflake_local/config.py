import logging
from localstack import config
ASSETS_BUCKET_NAME='snowflake-assets'
ASSETS_KEY_PREFIX='uploads/'
logger=logging.getLogger('snowflake_local')
logger.setLevel(logging.INFO)
if config.DEBUG:logger.setLevel(logging.DEBUG)