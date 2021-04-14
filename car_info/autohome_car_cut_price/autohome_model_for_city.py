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
srequest.mount('https://', HTTPAdapter(max_retries=20))

# 解决重连
srequest.keep_alive = False
srequest.adapters.DEFAULT_RETRIES = 10

# 连接MySQL数据库
conn = pymysql.connect(host="112.126.89.134", user="jgcdb", password="jingche000", port=3306, db="jgcproddb",charset="utf8")
# conn = pymysql.connect(host="localhost", user="root", password="", port=3306, db="jdbc", charset="utf8")
cursor = conn.cursor()  # 创建游标


class AutohomeSpider(object):
    """汽车之家降价车型爬取类"""
    def __init__(self):
        self.headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
    'Connection':'close',
    'cookie':'vlid=1598334632611x7bYbNr3JN; sessionid=BB0564B9-7B92-4628-A03D-6DE5063240D1%7C%7C2020-08-25+13%3A50%3A32.313%7C%7Cwww.baidu.com; autoid=edb260ee2f8896bcbe87a8bec00502e1; area=210106; ahpau=1; sessionuid=BB0564B9-7B92-4628-A03D-6DE5063240D1%7C%7C2020-08-25+13%3A50%3A32.313%7C%7Cwww.baidu.com; __ah_uuid_ng=c_BB0564B9-7B92-4628-A03D-6DE5063240D1; Hm_lvt_9924a05a5a75caf05dbbfb51af638b07=1598335812; jrsfvi=1598424705503IWzQEODWWC%7Cwww.autohome.com.cn%7C6841722; orderCount=eyJzaXRlSWQiOiI1MSIsImNhdGVnb3J5SWQiOiI4MjEiLCJzdWJDYXRlZ29yeUlkIjoiMTU0MjAiLCJ1c2VySWQiOiIiLCJwdmlkQ2hhaW4iOiIxMDE1OTQsMTAxNTk0LDEwMTU5NCwxMDE1OTQsNjg0MTcyMiIsImFjY2Vzc1R5cGUiOiIxIiwiYXBwS2V5IjoiIiwibG9jQ2l0eUlkIjoiMjEwMTAwIiwibG9jUHJvdmluY2VJZCI6IjIxMDAwMCIsImRldmljZUlkIjoiIiwibG9hZElkIjoiMTU5ODQyNDcwNTUwM0lXelFFT0RXV0MiLCJzZXNzaW9uSWQiOiJCQjA1NjRCOS03QjkyLTQ2MjgtQTAzRC02REU1MDYzMjQwRDF8fDIwMjAtMDgtMjUrMTM6NTA6MzIuMzEzfHx3d3cuYmFpZHUuY29tIiwidmlzaXRfaW5mbyI6IkJCMDU2NEI5LTdCOTItNDYyOC1BMDNELTZERTUwNjMyNDBEMXx8OTlFRDk2OTktQ0YzOC00MThBLUE0QTYtMTU1MUQxNERGRDg4fHwyMDIwMDUwOXx8MDF8fDYiLCJjdXJQdmFyZWFJZCI6IjY4NDE3MjIiLCJwdmFyZWFJZCI6IjY4NDE3MjIifQ==; Hm_lpvt_9924a05a5a75caf05dbbfb51af638b07=1598515794; ahsids=874_4745_5009_4105; FootPrints=45048%7C2020-8-27%2C44696%7C2020-8-27%2C37352%7C2020-8-27%2C38170%7C2020-8-27%2C45453%7C2020-8-27%2C; ahplid=1599162565800; ahpvno=94; sessionip=119.119.130.86; v_no=1; visit_info_ad=BB0564B9-7B92-4628-A03D-6DE5063240D1||58D95981-AAD3-41AA-A6C4-4824CC71D019||-1||-1||1; ref=www.baidu.com%7C0%7C0%7C0%7C2020-08-28+09%3A06%3A35.007%7C2020-08-25+13%3A50%3A32.313; sessionvid=58D95981-AAD3-41AA-A6C4-4824CC71D019; ahrlid=1598576794896Aidc0tZHac-1598576797201'
}

    def requ_data(self,url,a):
        resp_data = srequest.get(url=url, headers=self.headers, timeout=5).json()
        # print(resp_data)
        series_id = jsonpath.jsonpath(resp_data, '$..SeriesId')
        if series_id == False:
            pass
        try:
            for sid in series_id:
                base_url = 'https://buy.autohome.com.cn/Car/GetSpecInfo?pid=230000&cid={}&seriesId={}&specId=1'.format(a,sid)
                try:
                    spec_data = srequest.get(url=base_url,headers=self.headers,timeout=5,verify=False).json()
                    # time.sleep(1)
                    print(base_url)

                    yield spec_data
                except json.decoder.JSONDecodeError:
                    continue
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
            print('城市id', city_id)
            # 指导价
            guidance_price = jsonpath.jsonpath(spec_data, '$[specList]..MinOriginalPrice')
            # print('指导价', guidance_price)

            # 现价
            price = jsonpath.jsonpath(spec_data, '$[specList]..Price')
            # price = []
            # for num in price_list:
            #     if num >= 10000:
            #         num /= 10000
            #         price_num = '{}{}'.format(round(num, 3), '万')
            #         price.append(price_num)
            #         print(price_num)
            # print('现价', price)
            # 降价
            cut_price = (list(map(lambda x, y: x - y, guidance_price, price)))
            # cut_price = []
            # print('降价', cut_price_list)
            # for num in cut_price_list:
            #     if num >= 10000:
            #         num /= 10000
            #         price_num = '{}{}'.format(round(num, 3), '万')
            #         cut_price.append(price_num)
            #         print(price_num)
            #     else:
            #         cut_price.append(num)
            # print('降价',cut_price)
            # 最后一次更新时间
            # last_sync_time = datetime.now().strftime("%Y-%m")
            last_sync_time = datetime.now().strftime("%Y-%m-28 23:35:23")
            # last_sync_time = datetime.datetime.now().strftime("%Y-9-30 23:35:23")
            # print('最后更新时间',last_sync_time)

            yield spec_id,spec_name,city_id,guidance_price,cut_price,price,last_sync_time


    def storing_data(self,car_data):
        for data in car_data:
            print(data)
            spec_id = data[0]
            spec_name = data[1]
            city_id = data[2]
            guidance_price = data[3]
            cut_price = data[4]
            price = data[5]
            last_sync_time = data[6]
            for s_id, s_name, g_price, c_price, p_price in zip(spec_id, spec_name, guidance_price, cut_price, price):
                data = (s_id, s_name, city_id, g_price, c_price, p_price, last_sync_time)
                print('这是即将存到数据库的data', data)

                # 若 mysql 连接失败就重新连接
                conn.ping(reconnect=True)
                sql2 = "select * from t_car_detail_city where spec_id='{}'and city_id='{}' and cut_price='{}' and last_sync_time='{}'".format(data[0], data[2], data[4],data[6])
                cursor.execute(sql2)
                many = cursor.fetchone()
                if many:
                    print('此数据表中已存在')
                else:
                    sql_t_car_detail_city = "replace into t_car_detail_city(spec_id,spec_name,city_id,guidance_price,cut_price,price,last_sync_time) value(%s,%s,%s,%s,%s,%s,%s) "
                    cursor.execute(sql_t_car_detail_city, data)
                    conn.commit()  # 提交数据
                    print('数据提交完成')

    def query_data(self):
        # sql = "select city_id from national_cities"
        # cursor.execute(sql)
        # city_ids = cursor.fetchall()  # 得到品牌id数据
        # city_id = []
        # for id in city_ids:
        #     city_id.append(id[0])
        city_id = [110100, 120100, 130100, 130200, 130300, 130400, 130500, 130600, 130700, 130800, 130900, 131000, 131100, 140100, 140200, 140300, 140400,
                   140500, 140600, 140700, 140800, 140900, 141000, 141100, 150100, 150200, 150300, 150400, 150500, 150600, 150700, 150800, 150900, 152200,
                   152500, 210100, 210200, 210300, 210400, 210500, 210600, 210700, 210800, 210900, 211000, 211100, 211200, 211300, 211400, 220100, 220200,
                   220300, 220400, 220500, 220600, 220700, 220800, 222400, 230100, 230200, 230300, 230400, 230500, 230600, 230700, 230800, 230900, 231000,
                   231100, 231200, 232700, 310100, 320100, 320200, 320300, 320400, 320500, 320600, 320700, 320800, 320900, 321000, 321100, 321200, 321300,
                   330100, 330200, 330300, 330400, 330500, 330600, 330700, 330800, 330900, 331000, 331100, 340100, 340200, 340300, 340400, 340500, 340600,
                   340700, 340800, 341000, 341100, 341200, 341300, 341500, 341600, 341700, 341800, 350100, 350200, 350300, 350400, 350500, 350600, 350700,
                   350800, 350900, 360100, 360200, 360300, 360400, 360500, 360600, 360700, 360800, 360900, 361000, 361100, 370100, 370200, 370300, 370400,
                   370500, 370600, 370700, 370800, 370900, 371000, 371100, 371200, 371300, 371400, 371500, 371600, 371700, 410100, 410200, 410300, 410400,
                   410500, 410600, 410700, 410800, 410900, 411000, 411100, 411200, 411300, 411400, 411500, 411600, 411700, 419001, 420100, 420200, 420300,
                   420500, 420600, 420700, 420800, 420900, 421000, 421100, 421200, 421300, 422800, 429004, 429005, 429006, 430100, 430200, 430300, 430400,
                   430500, 430600, 430700, 430800, 430900, 431000, 431100, 431200, 431300, 433100, 440100, 440200, 440300, 440400, 440500, 440600, 440700,
                   440800, 440900, 441200, 441300, 441400, 441500, 441600, 441700, 441800, 441900, 442000, 445100, 445200, 445300, 450100, 450200, 450300,
                   450400, 450500, 450600, 450700, 450800, 450900, 451000, 451100, 451200, 451300, 451400, 460100, 460200, 460400, 469002, 469006, 469007,
                   500100, 510100, 510300, 510400, 510500, 510600, 510700, 510800, 510900, 511000, 511100, 511300, 511400, 511500, 511600, 511700, 511800,
                   511900, 512000, 513400, 520100, 520200, 520300, 520400, 520500, 520600, 530100, 530300, 530400, 530500, 530600, 530700, 530800, 530900,
                   532300, 532500, 532600, 532800, 532900, 533100, 540100, 610100, 610200, 610300, 610400, 610500, 610600, 610700, 610800, 610900, 611000,
                   620100, 620200, 620300, 620400, 620500, 620600, 620700, 620800, 620900, 621000, 621100, 621200, 622900, 630100, 630200, 632800, 640100,
                   640200, 640300, 640400, 650100, 650200, 650500, 652300, 652700, 652800, 652900, 653100, 653200, 654000, 654200, 654300, 659001]

        return city_id

    def main(self,city_id):
        num_list = [num for num in range(1, 30)]
        for a in city_id:
            for num in num_list:
                url = "https://buy.autohome.com.cn/Car/GetCarListModel?brandid=0&seriesid=0&specid=0&pid=210000&cid={}&page={}".format(a, num)
                auto.requ_data(url,a)
                auto.parse_data(auto.requ_data(url,a))
                auto.storing_data(auto.parse_data(auto.requ_data(url,a)))

if __name__ == '__main__':
    auto = AutohomeSpider()
    data = auto.query_data()
    auto.main(data)
    def job():
        data = auto.query_data()
        auto.main(data)
        cursor.close()
        print('关闭游标')
        conn.close()
        print('关闭连接')
    # BlockingScheduler 当调度器是应用中唯一要运行的任务时，使用BlockingScheduler
    scheduler = BlockingScheduler()
    # 当前任务会在每月的1号 15：04执行
    scheduler.add_job(job, 'cron', month='*', day = 1, hour=10, minute=23)
    scheduler.start()
"""
year (int|str) – 年，4位数字 
month (int|str) – 月 (范围1-12) 
day (int|str) – 日 (范围1-31) 
week (int|str) – 周 (范围1-53) 
day_of_week (int|str) – 周内第几天或者星期几 (范围0-6 或者 mon,tue,wed,thu,fri,sat,sun) 
hour (int|str) – 时 (范围0-23) 
minute (int|str) – 分 (范围0-59) 
second (int|str) – 秒 (范围0-59) 
start_date (datetime|str) – 最早开始日期(包含) 
end_date (datetime|str) – 最晚结束时间(包含) 
timezone (datetime.tzinfo|str) – 指定时区 
"""















































































