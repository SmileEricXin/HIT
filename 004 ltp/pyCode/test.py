# -*- coding: utf-8 -*-
from pyltp import SentenceSplitter as ss
from pyltp import Segmentor
import os
import nlp

def split_sentence(sentences):
    """分句"""
    sentence = ss.split(sentences)
    print('\n'.join(sentence))


def split_word(sentence):
    """分词"""
    segmentor = Segmentor()
    segmentor.load("../ltp/cws.model")
    words = segmentor.segment(sentence)
    # print('\n'.join(words))
    segmentor.release()
    # print(words)

    return words


def recognize_word(words):
    """命名实体识别"""
    from pyltp import NamedEntityRecognizer
    recognizer = NamedEntityRecognizer()
    recognizer.load("../ltp/ner.model")

    postags = ['nh', 'r', 'r', 'v']
    netags = recognizer.recognize(['元芳', '你', '怎么', '看'], postags)
    print('\t'.join(netags))
    recognizer.release()


if __name__ == "__main__":
    split = nlp.ner_sentence("我在金蝶云之家")
    print(list(split))
    # words = split_word("中国位于亚洲东部")
    # list_word = list(words)
    # print(list_word)
    # recognize_word(list_word)
    # split_word('辛浪在金蝶云之家工作')
    # split_sentence('元芳你怎么看？我就趴窗口上看呗！')

