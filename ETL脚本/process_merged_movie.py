import pymysql
import numpy as np
import pandas as pd
import csv
import threading

lock = threading.Lock()
title_index = 1
category_index = 2
genre_index = 4
directors_index = 11
starring_index = 12
actor_index = 13
producer_index = 15
studio_index = 16
meta_amazon_productId_index = 20
allName_index = 21

output_file = open('data/5_processed_merged_movie.csv', 'w', newline="", errors='ignore')
output_writer = csv.writer(output_file)
output_writer.writerow(['movieId','productTitle','category','date','genre','score','5starRate','4starRate','3starRate','2starRate','1starRate','director','star','actor','commentNum','producer','studio','runtime','rating','language','meta_amazon_productId','allName'])

# 列表中所有字符串按ch分割
def listOfStr_split_by_char(List, ch):
    tmp = List[:]  # 深拷贝
    List = []
    for i in tmp:
        small_list = i.split(ch)
        small_list = list(filter(lambda x: x != '' and
                                          x != ch, small_list))
        List = List + small_list

    return List

# 列表中所有字符串拼接成一个字符串
def listOfStr_strcat(List):
    str = ''
    for i in List:
        str += (i + ',')

    # 删去最后一个逗号
    str = str[:-1]
    return str

def process_duplicate(Str):
    if Str == None or Str == '':
        return None

    # step1: 按,分割
    List = Str.split(',')

    # step2: 去除每个人的首尾空格
    for i in range(len(List)):
        List[i] = List[i].strip(' ')

    # step3: 去除, nan
    List = list(filter(lambda x: x != ',' and x != 'nan',List))

    # step4: 去除重复元素
    List = np.unique(List)

    # step5: 重新拼接字符串
    result = listOfStr_strcat(List)
    if result == '':
        result = None
    return result

# 处理名字的函数
def process_names(name_str):
    raw_directors = name_str
    if name_str == '' or name_str == None:
        return None
    # step1: 按,分割
    directors = raw_directors.split(',')

    # step2: 去除每个人的首尾空格
    for i in range(len(directors)):
        directors[i] = directors[i].strip(' ')

    # step3: 删除列表中的,  n/a   N.A.  ---  *  =
    directors = list(filter(lambda x: x != 'n/a' and
                                      x != 'n/A' and
                                      x != 'N/a' and
                                      x != 'N/A' and
                                      x != 'N.A' and
                                      x != 'nan' and
                                      x != ',' and
                                      x != '' and
                                      x != '---' and
                                      x != '=' and
                                      x != '*' and
                                      x != 'x', directors))

    # step4: 按 & / 分割
    directors = listOfStr_split_by_char(directors, '&')
    directors = listOfStr_split_by_char(directors, '/')

    # step5: 去除每个人的首尾空格
    for i in range(len(directors)):
        directors[i] = directors[i].strip(' ')

    # step6: 删去人名后面的括号
    # step7: 删去字符串中的more...子串
    for i in range(len(directors)):
        directors[i] = directors[i].split('(')[0]
        directors[i] = directors[i].replace('more...', '')

    # step8: 删去various Various
    directors = list(filter(lambda x: x != 'various' and
                                      x != 'Various', directors))

    # step9: 判断子串(即去除名字缩写)
    for i in range(len(directors)):
        for j in range(len(directors)):
            if directors[i] in directors[j] and i != j:
                directors[i] = ''   # 标记为空串
    directors = list(filter(lambda x: x != '', directors))


    # stepN: 将列表中所有字符串拼接
    result = listOfStr_strcat(directors)
    if result == '':
        result = None
    return result

# 获取表4中的所有数据
data = pd.read_csv('data/4_further_merged_movie.csv', encoding='gbk')
data = data.values.tolist()

print('数据正在处理名字字符串，并插入表5中，请耐心等待......')

index = 1
for i in data:
    List = list(i)
    for j in range(1, 22):
        List[j] = str(List[j])
        if (List[j] == 'nan' or isinstance(List[j], float)):
            List[j] = ''


    List[directors_index] = process_names(List[directors_index])
    List[starring_index] = process_names(List[starring_index])
    List[actor_index] = process_names(List[actor_index])
    List[producer_index] = process_names(List[producer_index])

    # 给每个字段去重
    for j in range(1, 22):
        List[j] = process_duplicate(List[j])

    # 插入表5
    try:
        lock.acquire()
        List[0] = index
        output_writer.writerow(List)
        output_file.flush()
        index += 1
        lock.release()
    except Exception as e:
        print('插入表5出错！')
        print(e)
        print(i)
        exit(1)

print('数据全部成功插入表5！')