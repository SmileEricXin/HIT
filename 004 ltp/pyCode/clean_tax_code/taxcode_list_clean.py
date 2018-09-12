# -*- coding:utf-8 -*-
import os

# 文本具有的行数
COLOUM_LEN = 7
# 汇总项所在的列
HZX_COL = 6


def taxcode_list_clean(path):
    if not os.path.exists(path):
        print(path, ' not exist')
        return

    try:
        f_in = open(path, mode="r", encoding="utf-8")
        f_hzx = open(path + '.hzx', mode="w", encoding="utf-8")
        f_not_hzx = open(path + '.nothzx', mode="w", encoding="utf-8")

        line = f_in.readline()
        while line:
            words = line.split(sep="&&&")
            if len(words) == COLOUM_LEN:
                word_flag = words[HZX_COL - 1].strip()
                if word_flag == 'Y':  # 汇总项不能分类
                    f_hzx.writelines(line)
                elif word_flag == 'N':
                    f_not_hzx.writelines(line)
            line = f_in.readline()
    except():
        print("clean file fail")
    finally:
        if f_in:
            f_in.close()
        if f_hzx:
            f_hzx.close()
        if f_not_hzx:
            f_not_hzx.close()


if __name__ == "__main__":
    taxcode_list_clean("./税收分类编码表_行加入分隔符.txt")
