import logging
import uuid

logger = logging.getLogger(__name__)


def test_log_file():
    log_flag = uuid.uuid4().hex
    logger.info(log_flag)
    with open('./log/app.log', 'r') as f:
        assert log_flag in f.read()
