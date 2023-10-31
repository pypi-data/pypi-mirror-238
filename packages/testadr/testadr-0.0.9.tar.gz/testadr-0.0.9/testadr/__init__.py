from .case import TestCase
from .page import Page
from .running.runner import main
from .core.android import *
from .utils.config import config
from .utils.pytest_util import *
from .utils.allure_util import *
from .utils.log import logger
from .utils.exceptions import KError


__version__ = "0.0.9"
__description__ = "安卓平台自动化测试框架"
