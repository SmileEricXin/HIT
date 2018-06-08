# -*- coding:utf-8 -*-
import os
import re
import io


def take_length(data):
    return len(data.split(" "))


def line_unique(file_path):
    """
    file_path文件的每一行都不相同
    :param file_path:
    :return:
    """
    if not os.path.exists(file_path):
        print(file_path + " 不存在")
        return

    f_in = open(file_path, mode="r", encoding="utf-8")
    line = f_in.readline()
    lines = []
    while line:
        # print(line)
        lines.append(line.strip())
        line = f_in.readline()
    f_in.close()

    lines = list(set(lines))
    print("lines: %d" % len(lines))
    print(lines)
    lines.sort(key=take_length)
    print(lines)
    f_out = open(file_path + ".line_unique", mode="w", encoding="utf-8")
    for line in lines:
        f_out.write(line + "\n")
    f_out.close()


def word_unique(file_path):
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

    pattern = re.compile('(\S+)')
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

    f_out = open(file_path + ".word_unique", mode="w", encoding="UTF-8")
    words_len = len(words)
    print(words_len)
    f_out.write("名词总数：%(words_len)d\n" % {"words_len": words_len})
    f_out.write("\t".join(words))
    f_out.close()


if __name__ == "__main__":
    # line_unique("./data/train2.data.out")
    word_unique("./data/train2.data.out")
