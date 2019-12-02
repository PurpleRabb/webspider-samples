class Dog:
    num = 0  # 类属性

    def __init__(self, name, color):
        # __开头的为私有变量
        self.__name = name
        self.__color = color

    def set_color(self, color):
        self.__color = color

    # 类方法操作类属性
    @classmethod
    def setNum(cls, newNum):
        num = newNum

    @staticmethod
    def printTest():
        print("This is a static method attached to Dog")

    # Magic function __str__
    def __str__(self):
        return self.__name

    def __del__(self):
        print("__del__")


d1 = Dog("Tim", "Black")
print(d1)  # 自动调用__str__
# python中的私有成员并不是无法调用，只是被修改了名字
print(d1.__dict__)
print(d1._Dog__name)

d2 = d1
del d1  # 引用计数不为0，不会删除
print("-------1---------")
