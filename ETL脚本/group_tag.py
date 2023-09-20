import csv
import pymysql
import time
import os
import pandas as pd

def insert_into_csv(line):
    try:
        output_writer.writerow(line)
        output_file.flush()
        # sql = """delete from 1_raw_movie where productId='{}'""".format(line[0])
        # cursor.execute(sql)
        # conn.commit()
    except Exception as e:
        print('错误！', e)
        print(line)
        exit(1)



id_index = 0
rid_index = 20

# 创建二维空列表tag，作为辅助数组
tag = []

print('开始从表1读取数据......\n正在生成分组标签，请耐心等待......')
# 分类算法：O(n^2)

time_start = time.time()  # 记录开始时间

input_file = open('data/1_raw_movie.csv', 'r', errors="ignore")
output_file = open('data/2_grouped_movie.csv', 'w', newline="", errors='ignore')


output_writer = csv.writer(output_file)
data = pd.read_csv('data/1_raw_movie.csv', header=None, encoding='ISO-8859-1')
data = data.values.tolist()

output_writer.writerow(['productId','productTitle','category','date','genre','score','5starRate','4starRate','3starRate','2starRate','1starRate','director','star','actor','commentNum','producer','studio','runtime','rating','language','groupid'])

i = 0
maxIndex = 0
for line in data:
    if i == 0:
        i += 1
        continue
    # 进度显示
    i += 1

    time_now = time.time()
    time_length = (time_now - time_start) / 60

    if i % (len(data)//100) == 0 and i // (len(data)//100) > maxIndex:
        maxIndex += 1
        print('进度：{}%，已花时间：{}min'.format(i // (len(data)//100), time_length))


    line = list(line)   # 元组转列表
    # 不读入表头行
    if line[id_index] == 'productId':
        continue

    # 获取当前行id
    id = line[id_index]

    father_id = -1
    # 查看当前行id是否和别人有关
    jj = 0
    for j in data:
        if jj == 0:
            jj += 1
            continue

        if j[rid_index] == '' or j[rid_index] == None:
            continue
        if id in str(j[rid_index]):
            father_id = j[id_index]

    flag_continue = False
    # 如果有同类且同类已经来了，则加入
    if father_id != -1:
        for i in range(len(tag)):
            # 之前有同类来过，则加入
            if father_id in tag[i]:
                tag[i].append(id)
                line[rid_index] = i     # 打分组标号
                insert_into_csv(line)

                # 要continue掉最外层的循环！
                flag_continue = True
                break
            # 自己是同类里第一个到的，则自己创建组
            # ...

    if flag_continue:
        continue


    # (1)自己无同类，之前也没有人认他做同类
    if line[rid_index] == None or line[rid_index] == '':
        relative_id_list = [id]
    # (2)有同类但自己是第一个到的，创建这一行的group
    else:
        try:
            relative_id_list = str(line[rid_index]).split(',')
        except Exception as e:
            print('字符串分割出错！', e)
            print(line[rid_index])
            exit(1)

        if relative_id_list[0] != '':
            relative_id_list.append(id)
        else:
            relative_id_list = [id]

    # 这一行group加入tag二维数组中
    tag.append(relative_id_list)
    line[rid_index] = len(tag) - 1
    insert_into_csv(line)

input_file.close()
output_file.close()
print('成功存入表2！')