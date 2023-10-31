# sre is purposely a non propagating logger, but we need to
# do some additional work to get caplog to play nicely with this
import pytest
from _pytest.logging import LogCaptureFixture


@pytest.fixture
def caplog(caplog: LogCaptureFixture):
    import logging

    restore = []
    for logger in logging.Logger.manager.loggerDict.values():
        try:
            if not logger.propagate:
                restore += [(logger, logger.propagate)]
                logger.propagate = True
        except AttributeError:
            pass
    yield caplog
    for logger, value in restore:
        logger.propagate = value