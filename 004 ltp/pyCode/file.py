# -*- coding: utf-8 -*-
import os
import re
import nlp


def destination_data_recongnize(data_path):
    """
    对目标数据进行命名实体识别、词性标注
    是目标数据，也就是税务局数据是训练数据
    是目标数据，也就是税务局数据是训练数据
    是目标数据，也就是税务局数据是训练数据

    如：渔业/n(一般名词)/O/  类/n(一般名词)/O/

    处理完后，会在同目录下输出对应的.out文件
    :param data_path:
    :return:
    """
    if not os.path.exists(data_path):
        print(data_path + " not exist")
        return

    # 处理数据
    f = open(data_path, "r")
    f_out = open(data_path + ".out", "w")
    line = f.readline()
    while line:
        # 处理完后的数据写入output文件
        match = re.match('(.*\s+)(\d+)\s*', line)
        if match:
            first = match.group(1)
            second = match.group(2)
            print(first)

            # 进行命名实体识别、词性标注、分词等操作
            ner = nlp.ner_sentence(first)
            words_list = list(ner)
            write_str = ""
            for t in words_list:
                for i in range(len(t)):
                    write_str += t[i] + "/"

                write_str += "  "

            # 加上税收分类编码
            write_str += "  " + second + "\n"
            f_out.write(write_str)

        line = f.readline()
    f.close()
    f_out.close()


def train_destination_data(file_path):
    """
    对训练数据进行分析、词性标注、命名实体识别
    是训练数据
    是训练数据
    是训练数据

    会输出两个文件：
    文件一：
        将名词写入.noun.out，只是提出名词，没有加词性
        如：金蝶 记账王 财务 软件 正版 会计 企业

    文件二：
        将源数据保留，源数据后面加入提取的名词

    :return:
    """
    if not os.path.exists(file_path):
        print(file_path + " not exist")
        return

    try:
        # 处理数据
        f = open(file_path, mode="r", encoding="UTF-8")
        f_out = open(file_path + ".noun.out", mode="w", encoding="UTF-8")
        f_out_combine = open(file_path + ".noun.combine", mode="w", encoding="UTF-8")
        line = f.readline()
        while line:
            print(line)
            ner = nlp.ner_sentence(line)  # 包含分词、词性标注、命名实体识别3步
            words_list = list(ner)
            print(words_list)
            write_str = ""
            for t in words_list:
                # 词性标注为名词的才写入输出文件
                if len(t) > 1 and (t[1][:1] == "n" or t[1][:1] == "v" or t[1][:1] == "p" or t[1][:1] == "a" or \
                                               t[1][:1] == "b" or t[1][:1] == "i" or t[1][:1] == "j"):
                    write_str += str(t[0]) + " "

            # 加上税收分类编码
            if len(write_str) > 0:
                f_out.write(write_str + "\n")
                f_out.flush()

            write_str = line.strip() + " >>>>>> " + write_str + "\n"
            f_out_combine.write(write_str)
            f_out_combine.flush()

            line = f.readline()
        f.close()
        f_out.close()
        f_out_combine.close()
    except UnicodeError:
        print("UnicodeError:" + UnicodeError)


def word_length_of_line(data):
    """对输入按空格拆分并返回拆分后的长度"""
    return len(data.split(" "))


def unique_and_sort_line_file(file_path):
    """
    对文件内容按行去重，然后进行排序，重新输出.sort文件
    :param file_path:
    :return:
    """
    f_in = open(file_path, mode="r", encoding="utf-8")
    f_out = open(file_path + ".sort", mode="w", encoding="utf-8")

    line = f_in.readline()
    lines = []
    while line:
        line.strip()
        lines.append(line)
        line = f_in.readline()

    lines = list(set(lines))

    lines.sort(key=word_length_of_line)
    for line in lines:
        f_out.write(line)

    f_in.close()
    f_out.close()

