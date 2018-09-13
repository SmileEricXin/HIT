# -*- coding:utf-8 -*-
import os
import re
import nlp

# 文本具有的行数
COLOUM_LEN = 7
# 汇总项所在的列
HZX_COL = 6
# 测试标志
TEST = 0


def split_hzx_data(path):
    """
    把汇总项和非汇总项分开
    分别输出到.hzx 和 .nothzx 两个文件
    :param path:
    :return:
    """
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


def taxcode_map(path):
    """
    对包含简称和税收分类编码的编码数据进行处理
    简称不拆分
    简称不拆分
    简称不拆分

    对说明和关键字进行拆分，并提取出名词

    最后输出到.class.map文件
    :param path:
    :return:
    """
    if not os.path.exists(path):
        print(path, " 不存在")
        return

    test_count = 0
    try:
        f_in = open(path, mode="r", encoding="utf-8")
        f_out = open(path + ".map", mode="w", encoding="utf-8")

        pattern = re.compile('(\d+)\s+(.+)\s+(\S+)')
        line = f_in.readline()
        while line:
            # print('line：', line)
            result = pattern.findall(line)
            # print(result[0][0])
            if result and len(result) > 0:
                code = result[0][0]  # 税收分类编码
                class_key = result[0][2]  # 简称
                key_word = result[0][1]  # 待拆分和处理的名词

                # print('key_word:', key_word)

                out = nlp.ner_sentence(key_word)  # 词性标注
                out = list(out)
                key_word = []

                # print(out)
                for word in out:
                    if word[1] in nlp.noun_dict:    # 提取名词
                        key_word.append(word[0])

                f_out.write(code + ' ')
                f_out.write('[' + class_key + '] ')
                for word in key_word:
                    f_out.write(' ' + word)
                f_out.write('\n')

            test_count += 1
            print(':', test_count)

            if TEST == 1:
                if test_count > 10:
                    break

            line = f_in.readline()
    except():
        pass
    finally:
        if f_in:
            f_in.close()
        if f_out:
            f_out.close()


if __name__ == "__main__":
    taxcode_map("./clean_tax_code/03 税收分类编码表_非汇总项.class")
    taxcode_map("./clean_tax_code/03 税收分类编码表_汇总项.class")
    # split_hzx_data("./clean_tax_code/税收分类编码表_行加入分隔符.txt")

