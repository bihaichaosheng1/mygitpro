

import requests
import jsonpath
import json
import parsel
import time
import datetime
import pymysql


# 连接MySQL数据库
conn = pymysql.connect(host="112.126.89.134", user="jgcdb", password="jingche0000", port=3306, db="jgcproddb",charset="utf8")
# conn = pymysql.connect(host="localhost", user="root", password="", port=3306, db="jdbc", charset="utf8")
cursor = conn.cursor()  # 创建游标


headers = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
    'referer':'https://www.qctt.cn/home/video'
}

def get_data(url):
    print('链接',url)
    response = requests.get(url,headers=headers).text
    resp_json = json.loads(response)
    # print(response)
    video_id = jsonpath.jsonpath(resp_json,'$..id')
    # print(video_id)


    """
    拼接视频链接 https://www.qctt.cn/video/ + 'video_id'
    """
    # 请求视频链接
    for vid in video_id:
        detail_link = 'https://www.qctt.cn/video/' + vid
        # print(detail_link)
        time.sleep(0.7)
        detail_resp = requests.get(detail_link,headers=headers).text
        video_data = parsel.Selector(detail_resp)
        # 封面图片
        cover_map = video_data.xpath('//*[@id="video"]/@poster').get()
        # print(cover_map)

        # 头像
        publisher_head = video_data.xpath('//img[@class="avatar"]/@src').get()
        # print('头像',publisher_head)

        # 标题
        title = video_data.xpath('//div[@class="content-top"]/div[@class="title"]/text()').get()
        print(title)

        # 作者
        publisher = video_data.xpath('//div[@class="inlineStyle"]/a/text()').get()
        # print(publisher)

        # 时间
        create_time = datetime.datetime.now().strftime("%Y-%m-%d 23:35:23")

        # 视频链接
        video_link = video_data.xpath('//*[@id="video"]/@src').get()
        # print(video_link)

        type = '40'

        data = (cover_map,publisher_head,title,publisher,create_time,video_link,type)

        sql = "select * from t_car_video where cover_map='{}'and publisher_head='{}'and title ='{}' and publisher='{}'".format(data[0], data[1], data[2], data[3])
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
    for page in range(1,21):
        print(f'正在爬取第{page}页数据')
        url = f'https://www.qctt.cn/videoMore?page={page}&oldTime=2021-04-07+09%3A33%3A54'
        get_data(url)

    cursor.close()  # 关闭游标
    print('关闭游标')
    conn.close()  # 关闭连接
    print('关闭连接')

if __name__ == '__main__':
    main()