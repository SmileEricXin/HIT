import os


__doc__ = """
this file for base function, like split word, split sentences, and so on.
"""


# 名词标注列表
noun_dict = ["n", "nh", "ni"]


postag_dict = {
    "a": "形容",
    "b": "名词修饰",
    "c": "连词",
    "d": "副词",
    "e": "感叹",
    "g": "词素",
    "h": "字首",
    "i": "成语",
    "j": "缩写",
    "k": "后缀",
    "m": "数字",
    "n": "一般名词",
    "nd": "方向名词",
    "nh": "名字",
    "ni": "组织名",
    "nl": "位置名词",
    "ns": "地理名词",
    "nt": "时态名词",
    "nz": "专有名词",
    "o": "拟声",
    "p": "介词",
    "q": "数量",
    "r": "代词",
    "u": "助动词",
    "v": "动词",
    "wp": "标点",
    "ws": "外来词",
    "x": "非词干"
}


ner_dict = {
    "Nh": "人名",
    "Ni": "机构名",
    "Ns": "地名"
}


def postags_enhance(postags):
    """
    对磁性标注进行加注，比如a, 加注为a(形容词)。
    :param postags:
    :return: 加注后的词性标注
    """
    ret_postags = []
    for tag in postags:
        if tag in postag_dict.keys():
            # tag = tag + '(' + postag_dict[tag] + ')'
            ret_postags.append(tag)

    return ret_postags


def split_document(doc):
    """
    function: 将文档切分为语句
    doc: 待切分的文档
    """
    from pyltp import SentenceSplitter
    sentences = SentenceSplitter.split(doc)
    return list(sentences)


def split_sentence(sentence):
    """
    function: 将句子切分为词语
    sentence: 句子
    """
    from pyltp import Segmentor
    segmentor = Segmentor()
    segmentor.load("../ltp/cws.model")
    words = segmentor.segment(sentence)
    segmentor.release()

    return words


def postag_word(words):
    """
    function: 对words进行词性标注
    words: 待识别词语，list
    """
    from pyltp import Postagger
    postagger = Postagger()
    postagger.load("../ltp/pos.model")

    postags = postagger.postag(words)
    postagger.release()

    return postags


def recognize_word(words, postags):
    """
    function: 命名实体识别,
    wrods: 待识别单词
    postags: 单词词性标注
    """
    from pyltp import NamedEntityRecognizer
    recognizer = NamedEntityRecognizer()
    recognizer.load("../ltp/ner.model")

    nertags = recognizer.recognize(words, postags)
    recognizer.release()

    return nertags


def ner_sentence(sentence):
    """
    对句子进行命名实体识别，本函数包含分词、词性标注、命名实体识别三步
    :param sectence:
    :return:
    """
    words = split_sentence(sentence)
    # print(list(words))
    # print('\t'.join(words))
    postags = postag_word(words)
    postags = postags_enhance(postags)
    # print('\t'.join(postags))
    ner = recognize_word(words, postags)
    # print('\t'.join(ner))

    ret = zip(list(words), list(postags), list(ner))
    return ret
