

from requests.adapters import HTTPAdapter
import requests
import parsel
import pymysql
import datetime
import time
from concurrent.futures import ThreadPoolExecutor
#
#
#
#
#
# # 解决最大重连次数
# s = requests.session()
# s.mount('https://', HTTPAdapter(max_retries=60))
#
# # 解决ssl警告
# requests.packages.urllib3.disable_warnings()
#
#
# """
# 从库里读取车系id
# 车系表是从库里获取品牌id
# 这里是根据
# """
#
# """在售车型列表"""
# autohome_on_spec_id = []
#
# """预售车型列表"""
# autohome_pre_spec_id = []
#
# """停售车型列表"""
# autohome_halt_spec_id = []
#
# """所有车型id列表"""
# autohome_spec_id = []
#
#
# def requ_on_spec_html(on_link):
#     """在售"""
#     on_spec = s.get(on_link)
#     on_spec_data = parsel.Selector(on_spec.text)
#     spec_detail_list = on_spec_data.xpath('//ul[@class="interval01-list"]/li/@data-value').getall()
#     print(spec_detail_list)
#     for id in spec_detail_list:
#         autohome_on_spec_id.append(int(id))
#         print('已将在售车型', id, '添加进列表')
#         # 将在售车型id添加到所有车型id列表
#         autohome_spec_id.append(int(id))
#
# def requ_pre_spec_html(pre_link):
#     """预售"""
#     pre_spec = s.get(pre_link)
#     pre_spec_data = parsel.Selector(pre_spec.text)
#     spec_detail_list = pre_spec_data.xpath('//div[@id="divSeries"]/div[@class="interval01"]/ul/li')
#     for spec_detail in spec_detail_list:
#         """车型id"""
#         spec_id = spec_detail.xpath('./@data-value').getall()
#         for id in spec_id:
#             autohome_pre_spec_id.append(int(id))
#             print('已将预售车型', id, '添加进列表')
#             # 将预售车型id添加到所有车型id列表
#             autohome_spec_id.append(int(id))
#
#
# def requ_halt_spec_html(halt_link):
#     """停售"""
#     halt_spec = s.get(halt_link)
#     halt_spec_data = parsel.Selector(halt_spec.text)
#     spec_detail_list = halt_spec_data.xpath('//div[@id="divSeries"]/div[@class="interval01 interval01-sale"]')
#     for spec_detail in spec_detail_list:
#         """车型id"""
#         spec_id = spec_detail.xpath('./ul/li/@data-value').getall()
#         for id in spec_id:
#             autohome_halt_spec_id.append(int(id))
#             print('已将停售车型', id, '添加进列表')
#             # 将停售售车型id添加到所有车型id列表
#             autohome_spec_id.append(int(id))
#
#
# def write_file(autohome_on_spec_id,autohome_pre_spec_id,autohome_halt_spec_id,autohome_spec_id):
#     """写入文件"""
#     print('在售车型id', autohome_on_spec_id)
#     with open('autohome_on_spec_id.txt','w') as f:
#         autohome_on_spec_id = str(autohome_on_spec_id)
#         one = autohome_on_spec_id.replace('[', '')
#         two = one.replace(']', '')
#         f.write(two)
#         print('在售车型id写入完成')
#
#     print('预售车型id', autohome_pre_spec_id)
#     with open('autohome_pre_spec_id.txt','w') as f:
#         autohome_pre_spec_id = str(autohome_pre_spec_id)
#         one = autohome_pre_spec_id.replace('[', '')
#         two = one.replace(']', '')
#         f.write(two)
#         print('预售车型id写入完成')
#
#     print('停售车型id', autohome_halt_spec_id)
#     with open('autohome_halt_spec_id.txt','w') as f:
#         autohome_halt_spec_id = str(autohome_halt_spec_id)
#         one = autohome_halt_spec_id.replace('[', '')
#         two = one.replace(']', '')
#         f.write(two)
#         print('停售车型id写入完成')
#
#     num_set = set(autohome_spec_id)
#     nums_list = sorted(list(num_set))
#     print('所有车型id', autohome_spec_id)
#     with open('autohome_spec_id.txt', 'w')as f:
#         autohome_spec_id = str(nums_list)
#         one = autohome_spec_id.replace('[', '')
#         two = one.replace(']', '')
#         f.write(two)
#         print('所有车型id写入完成')
#
#
#
# def main():
#     conn = pymysql.connect(host="112.126.89.134", user="jgcdb", password="jgcdb123456", port=3306, db="jgcproddb",charset="utf8")
#     # conn = pymysql.connect(host="localhost", user="root", password="", port=3306, db="jdbc", charset="utf8")
#     cursor = conn.cursor()  # 创建游标
#     sql = "select series_id from t_car_category"
#     cursor.execute(sql)
#     series_ids = cursor.fetchall()  # 得到series_id数据
#     series_id = []
#     for id in series_ids:
#         series_id.append(id[0])
#     for sid in series_id:
#         """在售车系连接"""
#         on_link = 'https://car.autohome.com.cn/price/series-{}-0-1-0-0-0-0-1.html'.format(sid)
#         requ_on_spec_html(on_link)
#
#         """预售车系连接"""
#         pre_link = 'https://car.autohome.com.cn/price/series-{}-0-2-0-0-0-0-1.html'.format(sid)
#         requ_pre_spec_html(pre_link)
#
#         """停售车系连接"""
#         halt_link = 'https://car.autohome.com.cn/price/series-{}-0-3-0-0-0-0-1.html'.format(sid)
#         requ_halt_spec_html(halt_link)
#
#         write_file(autohome_on_spec_id,autohome_pre_spec_id,autohome_halt_spec_id,autohome_spec_id)
#     cursor.close()  # 关闭游标
#     print('关闭游标')
#     conn.close()  # 关闭连接
#     print('关闭连接')
#
#
# if __name__ == '__main__':
#     def doSth():
#         main()
#
#     def main_time(h=10, m=2):
#         while True:
#             # 判断是否达到设定时间，例如0:00
#             while True:
#                 now_time = datetime.datetime.now()
#                 print(now_time.hour, now_time.minute)
#                 # 到达设定时间，结束内循环
#                 if now_time.hour == h and now_time.minute == m:
#                     break
#                 # 不到时间就等60秒之后再次检测
#                 time.sleep(60)
#                 # 做正事，一天做一次
#             doSth()
#     main_time()


# 解决最大重连次数
s = requests.session()
s.mount('https://', HTTPAdapter(max_retries=60))

# 解决ssl警告
requests.packages.urllib3.disable_warnings()




"""
id_list = [3934,528,448,4797,209,5779,2608,]

"""

def spec_id():
    conn = pymysql.connect(host="112.126.89.134", user="jgcdb", password="jingche0000", port=3306, db="jgcproddb",
                           charset="utf8")
    # conn = pymysql.connect(host="localhost", user="root", password="", port=3306, db="jdbc", charset="utf8")
    cursor = conn.cursor()  # 创建游标
    sql = "select series_id from t_car_category"
    cursor.execute(sql)
    series_idlist = cursor.fetchall()  # 得到品牌id数据
    sid_list = []
    for id in series_idlist:
        sid_list.append(id[0])
    print(sid_list)
    cursor.close()
    conn.cursor()
    print('关闭数据库连接')

    """在售车型列表"""
    autohome_on_spec_id = []

    """预售车型列表"""
    autohome_pre_spec_id = []

    """停售车型列表"""
    autohome_halt_spec_id = []

    """所有车型id列表"""
    autohome_spec_id = []
    for sid in sid_list:
        """在售车系连接"""
        on_link = 'https://car.autohome.com.cn/price/series-{}-0-1-0-0-0-0-1.html'.format(sid)
        print(on_link)
        on_spec = s.get(on_link,verify=False)
        on_spec_data = parsel.Selector(on_spec.text)
        spec_detail_list = on_spec_data.xpath('//ul[@class="interval01-list"]/li/@data-value').getall()
        print(spec_detail_list)
        for id in spec_detail_list:
            autohome_on_spec_id.append(int(id))
            print('已将在售车型', id, '添加进列表')
            # 将在售车型id添加到所有车型id列表
            autohome_spec_id.append(int(id))
        on_link = 'https://car.autohome.com.cn/price/series-{}-0-1-0-0-0-0-2.html'.format(sid)
        print(on_link)
        on_spec = s.get(on_link,verify=False)
        on_spec_data = parsel.Selector(on_spec.text)
        spec_detail_list = on_spec_data.xpath('//ul[@class="interval01-list"]/li/@data-value').getall()
        print(spec_detail_list)
        for id in spec_detail_list:
            autohome_on_spec_id.append(int(id))
            print('已将在售车型', id, '添加进列表')
            # 将在售车型id添加到所有车型id列表
            autohome_spec_id.append(int(id))

        on_link = 'https://car.autohome.com.cn/price/series-{}-0-1-0-0-0-0-3.html'.format(sid)
        print(on_link)
        on_spec = s.get(on_link,verify=False)
        on_spec_data = parsel.Selector(on_spec.text)
        spec_detail_list = on_spec_data.xpath('//ul[@class="interval01-list"]/li/@data-value').getall()
        print(spec_detail_list)
        for id in spec_detail_list:
            autohome_on_spec_id.append(int(id))
            print('已将在售车型', id, '添加进列表')
            # 将在售车型id添加到所有车型id列表
            autohome_spec_id.append(int(id))

        """预售车系连接"""
        pre_link = 'https://car.autohome.com.cn/price/series-{}-0-2-0-0-0-0-1.html'.format(sid)
        print(pre_link)
        pre_spec = s.get(pre_link,verify=False)
        pre_spec_data = parsel.Selector(pre_spec.text)
        spec_detail_list = pre_spec_data.xpath('//div[@id="divSeries"]/div[@class="interval01"]/ul/li')
        for spec_detail in spec_detail_list:
            """车型id"""
            spec_id = spec_detail.xpath('./@data-value').getall()
            for id in spec_id:
                autohome_pre_spec_id.append(int(id))
                print('已将预售车型',id,'添加进列表')
                # 将预售车型id添加到所有车型id列表
                autohome_spec_id.append(int(id))
        pre_link = 'https://car.autohome.com.cn/price/series-{}-0-2-0-0-0-0-2.html'.format(sid)
        pre_spec = s.get(pre_link,verify=False)
        pre_spec_data = parsel.Selector(pre_spec.text)
        spec_detail_list = pre_spec_data.xpath('//div[@id="divSeries"]/div[@class="interval01"]/ul/li')
        for spec_detail in spec_detail_list:
            """车型id"""
            spec_id = spec_detail.xpath('./@data-value').getall()
            for id in spec_id:
                autohome_pre_spec_id.append(int(id))
                print('已将预售车型', id, '添加进列表')
                # 将预售车型id添加到所有车型id列表
                autohome_spec_id.append(int(id))

        """停售车系连接"""
        # 第一页
        halt_link = 'https://car.autohome.com.cn/price/series-{}-0-3-0-0-0-0-1.html'.format(sid)
        print(halt_link)
        halt_spec = s.get(halt_link,verify=False)
        halt_spec_data = parsel.Selector(halt_spec.text)
        spec_detail_list = halt_spec_data.xpath('//div[@id="divSeries"]/div[@class="interval01 interval01-sale"]')
        for spec_detail in spec_detail_list:
            """车型id"""
            spec_id = spec_detail.xpath('./ul/li/@data-value').getall()
            for id in spec_id:
                autohome_halt_spec_id.append(int(id))
                print('已将停售车型',id,'添加进列表')
                # 将停售售车型id添加到所有车型id列表
                autohome_spec_id.append(int(id))

        # 第二页
        halt_link = 'https://car.autohome.com.cn/price/series-{}-0-3-0-0-0-0-2.html'.format(sid)
        print(halt_link)
        halt_spec = s.get(halt_link,verify=False)
        halt_spec_data = parsel.Selector(halt_spec.text)
        spec_detail_list = halt_spec_data.xpath('//div[@id="divSeries"]/div[@class="interval01 interval01-sale"]')
        for spec_detail in spec_detail_list:
            """车型id"""
            spec_id = spec_detail.xpath('./ul/li/@data-value').getall()
            for id in spec_id:
                autohome_halt_spec_id.append(int(id))
                print('已将停售车型', id, '添加进列表')
                # 将停售售车型id添加到所有车型id列表
                autohome_spec_id.append(int(id))
        # 第三页
        halt_link = 'https://car.autohome.com.cn/price/series-{}-0-3-0-0-0-0-3.html'.format(sid)
        print(halt_link)
        halt_spec = s.get(halt_link,verify=False)
        halt_spec_data = parsel.Selector(halt_spec.text)
        spec_detail_list = halt_spec_data.xpath('//div[@id="divSeries"]/div[@class="interval01 interval01-sale"]')
        for spec_detail in spec_detail_list:
            """车型id"""
            spec_id = spec_detail.xpath('./ul/li/@data-value').getall()
            for id in spec_id:
                autohome_halt_spec_id.append(int(id))
                print('已将停售车型', id, '添加进列表')
                # 将停售售车型id添加到所有车型id列表
                autohome_spec_id.append(int(id))
        # 第四页
        halt_link = 'https://car.autohome.com.cn/price/series-{}-0-3-0-0-0-0-4.html'.format(sid)
        print(halt_link)
        halt_spec = s.get(halt_link,verify=False)
        halt_spec_data = parsel.Selector(halt_spec.text)
        spec_detail_list = halt_spec_data.xpath('//div[@id="divSeries"]/div[@class="interval01 interval01-sale"]')
        for spec_detail in spec_detail_list:
            """车型id"""
            spec_id = spec_detail.xpath('./ul/li/@data-value').getall()
            for id in spec_id:
                autohome_halt_spec_id.append(int(id))
                print('已将停售车型', id, '添加进列表')
                # 将停售售车型id添加到所有车型id列表
                autohome_spec_id.append(int(id))

    print('在售车型id', autohome_on_spec_id)
    with open('all_spec_id/autohome_on_spec_id.txt', 'w') as f:
        autohome_on_spec_id = str(autohome_on_spec_id)
        one = autohome_on_spec_id.replace('[', '')
        two = one.replace(']', '')
        f.write(two)
        print('写入完成')

    print('预售车型id', autohome_pre_spec_id)
    with open('all_spec_id/autohome_pre_spec_id.txt', 'w') as f:
        autohome_pre_spec_id = str(autohome_pre_spec_id)
        one = autohome_pre_spec_id.replace('[', '')
        two = one.replace(']', '')
        f.write(two)
        print('写入完成')

    print('停售车型id', autohome_halt_spec_id)
    with open('all_spec_id/autohome_halt_spec_id.txt', 'a') as f:
        autohome_halt_spec_id = str(autohome_halt_spec_id)
        one = autohome_halt_spec_id.replace('[', '')
        two = one.replace(']', '')
        f.write(two)
        print('写入完成')


    nums_list = sorted(set(autohome_spec_id), key=autohome_spec_id.index)
    print('所有车型id',autohome_spec_id)
    with open('all_spec_id/autohome_spec_id.txt', 'w')as f:
        autohome_spec_id = str(nums_list)
        one = autohome_spec_id.replace('[', '')
        two = one.replace(']', '')
        f.write(two)
        print('写入完成')

if __name__ == '__main__':
    with ThreadPoolExecutor(50) as t:
        t.submit(spec_id)
    def main_time(h=12, m=36):
        while True:
            # 判断是否达到设定时间，例如0:00
            while True:
                now_time = datetime.datetime.now()
                print(now_time.hour, now_time.minute)
                # 到达设定时间，结束内循环
                if now_time.hour == h and now_time.minute == m:
                    break
                # 不到时间就等60秒之后再次检测
                time.sleep(60)
                # 做正事，一天做一次
            with ThreadPoolExecutor(50) as t:
                t.submit(spec_id)
    main_time()




