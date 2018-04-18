"""
处理人民日报标注语料（1998年1月份），将其转换成字序列
"""
import os
import re

from pyparsing import unichr

project_root = os.path.dirname(os.path.realpath(__file__))
data_path = os.path.join(project_root, 'data')
people_daily_url = data_path + os.path.sep + '199801' + os.path.sep + '199801.txt'

result_path = project_root+os.path.sep+'result'
all_url = os.path.join(result_path, 'all-char-people-daily-199801')
train_data_url = result_path+os.path.sep+'train-char-people-daily-199801'
val_data_url = result_path+os.path.sep+'val-char-people-daily-199801'
test_data_url = result_path+os.path.sep+'test-people-daily-199801'

match_blank_pattern = re.compile('\\s+')

total_line_num = 0


def convert_fullwidth_to_halfwidth(in_str):
    """全角转半角"""
    ret_str = ""
    for uni_char in in_str:
        inside_code = ord(uni_char)
        if inside_code == 12288:  # 全角空格直接转换
            inside_code = 32
        elif 65281 <= inside_code <= 65374:  # 全角字符（除空格）根据关系转化
            inside_code -= 65248
        ret_str += unichr(inside_code)
    return ret_str

with open(people_daily_url, mode='r', encoding='utf-8') as file:
    for _ in file:  # 使用占位符，我只是想循环而已
        total_line_num += 1

with open(people_daily_url, 'r', encoding='utf-8') as src_file, \
        open(all_url, 'w', encoding='utf-8') as all_file, \
        open(train_data_url, 'w', encoding='utf-8') as train_file, \
        open(val_data_url, 'w', encoding='utf-8') as val_file, \
        open(test_data_url, 'w', encoding='utf-8') as test_file:
    curr_line = 0
    for line in src_file:
        curr_line += 1
        if line == '' or line == '\n':
            continue
        line = convert_fullwidth_to_halfwidth(line)
        to_write = ''
        split_result = match_blank_pattern.split(line)
        length = len(split_result)
        # "a  b  "会被切分成长度为3的数组
        if length <= 3:
            print(line)
            print('WTF', split_result[2], end='')
            continue
        for i in range(1, length):
            # 处理“[江/j  峡/j  大道/n]ns”这种情况
            tmp = split_result[i].split('/')
            for char in tmp[0]:
                if char != '[' and char != ']':
                    to_write += char + ' '
        rate = curr_line / total_line_num
        all_file.write(to_write+'\n')
        # 训练集：验证集：测试集=8：1.5：0.5
        if rate < 0.8:
            train_file.write(to_write+'\n')
        elif rate < 0.95:
            val_file.write(to_write+'\n')
        else:
            test_file.write(to_write+'\n')
