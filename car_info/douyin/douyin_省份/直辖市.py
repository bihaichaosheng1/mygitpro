# -*- coding:utf-8 -*-
import requests.adapters
from requests.adapters import HTTPAdapter
import jsonpath
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
        print(url,a)
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

            # 厂商id
            brand_id = jsonpath.jsonpath(spec_data, '$[specinfo]..fctid')[0]
            # print('品牌id',brand_id)

            # 厂商名称
            brand_name = jsonpath.jsonpath(spec_data, '$[specinfo]..fctname')[0]
            # print('品牌名称',brand_name)

            # 品牌id
            contain_brand_id = jsonpath.jsonpath(spec_data, '$[specinfo]..brandid')[0]
            # print('品牌id',brand_id)

            # 品牌名称
            contain_brand_name = jsonpath.jsonpath(spec_data, '$[specinfo]..brandname')[0]
            # print('品牌名称',brand_name)


            # 车系id
            series_id = jsonpath.jsonpath(spec_data,'$[specinfo]..seriesid')[0]
            # print('车系id',series_id)

            # 车系名称
            category_fullname = jsonpath.jsonpath(spec_data,'$[specinfo]..seriesname')[0]
            # print('车系名称',category_fullname)

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

            # 城市名称
            city_name = jsonpath.jsonpath(spec_data,'$..cityName')[0]
            # print('城市名称',city_name)

            # 指导价
            guidance_price = jsonpath.jsonpath(spec_data, '$[specList]..MinOriginalPrice')
            # print('指导价', guidance_price)

            # 现价
            price = jsonpath.jsonpath(spec_data, '$[specList]..Price')

            # 降价
            cut_price = (list(map(lambda x, y: x - y, guidance_price, price)))

            # 最后一次更新时间
            last_sync_time = datetime.now().strftime("%Y-%m")


            a_last_sync_time = datetime.now().strftime("%Y-%m-%d")
            yield brand_id, brand_name, series_id, category_fullname, spec_id, spec_name, city_id, city_name, guidance_price, cut_price, price, contain_brand_id, contain_brand_name, last_sync_time, a_last_sync_time

    def storing_data(self, car_data):
        # 连接MySQL数据库
        conn = pymysql.connect(host="112.126.89.134", user="jgcdb", password="jingche0000", port=3306,
                               db="jgcproddb",
                               charset="utf8")
        # conn = pymysql.connect(host="localhost", user="root", password="", port=3306, db="jdbc", charset="utf8")
        cursor = conn.cursor()  # 创建游标
        num = 28800
        stime = 3
        _number = 0
        _status = True
        while _status and _number <= num:
            try:
                conn.ping()  # cping 校验连接是否异常
                _status = False
            except:
                if conn == True:  # 重新连接,成功退出
                    _status = False
                    break
                _number += 1
                time.sleep(stime)  # 连接不成功,休眠3秒钟,继续循环，直到循环8小时
        conn.ping()
        for data in car_data:
            # print(data)
            brand_id = data[0]
            brand_name = data[1]
            series_id = data[2]
            category_fullname = data[3]
            spec_id = data[4]
            spec_name = data[5]
            city_id = data[6]
            city_name = data[7]
            guidance_price = data[8]
            cut_price = data[9]
            price = data[10]
            contain_brand_id = data[11]
            contain_brand_name = data[12]
            last_sync_time = data[13]
            a_last_sync_time = data[14]

            for s_id, s_name, g_price, c_price, p_price in zip(spec_id, spec_name, guidance_price, cut_price,
                                                               price):
                data = (
                    brand_id, brand_name, series_id, category_fullname, s_id, s_name, city_id, city_name,
                    g_price,
                    c_price, p_price, contain_brand_id, contain_brand_name, last_sync_time)
                print('这是即将存到抖音优惠表的data', data)

                # 根据 车型id 城市id 判断 车型是否存在  时间就是确保 库里只保留本月的数据
                sql = "select * from t_car_detail_city_douyin where spec_id='{}'and city_id='{}'and cut_price ='{}' and contain_brand_id ='{}' and last_sync_time='{}'".format(
                    data[4], data[6], data[9], data[11], data[13])
                # print(sql)
                cursor.execute(sql)
                many = cursor.fetchone()
                if many:
                    print('抖音表中已存在')

                    updata_sql = "UPDATE t_car_detail_city_douyin SET cut_price='{}',price='{}' where spec_id = '{}'and city_id = '{}'".format(data[9], data[10], data[4], data[6])
                    cursor.execute(updata_sql)
                    conn.commit()
                    print('抖音数据已更新')
                else:
                    cursor.execute(
                        "insert into t_car_detail_city_douyin(brand_id,brand_name,series_id,category_fullname,spec_id,spec_name,city_id,city_name,guidance_price,cut_price,price,contain_brand_id,contain_brand_name,last_sync_time) value(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ",
                        data)
                    conn.commit()  # 提交数据
                    print('抖音数据已提交')

        cursor.close()  # 关闭游标
        print('关闭游标')
        conn.close()  # 关闭连接
        print('关闭连接')

    def query_data(self):
        city_id = [110100,120100,500100,310100]
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
    def main_time(h=22):
        while True:
            # 判断是否达到设定时间，例如0:00
            while True:
                now_time = datetime.now()
                print(now_time.hour, now_time.minute)
                # 到达设定时间，结束内循环
                if now_time.hour == h:
                    break
                # 不到时间就等60秒之后再次检测
                time.sleep(60)
                # 做正事，一天做一次
            auto = AutohomeSpider()
            data = auto.query_data()
            auto.main(data)
    main_time()
