"""
利用朴素贝叶斯方法对训练集进行模型训练
data文件夹下的train文件即为data_train里的 01 train_new.txt.unique_sort.part2.patch.check
"""
import os
import re
import nlp
import json
import sklearn as skl


"""
可以参考此文章： https://blog.csdn.net/lyl771857509/article/details/78993493

P(T|S)*P(S) = P(T)*P(S|T)
目标是求P(T|S),因为P(S)作为分母，值相同，可以只计算P(T)*P(S|T)
P(T): 税收分类种类在所有训练集中出现的次数
P(S|T): 在该税收分类编码种类中，单词S出现的概率。抓取所有出现T的训练样本，统计这些样本中出现S的次数，用S的次数除以T的次数
"""


def calc_cateory_priority(file_train):
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


def fetch_category_words(file_train):
    """
    提取category对应的words
    比如 ‘*印刷品*汉娜和糖糖 10602010199’， 将印刷品作为key， 汉娜和糖糖作为value
    :param file_train:
    :return:
    """
    if not os.path.exists(file_train):
        print(file_train + ' not exist')
        return

    t_words_map = dict()  # key: 种类  value:list，用来存放key对应的训练集样本
    f_in = open(file_train, mode="r", encoding="utf-8")
    line = f_in.readline().strip()
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

    f_out = open(file_train + ".cat_words_map", mode="w", encoding="utf-8")
    for key in t_words_map.keys():
        f_out.write(key + ' ' + str(t_words_map[key]) + '\n')

    if f_out:
        f_out.close()

    # print(t_words_map)


def wash_words_and_get_noun(line):
    """
    对line进行分词，提取名词
    :param line:
    :return:
    """
    # 去掉停用词
    cm = re.compile('[\dA-Z./!~@#$%&()*-=+:\\\;\'\]\[°（）【】？。，；：‘“]+', re.I)
    words_list = re.sub(cm, ' ', line)

    # print(words_list)
    words = nlp.ner_sentence(words_list)
    words = list(words)
    word_list = list()
    for word in words:
        if len(word) == 2:
            # print(word)
            pos = word[1]
            if pos.find('n') != -1:
                word_list.append(word[0])

    print("word list:", words_list)
    return word_list


def wash_words_of_list(words_list):
    """
    传入的是商品名称的列表，对该列表进行分词，提取名词
    :param words_list:
    :return: 返回map，key为分词后的名词，value为key的计数
    """
    # 去掉停用词
    cm = re.compile('[\dA-Z./!~@#$%&()*-=+:\\\;\'\]\[°（）【】？。，；：‘“]+', re.I)
    words_list = re.sub(cm, ' ', words_list)

    # print(words_list)
    words = nlp.ner_sentence(words_list)
    words = list(words)
    word_count_map = dict()
    for word in words:
        if len(word) == 2:
            # print(word)
            pos = word[1]
            if pos.find('n') != -1:
                if word[0] in word_count_map.keys():
                    v = word_count_map[word[0]]
                    v += 1
                    word_count_map[word[0]] = v
                else:
                    word_count_map[word[0]] = 1

    return word_count_map


def split_train_wrod_and_count(line):
    """
    将种类对应的词汇进行分词并清洗
    :param line:
    :return:
    """
    line = line.strip()
    cm = re.compile('(\S+)\s+(.+)')
    if line:
        ma = re.match(cm, line)
        if ma:
            # print('========')
            # print(ma.group(1))
            # print(ma.group(2))
            word_count_map = wash_words_of_list(ma.group(2))
            # print('----------------')
            # print(word_count_map)

    return ma.group(1), word_count_map


def calc_condition_priority(file1, file2):
    """
    计算条件概率，即P(S|T),T为目标种类
    使用 train.cat_words_map 进行计算

    file1: 读取T的次数
    file2: 统计S的次数
    :return:
    """
    if not os.path.exists(file1):
        print(file1 + 'not exist')
        return

    if not os.path.exists(file2):
        print(file2 + 'not exist')
        return

    # 读取T的概率
    f_1 = open(file1, mode="r", encoding="utf-8")
    line = f_1.readline().strip()
    cat_count_map = {}    # 保存T的概率
    while len(line) > 0:
        if line[0] == '{':
            print('last:', line)
            cat_count_map = json.loads(line, encoding="utf-8")
            break
        line = f_1.readline().strip()

    print('category size:', len(cat_count_map))
    print('map:', cat_count_map)

    if f_1:
        f_1.close()

    # 读取S，并统计S
    f_2 = open(file2, mode="r", encoding="utf-8")
    f_out = open(file2 + '.st', mode="w", encoding="utf-8")

    line = f_2.readline().strip()
    while line:
        ret = split_train_wrod_and_count(line)
        category = ret[0]
        word_count_dict = ret[1]

        if category in cat_count_map.keys():
            for key, value in word_count_dict.items():
                print('key:', key, ' value:', value)

                pri = value * 1.0 / cat_count_map[category]
                # print(pri)
                f_out.write('P({}|{}):{}\n'.format(key, category, pri))

        line = f_2.readline().strip()

    if f_2:
        f_2.close()
    if f_out:
        f_out.close()


def get_s_t_priority():
    """
    读取条件概率P(S|T)
    :return:
    """
    file1 = "./data/train.cat_words_map.st"

    s_t_map = {}
    com = re.compile('P\(([^)]+)\):([0-9.]+)')
    f_1 = open(file1, mode="r", encoding="utf-8")
    line = f_1.readline().strip()
    while line:
        ma = re.match(com, line)
        if ma:
            s_t_map[ma.group(1)] = ma.group(2)
        line = f_1.readline().strip()

    f_1.close()

    return s_t_map


def get_t_priority():
    """
    获取P(T)
    :return:
    """
    file2 = "./data/train.category"
    t_map = {}
    com = re.compile('P\("([^"]+)"\)=([0-9.]+)')
    f_2 = open(file2, mode="r", encoding="utf-8")
    line = f_2.readline().strip()
    while line:
        ma = re.match(com, line)
        if ma:
            t_map[ma.group(1)] = ma.group(2)
        line = f_2.readline().strip()

    f_2.close()

    return t_map


def evaluate_category_of_good(s_t_map, t_map, good):
    """
    评估商品的种类,获取最大的P(T|S)

    :param good: 商品名称
    :return:
    """
    nouns = wash_words_and_get_noun(good)

    t_s_map = {}
    for word in nouns:  # 循环读取S
        for category in t_map.keys():  # 循环读取T
            s_t = word + '|' + category
            if s_t in s_t_map.keys():
                # print('s_t:', s_t)
                # print('category:', category)

                p_s_t = float(s_t_map[s_t])
                p_t = float(t_map[category])
                # print('p_s_t', p_s_t)
                # print('p_t', p_t)

                t_s = category + '|' + word
                p = p_s_t * p_t * 1.0
                # print('t_s:', t_s)
                # print('p:', p)
                t_s_map[t_s] = p_s_t * p_t * 1.0

    max_value = 0
    for key, value in t_s_map.items():
        if max_value < value:
            max_value = value
            max_key = key

    print('{}:{}'.format(max_key, max_value))


if __name__ == "__main__":
    # fetch_all_cateory('./data/train')
    # fetch_category_words('./data/train')
    # print(dir(nlp))
    # calc_condition_priority('./data/train.category', './data/train.cat_words_map')

    # 测试
    # 读取条件概率 P(S|T)
    s_t_map = get_s_t_priority()

    # 读取P(T)
    t_map = get_t_priority()

    # 计算P(T|S)
    evaluate_category_of_good(s_t_map, t_map, '密封胶')
    evaluate_category_of_good(s_t_map, t_map, '水表电池')
    evaluate_category_of_good(s_t_map, t_map, '中华牙膏')
    evaluate_category_of_good(s_t_map, t_map, '喷雾器')
    evaluate_category_of_good(s_t_map, t_map, '会议桌')
    evaluate_category_of_good(s_t_map, t_map, '小风扇')

    # test
    # cm = re.compile('[\dA-Z./!~@#$%&()*-=+:\\\;\'\]\[°（）【】？。，；：‘“]+', re.I)
    # test = re.sub(cm, ' ', "['2018年10abd\月【】：；‘“，。？店长....管理///服!务DD费', '2018年10月线~上会@#$%员（散装）管aadd理()服&*务费', '2018年10月财务-=+:;管理服40.6°450ml务费]',")
    # print(test)


