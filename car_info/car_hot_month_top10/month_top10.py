# -*- coding:utf-8 -*-
import requests
import parsel
import aiohttp
import asyncio
import time
import pymysql
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler


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

# 车系名称
series_list = []

# 车主之家 销量详情连接
series_link_list = []

# 库里series_id
series_id_list = []




async def get_html(url):
    # with(await sem):
    async with aiohttp.ClientSession()as session:
        async with session.get(url,headers=headers)as response:
            html = await response.text()  # 可以直接获取bytes
            resp = parsel.Selector(html)
            tr_list = resp.xpath('//table[@class="xl-table-def xl-table-a"]//tr[position()>1][position()<16]')
            for tr in tr_list:
                series_name = tr.xpath('./td[2]/a/text()').get()

                if series_name == '宏光MINI EV':
                    series_name='宏光MINIEV'

                """获取车系id"""
                cursor.execute("select series_id from t_car_category where category_fullname='{}'".format(series_name))
                id_list = cursor.fetchall()
                series_id = ''
                for id in id_list:
                    series_id = id[0]
                    series_id_list.append(series_id)

                # 更新时间
                last_sync_time = datetime.datetime.now().strftime("%Y-%m")
                data = (series_id,last_sync_time)
                select_sql = "select * from inquiry_hot_selling_models where spec_id='{}' and hot_sign ".format(data[0],data[1])
                cursor.execute(select_sql)
                many = cursor.fetchone()
                if many:
                    print('此数据表中已存在')
                else:
                    insert_sql = "insert into inquiry_hot_selling_models(spec_id,hot_sign)values (%s,%s)"
                    cursor.execute(insert_sql,data)
                    conn.commit()




def main():

    loop = asyncio.get_event_loop() # 获取事件循环
    tasks = [get_html(url)]  # 把所用任务放到一个列表中
    print(tasks)
    loop.run_until_complete(asyncio.wait(tasks))  # 激活协程
    loop.close() # 关闭事件循环

if __name__ == '__main__':
    # start = time.time()
    # main()
    # cursor.close()
    # conn.close()
    # print('数据库连接已关闭')
    # print('总耗时：%.5f秒'%float(time.time()-start))
    # print(series_id_list)
    # 总耗时：9.02079秒
    def job():
        start = time.time()
        main()
        cursor.close()
        conn.close()
        print('数据库连接已关闭')
        print('总耗时：%.5f秒' % float(time.time() - start))
    # BlockingScheduler 当调度器是应用中唯一要运行的任务时，使用BlockingScheduler
    scheduler = BlockingScheduler()
    # 当前任务会在每月的1号 15：04执行
    scheduler.add_job(job, 'cron', month='*', day = '1', hour='1', minute='0')
    scheduler.start()




































