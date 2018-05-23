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
    用于论文的语料预处理
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

if __name__ == "__main__":
    # test()
    train_paper_data("src.data")
