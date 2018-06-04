# *-* coding:utf-8 *-*
import re


def tax_code_split_line(line):
    """
    line:开票明细名称、税收分类编码
    :param line:
    :return:
    """
    if len(line) == 0:
        return []

    try:
        pattern = re.compile('(?<=)(.+)(\d+)')
        words = pattern.findall(line)
        for word in words:
            print(word)
    except ValueError as e:
        print("ValueError:" + e)

    return []


if __name__ == "__main__":
    tax_code_split_line("餐饮	103010101")
