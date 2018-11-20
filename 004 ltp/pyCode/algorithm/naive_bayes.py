"""
利用朴素贝叶斯方法对训练集进行模型训练
data文件夹下的train文件即为data_train里的 01 train_new.txt.unique_sort.part2.patch.check
"""
import os
import re
import sklearn as skl


def fetch_all_cateory(file_train):
    """
    从train文件夹下提取出所有的简称，即目标的种类。计算种类的概率，即P(T)

    计算先验概率
    :param file_train:
    :return:
    """
    if not os.path.exists(file_train):
        print("file not exist")
        return

    # 提取简称
    f_in = open(file_train, mode="r", encoding="utf-8")
    line = f_in.readline().strip()
    category = dict()
    count = 0
    match_pattern = re.compile('^\*([^*]+)\*')
    while line:
        count += 1
        ma = re.match(match_pattern, line)
        jc = ma.group(1)
        if jc in category.keys():
            category[jc] += 1
        else:
            category[jc] = 1

        line = f_in.readline().strip()

    if f_in:
        f_in.close()

    # 保存简称
    f_out = open(file_train + '.category', mode="w+", encoding="utf-8")
    f_out.write('种类（简称）总数： {}\n'.format(len(category.keys())))

    count = 0
    for key in category.keys():
        count += category[key]
    f_out.write('训练集总数： {}\n'.format(count))

    # 算每种简称的概率，即P(T)
    for key in category.keys():
        pro = category[key] * 100 / count
        f_out.write('P("{}")={}\n'.format(key, pro))

    f_out.write(str(category) + '')

    if f_out:
        f_out.close()


def fetch_category_word(src):
    """
    对 “*营养保健食品*汤臣倍健胶原软骨素钙片” 数据进行提取
    将 ‘营养保健食品’ 和 ‘汤臣倍健胶原软骨素钙片’ 进行返回
    :param src:
    :return:
    """
    pat = re.compile('^\*([^*]+)\*(.*)\s+\d+')
    ma = re.match(pat, src.strip())
    category = ''
    word = ''
    if ma:
        category = ma.group(1)
        word = ma.group(2)

    return category, word


def calc_condition_priority(file_train):
    """
    计算条件概率，即P(S|T)
    S:先验词汇   T:目标种类
    最后是为了计算P(T|S)
    :param file_train:
    :return:
    """
    if not os.path.exists(file_train):
        print(file_train + ' not exist')
        return

    t_words_map = dict()  # key: 种类  value:list，用来存放key对应的训练集样本
    f_in = open(file_train, mode="r", encoding="utf-8")
    line = f_in.readline().strip()
    count = 0
    while line:
        cate_word = fetch_category_word(line)
        # print(cate_word)
        if len(cate_word) == 2:
            if cate_word[0] in t_words_map.keys():
                v = t_words_map[cate_word[0]]
                v.append(cate_word[1])
                t_words_map[cate_word[0]] = v
            else:
                # print(cate_word[1])
                v = list()
                v.append(cate_word[1])
                t_words_map[cate_word[0]] = v

        line = f_in.readline().strip()

    if f_in:
        f_in.close()

    print(t_words_map)


if __name__ == "__main__":
    calc_condition_priority('./data/train')
    # test = fetch_category_word('*营养保健食品*汤臣倍健胶原软骨素钙片 103020899')
    # print(test)
    # # print(help(skl))
    # fetch_all_cateory('./data/train')

