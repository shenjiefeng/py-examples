# encoding: utf-8
__author__ = 'fengshenjie'
import logging
from logging import Formatter, StreamHandler, FileHandler


def getLogger(name='default'):
    # logging模块输出格式
    fmt = Formatter('[%(asctime)s] %(levelname)s: %(message)s')
    logger = logging.getLogger(name)
    # 输出到文件
    fhd = logging.FileHandler('logs/{0}.log'.format(name), encoding='utf-8')
    fhd.setFormatter(fmt)
    # 输出到控制台
    stdout_hd = logging.StreamHandler()
    stdout_hd.setFormatter(fmt)

    logger.addHandler(fhd)
    logger.addHandler(stdout_hd)
    logger.setLevel(logging.INFO)
    return logger


logger = getLogger()
