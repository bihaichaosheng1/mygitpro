# -*- coding:utf-8 -*-

import requests
import parsel
import random
import datetime
from urllib.parse import urlencode,quote,unquote
import pymysql
import time
from apscheduler.schedulers.blocking import BlockingScheduler




def req_hot_data():
    # 连接MySQL数据库
    conn = pymysql.connect(host="112.126.89.134", user="jgcdb", password="jingche0000", port=3306, db="jgcproddb",
                           charset="utf8")
    # conn = pymysql.connect(host="localhost", user="root", password="", port=3306, db="jdbc", charset="utf8")
    # 创建游标
    cursor = conn.cursor()
    # 删除 历史热点新闻

    del_sql = "delete from t_cms_article where channel_key = 'morning_paper_hot_news' "
    del_sql_two = "delete from t_cms_article where channel_key = 'morning_paper_auto_news' "
    cursor.execute(del_sql)
    cursor.execute(del_sql_two)
    conn.commit()
    print('完成')


    url = 'https://ent.163.com/'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
    }
    print(url)
    resp = requests.get(url,headers=headers,verify=False)
    # print(resp.text)
    resp_data = parsel.Selector(resp.text)
    li_list = resp_data.xpath('//ul[@class="scroll_ul lf_comment_lists"]/li')
    print(li_list)
    for li in li_list:
        print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        # id
        article_no = str(random.randint(1302470534865694722,1302470539999999999))
        print('article_on:',article_no)

        # article_key
        article_key = 'wynews'+str(random.randint(1,20))
        print('article_key:',article_key)

        # 标题
        article_title = li.xpath('./a/p/@title').get()
        print('article_title:',article_title)

        detail_link = li.xpath('./a/@href').get()
        print('连接:',detail_link)
        detail_resp = requests.get(detail_link,headers=headers,verify=False)
        detail_data = parsel.Selector(detail_resp.text)

        # 内容
        # article_content = ''.join(detail_data.xpath('//div[@id="endText"]|//div[@class="post_body"]').getall()).replace('网易娱乐','娱乐')
        article_content = detail_data.xpath('//div[@id="endText"]|//div[@class="post_body"]').getall()
        # article_content = quote(article_content1)
        if article_content == '':
            pass
        print('article_content:',article_content)


        # channel_key
        channel_key = 'morning_paper_hot_news'
        # print('channel_key:',channel_key)

        #is_banner
        is_banner = 0
        # print('is_banner:',is_banner)

        # 发布时间
        release_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # print('发布时间:',release_time)

        # 创建时间
        create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # print('创建时间',create_time)

        # 更新时间
        update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # print('更新时间',update_time)

        data=(article_no,article_key,article_title,article_content,channel_key,is_banner,release_time,create_time,update_time)
        print(data)
        try:
            select_sqlone = "select * from t_cms_article where article_title='{}' ".format(data[2])
            cursor.execute(select_sqlone)
            many = cursor.fetchone()
            if many:
                print('此数据表中已存在')

            else:
                insert_sqlone = "insert into t_cms_article(article_no,article_key,article_title,article_content,channel_key,is_banner,release_time,create_time,update_time)value (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(insert_sqlone,data)
                conn.commit()
                print('+++++++++++++++++++++++++数据已提交+++++++++++++++++++++++++++++')
        except:
            continue


    url = 'http://www.chinaautonews.com.cn/'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
    }

    resp = requests.get(url, headers=headers)
    resp_data = parsel.Selector(resp.text)
    li_list = resp_data.xpath('//div[@class="bd-right"]/ul/li')
    for li in li_list:
        # id
        article_no = str(random.randint(1302470539999999999, 1302470566666666666))
        print('article_on:', article_no)

        # article_key
        article_key = 'wynews' + str(random.randint(1,100))
        print('article_key:', article_key)

        # 标题
        article_title = li.xpath('./a/@title').get()

        # 详情链接
        detail_link = li.xpath('./a/@href').get()
        detail_resp = requests.get(detail_link, headers=headers)
        detail_data = parsel.Selector(detail_resp.text)
        print(article_title, detail_link)

        # 内容
        article_content = ''.join(detail_data.xpath('//div[@class="lside"]').getall()).replace(
            '<a href="http://www.chinaautonews.com.cn">首页</a><span>&gt;</span><a href="http://www.chinaautonews.com.cn/list-6-1.html">新闻</a> &gt; <a href="http://www.chinaautonews.com.cn/list-10-1.html">资讯</a> &gt;  正文',
            '')
        # print(article_content)

        # channel_key
        channel_key = 'morning_paper_auto_news'

        # is_banner
        is_banner = 0

        # 发布时间
        release_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print('发布时间:', release_time)

        # 创建时间
        create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print('创建时间', create_time)

        # 更新时间
        update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print('更新时间', update_time)

        data = (article_no, article_key, article_title, article_content, channel_key, is_banner, release_time, create_time,update_time)
        select_sql = "select * from t_cms_article where article_title='{}' ".format(data[2])
        cursor.execute(select_sql)
        many = cursor.fetchone()
        if many:
            print('此数据表中已存在')
            continue
        else:
            insert_sql2 = "insert into t_cms_article(article_no,article_key,article_title,article_content,channel_key,is_banner,release_time,create_time,update_time)value (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            print(insert_sql2)
            cursor.execute(insert_sql2, data)
            conn.commit()
            print('+++++++++++++++++++++++++数据已提交+++++++++++++++++++++++++++++')

    cursor.close()
    conn.close()
    print('库已关闭')

if __name__ == '__main__':
    req_hot_data()
    def main_time(h=7, m=0):
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
            req_hot_data()
    main_time()






