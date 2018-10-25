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


def combine_final_data(file1, file2):
    """
    以简称进行分类，共有408类
    这408类目前共有两个映射文件，其实一个是 code_category.map，这个文件是类与分类编码的映射
    另一个文件是03 税收分类编码表_汇总项.class.map.combine.merge，这个文件是类与其关键词的映射

    现在将这两个表合并，形成以下映射关系：
    种类  --  编码  --  关键词
    :return:
    """
    try:
        f1 = open(file1, mode="r", encoding="utf-8")
        f2 = open(file2, mode="r", encoding="utf-8")
        f_out = open('./clean_tax_code/final.merge', mode="w+", encoding="utf-8")

        line1 = f1.readline()
        save_dict = {}
        while line1:
            pos = line1.find('[')
            word1 = line1[0:pos]
            word2 = line1[pos:-1]

            word1 = word1.strip()
            word1 = '[' + word1 + ']'  # 另外一个文件的种类名称带方括号
            save_dict[word1] = word2.strip()

            line1 = f1.readline()

        line2 = f2.readline()
        while line2:
            pos = line2.index('[', 1)
            word1 = line2[0:pos]
            word2 = line2[pos:-1]
            word1 = word1.strip()

            if word1 in save_dict.keys():
                save_dict[word1] = save_dict[word1] + ' ' + word2.strip()
                # print(save_dict[word1])

            line2 = f2.readline()

        for key, values in save_dict.items():
            f_out.write(key + ' ' + values + '\r')

    except UnicodeError:
        pass
    finally:
        if f1:
            f1.close()
        if f2:
            f2.close()
        if f_out:
            f_out.close()


def line_unique(file):
    """
    对文件的按行读取，保证每行的数据不同，统计其数量
    :param file:
    :return:
    """
    f = open(file, mode="r", encoding="utf-8")
    line = f.readline()
    words = {}
    while line:
        if line not in words.keys():
            words[line] = '0'

        line = f.readline()

    print('words number:', len(words.keys()))
    f.close()


if __name__ == "__main__":
    # combine_final_data("./clean_tax_code/code_category.map", "./clean_tax_code/03 税收分类编码表_汇总项.
    # class.map.combine.merge")
    line_unique('./clean_tax_code/test.txt')
