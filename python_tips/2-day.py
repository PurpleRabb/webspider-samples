def testA(a, b, c, *args, **kwargs):
    print(a)
    print(b)
    print(c)
    print(args)
    print(kwargs)


# 函数参数的传递都是引用传递，当传递的参数是可修改的时候会直接修改原来的值，
# 如果传递的是不可变的数据，比如常数或者元组，则会发生复制

def testB(dic_a, b, lists):
    print(id(lists))
    a["name"] = "aaaa"
    b = 200
    # lists = lists + lists #注意这里的lists会发生复制，不会改变原来的lists
    lists += lists # 这里直接在源lists上操作，将改变原来的值,区别与lists+lists
    print(id(lists))


if __name__ == "__main__":
    A = ['t', 'e', 't']
    B = {'name': 'xxx', 'age': 18}

    # '*'有解包的作用，一个*可以解元组列表，两个可以解字典
    testA(1, 2, 3, 4, 5, 6, A, B, m='123', n='321')
    print("------------------------------------------")
    testA(1, 2, 3, 4, 5, 6, *A, **B, m='123', n='321')

    # 字典的Key值必须是不可变的数据类型，可变的数据类型不能做Hash
    A = {"name": "xxx", "age": 18, (1, 2, 3): "value"}  # ["11"]: 22}

    a = {"name": "123"}
    lists = [11, 22]
    print(id(lists))
    testB(a, 100, lists)
    print(lists)
    print(a)
