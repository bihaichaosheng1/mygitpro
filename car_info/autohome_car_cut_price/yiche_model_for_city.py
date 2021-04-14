# coding=utf-8
# import requests
# import re
# import parsel
# import datetime
# import pymysql
#
# """
# 易车--东北三省（省会）汽车降价数据
# """
#
# # 连接MySQL数据库
# conn = pymysql.connect(host="112.126.89.134", user="jgcdb", password="jgcdb123456", port=3306, db="jgcdb",charset="utf8")
# # conn = pymysql.connect(host="localhost", user="root", password="", port=3306, db="jdbc", charset="utf8")
# # 创建游标
# cursor = conn.cursor()
#
#
# # 先对易车做一个请求，得到品牌链接（后部分）与车系id
# url = 'https://apicar.bitauto.com/CarInfo/getlefttreejson.ashx?tagtype=jiangjia&pagetype=masterbrand&objid=157&cityid=_c1401'
# resp_data = requests.get(url=url)
# resp_json = resp_data.text
# id_data = re.findall(r'id:[0-9]*',resp_json)  # 得到品牌id
# # print('品牌id',id_data) # type:list  格式:'id:9'  共253个
#
# address = [1101,1401,1701,1402,1708,1106] # 哈尔滨,长春,沈阳,吉林市,大连,佳木斯
# """根据得到的品牌id 循环传参进初始链接 得到车系链接（后部分）"""
# for a in address:
#     for ids in id_data:
#         id = ids.replace('id:','')
#         base_url = 'https://apicar.bitauto.com/CarInfo/getlefttreejson.ashx?tagtype=jiangjia&pagetype=masterbrand&cityid=_c{}&objid={}'.format(a,id)
#         resp_data = requests.get(url=base_url)
#         resp_json = resp_data.text
#         series_link_after = re.findall(r'/nb[0-9]*_[a-z][0-9]*', resp_json)  # 得到品牌的后半部分链接
#         # print(series_link_after)
#         # 对车系链接发起请求
#         for link in series_link_after:
#             for page in range(1,11):
#                 base_url = "https://jiangjia.bitauto.com{}?pid={}".format(link,page)
#                 # base_url = "https://jiangjia.bitauto.com" + str
#                 series_info = requests.get(url=base_url)
#                 if series_info.text == None:
#                     continue
#                 print(base_url)
#                 series_data = parsel.Selector(series_info.text)
#
#                 spec_list = series_data.xpath('//div[@class="main-inner-section sales-agent-list"]/div[@class="row reduce-list"]')
#                 if spec_list == []:
#                     continue
#                 for spec in spec_list:
#                     # 车系名称
#                     series_name = series_data.xpath('//div[@class="box"]/h2/text()').get()
#                     print('车系名称',series_name)
#                     # 车型id
#                     spec_link = spec.xpath('./div/h6/a/@href').get()
#                     spec_id = "".join(re.findall(r'[0-9]*/ne', spec_link)).replace('/ne', '')
#                     # print('车型id',spec_id)
#                     # 车型名称
#                     spec_name = spec.xpath('./div/h6/a/text()').get().replace('TID',' TID')
#                     # print('名称：',spec_name)
#                     # 城市id
#                     city_id = series_data.xpath('//div[@class="col-ads"]/ins/@cityid').get()
#                     # print('城市id', city_id)
#                     # 车型指导价
#                     guidance_price = spec.xpath('./div/div/div[@class="col-xs-7 middle"]/p/span[@class="market-price"]/text()').get()
#                     # print('指导价：',guidance_price)
#                     # 现在价格
#                     price = spec.xpath('./div/div/div[@class="col-xs-7 middle"]/p/span[@class="now-price"]/text()').get()
#                     # print('现价：',price)
#                     # 降价
#                     cut_price = spec.xpath('./div/div/div[@class="col-xs-7 middle"]/h3/a[@class="reduce-price"]/text()').get()
#                     # print('降价',cut_price)
#                     # 最后一次更新时间
#                     # last_sync_time = datetime.datetime.now().strftime("%Y-%m")
#                     last_sync_time = datetime.datetime.now().strftime("%Y-8-30 %H:%M:%S")
#                     # print(last_sync_time)
#                     # 来源（app）
#                     app_id = '4'  # 数据来自易车
#
#                     # 数据存储
#                     data = (series_name,spec_name, city_id, guidance_price, cut_price, price, last_sync_time, app_id)
#                     print('这是即将存到数据库的data', data)
#                     sql2 = "select * from t_car_cut_price_to_app where spec_name='{}'and city_id='{}'and price='{}'".format(data[1], data[2],data[5])
#                     cursor.execute(sql2)
#                     many = cursor.fetchone()
#                     if many:
#                         print('此数据表中已存在')
#                     else:
#                         sql_yiche_car_detail_city = "insert into t_car_cut_price_to_app(series_name,spec_name, city_id, guidance_price, cut_price, price, last_sync_time, app_id) value(%s,%s,%s,%s,%s,%s,%s,%s) "
#                         cursor.execute(sql_yiche_car_detail_city, data)
#                         conn.commit()  # 提交数据
#                         print('数据提交完成')
#
#
# cursor.close()  # 关闭游标
# conn.close()  # 关闭连接

import requests
import re
import parsel
import datetime
import pymysql
import concurrent.futures
"""
易车--东北三省（省会）汽车降价数据
"""

# 连接MySQL数据库
conn = pymysql.connect(host="112.126.89.134", user="jgcdb", password="jingche0000", port=3306, db="jgcproddb",charset="utf8")
# conn = pymysql.connect(host="localhost", user="root", password="", port=3306, db="jdbc", charset="utf8")
# 创建游标
cursor = conn.cursor()

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
        'Connection': 'close'
    }

def res_json(url):
    # 请求函数json
    # 对易车的品牌id进行抓取
    resp_data = requests.get(url=url,headers=headers,verify=False)
    resp_json = resp_data.text
    id_data = re.findall(r'id:[0-9]*', resp_json)  # 得到品牌id
    return id_data

def res_data(id_data):
    # 请求函数
    # address = [1101, 1401, 1701, 1402, 1708, 1106]  # 哈尔滨,长春,沈阳,吉林市,大连,佳木斯

    address = [ 422800, 460300, 469021,
                469022, 469023, 469024, 469025, 469026, 469027, 469028, 469029, 469030, 532300, 532900, 622900, 652300,
                659006, 659007, 659008, 659009, 710000, 810000, 820000]

    for a in address:
        for ids in id_data:
            id = ids.replace('id:', '')
            try:
                base_url = 'https://apicar.bitauto.com/CarInfo/getlefttreejson.ashx?tagtype=jiangjia&pagetype=masterbrand&cityid=_c{}&objid={}'.format(a, id)
                resp_data = requests.get(url=base_url,verify=False)
                resp_json = resp_data.text
                series_link_after = re.findall(r'/nb[0-9]*_[a-z][0-9]*', resp_json)  # 得到品牌的后半部分链接
                # print(series_link_after)
                for link in series_link_after:
                    yield link
            except requests.exceptions.ConnectionError:
                continue

def parse_data(link):
    # 解析函数
    for l in link:
        try:
            for page in range(1, 6):
                base_url = "https://jiangjia.bitauto.com{}?pid={}".format(l, page)
                print(base_url)
                series_info = requests.get(url=base_url,headers=headers,verify=False)

                series_data = parsel.Selector(series_info.text)

                spec_list = series_data.xpath('//div[@class="main-inner-section sales-agent-list"]/div[@class="row reduce-list"]')
                if spec_list == []:
                    continue
                for spec in spec_list:
                    # 车系名称
                    series_name = series_data.xpath('//div[@class="box"]/h2/text()').get()
                    # print('车系名称', series_name)
                    # 车型id
                    spec_link = spec.xpath('./div/h6/a/@href').get()
                    spec_id = "".join(re.findall(r'[0-9]*/ne', spec_link)).replace('/ne', '')
                    # print('车型id',spec_id)
                    # 车型名称
                    spec_name = spec.xpath('./div/h6/a/text()').get().replace('TID', ' TID')
                    # print('名称：',spec_name)
                    # 城市id
                    city_id = series_data.xpath('//div[@class="col-ads"]/ins/@cityid').get()
                    # print('城市id', city_id)
                    # 车型指导价
                    guidance_price = spec.xpath('./div/div/div[@class="col-xs-7 middle"]/p/span[@class="market-price"]/text()').get()
                    # print('指导价：',guidance_price)
                    # 现在价格
                    price = spec.xpath('./div/div/div[@class="col-xs-7 middle"]/p/span[@class="now-price"]/text()').get()
                    # print('现价：',price)
                    # 降价
                    cut_price = spec.xpath('./div/div/div[@class="col-xs-7 middle"]/h3/a[@class="reduce-price"]/text()').get()
                    # print('降价',cut_price)
                    # 最后一次更新时间
                    # last_sync_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    last_sync_time = datetime.datetime.now().strftime("%Y-8-30 14:22:09")
                    # print(last_sync_time)
                    # 来源（app）
                    app_id = '4'  # 数据来自易车

                    yield series_name,spec_name,city_id,guidance_price,cut_price,price,last_sync_time,app_id
        except requests.exceptions.ConnectionError:
            continue

def store_data(spec_data):
    # 数据存储
    # print(spec_data[0])
    for data in spec_data:
        # print('123123123123123123123123123123123',data)
        print(data[1], data[2], data[5],data[6])
        print('这是即将存到数据库的data', data)

        # 若 mysql 连接失败就重新连接
        conn.ping(reconnect=True)

        # sql2 = "select * from t_car_cut_price_to_app where spec_name='{}'and city_id='{}'and price='{}'and last_sync_time='{}'".format(data[1], data[2],data[5],data[6])
        sql2 = "select * from t_car_cut_price_to_app where spec_name='{}'and city_id='{}'and price='{}'".format(data[1],data[2],data[5])
        cursor.execute(sql2)
        many = cursor.fetchone()
        if many:
            print('此数据表中已存在')
        else:
            sql_yiche_car_detail_city = "insert into t_car_cut_price_to_app(series_name,spec_name, city_id, guidance_price, cut_price, price, last_sync_time, app_id) value(%s,%s,%s,%s,%s,%s,%s,%s) "
            cursor.execute(sql_yiche_car_detail_city, data)
            conn.commit()  # 提交数据
            print('数据提交完成')
    cursor.close()
    print('关闭游标')
    conn.close()
    print('关闭连接')

def main():
    # 主函数
    url = 'https://apicar.bitauto.com/CarInfo/getlefttreejson.ashx?tagtype=jiangjia&pagetype=masterbrand&objid=157&cityid=_c1401'
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=12)  # 最大线程等于10

    id_data = res_json(url)

    executor.submit(res_data,id_data)

    executor.submit(parse_data(res_data(id_data)))

    executor.submit(store_data,parse_data(res_data(id_data)))

    executor.shutdown()

if __name__ == '__main__':
    main()
