# -*- coding:utf-8 -*-
import requests
import parsel
import aiohttp
import asyncio
import time
import pymysql
import datetime

# 连接MySQL数据库
conn = pymysql.connect(host="112.126.89.134", user="jgcdb", password="jingche0000", port=3306, db="jgcproddb",charset="utf8")
# conn = pymysql.connect(host="localhost", user="root", password="", port=3306, db="jdbc", charset="utf8")
cursor = conn.cursor()  # 创建游标



sem = asyncio.Semaphore(10)  # 信号量，控制协程数，防止爬的过快

url = 'https://xl.16888.com/style.html'

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    'cookie': 'UM_distinctid=17645e21224139-0630dbe1e44923-c791039-144000-17645e21225aa8; car16888_area[cityId]=244; car16888_area[area_dir]=sy; car16888_area[area_id]=220; car16888_set_area=220; car16888_set_areaName=%E6%B2%88%E9%98%B3; car16888_set_province_name=%E8%BE%BD%E5%AE%81; car16888_set_areaDir=sy; car16888_set_provinceId=18; car16888_set_cityId=244; car16888_set_iscity=; CNZZDATA2314159=cnzz_eid%3D1408780680-1609385015-https%253A%252F%252Ftop.16888.com%252F%26ntime%3D1609385015'
}

# 详情连接列表
series_link_list = []

# 数据存储列表
data_list = []

async def get_html(url):
    async with aiohttp.ClientSession()as session:
        async with session.get(url,headers=headers)as response:
            html = await response.text()  # 可以直接获取bytes
            resp = parsel.Selector(html)
            tr_list = resp.xpath('//table[@class="xl-table-def xl-table-a"]//tr[position()>1]')
            for tr in tr_list:
                # ranking = tr.xpath('./td[@class="xl-td-t1"]/text()').get()
                # # print('排名',ranking)

                series_name = tr.xpath('./td[2]/a/text()').get()
                if series_name == '宏光MINI EV':
                    series_name='宏光MINIEV'
                # print('车系名称',series_name)
                """获取车主之家车系销量的连接"""
                series_link = 'https://xl.16888.com'+tr.xpath('./td[2]/a/@href').get()
                series_link_list.append(series_link)
                # print(series_link)

            """月销量数据"""
            for url in series_link_list:
                detail_resp = requests.get(url, headers).text
                detail_data = parsel.Selector(detail_resp)
                # print(detail_resp)
                # 车系
                series_name = detail_data.xpath('//div[@class="xl-level-head clr"]/span/text()').get().replace('销量详情','')
                if series_name == '宏光MINI EV':
                    series_name = '宏光MINIEV'

                """获取车系id/厂商id"""
                cursor.execute("select series_id,car_series_id,car_series,car_brand_id from t_car_category where category_fullname='{}'".format(series_name))
                id_list = cursor.fetchall()
                # 车系id
                series_id = ''
                # 厂商id
                car_series_id = ''
                # 厂商名称
                car_series = ''
                # 品牌id
                brand_id = ''
                for id in id_list:
                    series_id = id[0]
                    car_series_id = id[1]
                    car_series = id[2]
                    brand_id = id[3]


                """获取品牌名称"""
                cursor.execute("select brand_name from t_car_brand where brand_id='{}'".format(brand_id))
                brand_name = cursor.fetchone()[0]


                tr_list = detail_data.xpath('//table[@class="xl-table-def xl-table-a"]/tr[position()>1][position()<24]')
                # print(tr_list)
                for tr in tr_list:
                    # 时间
                    sale_time = tr.xpath('./td[1]/text()').get()
                    # print(sale_time)

                    # 月销量
                    monthly_sales = tr.xpath('./td[2]/text()').get()
                    # print(monthly_sales)

                    # 当前销量排行
                    now_monthly_sales = tr.xpath('./td[3]/a/text()').get()
                    # print(now_monthly_sales)

                    # 占厂商份额
                    share_of_manufacturers = tr.xpath('./td[4]/text()').get()
                    # print(share_of_manufacturers)

                    # 在厂商排名
                    ranking_among_manufacturers = tr.xpath('./td[5]/a/text()').get()
                    # print(ranking_among_manufacturers)

                    # 在SUV排名
                    ranking_in_suv = tr.xpath('./td[6]/a/text()').get()
                    # print(ranking_in_suv)

                    # 更新时间
                    last_sync_time = datetime.datetime.now().strftime("%Y-%m-28 23:35:23")
                    data = (series_id,series_name,car_series_id,car_series,brand_id,brand_name,sale_time,monthly_sales,now_monthly_sales,share_of_manufacturers,ranking_among_manufacturers,ranking_in_suv,last_sync_time)
                    data_list.append(data)


def data_storage():
    for datas in data_list:
        data = datas
        insert_sql = 'insert into t_car_detail_city_sales(series_id,series_name,car_series_id,car_series,brand_id,brand_name,sale_time,monthly_sales,now_monthly_sales,share_of_manufacturers,ranking_among_manufacturers,ranking_in_suv,last_sync_time)values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'

        cursor.execute(insert_sql, data)
        conn.commit()  # 提交数据
        print('数据提交完成')
    cursor.close()  # 关闭游标
    print('关闭游标')
    conn.close()  # 关闭连接
    print('关闭连接')


def main():
    loop = asyncio.get_event_loop() # 获取事件循环
    tasks = [get_html(url)]  # 把所用任务放到一个列表中
    # print(tasks)
    loop.run_until_complete(asyncio.wait(tasks))  # 激活协程
    loop.close() # 关闭事件循环
    data_storage()

if __name__ == '__main__':
    start = time.time()
    main()
    # print(series_list)
    # print(series_link_list)
    # print(series_id_list)
    print('总耗时：%.5f秒'%float(time.time()-start))
    # 总耗时：9.02079秒



































