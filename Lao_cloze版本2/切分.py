# 切分训练验证集
from tqdm import tqdm

path = r'data/output/3_random_88299/3_random_pos_file.txt'

with open(path , 'r', encoding='utf-8') as f1:
    counts = 0
    len_split = (88299 // 10)
    for line in tqdm(f1.readlines()):
        counts += 1
        if counts < len_split * 7:
            with open(path[:-4] + '_train.txt', 'a+', encoding='utf-8') as f2:
                f2.write(line)
        if len_split * 7 <= counts < len_split * 9:
            with open(path[:-4] + '_dev.txt', 'a+', encoding='utf-8') as f3:
                f3.write(line)
        if len_split * 9 <= counts:
            with open(path[:-4] + '_test.txt', 'a+',
                      encoding='utf-8') as f3:
                f3.write(line)
