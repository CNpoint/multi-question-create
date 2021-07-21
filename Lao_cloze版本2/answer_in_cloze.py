import random
from random import sample
from tqdm import tqdm
import re
import os
import time

# TODO 你需修改都在TODO里。
'''
    author：Guofeng S
    本文档用于生产完形填空文件，从形近词、近义词文件中寻找最近的前k个词语，搭配上库中的随机option，共n个词语
    
    
    输入文件：
        文字格式为 答案|段落，例如：
            setengah hati|Itu pun dengan setengah hati.
    
    
    输出：
    1.result_key是答案；
    2.cloze_seg是挖空句子；
    3.choice_num是选项的个数，一般来说是4个；
    4.que_choice 是选项+句子，例如：
        ['setengah hati', 'semangat kebangsaan']|['Itu pun dengan <option000000>.']

    5.option_num,挖空编号，如：
            <option000001#
    option_index，问题编号的选项中的答案索引，0是指第一个，

    一个完整例子，例如 ：
               原句为：
                    Itu pun dengan setengah hati.（太心不在焉了。）
               问题和选项为：
                    问题：['Itu pun dengan <option000000>.']
                    选项：['setengah hati', 'semangat kebangsaan']
               选项：['setengah hati', 'semangat kebangsaan']
               答案是：setengah hati
               选项编号为：<option000000#
               则索引为：0
    '''


def create_list(path_file):
    # 创建一个用于组成选项的候选词集合
    with open(path_file, 'r', encoding='utf-8') as f:
        str0 = []
        for line in f:
            str3 = line.split('|')
            str0.append(str3[0])
            # str0是表格

        option_list = list(set(str0))

        return option_list


def create_cloze(mix_line, key_num):
    # 创建完形填空题，生成answer和带填空例句
    hang = 0
    line2 = mix_line.split('|')
    # print(line2)
    keyword = line2[0]
    if re.findall(keyword, line2[1], flags=re.IGNORECASE):
        # 如果前面的option在例句中，就用<option>换掉
        # print(line2)
        option = line2[0]
        # seg = line2[1].replace(keywords[i],'<option>')
        capital_python = re.findall(keyword, line2[1], flags=re.IGNORECASE)
        # 忽略大小写找option

        option_num = ' <option' + str("{:0>6d}".format(key_num)) + '> '
        # option位置id

        # TODO 只想替换一行中多个中的一个

        sub_result = line2[1].replace(keyword, option_num, 1)
        # sub_result = re.sub(keyword, option_num, line2[1], flags=re.IGNORECASE)

        # 替换option

        # 这是答案
        result_key = keyword
        answer_result = option_num + ',' + result_key

        # with open(ans_file, "a+", encoding='utf-8') as f3:
        #     f3.write(option_num + ',' + resul_key + '\n')

        capital_python = str(capital_python)
        capital_python = capital_python.lower()
        # 有多个option，但是大小写不同，忽略大小写
        capital_python = eval(capital_python)
        capital_python = set(capital_python)

        seg = str(sub_result)
        # print(option,'|',seg)
        # with open(cloze_file, "a+", encoding='utf-8') as f2:
        #     f2.write(option + '|' + seg)
        # 这是完形填空句子
        cloze_seg = option + '|' + seg
        fag = '<option'
        hang += 1
        time = seg.count(fag)
        # if time > 1:
        #     print('多个option存在的行：', hang, '个数：', time)
        return result_key, seg, option_num


# 读取对应固定短语的近义词并输出他的列表,输入行，答案，返回近义词列表
# option_input是要找的option他的近义词，near_path是近义词文件
def Get_Synonyms(option_input, file_path, Synonyms_count):
    with open(file_path, 'r', encoding='utf-8')as f:
        for line in f.readlines():
            line = line.replace('\n', '')
            segs = line.split('|')
            # segs[0]是option, segs[1]是他的近义词们
            option_0 = segs[0]
            option_nears = segs[1].split(',')
            # TODO 这里ramdom输出4个近义词
            # option_near = random.sample(option_nears, 4)
            # TODO 或者输出列表前四个
            option_near = option_nears[:Synonyms_count]
            if option_input == option_0:
                # 输出的是其近义词列表~
                return option_near

            else:
                continue


# 返回随机选项
def Get_random_options(option_input, file_path):
    with open(file_path, 'r', encoding='utf-8')as f:
        for line in f.readlines():
            line = line.replace('\n', '')
            segs = line.split('|')
            # segs[0]是option, segs[1]是他的近义词们
            option_0 = segs[0]
            option_nears = segs[1].split(',')
            # TODO 这里ramdom输出1个近义词
            option_near = random.sample(option_nears, 1)
            # TODO 或者输出列表前四个
            # option_near = option_nears[:1]
            if option_input == option_0:
                # 输出的是其近义词列表~
                return option_near

            else:
                continue


# 找形似词
def Get_Resemble(option_input, file_path, Resemble_count):
    with open(file_path, 'r', encoding='utf-8')as f:
        for line in f.readlines():
            line = line.replace('\n', '')
            segs = line.split('|')
            # segs[0]是option, segs[1]是他的近义词们
            option_0 = segs[0]
            option_nears = segs[1].split(',')
            # TODO 这里ramdom输出2个形近词
            # option_near = random.sample(option_nears, 4)
            # TODO 或者输出列表前四个
            option_near = option_nears[:Resemble_count]
            if option_input == option_0:
                # 输出的是其近义词列表~
                return option_near

            else:
                continue


def question_file(list_file, result_key, cloze_line, choice_num, Synonyms_file_path, Resemble_file_path, Synonyms_count,
                  Resemble_count):
    # 生成组合文件，文件有多个候选项，
    # 获取近义词函数 near_keywords
    Synonyms_keywords = Get_Synonyms(result_key, Synonyms_file_path, Synonyms_count)
    Resemble_keywords = Get_Resemble(result_key, Resemble_file_path, Resemble_count)
    # print(Resemble_keywords)
    near_keywords = Synonyms_keywords + Resemble_keywords
    r = random.random
    # print(str(time.time()).split('.')[1])
    random.seed(int(str(time.time()).split('.')[1]))
    random.shuffle(near_keywords, r)
    # print('-----')
    # print(near_keywords)
    # random_keyword = list_file
    # keywords = near_keywords.append(random_keyword)
    # print(keywords)
    # 读取列表形式
    # print(len(keywords))
    # with open(r"data/630/output/固定短语/固定短语_8962_完形填空.txt", "r", encoding='utf-8') as f1:
    hang = 1
    counts = 0
    list_options = near_keywords
    # print(list_options)

    # option
    list_examples = []
    # 例句
    # hangs = len(f1.readlines())
    # print(hangs)

    cloze_line = cloze_line.replace('\n', '')
    line2 = cloze_line
    seg = line2.split('|')
    hang += 1
    # print(seg[0])
    list_options.append(seg[0])
    # option集合，首先要有个标准答案 ↑
    r = random.random
    # print(str(time.time()).split('.')[1])
    random.seed(int(str(time.time()).split('.')[1]))
    random.shuffle(list_options, r)
    list_examples.append(seg[1])
    # 例句集合
    counts += 1
    # print(list_options)

    # 每1行输出1个option集合的列表，并重置列表，行数
    if counts == 1:
        options = list_options  # 带答案的option选项列表
        # print(hang)
        examples = list_examples
        set_options_out = list(set(options))
        r = random.random
        # print(str(time.time()).split('.')[1])
        random.seed(int(str(time.time()).split('.')[1]))
        random.shuffle(set_options_out, r)
        # 答案options

        # print(set_options_num)
        # print(len(options),len(set(options)))

        result_num = len(set(set_options_out))
        # 每7条例句的答案个数
        add_num = choice_num - result_num
        # 需要添加的option个数

        while len(set_options_out) < choice_num:
            # 添加option元素直到满足choice_id个选项
            # sample(a,n):从序列a中随机抽取n个元素，并将n个元素生以list形式返回。
            r = random.random
            # print(str(time.time()).split('.')[1])
            random.seed(int(str(time.time()).split('.')[1]))
            random.shuffle(list_file, r)

            add_keys = list_file[0]
            add_keys = str(add_keys)
            add_keys = add_keys.replace('[', '')
            add_keys = add_keys.replace(']', '')
            add_keys = add_keys.replace("'", '')
            set_options_out.append(add_keys)

            set_options_out = list(set(set_options_out))
            r = random.random
            # print(int(time.time()))
            random.seed(int(time.time()))
            random.shuffle(set_options_out,r)
            # set防止选项有重复！

        # print(set_options_out)
        # print(len(set_options_out),len(examples))
        # 10  7

        # with open(r'data/630/output/固定短语/固定短语_8962_选项_题目.txt', "a+", encoding='utf-8') as fa:
        #     fa.write(str(set_options_out) + '|' + str(examples) + '\n')

        ques_choice = str(set_options_out) + '|' + str(examples)

        counts = 0
        list_options = []
        # option
        list_examples = []
        # 例句
        return ques_choice, set_options_out


# 创建答案索引 choice_index
def create_index(ques_line, answer_option, option_num):
    # line是选项_题目的line，lines是answer的line
    ques_line = ques_line.replace('\n', '')
    line2 = ques_line.split('|')
    list_option = eval(line2[0])
    # 选项_题目的所有选项
    list_question = eval(line2[1])
    # 读取所有例句
    # print(list_option,len(list_option))
    # 10
    # print(list_question,len(list_question))
    # 7
    # with open(r"data/630/output/固定短语/固定短语_8962_answer.txt", 'r', encoding='utf-8') as f1:
    #     for lines in f1.readlines():

    # 对应答案
    # print(option_num,option_ans)
    # index1 = list.index('a')
    for i in range(len(list_question)):
        # 如果答案编号在例句中，则得到该词语在选项中索引位置
        if option_num in list_question[i]:
            option_index = list_option.index(answer_option)
            # print(option_num,option_index,option_ans)

            return option_num, option_index
            # with open(r"data/630/output/固定短语/固定短语_8962_index.txt", 'a+', encoding='utf-8') as f2:
            #     f2.write(str(option_num) + ',' + str(option_index) + '\n')
        else:
            print("找不到目标答案索引！")


# 格式化处理文本
def format_file(input_line, option_index):
    input_line = input_line.replace('|', ', "sentence": ')
    line2 = input_line.replace('\n', '')
    output_line = '"],"answer":[' + "'" + str(option_index) + "']" + ',"candidates": ' + line2 + '}' + '\n'
    return output_line


# 存储文件
def save_file(file_path, seg):
    with open(file_path, 'a+', encoding='utf-8') as f:
        seg = seg.replace('\n', '')
        f.write(str(seg) + '\n')


# 读取文件夹下所有文件
def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        # 当前目录
        # print(root)
        # 当前目录下所有子目录
        # print(dirs)
        # 当前路径下所有非目录文件
        # print(files)
        return root, files


def main(input_file, index_path, quest_path, list_path, choice_count, Synonyms_file_path, Resemble_file_path,
         Synonyms_count, Resemble_count):
    option_list = create_list(input_file)
    # Synonyms_list = create_list(Synonyms_file_path)
    # Resemble_list = create_list(Resemble_file_path)
    # list_file = option_list + Synonyms_list + Resemble_list
    # print(option_list)
    # save_file(list_path, str(option_list))
    with open(input_file, 'r', encoding='utf-8') as f2:
        count = 0
        list_file = []
        for line in tqdm(f2.readlines()):
            # 获取答案和题目
            result_key, cloze_seg, option_num = create_cloze(mix_line=line, key_num=count)
            # 答案加题目
            option_seg = result_key + '|' + cloze_seg
            # option数
            count += 1
            # result_key是答案，cloze_seg是挖空句子
            # print('================')
            # print(result_key,cloze_seg)
            # choice_num是选项的个数

            que_choice, set_options_out = question_file(list_file=option_list, result_key=result_key,
                                                        cloze_line=option_seg,
                                                        choice_num=choice_count, Synonyms_file_path=Synonyms_file_path,
                                                        Resemble_file_path=Resemble_file_path,
                                                        Synonyms_count=Synonyms_count, Resemble_count=Resemble_count)
            # print('**************')
            # que_choice 是选项+句子
            # ['setengah hati', 'semangat kebangsaan']|['Itu pun dengan <option000000>.']
            # print('++++++++')
            # print(que_choice)
            # ques_line是选项_题目的line，answer_line是answer的line
            option_num, option_index = create_index(que_choice, result_key, option_num)
            # print('########')
            # option000001# ('<option000001>', 0) 问题编号及索引，0是指第一个
            # print(option_num,option_index)

            # 组合格式
            index_file = str(option_num) + ',' + str(option_index) + '\n'
            quest_file = format_file(que_choice, option_index)

            list_file = list(list_file) + list(set_options_out) + list(option_list)
            # print(list_file)
            list_file = set(list_file)
            # print(list_file)

            # save_file(index_path, index_file)
            save_file(quest_path, quest_file)
        print(len(list_file))
        save_file(list_path, str(list(list_file)))


def cut_file(path,hang):
    with open(path, 'r', encoding='utf-8') as f1:
        counts = 0
        len_split = (hang // 10)
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




if __name__ == '__main__':
    # 输入例句段落文件地址
    # TODO 需要处理的文件地址，该地址下的所有文件都会被处理
    files_dir = r'data/input'
    # 批量制作文件夹下所有文件的完型填空
    root, files = file_name(files_dir)
    for i in range(len(files)):
        input_file = root + '/' + files[i]
        # 原始文档
        # TODO 近义词文件地址
        Synonyms_file_path = r'data/neighbour_files/wordlist_synonyms.txt'
        # TODO 形近词文件地址
        Resemble_file_path = r'data/neighbour_files/wordlist_resemble.txt'
        files_name = files[i]
        # 取出文件名
        # print('===')
        # print(files_name)
        # TODO 你想要一共几个词做选项？这里是4个
        choice_num = 4
        # print(files_name)

        # TODO 你想要几个近义词做选项？
        Synonyms_count = 3
        # TODO 你想要形近词做选项？
        Resemble_count = 0
        # print(files_name)
        # TODO 什么搭配
        with_out = '3_synonyms'

        index_path = os.path.join('data', 'output', with_out, with_out + '_index_file.txt')
        # 输出答案索引文件
        quest_path = os.path.join('data', 'output', with_out, with_out + '_file.txt')
        # 输出题目训练文件
        list_path = os.path.join('data', 'output', with_out, with_out + '_list.txt')
        # 输出list文件
        print('开始生成数据集...')
        main(input_file=input_file, index_path=index_path, quest_path=quest_path,
             list_path=list_path, choice_count=choice_num, Synonyms_file_path=Synonyms_file_path,
             Resemble_file_path=Resemble_file_path, Synonyms_count=Synonyms_count, Resemble_count=Resemble_count)

        print('数据集生成完毕，开始并入POS...')
        train_file_path = quest_path[:-4]+'_pos_file.txt'
        print(train_file_path)
        with open(r'data/59536_合并前置文档.txt', 'r', encoding='utf-8') as fa:
            with open(quest_path, 'r', encoding='utf-8') as fb:
                with open(train_file_path, 'a+',
                          encoding='utf-8') as fc:
                    for line in fa:
                        fc.write(line.strip('\r\n'))
                        fc.write(fb.readline())

        # print('并入完毕开始切分...')
        # cut_file(train_file_path,hang=59536)
        # print('切分完成！')
        os.unlink(quest_path)