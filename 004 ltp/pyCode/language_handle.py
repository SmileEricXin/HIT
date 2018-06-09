# -*- coding: utf-8 -*-
import os
import re
import base_function as bf


__doc__ = """
this file for parctice
"""


def test():
    doc = "我在哈尔滨工业大学读工程硕士。你要不要一起来？Future is full of imagination."
    # doc = "我在哈尔滨工业大学读工程硕士。"
    sentences = bf.split_document(doc)
    print(sentences)
    print(type(sentences))

    for sentence in sentences:
        words = bf.split_sentence(sentence)
        print("切分后的词语：" + '\t'.join(words))

        postags = bf.postag_word(words)
        postags = bf.postags_enhance(postags)
        print("词性标注：" + '\t'.join(postags))

        nertags = bf.recognize_word(words, postags)
        print("命名实体识别：" + '\t'.join(nertags))


def train_paper_data(data_path):
    """
    用于论文的训练语料预处理
    处理完后，会在同目录下输出对应的output文件
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

            ner = bf.ner_sentence(first)
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
    对税务局数据进行分析、词性标注、命名实体识别
    :return:
    """
    if not os.path.exists(file_path):
        print(file_path + " not exist")
        return

    try:
        # 处理数据
        f = open(file_path, mode="r", encoding="UTF-8")
        f_out = open(file_path + ".out", mode="w", encoding="UTF-8")
        f_out_combine = open(file_path + ".combine", mode="w", encoding="UTF-8")
        line = f.readline()
        while line:
            print(line)
            ner = bf.ner_sentence(line)  # 包含分词、词性标注、命名实体识别3步
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


if __name__ == "__main__":
    # test()
    train_destination_data("data/train2_test.data")
    # train_destination_data("data/destination.data")
