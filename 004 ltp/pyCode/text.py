# -*- coding:utf-8 -*-
import os
import re
import io


def word_length_of_line(data):
    """对输入按空格拆分并返回拆分后的长度"""
    return len(data.split(" "))


def line_unique(file_path):
    """
    先对file_path去重
    然后按空格分词，以分词长度进行排序
    最后输出到.line_unique文件中

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
    lines.sort(key=word_length_of_line)
    print(lines)
    f_out = open(file_path + ".line_unique", mode="w", encoding="utf-8")
    for line in lines:
        f_out.write(line + "\n")
    f_out.close()


def word_unique(file_path):
    """
    对 file_path 文件的名词进行处理，保证没有重复的名词
    最后输出到.word_unique文件
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


def tax_code_split_line(line):
    """
    line:开票明细名称、税收分类编码
    :param line:
    :return:
    """
    if len(line) == 0:
        return []

    try:
        pattern = re.compile('(?<=)(.+)(\d+)')
        words = pattern.findall(line)
        for word in words:
            print(word)
    except ValueError as e:
        print("ValueError:" + e)

    return []