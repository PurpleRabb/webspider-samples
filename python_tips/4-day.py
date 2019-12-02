# 单例模式
import threading
import time


class Singleton:

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
            Singleton._instance = super().__new__(cls)
        else:
            return Singleton._instance

    # def __str__(self):
    #   print(self)


def task(arg):
    s = Singleton()
    print(s)


s = Singleton()
print(Singleton.__dict__)


for i in range(10):
    t = threading.Thread(target=task, args=[i, ])
    t.start()
