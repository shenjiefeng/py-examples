# encoding: utf-8
__author__ = 'fengshenjie'
import traceback, time, os
import logging
import datetime


def timecount(funcname=''):
    '''带返回值'''

    def timecount_hander(func):
        def wrapper(*args, **kwargs):
            if funcname:
                name = funcname
            else:
                name = func
            timeStart = time.time()
            print(time.strftime('%H:%M:%S'), '{} start'.format(name))
            res = func(*args, **kwargs)
            timeEnd = time.time()
            print(time.strftime('%H:%M:%S'), '{} Time elapsed: {}'.format(name, timeEnd - timeStart))
            return res

        return wrapper

    return timecount_hander


def errHander(funcname=''):
    def fsjhandler(func):
        '''send aler email when catch exception'''

        def wrapper(*args, **kwargs):
            try:
                res = func(*args, **kwargs)
                return res
            except Exception as e:
                traceback.print_exc()
                # sendmail

        return wrapper

    return fsjhandler


def write2file(lst, filename, path):
    assert lst is not None
    assert isinstance(lst, list)
    if not os.access(path, os.W_OK):
        os.mkdir(path)
    with open(path + filename, 'w', encoding='utf8') as fp:
        fp.writelines([str(i) + '\n' for i in lst])
    print(path + filename + ' created.')


def getLogger(proj_name, logLevel, logPath=None):
    logger = logging.getLogger(proj_name)
    today = datetime.now().strftime('%Y-%m-%d')
    if isinstance(logPath, str) and logPath:
        handler = logging.FileHandler(logPath + today, 'a', 'utf-8')
    else:
        handler = logging.FileHandler("./log/" + today + ".log", 'a', 'utf-8')
    try:
        handler.setLevel(logLevel)
    except:
        handler.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def doubleLog(content, logger=None):
    print(time.strftime('%H:%M:%S'), content)
    if isinstance(logger, logging.Logger):
        logger.info(content)


if __name__ == '__main__':
    pass
