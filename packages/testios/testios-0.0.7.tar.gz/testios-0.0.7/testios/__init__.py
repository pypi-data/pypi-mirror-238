from .case import TestCase
from .page import Page
from .core.ios import *
from .running.runner import main
from .utils.config import config
from .utils.pytest_util import *
from .utils.allure_util import *
from .utils.log import logger
from .utils.exceptions import KError


__version__ = "0.0.7"
__description__ = "IOS平台自动化测试框架"
