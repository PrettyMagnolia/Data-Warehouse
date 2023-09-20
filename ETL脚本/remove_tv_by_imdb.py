import pandas as pd
import csv

# 读入amazon整合好的数据
data = pd.read_csv('5_processed_merged_movie.csv', header=None, encoding='gb18030', error_bad_lines=False)
data=data.values[0::,0::]

# 读入imdb数据
judgeData = pd.read_csv('movie_from_imdb_mini.csv', header=None, encoding='gb18030', error_bad_lines=False)
judgeData = judgeData.values[0::,0::]

# 输出文件
output_file = open('6_noTV_amazon_data.csv', 'w', newline="", errors='ignore')
output_writer = csv.writer(output_file)

# 利用imdb得到的分类数据，筛掉amazon数据中的TV
i_amazon = 0
j_imdb = 0

print('开始处理，请耐心等待......')

def smashLineNan(line):
    for i in range(len(line)):
        if 'nan' in str(line[i]):
            print("nan!")
            line[i] = None

while i_amazon < len(data):
# for i_amazon in range(len(data)):
    # 不读入表头行
    if(i_amazon == 0):
        i_amazon += 1
        j_imdb += 1
        continue

    if(j_imdb == len(judgeData)-1):
        smashLineNan(data[i_amazon])
        output_writer.writerow(data[i_amazon])
        i_amazon += 1
        continue

    data[i_amazon][0] = int(data[i_amazon][0])
    judgeData[j_imdb][0] = int(judgeData[j_imdb][0])

    assert(i_amazon == data[i_amazon][0])

    if(i_amazon < judgeData[j_imdb][0]):
        smashLineNan(data[i_amazon])
        output_writer.writerow(data[i_amazon])
        i_amazon += 1
        continue

    if i_amazon == judgeData[j_imdb][0]:
        imdb_genre = judgeData[j_imdb][4]
        # 如果imdb判断确实是movie，加入到最新列表中
        if not('movie' not in imdb_genre and 'Movie' not in imdb_genre and imdb_genre != 'video'):
            smashLineNan(data[i_amazon])
            output_writer.writerow(data[i_amazon])
        i_amazon += 1
        j_imdb += 1
        continue

    print('error')

output_file.close()

print("处理完成！")