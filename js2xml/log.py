import logging

# basic example from https://docs.python.org/2/howto/logging.html#configuring-logging
logger = logging.getLogger('js2xml')
logger.setLevel(logging.ERROR)
handler = logging.StreamHandler()
handler.setLevel(logging.ERROR)
formatter = logging.Formatter('[%(name)s] %(levelname)s: %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
