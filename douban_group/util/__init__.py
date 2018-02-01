# encoding: utf-8
__author__ = 'fengshenjie'
import time
import traceback


'''common util'''


def timecount(arg=True):
    if arg:
        def _timecount(func):
            def wrapper(*args, **kwargs):
                timeStart = time.time()
                func(*args, **kwargs)
                timeEnd = time.time()
                print('Time elapsed: {0}'.format(timeEnd - timeStart))

            return wrapper
    else:
        def _timecount(func):
            return func
    return _timecount


def except_hander(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except:
            traceback.print_exc()
            print(*args)
            print(**kwargs)

    return wrapper


@except_hander
def main():
    raise Exception('666')


if __name__ == '__main__':
    main()


