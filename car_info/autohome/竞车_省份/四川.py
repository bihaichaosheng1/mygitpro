# -*- coding:utf-8 -*-


import requests.adapters
from requests.adapters import HTTPAdapter
import jsonpath
import datetime
import pymysql
import time
import json
import re
import gc
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

"""
汽车之家--东北三省（省会）汽车降价数据
"""

# 解决ssl证书警告
requests.packages.urllib3.disable_warnings()

# 解决超过最大链接
srequest = requests.session()
srequest.mount('https://', HTTPAdapter(max_retries=60))

# 解决重连
srequest.keep_alive = False
srequest.adapters.DEFAULT_RETRIES = 10





class AutohomeSpider(object):
    """汽车之家降价车型爬取类"""
    def __init__(self):
        self.headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
    'Connection':'close',
    'cookie':'vlid=1598334632611x7bYbNr3JN; sessionid=BB0564B9-7B92-4628-A03D-6DE5063240D1%7C%7C2020-08-25+13%3A50%3A32.313%7C%7Cwww.baidu.com; autoid=edb260ee2f8896bcbe87a8bec00502e1; area=210106; ahpau=1; sessionuid=BB0564B9-7B92-4628-A03D-6DE5063240D1%7C%7C2020-08-25+13%3A50%3A32.313%7C%7Cwww.baidu.com; __ah_uuid_ng=c_BB0564B9-7B92-4628-A03D-6DE5063240D1; Hm_lvt_9924a05a5a75caf05dbbfb51af638b07=1598335812; jrsfvi=1598424705503IWzQEODWWC%7Cwww.autohome.com.cn%7C6841722; orderCount=eyJzaXRlSWQiOiI1MSIsImNhdGVnb3J5SWQiOiI4MjEiLCJzdWJDYXRlZ29yeUlkIjoiMTU0MjAiLCJ1c2VySWQiOiIiLCJwdmlkQ2hhaW4iOiIxMDE1OTQsMTAxNTk0LDEwMTU5NCwxMDE1OTQsNjg0MTcyMiIsImFjY2Vzc1R5cGUiOiIxIiwiYXBwS2V5IjoiIiwibG9jQ2l0eUlkIjoiMjEwMTAwIiwibG9jUHJvdmluY2VJZCI6IjIxMDAwMCIsImRldmljZUlkIjoiIiwibG9hZElkIjoiMTU5ODQyNDcwNTUwM0lXelFFT0RXV0MiLCJzZXNzaW9uSWQiOiJCQjA1NjRCOS03QjkyLTQ2MjgtQTAzRC02REU1MDYzMjQwRDF8fDIwMjAtMDgtMjUrMTM6NTA6MzIuMzEzfHx3d3cuYmFpZHUuY29tIiwidmlzaXRfaW5mbyI6IkJCMDU2NEI5LTdCOTItNDYyOC1BMDNELTZERTUwNjMyNDBEMXx8OTlFRDk2OTktQ0YzOC00MThBLUE0QTYtMTU1MUQxNERGRDg4fHwyMDIwMDUwOXx8MDF8fDYiLCJjdXJQdmFyZWFJZCI6IjY4NDE3MjIiLCJwdmFyZWFJZCI6IjY4NDE3MjIifQ==; Hm_lpvt_9924a05a5a75caf05dbbfb51af638b07=1598515794; ahsids=874_4745_5009_4105; FootPrints=45048%7C2020-8-27%2C44696%7C2020-8-27%2C37352%7C2020-8-27%2C38170%7C2020-8-27%2C45453%7C2020-8-27%2C; ahplid=1599162565800; ahpvno=94; sessionip=119.119.130.86; v_no=1; visit_info_ad=BB0564B9-7B92-4628-A03D-6DE5063240D1||58D95981-AAD3-41AA-A6C4-4824CC71D019||-1||-1||1; ref=www.baidu.com%7C0%7C0%7C0%7C2020-08-28+09%3A06%3A35.007%7C2020-08-25+13%3A50%3A32.313; sessionvid=58D95981-AAD3-41AA-A6C4-4824CC71D019; ahrlid=1598576794896Aidc0tZHac-1598576797201'
}

    def requ_data(self,url,a):
        resp = srequest.get(url=url, headers=self.headers, timeout=5, verify=False)
        if resp.content:
            resp_data = resp.json()
            # print(resp_data)
            series_id = jsonpath.jsonpath(resp_data, '$..SeriesId')
            if series_id == False:
                pass
            try:
                for sid in series_id:
                    base_url = 'https://buy.autohome.com.cn/Car/GetSpecInfo?pid=230000&cid={}&seriesId={}&specId=1'.format(
                        a, sid)
                    print(base_url)
                    spec_resp = srequest.get(url=base_url, headers=self.headers, timeout=5, verify=False)
                    if spec_resp.content:
                        spec_data = spec_resp.json()
                        yield spec_data
            except TypeError:
                pass

    def parse_data(self,spec_datas):
        # print(spec_datas)
        for spec_data in spec_datas:
            spec_id = jsonpath.jsonpath(spec_data, '$[specList]..specId')
            # print('车型id',spec_id)
            if spec_id == False:
                continue

            """将车系名称与车型名称拼接"""
            # 车系名称
            series_names = jsonpath.jsonpath(spec_data, '$[specList]..SeriesName')
            # 车型名称
            spec_names = jsonpath.jsonpath(spec_data, '$[specList]..specName')
            # 将车系名称拼接到车型名称之前
            spec_name_list = []
            for i in range(0, len(series_names)):
                spec_name_list.append(series_names[i] + ' ' + spec_names[i])
            # print('名称',spec_name_list)

            # 提取年款 拼接到名称最后
            spec_name_list2 = []
            for name in spec_name_list:
                s_name = "".join(re.findall(r'[0-9]{4}款*', name))
                sp_name = name.replace(s_name + " ", '')
                spec_names = sp_name + s_name
                spec_name_list2.append(spec_names)
            # print(spec_name_list2)

            # 手动
            spec_name_shou = []
            for name in spec_name_list2:
                name1 = name.replace('手动', '手动 ')
                spec_name_shou.append(name1)
            # print(spec_name_shou)
            # 更改后
            spec_name = []
            for name in spec_name_shou:
                name1 = name.replace('自动', '自动 ')
                spec_name.append(name1)
            # print(spec_name)
            gc.collect()

            # 城市id
            city_id = jsonpath.jsonpath(spec_data, '$..cid')[0]
            # print('城市id', city_id)

            # 指导价
            guidance_price = jsonpath.jsonpath(spec_data, '$[specList]..MinOriginalPrice')
            # print('指导价', guidance_price)

            # 现价
            price = jsonpath.jsonpath(spec_data, '$[specList]..Price')

            # 降价
            cut_price = (list(map(lambda x, y: x - y, guidance_price, price)))

            # 最后一次更新时间
            last_sync_time = datetime.now().strftime("%Y-%m-30 23:35:23")

            yield spec_id,spec_name,city_id,guidance_price,cut_price,price,last_sync_time


    def storing_data(self,car_data):
        # 连接MySQL数据库
        conn = pymysql.connect(host="112.126.89.134", user="jgcdb", password="jingche0000", port=3306, db="jgcproddb",
                               charset="utf8")
        # conn = pymysql.connect(host="localhost", user="root", password="", port=3306, db="jdbc", charset="utf8")
        cursor = conn.cursor()  # 创建游标
        for data in car_data:
            # print(data)
            spec_id = data[0]
            spec_name = data[1]
            city_id = data[2]
            guidance_price = data[3]
            cut_price = data[4]
            price = data[5]
            last_sync_time = data[6]

            for s_id, s_name, g_price, c_price, p_price in zip(spec_id, spec_name, guidance_price, cut_price,
                                                               price):
                data = (s_id, s_name, city_id , g_price,c_price, p_price, last_sync_time)
                print('这是即将存到数据库的data', data)

                # 根据 车型id 城市id 判断 车型是否存在  时间就是确保 库里只保留本月的数据
                sql = "select * from t_car_detail_city where spec_id='{}'and city_id='{}'and cut_price ='{}' and last_sync_time='{}'".format(data[0], data[2], data[4], data[6])
                cursor.execute(sql)
                many = cursor.fetchone()
                if many:
                    print('此数据表中已存在')
                else:
                    insert_sql = "insert into t_car_detail_city(spec_id,spec_name,city_id,guidance_price,cut_price,price,last_sync_time) value(%s,%s,%s,%s,%s,%s,%s) "
                    cursor.execute(insert_sql,data)
                    conn.commit()  # 提交数据
                    print('数据提交完成')

        cursor.close()  # 关闭游标
        print('关闭游标')
        conn.close()  # 关闭连接
        print('关闭连接')

    def query_data(self):
        city_id = [510100,510300,510400,510500,510600,510700,510800,510900,511000,511100,511300,511400,511500,511600,511700,511800,511900,512000,513400]
        return city_id

    def main(self,city_id):
        num_list = [num for num in range(1, 30)]
        for a in city_id:
            for num in num_list:
                url = "https://buy.autohome.com.cn/Car/GetCarListModel?brandid=0&seriesid=0&specid=0&pid=210000&cid={}&page={}".format(a, num)
                self.requ_data(url,a)
                self.parse_data(self.requ_data(url,a))
                self.storing_data(self.parse_data(self.requ_data(url,a)))


if __name__ == '__main__':
    auto = AutohomeSpider()
    data = auto.query_data()
    auto.main(data)
    def main_time(h=20, m=4):
        while True:
            # 判断是否达到设定时间，例如0:00
            while True:
                now_time = datetime.now()
                print(now_time.hour, now_time.minute)
                # 到达设定时间，结束内循环
                if now_time.hour == h and now_time.minute == m:
                    break
                # 不到时间就等60秒之后再次检测
                time.sleep(60)
                # 做正事，一天做一次
            auto = AutohomeSpider()
            data = auto.query_data()
            auto.main(data)


    main_time()
