# 单例模式
import threading
import time


class Singleton1:

    def __init__(self):
        return
        time.sleep(1)

    def __new__(cls, *args, **kwargs):
        # try:
        #     return Singleton._instance
        # except AttributeError:
        #     Singleton._instance = super().__new__(cls)
        # return Singleton._instance
        # 注意_instance不要用双_,会导致私有变量重命名,hasattr每次都返回false
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
        else:
            return cls._instance


class Singleton2:
    __instance = None
    __first_init = False

    def __init__(self):
        if not self.__first_init:
            print("first init")
            self.__first_init = True
        time.sleep(1)

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
        return cls.__instance


def task(arg):
    s = Singleton2()
    print(s)


s = Singleton1()

for i in range(10):
    t = threading.Thread(target=task, args=[i, ])
    t.start()
