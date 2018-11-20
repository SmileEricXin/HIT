# *-* coding:utf-8 *-*
import os
import re


def save_data_and_count(total_words, save_path):
    """
    对 total_words 进行保存并计数
    :param total_words:
    :param save_path:
    :return:
    """
    dict_words_count = len(total_words)  # 字典词语总数，notepad++通过正则获取
    # print(dict_words_count)
    try:
        f = open(save_path, mode="w", encoding="utf-8")
        word_set = set(total_words)
        word_map = {}
        for word in total_words:
            if word in word_set:
                if word in word_map.keys():
                    word_map[word] += 1
                else:
                    word_map[word] = 1

        for key in word_map.keys():
            if word_map[key] > 50:
                p = float(word_map[key]) / dict_words_count
                f.write(key + ":" + str(word_map[key]) + ":" + str(p) + "\n")

    finally:
        f.close()


def calc_word_probility(path):
    """
    每1000行进行一次统计
    :param path:
    :return:
    """
    if not os.path.exists(path):
        print(path + " 不存在")
        return

    total_words = []
    line_count = 0
    try:
        f_in = open(path, mode="r", encoding="utf-8")
        line = f_in.readline()
        while line:
            line_count += 1
            line.strip()
            line_words = line.split()
            total_words.extend(line_words)
            if line_count % 10000 == 0:
                save_data_and_count(total_words, path + ".count." + str(line_count))
                total_words = []

            line = f_in.readline()
    finally:
        print("处理完成")
        if len(total_words) > 0:
            save_data_and_count(total_words, path + ".count." + str(line_count))
        f_in.close()


if __name__ == "__main__":
    calc_word_probility("../data/dict/dict_src.data.out")
