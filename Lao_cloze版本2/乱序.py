
# 乱序1

import os, sys
import random
from tqdm import tqdm
#
def get_line_offset(f):
    lines_start_offset=list()
    f.seek(0)
    lines_start_offset.append(f.tell())
    line = f.readline()
    while line:
        line=line.strip()
        lines_start_offset.append(f.tell())
        line = f.readline()
    return lines_start_offset

def rewrite_file(f_in, f_out, lines_start_offset):
    for i in tqdm(range(len(lines_start_offset))):
        f_in.seek(lines_start_offset[i], 0)
        line=f_in.readline()
        f_out.write(line)

if __name__ == "__main__":
    path1 = r'data/input/Laos_dataset.txt'
    path2 = r'data/input/Laos_dataset_mix.txt'
    f = open(path1, 'r', encoding='utf-8')
    f_out = open(path2, 'w', encoding='utf-8')
    lines_start_offset = get_line_offset(f)
    random.shuffle(lines_start_offset)
    rewrite_file(f, f_out, lines_start_offset)
    f.close()
    f_out.close()


# 乱序2
# import sys,random
# from tqdm import tqdm
# lines = sys.stdin.readlines()
# olines=[]
# while lines:
#     olines.append(lines.pop(random.randrange(len(lines))))
#     tqdm(sys.stdout.write(r'data/606/mix_1974_例句4.txt'.join(olines)))


# 乱序3
# import os
# import random
#
# j = 0
# for i in tqdm(range(1)):
#     j = i + 1
#     out = open(r'data/610/mix例句/1000_mix_'+str(j)+'.txt','w',encoding='utf-8')
#     lines=[]
#
#     with open(r'data/610/mix例句/1000_mix_'+str(i)+'.txt', 'r',encoding='utf-8') as infile:
#         for line in infile:
#             lines.append(line)
#         random.shuffle(lines)
#         for line in lines:
#             out.write(line)


