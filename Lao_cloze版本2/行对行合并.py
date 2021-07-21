from tqdm import tqdm


with open(r'data/output/合并文档_pos.txt','r',encoding='utf-8') as fa:
    with open(r'D:\SGF\老挝语相关\Lao_cloze版本2\data\output\3_random\3_random_file.txt','r',encoding='utf-8') as fb:
        with open(r'D:\SGF\老挝语相关\Lao_cloze版本2\data\output\3_random\3_random_pos_file.txt','a+',encoding='utf-8') as fc:
            for line in fa:
                fc.write(line.strip('\r\n'))
                fc.write(fb.readline())
