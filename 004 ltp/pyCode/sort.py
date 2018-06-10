# *-* coding:utf-8 *-*


def take_length(data):
    return len(data.split(" "))


def sort_file_data(file_path):
    """
    对文件内容进行排序，重新输出
    :param file_path:
    :return:
    """
    f_in = open(file_path, mode="r", encoding="utf-8")
    f_out = open(file_path + ".sort", mode="w", encoding="utf-8")

    line = f_in.readline()
    lines = []
    while line:
        line.strip()
        lines.append(line)
        line = f_in.readline()

    lines = list(set(lines))
    
    lines.sort(key=take_length)
    for line in lines:
        f_out.write(line)

    f_in.close()
    f_out.close()


if __name__ == "__main__":
    sort_file_data("./data/v2.1/./data/v2.1/train2.1.01.data.out")
