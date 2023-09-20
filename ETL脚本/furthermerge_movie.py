import pandas as pd
import pymysql
import numpy as np
import csv
import threading
import pandas

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


data = pd.read_csv('data/3_merged_movie.csv', encoding='gbk')
data = data.values.tolist()

output_file = open('data/4_further_merged_movie.csv', 'w', newline="", errors='ignore')
output_writer = csv.writer(output_file)
output_writer.writerow(['movieId','productTitle','category','date','genre','score','5starRate','4starRate','3starRate','2starRate','1starRate','director','star','actor','commentNum','producer','studio','runtime','rating','language','meta_amazon_productId','allName'])
print('正在进一步合并电影，并存入表4中......')
tmp = ['','','','','','','','','','','','','','','','','','','','','','']

flag = True
for i in range(len(data)):
    if flag:
        flag = False
        continue


    List = list(data[i])
    if List[title_index] == tmp[title_index]:
        print(type(List[starring_index]))
        if(isinstance(List[starring_index], float) or List[starring_index] == 'nan'):
            List[starring_index] = None

        if (isinstance(tmp[starring_index], float)or tmp[starring_index] == 'nan'):
            tmp[starring_index] = None

        # None转为空字符串，方便字符串连接
        for i in range(22):
            if List[i] == None:
                List[i] = ''
            if tmp[i] == None:
                tmp[i] = ''

        productId = data[i][0]
        try:
            List[genre_index] += tmp[genre_index]
        except:
            print("genre是float???")
        List[category_index] = tmp[category_index]
        try:
            List[directors_index] += tmp[directors_index]
        except:
            print("director是float???")
        try:
            List[starring_index] += tmp[starring_index]
        except:
            print("star是float???")
        try:
            List[actor_index] += tmp[actor_index]
        except:
            print("actor是float???")
        try:
            List[studio_index] += tmp[studio_index]
        except:
            print("studio是float?")
        List[meta_amazon_productId_index] += tmp[meta_amazon_productId_index]
        List[allName_index] += tmp[allName_index]
        # for i in range(1,21):
        #     List[i] += str(tmp[i])

        # 空字符串转为None
        for i in range(21):
            if List[i] == '':
                List[i] = None
    else:
        try:
            lock.acquire()
            output_writer.writerow(List)
            output_file.flush()
            lock.release()
        except Exception as e:
            print('插入表4出错！')
            print(e)
            print(i)
            exit(1)

    tmp = List

print('数据全部成功存入表4！')
output_file.close()
