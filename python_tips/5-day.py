import sys


# 自定义异常
class ShortException(Exception):
    def __init__(self, length, atleast):
        self.length = length
        self.atleast = atleast


def testA():
    print("testA")


try:
    s = input("请输入参数：")
    if len(s) < 3:
        raise ShortException(len(s), 3)
except ShortException as result:
    print("输入参数%d,小于%d" % (result.length, result.atleast))

# __name__的作用：当python直接调用该脚本时值为__main__,其他脚本调用时为本身模块的名字
print(__name__)

# import的搜索顺序：1.当前目录 2.Python PATH 3.默认路径 4.sys.path
print(sys.path)

# 此时被导入模块若定义了__all__属性，则只有__all__内指定的属性、方法、类可被导入；
# 若没定义，则导入模块内的所有公有属性，方法和类。注意：仅对import *起作用
__all__ = ('ShortException', 'testA')
