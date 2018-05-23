# -*- coding: utf-8 -*-
import os


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
            tag = tag + '(' + postag_dict[tag] +')'
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


if __name__ == "__main__":
    # doc = "我在哈尔滨工业大学读工程硕士。你要不要一起来？Future is full of imagination."
    doc = "我在哈尔滨工业大学读工程硕士。"
    sentences = split_document(doc)
    print(sentences)
    print(type(sentences))

    for sentence in sentences:
        words = split_sentence(sentence)
        print("切分后的词语：" + '\t'.join(words))

        postags = postag_word(words)
        postags = postags_enhance(postags)
        print("词性标注：" + '\t'.join(postags))

        nertags = recognize_word(words, postags)
        print("命名实体识别：" + '\t'.join(nertags))
