import sys
from .setup import *


if "proxies-build" not in sys.argv[0]:
    try:
        from .pytor import *
    except Exception as e:
        exit(e)
