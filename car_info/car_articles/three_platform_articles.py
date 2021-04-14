# -*- coding:utf-8 -*-


"""
老司机---导购文章
"""
import requests
import parsel
import datetime
import json
import jsonpath
import time
import pymysql
import sys
sys.setrecursionlimit(1000000)




def req_url(url):
    """请求函数"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
        'Cookie': 'sogouPlatform=null; dubaReferer=null; LSJCITYOBJ=%7B%22code%22%3A131%2C%22name%22%3A%22%E5%8C%97%E4%BA%AC%22%7D; OdStatisticsToken=03415f44-722d-4cf8-82e5-93d141aaa102-1600747086164; LSJLOGCOOKIE=11911911946108971111151051061054699111109-16495225-1600747086341; UM_distinctid=174b3f6220bbb8-06e39ab82c8273-333769-144000-174b3f6220cc58; _ga=GA1.2.1424285701.1600747090; BAIDU_SSP_lcr=https://www.baidu.com/link?url=x_JbWkLpSzEaIK_i6Xi4yOgnVXbzKS61xQQJPkV4MeOy0EGI0hvzJVinEy6R5keQ&ck=8596.1.71.271.149.267.137.360&shh=www.baidu.com&wd=&eqid=b637da4700016832000000025f6d4f5b; Hm_lvt_9fa8070d0f1a747dc1fd8cc5bdda4088=1600747087,1600999264; _gid=GA1.2.118480394.1600999285; CNZZDATA1261736092=543113352-1600745413-%7C1600999490; JSESSIONID=A50F1E9FE25E460BD3B393C5B6039DE8; Hm_lpvt_9fa8070d0f1a747dc1fd8cc5bdda4088=1600999618'
    }
    for page in range(1, 51):
        data = {
            'method': '/home/ywf/tablist',
            'tabid': '32',
            'page': str(page)
        }
        resp_article_data = requests.post(url=url,headers=headers,data=data)
        yield resp_article_data

def req_detail(resp_article_data):
    """请求详情、解析函数"""
    for response in resp_article_data:
        resp_json = json.loads(response.text)
        article_id = jsonpath.jsonpath(resp_json,'$..resourceid')
        for a_id in article_id:
            acticle_link = 'https://www.laosiji.com/thread/{}.html'.format(a_id)
            article = requests.post(url=acticle_link)

            print('===============================================老   司   机======================================================')

            # 解析数据
            article_data = parsel.Selector(article.text)

            """文章链接"""
            print('文章详情连接', acticle_link)

            """文章标题"""
            article_title = article_data.xpath('//div[@class="thread-box article"]/h1[@class="title"]/text()').get()
            # print('文章标题',article_title)

            """显示图片（三张）"""
            article_img = str(article_data.xpath('//div[@class="thread-box article"]/div[@class="threa-main-box"]/li/div[@class="img-box"]/a/img/@src').getall()[0:3])
            # print("文章显示图片（三张）", article_img)

            """发布时间"""
            article_time = article_data.xpath('//div[@class="thread-box article"]/div[@class="topic-list-div clearfix"]/p/text()').get()
            # print("上传时间",article_time)

            """文章来源"""
            article_source = '老司机'
            # print("来  源",article_source)

            """文章作者"""
            article_author = article_data.xpath('//div[@class="right-box fl"]/div[@class="author-information"]/a/div[@class="author-name"]/span/text()').get()
            # print("文章作者",article_author)

            """作者头像"""
            head_portrait = article_data.xpath('//div[@class="author-information"]/a/img/@src').get()
            # print('作者头像',head_portrait)

            """文章内容"""
            article_content = ''.join(article_data.xpath('//div[@class="thread-box article"]/div[@class="threa-main-box"]/p|//div[@class="thread-box article"]/div[@class="threa-main-box"]/li/div/p|//div[@class="thread-box article"]/div[@class="threa-main-box"]/li/div[@class="img-box"]/a/img').getall())
            # print('文章内容',article_content)

            """点 赞 量"""
            likes = article_data.xpath('//a[@id="threadPraise"]/span/text()').get()
            # print('点 赞 量',likes)

            """更新时间"""
            last_sync_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # print('更新时间',last_sync_time)

            """来自app"""
            app_id = '3'
            # print('来源appID',app_id)
            yield article_title,article_img,article_time,article_source,article_author,head_portrait,article_content,likes,last_sync_time,app_id

def store_data(article_datas):
    """存储函数"""
    # 连接MySQL数据库
    conn = pymysql.connect(host="112.126.89.134", user="jgcdb", password="jingche000", port=3306, db="jgcproddb",charset='utf8')
    # conn = pymysql.connect(host="localhost", user="root", password="", port=3306, db="jdbc", charset="utf8")
    # 创建游标
    cursor = conn.cursor()

    for data in article_datas:
        try:
            print('即将存到数据库中的数据',data)
            sql2 = "select * from t_external_articles where article_title='{}'".format(data[0])
            cursor.execute(sql2)
            many = cursor.fetchall()
            if many:
                print('数据已存在')
            else:
                sql = "insert into t_external_articles(article_title,article_img,article_time,article_source,article_author,head_portrait,article_content,likes,last_sync_time,app_id) value(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "
                cursor.execute(sql, data)
                conn.commit()  # 提交数据
                print('数据提交完成')

        except pymysql.err.InternalError as e:
            continue
    cursor.close()  # 关闭游标
    print('关闭游标')
    conn.close()  # 关闭连接
    print('关闭连接')


def laosiji_main():
    """主函数"""
    url = 'https://www.laosiji.com/proxy/api'
    resp_article_data = req_url(url)
    article_datas = req_detail(resp_article_data)
    store_data(article_datas)

if __name__ == '__main__':
    laosiji_main()


"""
汽车人---人物文章
"""
import requests
import parsel
import datetime
import re
import random
import pymysql
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
    'Cookie': 'zh_choose=s; UM_distinctid=174c33a131a8de-0c9ee05063636c-333769-144000-174c33a131bad8; CNZZDATA1260105523=1199699615-1601003197-http%253A%252F%252Fwww.cnqcr.com%252F%7C1601003197',
    'Content-Type': 'text/html',
    'Accept-Ranges': 'bytes',
    'Content-Encoding': 'gzip',
    'ETag': '652f6b53c92d61:0'
}


def req_html(url):
    """请求函数"""
    req_auticle = requests.get(url, headers=headers)
    req_auticle.encoding = 'gbk'
    auticle_data = parsel.Selector(req_auticle.text)
    div_list = auticle_data.xpath('//div[@class="nyxwlb"]/div[@class="sylb"]')
    for div in div_list:
        """详情连接"""
        article_url = 'http://www.cnqcr.com' + div.xpath('./div[@class="wz"]/span/a/@href').get()
        yield article_url


def req_detail(article_url):
    """请求详情函数"""
    for url in article_url:
        print(url)
        response_list = requests.get(url, headers=headers)
        response_list.encoding = 'utf-8'
        yield response_list


def par_data(response_list):
    """解析函数"""
    print(
        '===============================================汽   车   人======================================================')
    for responses in response_list:
        try:
            """文章标题"""
            response = parsel.Selector(responses.text)
            article_title = response.xpath('//div[@class="nrzw"]/div[@class="nrbt"]/h1/text()').get()
            print('文章标题', article_title)

            """文章显示图片（三张）"""
            # article_cover_photo = response.xpath('//div[@class="nrxq"]/p[1]/img/@src').get().replace('/d','http://www.cnqcr.com/d')
            article_img = response.xpath(
                '//div[@class="nrxq"]/p/img/@src|//div[@class="nrxq"]/p/strong/img/@src').get().replace('/d',
                                                                                                        'http://www.cnqcr.com/d')
            print('文章显示图片', article_img)

            """上传时间"""
            article_time = ''.join(re.findall('：\d+-\d+-\d+ \d+:\d+:\d+', response.xpath(
                '//div[@class="nrzw"]/div[@class="nrbt"]/span/text()').get())).replace('：', '')
            print('上传时间', article_time)

            """文章来源"""
            article_source = '汽车人传媒'
            print(article_source)

            """文章作者"""
            article_author = response.xpath('//div[@class="nrzw"]/div[@class="nrbt"]/span/a[2]/text()').get()
            if article_author == None:
                article_author = '汽车人'
            print('文章作者', article_author)

            """作者头像"""
            # 汽车人文章没有作者头像字段
            head_portrait = 'zanwu'

            """文章内容"""
            article_content = "".join(response.xpath(
                # '//div[@class="nyxwlb"]/div[@class="nrzw"]/div[@class="nrxq"]/p|//div[@class="nrzw"]/div[@class="nrxq"]/p/img/@src').getall().replace('/d','http://www.cnqcr.com/d')
                '//div[@class="nyxwlb"]/div[@class="nrzw"]/div[@class="nrxq"]/p').getall()).replace('/d',
                                                                                                    'http://www.cnqcr.com/d')
            print('文章内容', article_content)

            """点 赞 量"""
            likes = random.randint(1, 500)
            print('点 赞 量', likes)

            """更新时间"""
            last_sync_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print('更新时间', last_sync_time)

            """来自app"""
            app_id = '1'
            print('来源appID', app_id)
            yield article_title, article_img, article_time, article_source, article_author, head_portrait, article_content, likes, last_sync_time, app_id
        except AttributeError:
            continue


def store_data(article_datas):
    """存储函数"""
    # 连接MySQL数据库
    conn = pymysql.connect(host="112.126.89.134", user="jgcdb", password="jingche000", port=3306, db="jgcproddb",
                           charset="utf8mb4")
    # conn = pymysql.connect(host="localhost", user="root", password="", port=3306, db="jdbc", charset="utf8")
    # 创建游标
    cursor = conn.cursor()
    for data in article_datas:
        print('即将存到数据库中的数据', data)
        sql2 = "select * from t_external_articles where article_title='{}'".format(data[0])
        cursor.execute(sql2)
        many = cursor.fetchall()
        try:
            if many:
                print('数据已存在')
            else:
                sql = "insert into t_external_articles(article_title,article_img,article_time,article_source,article_author,head_portrait,article_content,likes,last_sync_time,app_id) value(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "
                cursor.execute(sql, data)
                conn.commit()  # 提交数据
                print('数据提交完成')
        except pymysql.err.InternalError:
            continue
        except pymysql.err.DataError:
            continue
    cursor.close()  # 关闭游标
    print('关闭游标')
    conn.close()  # 关闭连接
    print('关闭连接')


def qicheren_main():
    """主函数"""
    for page in range(1, 96):
        url = 'http://www.cnqcr.com/renwu/index_{}.html'.format(page)
        article_url = req_html(url)
        response_list = req_detail(article_url)
        article_datas = par_data(response_list)
        store_data(article_datas)


if __name__ == '__main__':
    qicheren_main()


"""
汽车头条
"""
import requests
import parsel
import json
import jsonpath
import datetime
import time
import pymysql
import sys

sys.setrecursionlimit(1000000)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
    'cookie': 'right_bottom_ad=null; left_right_1=null; left_right_2=null; right_bottom_ad2=0; PHPSESSID=fffb66f48e4b627d078c1bb1596c81f4; right_bottom_ad=null; left_right_1=null; left_right_2=null; right_bottom_ad2=0; Hm_lvt_70af9ea91e7adc8195f6d49511b9a2f1=1601008919,1601025767; open_ad=1; vcode=pg2u; XSRF-TOKEN=eyJpdiI6ImpWUnEwVGk4ejh6dFFKWnZPaVFjSFE9PSIsInZhbHVlIjoiM3owVFI5VERQaVp2cWh0RWVnaUFXU0xldGp3R3N1SXJ3a0lmamVIaDZpMk4zZGU1NnMxbmhSaGhrUFJXbXFJcUxoTVNhRTN1eThWaHY2YXhhK2Q2dXc9PSIsIm1hYyI6ImIxNjliN2ZkZGQzMThlOGQyODU2OTFlZjM4NmIzNmE1NTM4YWY0MmIxZmU0OTYzN2I4Mjc2MWU1ZTExZTgyMjgifQ%3D%3D; laravel_session=eyJpdiI6InNqTHJJWkluK2J2NG4rYkxuOU15Vnc9PSIsInZhbHVlIjoibkFBYlRaSGI4RlVHY3MwWU93NjZvWnp4OExjOG1pRlZKR3NYdUc0TisxUk00WlhrcFNhWUc1TUxhTFZFSWQwaERpNjVBNUxFMDJYKzVuT0t1XC9nRlpRPT0iLCJtYWMiOiIzOGNhODkxYWMyNDYwOWVjNTk1MDE3NzY2YTBjNTc1YjE5NTVlOTM5ODEyN2ViZDNiZTE1Njc5NTdkYWU1ZjE5In0%3D; Hm_lpvt_70af9ea91e7adc8195f6d49511b9a2f1=1601047283',
    'path': '/news/833489'
}


def req_html(url):
    """请求函数"""
    try:
        time.sleep(1)
        resp_data = requests.get(url=url, headers=headers, timeout=60)
        resp_json = json.loads(resp_data.text)
        print(resp_json)
        article_id_list = jsonpath.jsonpath(resp_json, '$..id')
        for article_id in article_id_list:
            yield article_id
    except json.decoder.JSONDecodeError:
        print('json---期望值：行1列1（字符0）')
    except requests.exceptions.ReadTimeout:
        pass


def req_detail(article_id):
    """请求详情函数"""
    for id in article_id:
        print(id)
        article_url = 'https://www.qctt.cn/news/' + str(id)
        print(
            '===============================================汽   车   人======================================================')
        print(article_url)
        time.sleep(1)
        article_response = requests.get(article_url, headers=headers, timeout=60)
        yield article_response  # yield 返回一个生成器


def par_data(article_response):
    """解析函数"""
    for response in article_response:
        print('这是响应', response)
        article_data = parsel.Selector(response.text)
        """文章标题"""
        article_title = article_data.xpath('//div[@class="content_detail_left"]/div[@class="title"]/text()').get()
        if article_title == None:
            continue
        print('文章标题', article_title)

        """封面图片"""
        article_img = article_data.xpath(
            '//div[@class="content_detail_left"]/div[@class="y_text2"]//img/@src').get()
        print('封面图片', article_img)

        """发布时间"""
        article_time = article_data.xpath(
            '//div[@class="content_detail_left"]/div[@class="part2"]/span/text()').get()
        print('发布时间', article_time)

        """文章来源"""
        article_source = '汽车头条'
        print('文章来源', article_source)

        """文章作者"""
        article_author = article_data.xpath(
            '//div[@class="content_detail_left"]/div[@class="part2"]/a/text()').get()
        print('文章作者', article_author)

        """作者头像"""
        head_portrait = 'zanwu'

        """文章内容"""
        article_content = ''.join(article_data.xpath('//div[@class="y_text2"]').getall()).replace(
            '<div class="y_text2">', '').replace('</div>', '')
        print('文章内容', article_content)

        """阅 读 量"""
        likes = article_data.xpath(
            '//div[@class="part2"]/span[@style="float:right;margin-right:20px"]/span[@style="color:#17abc1"]/text()').get()
        print('阅 读 量', likes)

        """更新时间"""
        last_sync_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print('更新时间', last_sync_time)

        """来自app"""
        app_id = '2'
        print('来自appID', app_id)
        yield article_title, article_img, article_time, article_source, article_author, head_portrait, article_content, likes, last_sync_time, app_id


def store_data(article_datas):
    """存储函数"""
    # 连接MySQL数据库
    conn = pymysql.connect(host="112.126.89.134", user="jgcdb", password="jingche000", port=3306, db="jgcproddb",
                           charset="utf8")
    # conn = pymysql.connect(host="localhost", user="root", password="", port=3306, db="jdbc", charset="utf8")
    # 创建游标
    cursor = conn.cursor()
    for data in article_datas:
        print('即将存到数据库中的数据', data)
        # sql2 = "select * from t_external_articles where article_title='{}'".format(data[0])
        sql2 = "select * from t_external_articles where article_title='{}'".format(data[1])
        cursor.execute(sql2)
        many = cursor.fetchall()
        if many:
            print('数据已存在')
        else:
            sql = "insert into t_external_articles(article_title,article_img,article_time,article_source,article_author,head_portrait,article_content,likes,last_sync_time,app_id) value(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "
            cursor.execute(sql, data)
            conn.commit()  # 提交数据
            print('数据提交完成')
    cursor.close()  # 关闭游标
    print('关闭游标')
    conn.close()  # 关闭连接
    print('关闭连接')


def qichetoutiao_main():
    """主函数"""
    for page in range(1, 51):
        # url = 'https://www.qctt.cn/channel_loadmore/0_1?_token=XzX4HesrTPWDvvupIr4rruMUhQF3C5SQCeHSoOUw&page={}&oldTime=2020-09-25+22%3A48%3A48'.format(page)
        url = 'https://www.qctt.cn/channel_loadmore/page={}'.format(page)
        print(url)
        article_id = req_html(url)
        article_response = req_detail(article_id)
        article_datas = par_data(article_response)
        store_data(article_datas)


if __name__ == '__main__':
    qichetoutiao_main()

    def main_time(h=12, m=0):
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
            laosiji_main()
            qicheren_main()
            qichetoutiao_main()
    main_time()






