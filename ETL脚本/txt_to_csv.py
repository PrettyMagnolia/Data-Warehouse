import numpy as np
import pandas as pd
import csv

txt_path = "./data/movies.txt/movies.txt"
csv_path = "./data/all_productId.csv"

f_input = open(txt_path, 'r', encoding='utf-8', errors='ignore')
f_ouput = open(csv_path, 'w', newline="")
writer = csv.writer(f_ouput)

print('开始逐行读取！请耐心等待！')

flag = ''
while True:
    line = f_input.readline()
    if not line:
        break
    if('productId' in line):
        id = line.split()[1]
        if flag != id:
            flag = id
            writer.writerow([id])
            # print(id)


f_input.close()
f_ouput.close()

print('读取完毕！')


