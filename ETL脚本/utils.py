import requests
import bs4
import random
from lxml import etree
from fake_useragent import UserAgent
import os
import pandas as pd
import threading

def get_ip_list(url, headers):
	web_data = requests.get(url, headers=headers)
	soup = bs4.BeautifulSoup(web_data.text, 'lxml')
	ips = soup.find_all('tr')
	ip_list = []
	for i in range(1, len(ips)):
		ip_info = ips[i]
		tds = ip_info.find_all('td')
		ip_list.append(tds[1].text + ':' + tds[2].text)
	return ip_list


def get_random_ip(ip_list):
	proxy_list = []
	for ip in ip_list:
		proxy_list.append('http://' + ip)
	proxy_ip = random.choice(proxy_list)
	proxies = {'http': proxy_ip}
	return proxies

def writeTXT(res):
	with open("./data/codes.txt", "w", encoding='utf-8') as f:
		f.write(res.text)

class FreeIp():
    def __init__(self):
        self.start_url = "https://ip.jiangxianli.com/?page={}"
        self.url_list = [self.start_url.format(i) for i in range(1, 6)]  # 这里可以按实际情况更改
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"}

    def parse(self, html):
        tr_list = html.xpath("//table[@class='layui-table']/tbody/tr")
        ip_list = []
        for tr in tr_list:
            if tr.xpath("./td/text()")[2] == "高匿" and tr.xpath("./td/text()")[3] == "HTTP":
                ip = {}
                ip["ip"] = tr.xpath("./td/text()")[0]
                ip["port"] = tr.xpath("./td/text()")[1]
                ip_list.append(ip)

        return ip_list

    def check_ip(self, ip_list):
        correct_ip = []
        for ip in ip_list:
            ip_port = ip["ip"] + ":" + ip["port"]
            proxies = {'http': ip_port}
            try:
                response = requests.get('http://icanhazip.com/', proxies=proxies,
                                        timeout=5).text
                if response.strip() == ip["ip"]: # 如果请求该网址，返回的IP地址与代理IP一致，则认为代理成功
                    print("可用的IP地址为：{}".format(ip_port))
                    correct_ip.append(ip_port)
            except:
                print("不可用的IP地址为：{}".format(ip_port))
        return correct_ip

    def get_ip(self):
        # 获得URL地址
        correct_all_ip = []
        for url in self.url_list:
            # 获得请求，
            response = requests.get(url, headers=self.headers).content.decode()
            # 解析页面
            html = etree.HTML(response)
            # 得到IP
            ip_list = self.parse(html)
            # 检查IP
            correct_ip = self.check_ip(ip_list)
            correct_all_ip.extend(correct_ip)
        # 返回所有IP
        return correct_all_ip

def GetUserAgent():
    '''
    功能：随机获取HTTP_User_Agent
    '''

    ua = UserAgent()
    user_agent = ua.random
    return user_agent

def resetHeaders(headers):
    mycookie = 'session-id=141-6875170-2315803; ubid-main=130-1759823-8364416; av-timezone=Asia/Shanghai; lc-main=en_US; x-main="pVaTxebzQiwz90uGQgr9k1@plEHzYa5JZvksQF912iCVriiTegY8EgR5RLq942ds"; at-main=Atza|IwEBIOx9R1T0Y2UvzfhMlDnd44D2Yv9ksXOxFFAY_F5WM3YGbStP37dnw8qQwHbNDEDYgMQ3L7DzopxqAsYMXdIe4eeDhl4robemocBqTytNu8mTdIU5nO4b4eIo8gRDozMr1HnXQorhEYvjzgd625Nxt0xXyxON0JrXo2Q4VQwnkkvTBCz1VKR92g0al8sqC8tMbexJckxJncf69c1ZMjjRMWqA; sess-at-main="6EyvMZkvEphCrInxZCnj3we2jnO4xRNODJNLztVXTBs="; sst-main=Sst1|PQF4A8ou7BKKVbt9BC-4OOZVCUZPzUYNiimY-0WgLL0J_Q2vw2E8dgZCFqePUGVioKTS1L54hHKAZ2mgtLr_-aRxvjcQ3TW30rHgRqXXX9uZGnML1yyJkPBZcMajk1Lh-TVyn13vVuczSo77ONigcA592lBUb6m1bPYUTIHS6Fmf76d1wLE2xxqPCinEGb370ZPMhy5AKzXG8XIUF6SYaMbEwzgGbdSGpj1jnvn4FFjXQTCiuaa-BUDhn6iv4eu-IwWpPzZ1m92CBFB_e_wP1gPaR15Kth25ZCPdWqRGLGkugQQ; i18n-prefs=USD; session-id-time=2082787201l; session-token="dsW1Alx4k3mY3+cBAfyzwlPvyx//Gazmk5T5SYFj/9e58EE74W1DXEPLR0+M/Z+yIXoYo/kviOfuaTftwaGt3PLw1g3X+6cPslHr0CKrtZSaumBVx40+IejWm7qNyczNZbAxj+NFu9GCK2RIQshgIzshEy0wCs8OojEvqE9TgtfY0ERBCqEyYjatfGJCvDFfzK22q1VQYyaauROKCRNAEdOpxdnP4Ll2KFPNE9kINQBWlOtg4aLQ8g=="'
    mycookie = 'session-id=141-6875170-2315803; ubid-main=130-1759823-8364416; av-timezone=Asia/Shanghai; lc-main=en_US; x-main="pVaTxebzQiwz90uGQgr9k1@plEHzYa5JZvksQF912iCVriiTegY8EgR5RLq942ds"; at-main=Atza|IwEBIOx9R1T0Y2UvzfhMlDnd44D2Yv9ksXOxFFAY_F5WM3YGbStP37dnw8qQwHbNDEDYgMQ3L7DzopxqAsYMXdIe4eeDhl4robemocBqTytNu8mTdIU5nO4b4eIo8gRDozMr1HnXQorhEYvjzgd625Nxt0xXyxON0JrXo2Q4VQwnkkvTBCz1VKR92g0al8sqC8tMbexJckxJncf69c1ZMjjRMWqA; sess-at-main="6EyvMZkvEphCrInxZCnj3we2jnO4xRNODJNLztVXTBs="; sst-main=Sst1|PQF4A8ou7BKKVbt9BC-4OOZVCUZPzUYNiimY-0WgLL0J_Q2vw2E8dgZCFqePUGVioKTS1L54hHKAZ2mgtLr_-aRxvjcQ3TW30rHgRqXXX9uZGnML1yyJkPBZcMajk1Lh-TVyn13vVuczSo77ONigcA592lBUb6m1bPYUTIHS6Fmf76d1wLE2xxqPCinEGb370ZPMhy5AKzXG8XIUF6SYaMbEwzgGbdSGpj1jnvn4FFjXQTCiuaa-BUDhn6iv4eu-IwWpPzZ1m92CBFB_e_wP1gPaR15Kth25ZCPdWqRGLGkugQQ; i18n-prefs=USD; skin=noskin; sp-cdn="L5Z9:CN"; session-id-time=2082787201l; session-token="mI4zLGdZG9Pzl16z1pYpUZ+rQBmS8VgX3PjjD0NdZx3fNEpu9emfAASsDH8NGE2yLszTECFRhm4dmlxlQgX0NUMloWsxfqe/HrliUR5t/G2VSRUfN38yuFU4J7HCBAguUSOnEHUvltgLNpEntC3G28AobMXI4HfnfBLKUiNyBJAqkuz6BLIs7KIqqYCCSmH6wSzYUOxvZwgB76QX8pEtRBLioJykgYb+C9SLaUkA68beYeyblLYaIA=="'
    headers = {
        "Cookie": mycookie,
        "User-Agent": GetUserAgent(),
        # "Referer": "https://www.amazon.com/"
    }
    return headers

class PyCSV:

    def merge_csv(self, save_name, file_dir, csv_encoding='utf-8'):
        """
        :param save_name: 合并后保存的文件名称，需要用户传入
        :param file_dir: 需要合并的csv文件所在文件夹
        :param csv_encoding: csv文件编码, 默认 utf-8
        :return: None
        """
        # 合并后保存的文件路径 = 需要合并文件所在文件夹 + 合并后的文件名称
        self.save_path = os.path.join(file_dir, save_name)
        self.__check_name()
        # 指定编码
        self.encoding = csv_encoding
        # 需要合并的csv文件所在文件夹
        self.file_dir = file_dir
        self.__check_dir_exist(self.file_dir)
        # 文件路径列表
        self.file_list = [os.path.join(self.file_dir, i) for i in os.listdir(self.file_dir)]
        self.__check_singal_dir(self.file_list)
        # 合并到指定文件中
        print("开始合并csv文件 ！")
        for file in self.file_list:
            df = pd.read_csv(file, encoding=self.encoding)
            df.to_csv(self.save_path, index=False, quoting=1, header=not os.path.exists(self.save_path), mode='a')
            print(f"{file} 已经被合并到 {self.save_path} ！")
        print("所有文件已经合并完成 ！")

    def split_csv(self, csv_path, save_dir, split_line=100000, csv_encoding='utf-8'):
        """
        切分文件并获取csv文件信息。
        :param csv_path: csv文件路径
        :param save_dir: 切分文件的保存路径
        :param split_line: 按照多少行数进行切分，默认为10万
        :param csv_encoding: csv文件的编码格式
        :return: None
        """

        # 传入csv文件路径和切分后小csv文件的保存路径
        self.csv_path = csv_path
        self.save_dir = save_dir

        # 检测csv文件路径和保存路径是否符合规范
        self.__check_dir_exist(self.save_dir)
        self.__check_file_exist(self.csv_path)

        # 设置编码格式
        self.encoding = csv_encoding

        # 按照split_line行，进行切分
        self.split_line = split_line

        print("正在切分文件... ")

        # 获取文件大小
        self.file_size = round(os.path.getsize(self.csv_path) / 1024 / 1024, 2)

        # 获取数据行数
        self.line_numbers = 0
        # 切分后文件的后缀
        i = 0
        # df生成器，每个元素是一个df，df的行数为split_line，默认100000行
        df_iter = pd.read_csv(self.csv_path,
                              chunksize=self.split_line,
                              encoding=self.encoding)
        # 每次生成一个df，直到数据全部取玩
        for df in df_iter:
            # 后缀从1开始
            i += 1
            # 统计数据总行数
            self.line_numbers += df.shape[0]
            # 设置切分后文件的保存路径
            save_filename = os.path.join(self.save_dir, self.filename + "_" + str(i) + self.extension)
            # 打印保存信息
            print(f"{save_filename} 已经生成！")
            # 保存切分后的数
            df.to_csv(save_filename, index=False, encoding='utf-8', quoting=1)

        # 获取数据列名
        self.column_names = pd.read_csv(self.csv_path, nrows=10).columns.tolist()
        print("切分完毕！")

        return None

    def __check_dir_exist(self, dirpath):
        """
        检验 save_dir 是否存在，如果不存在则创建该文件夹。
        :return: None
        """
        if not os.path.exists(dirpath):
            raise FileNotFoundError(f'{dirpath} 目录不存在，请检查！')

        if not os.path.isdir(dirpath):
            raise TypeError(f'{dirpath} 目标路径不是文件夹，请检查！')

    def __check_file_exist(self, csv_path):
        """
        检验 csv_path 是否是CSV文件。
        :return: None
        """
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f'{csv_path} 文件不存在，请检查文件路径！')

        if not os.path.isfile(csv_path):
            raise TypeError(f'{csv_path} 路径非文件格式，请检查！')

        # 文件存在路径
        self.file_path_root = os.path.split(csv_path)[0]
        # 文件名称
        self.filename = os.path.split(csv_path)[1].replace('.csv', '').replace('.CSV', '')
        # 文件后缀
        self.extension = os.path.splitext(csv_path)[1]

        if self.extension.upper() != '.CSV':
            raise TypeError(f'{csv_path} 文件类型错误，非CSV文件类型，请检查！')

    def __check_name(self):
        """
        检查文件名称是否 .csv 结尾
        :return:
        """
        if not self.save_path.upper().endswith('.CSV'):
            raise TypeError('文件名称设置错误')

    def __check_singal_dir(self, file_list):
        """
        检查需要被合并的csv文件所在文件夹是否符合要求。
        1. 不应该存在除csv文件以外的文件
        2. 不应该存在文件夹。
        :return:
        """
        for file in file_list:
            if os.path.isdir(file):
                raise EnvironmentError(f'发现文件夹 {file}, 当前文件夹中存其他文件夹，请检查！')
            if not file.upper().endswith('.CSV'):
                raise EnvironmentError(f'发现非CSV文件：{file}, 请确保当前文件夹仅存放csv文件！')

