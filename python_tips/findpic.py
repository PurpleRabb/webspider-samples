import threading
import time

from PIL import Image
import sys
import os
import shutil

"""通过直方图计算两张图图片的相似度，适用于测试截图的比对"""
g_pic_dir = "F:\screenshots\screen"
g_ok_pic = "F:\screenshots\screen\screen1.jpg"
g_base_his = []
group_size = 50
THRESHOLD = 0.995
result = []


def hist_similar(lh, rh):
    print("checking...")
    if len(lh) != len(rh):
        return -1
    _sum = 0
    for l, r in zip(lh, rh):
        _res = 0.0
        if l == r:
            _res = 0
        else:
            _res = abs(l - r) / max(l, r)
        _sum += 1 - _res
    print(_sum / len(lh))
    return _sum / len(lh)
    # return sum(1 - (0 if l == r else float(abs(l - r)) / max(l, r)) for l, r in zip(lh, rh)) / len(lh)


def task(lists, _id):
    print("start thread id = %d" % _id)
    for file in lists:
        filename = os.path.join(g_pic_dir, file)
        if filename == g_ok_pic:
            continue
        try:
            img = Image.open(filename)
        except Exception as error:
            print(error)
            continue
        if hist_similar(g_base_his, img.histogram()) < THRESHOLD:
            result.append(filename)


if __name__ == "__main__":
    # python findpic [截图保存的文件夹] [正确结果的截图]
    # 例如: python findpic.py F:\screenshots\screen screen1.jpg
    g_pic_dir = sys.argv[1]
    g_ok_pic_name = sys.argv[2]
    g_ok_pic = os.path.join(g_pic_dir, g_ok_pic_name)
    try:
        g_base_his = Image.open(g_ok_pic).histogram()
    except Exception as e:
        print(e)

    pic_lists = os.listdir(g_pic_dir)
    pic_lists_size = len(pic_lists)
    start = time.time()

    # 图片数量超过group_size的时候启用多线程
    if pic_lists_size > group_size:
        t_obj = []
        for i in range(0, pic_lists_size, group_size):
            b = pic_lists[i:i + group_size]
            t = threading.Thread(target=task, args=(b, int(i / group_size)))
            t.start()
            t_obj.append(t)
        # 等待子线程结束
        for t in t_obj:
            t.join()
    else:
        task(pic_lists, 0)
    # 打印并保存结果
    print(result)
    res_dir = os.path.join(g_pic_dir, 'res')
    if not os.path.exists(res_dir):
        os.mkdir(res_dir)
    for res in result:
        shutil.copy(res, res_dir)
    end = time.time()
    print("Exit after:{time}s".format(time=end - start))
