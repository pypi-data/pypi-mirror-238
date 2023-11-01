"""
mylogger.py: 一个自定义日志记录器模块，提供了两种日志记录器：标准日志记录器和彩色日志记录器。

此模块包含以下功能：

1. 标准日志记录器：输出具有自定义格式的日志信息。
2. 彩色日志记录器：根据日志级别输出不同颜色的日志信息。
3. get_logger() 函数：提供日志记录器名称，返回相应的日志记录器实例。

使用示例：

导入模块并获取所需的日志记录器，然后使用该记录器记录日志信息。

from mylogger import get_logger

logger = get_logger('colorful')
logger.info("这是一条信息级别的日志")
logger.warning("这是一条警告级别的日志")
logger.error("这是一条错误级别的日志")
"""
import logging
from colorlog import ColoredFormatter
import sys
import os
import time


# 确保日志打印的时间为北京时间
os.environ["TZ"] = "Asia/Shanghai"
time.tzset()


def remove_logger_by_name(logger_name):
    '''
    删除已经存在的logger
    :param logger_name: logger名称
    :return: 是否删除成功
    '''
    if logger_name in logging.Logger.manager.loggerDict:
        del logging.Logger.manager.loggerDict[logger_name]
        return True
    return False


def standard_logger():
    # 自定义日志记录器类
    class CustomFormatter(logging.Formatter):
        def format(self, record):
            levelname = record.levelname
            record.levelname = f"[{levelname}]".ljust(9)
            return super().format(record)

    # 自定义格式化字符串
    log_format = "%(asctime)s %(levelname)s %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    # 设置日志级别
    remove_logger_by_name('standard')
    logger = logging.getLogger('standard')
    logger.setLevel(logging.DEBUG)

    # 设置日志处理器和格式化器
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(CustomFormatter(log_format, datefmt=date_format))
    logger.addHandler(handler)
    return logger


def colorful_logger():
    LOG_FORMAT = "%(asctime)s %(log_color)s[%(levelname)s] %(message)s"
    formatter = ColoredFormatter(
        LOG_FORMAT,
        datefmt="%Y-%m-%d %H:%M:%S",
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        }
    )

    # 配置彩色logger
    remove_logger_by_name('colorful')
    logger = logging.getLogger('colorful')
    logger.setLevel(logging.DEBUG)

    # Set up the console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger


def get_logger(name):
    if name == 'standard':
        return standard_logger()
    elif name == 'colorful':
        return colorful_logger()
    else:
        raise ValueError('不合法的logger name: %s' % name)
