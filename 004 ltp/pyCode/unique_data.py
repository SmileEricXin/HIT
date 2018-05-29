# -*- coding:utf-8 -*-
import os
import re
import io


def uniqe_data(file_path):
    """
    对 file_path 文件的名词进行处理，保证没有重复的名词
    :param file_path:
    :return:
    """
    if not os.path.exists(file_path):
        print(file_path + "不存在")
        return

    f_in = open(file_path, mode="r", encoding="UTF-8")
    line_in = f_in.readline()

    pattern = re.compile('([^/]+)\S+')
    words = []
    while line_in:
        result = pattern.findall(line_in)
        for word in result:
            word = word.strip()
            if len(word) > 1:
                words.append(word)
            
        line_in = f_in.read()
        words = list(set(words))

    f_in.close()

    f_out = open(file_path + ".unique", mode="w", encoding="UTF-8")
    words_len = len(words)
    print(words_len)
    f_out.write("名词总数：%(words_len)d\n" % {"words_len": words_len})
    f_out.write("\t".join(words))
    f_out.close()


if __name__ == "__main__":
    uniqe_data("./data/destination.data.out")
