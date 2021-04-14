



import requests
import jsonpath
import pymysql
import datetime
import time
from datetime import datetime

# 连接MySQL数据库
conn = pymysql.connect(host="112.126.89.134", user="jgcdb", password="jingche0000", port=3306, db="jgcproddb",charset="utf8")
# conn = pymysql.connect(host="localhost", user="root", password="", port=3306, db="jdbc", charset="utf8")
cursor = conn.cursor()  # 创建游标

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
    'Cookie': 'sogouPlatform=null; dubaReferer=null; LSJCITYOBJ=%7B%22code%22%3A131%2C%22name%22%3A%22%E5%8C%97%E4%BA%AC%22%7D; OdStatisticsToken=773395ed-2ca3-4008-a1b4-039ca619ec8e-1616029372305; LSJLOGCOOKIE=11911911946108971111151051061054699111109-16713825-1616029372434; UM_distinctid=17842db501928-01e35185defce4-5771031-144000-17842db501aacb; CNZZDATA1261736092=1884920661-1616027319-https%253A%252F%252Fwww.baidu.com%252F%7C1616027319; Hm_lvt_9fa8070d0f1a747dc1fd8cc5bdda4088=1616029373; _ga=GA1.2.1458876135.1616029440; _gid=GA1.2.663022414.1616029440; Hm_lpvt_9fa8070d0f1a747dc1fd8cc5bdda4088=1616030701; JSESSIONID=E040FD0C0CAE5103D743BA1B5BB5DAF1'
}



def get_data(url):
    for page in range(1,2):

        data = {
            'method': '/home/ywf/tablist',
            'tabid': '20',
            'page': page
        }


        response = requests.post(url=url,headers=headers,data=data).json()
        # print(response)

        # 封面图片
        cover_photo = jsonpath.jsonpath(response,'$..snslist.list..image.url')[0::3]
        # print(cover_photo)

        # 头像
        head_portrait = jsonpath.jsonpath(response,'$..snslist.list..image.url')[2::3]
        # print(head_portrait)

        # 标题
        title = jsonpath.jsonpath(response,'$..snslist.list..title')[::2]
        # print(title)

        # 作者
        letterAndName = jsonpath.jsonpath(response,'$..snslist.list..letterAndName')
        # print(letterAndName)

        # 时间
        create_time = datetime.now().strftime("%Y-%m-%d 23:35:23")
        # print(create_time)

        # 视频连接
        videourl = jsonpath.jsonpath(response,'$..snslist.list..videourl..bdinfo..url')
        # print(videourl)

        type = '20'

        for c,h,t,l,v in zip(cover_photo,head_portrait,title,letterAndName,videourl):
            data = (c,h,t,l,create_time,v,type)
            if t == '':
                continue
            print(data)
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
    url = 'https://www.laosiji.com/proxy/api'
    get_data(url)


if __name__ == '__main__':
    main()
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




