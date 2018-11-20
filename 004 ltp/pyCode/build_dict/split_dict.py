# *-* coding:utf-8 *-*
import os
import re


def line_pre_handle(line):
    """
    数据预处理：删除空格、标点
    :param line:
    :return:
    """
    p = re.compile('\s|\d|[a-z，。、《》；‘！@#￥%……&*（）——+,.;]')
    line = p.sub("", line)
    return line


def line_parse(line, finess):
    """
    对源数据进行拆分
    finess: 拆分粒度，比如源数据为“这朵花好漂亮”，finess为2时，拆分结果为 “这 这朵 朵 朵花 花  花好”
    finess为3时，拆分结果为“这 这朵 这朵花 朵 朵花 朵花好”
    :param finess:
    :return:
    """
    ret_data = ""
    line = line_pre_handle(line)
    for i in range(len(line)):
        for j in range(finess):
            if i+j < len(line):
                ret_data += (line[i:i + j + 1]) + " "

    return ret_data


def parse_dict(path, finess):
    """
    对源数据进行拆分
    finess: 拆分粒度，比如源数据为“这朵花好漂亮”，finess为2时，拆分结果为 “这 这朵 朵 朵花 花  花好”
    finess为3时，拆分结果为“这 这朵 这朵花 朵 朵花 朵花好”
    :param finess:
    :return:
    """
    if not os.path.exists(path):
        print(path + " 不存在")
        return

    if finess < 1:
        print("finess 应该大于等于1")
        return

    try:
        f_in = open(path, mode="r", encoding="utf-8")
        f_out = open(path + ".out", mode="w", encoding="utf-8")
        line = f_in.readline()
        while line:
            line = line.strip()
            write_data = line_parse(line, finess)
            f_out.write(write_data + "\n")
            f_out.flush()

            line = f_in.readline()

    finally:
        print("try..finally")
        f_in.close()
        f_out.close()


if __name__ == "__main__":
    # print(line_pre_handle("这是 个送das！@#￥……*（（）……%#￥,.af345测，。；’试  1837  哈根"))
    parse_dict("../data/dict/dict_src.data", 2)
