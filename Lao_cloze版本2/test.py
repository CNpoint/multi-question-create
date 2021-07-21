with open(r'data/output/3_synonyms/3_synonyms_list.txt','r',encoding='utf-8')as f:
    list = eval(f.readline())
    print(len(list))