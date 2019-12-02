# import this
# import turtle


# turtle.pensize(4)
# turtle.pencolor('red')
# turtle.forward(100)
# turtle.right(90)
# turtle.forward(100)
# turtle.right(90)
# turtle.forward(100)
# turtle.right(90)
# turtle.forward(100)
# turtle.mainloop()
import logging


def using_logger(func):
    def wrapper():
        print("using logger:")
        return func()
    return wrapper


@using_logger
def m_log():
    print("_m_log")


def use_logging(func):
    def wrapper():
        logging.warn("%s is running" % func.__name__)
        return func()
    return wrapper


@use_logging
def foo():
    print("i am foo")


def test():
    """HELP"""
    print("helloworld")


if __name__ == "__main__":
    m_log()
    help(test)
