


"""
易车交通事故
"""
import requests
import jsonpath
import parsel
import re
import json
import pymysql
import datetime
import time
from datetime import datetime

requests.packages.urllib3.disable_warnings()


# 连接MySQL数据库
conn = pymysql.connect(host="112.126.89.134", user="jgcdb", password="jingche0000", port=3306, db="jgcproddb",charset="utf8")
# conn = pymysql.connect(host="localhost", user="root", password="", port=3306, db="jdbc", charset="utf8")
cursor = conn.cursor()  # 创建游标

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
    'Cookie':'locatecity=210100; bitauto_ipregion=175.168.56.62%3a%e8%be%bd%e5%ae%81%e7%9c%81%e6%b2%88%e9%98%b3%e5%b8%82%3b1701%2c%e6%b2%88%e9%98%b3%e5%b8%82%2cshenyang; CIGDCID=cd1771b5f02044ecb13150c308ccf27c; G_CIGDCID=cd1771b5f02044ecb13150c308ccf27c; CIGUID=36375428-0b68-441e-84a5-6883cdb2c033; selectcity=210100; selectcityid=1701; selectcityName=%E6%B2%88%E9%98%B3; auto_id=63b70ea4c3e24267a4e259dcb88c867f; UserGuid=36375428-0b68-441e-84a5-6883cdb2c033; Hm_lvt_610fee5a506c80c9e1a46aa9a2de2e44=1616290018; XCWEBLOG_testcookie=yes; report-cookie-id=428311892_1616290021490; Hm_lvt_f69697b4b54908f4b7129fa24bbfdbbe=1616290026; Hm_lpvt_610fee5a506c80c9e1a46aa9a2de2e44=1616290059; Hm_lpvt_f69697b4b54908f4b7129fa24bbfdbbe=1616290059'
}


def get_data(url):
    response = requests.get(url=url,headers=headers,verify=False).text
    resp_html = parsel.Selector(response)

    # 解析数据
    div_list = resp_html.xpath('//div[@class="main-v-list clearfix"]/div')
    for div in div_list:
        title = div.xpath('.//a/img/@title').get()
        print(title)

        cover_map = 'https:'+div.xpath('.//a/img/@src').get()
        print(cover_map)

        detail_link = 'https:'+div.xpath('.//a/@href').get()
        # print(detail_link)

        # 请求详情
        detail_page = requests.get(detail_link,headers=headers,verify=False).text

        # 视频连接
        video_link = re.findall('"name":"FHD","url":"http:.*?\.f40\.mp4"',detail_page)[0].replace('"name":"FHD","url":','').replace('"','')
        print('视频连接',video_link)

        detail_data = parsel.Selector(detail_page)

        # 头像
        publisher_head = 'https:'+detail_data.xpath('//div[@class="video-avthor"]/a/img/@src').get()
        print('头像',publisher_head)

        # 作者
        publisher = detail_data.xpath('//div[@class="video-user-info"]/a/text()').get()
        print('作者',publisher)

        type = '30'

        # 时间
        create_time = datetime.now().strftime("%Y-%m-%d 23:35:23")
        # print(create_time)

        data = (cover_map,publisher_head,title,publisher,create_time,video_link,type)

        print(data)
        sql = "select * from t_car_video where cover_map='{}'and publisher_head='{}'and title ='{}' and publisher='{}'".format(
            data[0], data[1], data[2], data[3])
        cursor.execute(sql)
        many = cursor.fetchone()
        if many:
            print('此数据表中已存在')
        else:
            insert_sql = 'insert into t_car_video(cover_map,publisher_head,title,publisher,create_time,video_link,type)values (%s,%s,%s,%s,%s,%s,%s)'
            cursor.execute(insert_sql, data)
            conn.commit()  # 提交数据
            print('数据提交完成')


def main():
    for page in range(1, 2):
        url = "https://v.yiche.com/cate_147_0_{}.html".format(page)
        get_data(url)

if __name__ == '__main__':
    def main_time(h=1, m=4):
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
            main()
            cursor.close()  # 关闭游标
            print('关闭游标')
            conn.close()  # 关闭连接
            print('关闭连接')
    main_time()








