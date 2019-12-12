# 列表推导式

a = [11, 22, 33, 44, 33, 55]
b = set(a)  # 用集合去重
c = list(b)
print(a, b, c)

ll = [(x, y) for x in range(1, 5) for y in range(1, 3)]
print(ll)


# 参数传递注意点：
def test_parameters(num, origin=[]):
    origin.append(num)
    return origin


list1 = test_parameters(100)  # 不传参的时候，origin只初始化一次，所以后续的操作都是基于第一次。
print(list1)  # 输出100
list2 = test_parameters(200, [1, 2, 3])
list3 = test_parameters(300)
print(list3)  # 输出[100,300]

print(list1, list2, list3)