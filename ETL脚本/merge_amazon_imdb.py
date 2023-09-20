import pandas as pd
import csv
import numpy as np

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
date_index = 3

imdb_genre_index = 7
imdb_star_index = 5
imdb_actor_index = 6
imdb_director_index = 3
imdb_date_index = 8
imdb_productId_index = 1

# 读入amazon数据
amazonData = pd.read_csv('6_noTV_amazon_data.csv', header=None, encoding='gb18030', error_bad_lines=False)
amazonData=amazonData.values[0::,0::]

# 读入imdb数据
imdbData = pd.read_csv('movie_from_imdb_pro.csv', header=None, encoding='ISO-8859-1', error_bad_lines=False)
imdbData = imdbData.values[0::,0::]

# 输出文件
output_file = open('right_final_merged_data.csv', 'w', newline="", errors='ignore')
output_writer = csv.writer(output_file)

i_amazon = 0
j_imdb = 0

def smashItemNan(item):
    if(type(item) != 'string'):
        return item

    if 'nan' in item:
        return None

def smashLineNan(line):
    for i in range(len(line)):
        if 'nan' in str(line[i]):
            line[i] = None

    return line


def merge(str1, str2):
    return str1 + "," + str2

def compensate(old, new):
    if(old != None):
        return old

    if(old == None and new == None):
        return None

    if(old == None and new != None):
        return new


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

print(len(amazonData))
print("开始处理......")
while i_amazon < len(amazonData):
    print(amazonData[i_amazon][0])
    if amazonData[i_amazon][0] == 111234:
        print('here!')
# for i_amazon in range(len(amazonData)):
    # 不读入表头行
    if(i_amazon == 0):
        i_amazon += 1
        j_imdb += 1
        continue

    if (j_imdb >= len(imdbData)):
        smashLineNan(amazonData[i_amazon])
        output_line = list(amazonData[i_amazon])
        output_line.append(None)
        if output_line[0]==111234 or output_line[0]=='111234':
            print('now here!')
        output_writer.writerow(output_line)
        i_amazon += 1
        continue

    amazonData[i_amazon][0] = int(amazonData[i_amazon][0])
    imdbData[j_imdb][0] = int(imdbData[j_imdb][0])

    if(amazonData[i_amazon][0] < imdbData[j_imdb][0]):
        smashLineNan(amazonData[i_amazon])
        output_line = list(amazonData[i_amazon])
        output_line.append(None)
        if output_line[0]==111234 or output_line[0]=='111234':
            print('now here!')
        output_writer.writerow(output_line)
        i_amazon += 1
        continue

    # temp = i_amazon
    # i_amazon = amazonData[i_amazon][0]
    # 如果对应上了
    # 1.合并genre,star,actor,director
    # 2.补充date
    # 3.新增meta_imdb_productId
    if amazonData[i_amazon][0] == imdbData[j_imdb][0]:
        # 1.合并genre,star,actor,director
        try:
            amazonData[i_amazon][genre_index] = merge(amazonData[i_amazon][genre_index], imdbData[j_imdb][imdb_genre_index])
        except:
            1

        try:
            amazonData[i_amazon][starring_index] = merge(amazonData[i_amazon][starring_index], imdbData[j_imdb][imdb_star_index])
        except:
            1

        try:
            amazonData[i_amazon][actor_index] = merge(amazonData[i_amazon][actor_index], imdbData[j_imdb][imdb_actor_index])
            # 主演也要添到参演人员里面
            amazonData[i_amazon][actor_index] = merge(amazonData[i_amazon][actor_index], amazonData[i_amazon][starring_index])
        except:
            1

        try:
            amazonData[i_amazon][directors_index] = merge(amazonData[i_amazon][directors_index], imdbData[j_imdb][imdb_director_index])
        except:
            1

        # 给上面四个属性做字符串处理
        try:
            amazonData[i_amazon][starring_index] = process_names(amazonData[i_amazon][starring_index])
        except:
            1

        try:
            amazonData[i_amazon][actor_index] = process_names(amazonData[i_amazon][actor_index])
        except:
            1

        try:
            amazonData[i_amazon][directors_index] = process_names(amazonData[i_amazon][directors_index])
        except:
            1

        # 2.补充date
        amazonData[i_amazon][date_index] = compensate(amazonData[i_amazon][date_index], imdbData[j_imdb][imdb_date_index])



        # amazonData[i_amazon].append(imdbData[j_imdb][imdb_productId_index])

        # 3.给每个字段去重，去nan
        for ii in range(len(amazonData[i_amazon])):
            amazonData[i_amazon][ii] = process_duplicate(str(amazonData[i_amazon][ii]))
            amazonData[i_amazon][ii] = smashItemNan(amazonData[i_amazon][ii])

        # 4.输出到新文件
        output_line = list(amazonData[i_amazon])


        # 5.新增meta_imdb_productId
        output_line.append(imdbData[j_imdb][imdb_productId_index])
        # np.append(amazonData[i_amazon], imdbData[j_imdb][imdb_productId_index])
        if output_line[0]==111234 or output_line[0]=='111234':
            print('now here!')
        output_writer.writerow(output_line)

        i_amazon += 1
        j_imdb += 1
        continue

    if j_imdb < len(imdbData):
        j_imdb += 1
    continue
    # print("error")


output_file.close()
print("处理完成！")