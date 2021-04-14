

"""
爬取梨视频
"""
import requests
import parsel
import jsonpath
import datetime
import pymysql

# 连接MySQL数据库
conn = pymysql.connect(host="112.126.89.134", user="jgcdb", password="jingche0000", port=3306, db="jgcproddb",charset="utf8")
# conn = pymysql.connect(host="localhost", user="root", password="", port=3306, db="jdbc", charset="utf8")
cursor = conn.cursor()  # 创建游标


# 解决ssl警告
requests.packages.urllib3.disable_warnings()

for num in range(300):
    if (num % 12) == 0:

        url = "https://www.pearvideo.com/category_loading.jsp?reqType=5&categoryId=31&start={}&mrd=0.9997950571058631".format(num)

        """
        108
        120
        132
        相差 12 
        """
        one_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
            'Referer':'https://www.pearvideo.com/category_31'
        }

        response = requests.get(url,headers=one_headers,verify=False).text
        # print(response)
        # 转为计算机识别
        resp_html = parsel.Selector(response)
        # 解析数据 获得li_list
        li_list = resp_html.xpath('//body/li')
        # print(li_list)

        for li in li_list:
            detail_link = 'https://www.pearvideo.com/'+li.xpath('.//a/@href').get()
            # print(detail_link)

            # 请求详情页
            detail_page_data = requests.get(detail_link,verify=False).text
            detail_data = parsel.Selector(detail_page_data)

            contID = detail_link.split('_')[1]

            video_date = f'https://www.pearvideo.com/videoStatus.jsp?contId={contID}&mrd=0.7890920916276076'

            two_headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
                'Referer': detail_link  # 防盗链：溯源当前请求的链接地址的上一级url，
            }

            # 请求视频链接,获得响应
            video_response = requests.get(video_date, headers=two_headers, verify=False).json()
            # print(video_response)

            # 解析数据，拿到视频原始链接
            srcUrl = jsonpath.jsonpath(video_response, '$..srcUrl')[0]
            # print(srcUrl)

            # 获得随机参数
            systemTime = jsonpath.jsonpath(video_response, '$..systemTime')[0]
            # print(systemTime)

            # 修正视频链接
            video_link = srcUrl.replace(systemTime, f'cont-{contID}')
            # print(video_link)

            # 头像
            publisher_head = detail_data.xpath('//div[@class="col-name"]/i/img/@src').get()
            # print(publisher_head)

            # 标题
            title = detail_data.xpath('//div[@class="box-left clear-mar"]/h1/text()').get()
            # print(title)

            # 视频封面
            cover_photo = jsonpath.jsonpath(video_response, '$..video_image')[0]
            # print(cover_photo)

            # 作者
            publisher = detail_data.xpath('//div[@class="col-name"]/i/img/@alt').get()
            # print(publisher)

            # 时间
            create_time = datetime.datetime.now().strftime("%Y-%m-%d 23:35:23")

            # 类别
            type = '60'

            data = (video_link, title, cover_photo, publisher_head, publisher, create_time, type)

            print(data)
            sql = "select * from t_car_video where video_link='{}' and title='{}'".format(data[0], data[1])
            cursor.execute(sql)
            many = cursor.fetchone()
            if many:
                print('此数据表中已存在')
            else:
                insert_sql = 'insert into t_car_video(video_link,title,cover_map,publisher_head,publisher,create_time,type)values (%s,%s,%s,%s,%s,%s,%s)'
                cursor.execute(insert_sql, data)
                conn.commit()  # 提交数据
                print('数据提交完成')

cursor.close()  # 关闭游标
print('关闭游标')
conn.close()  # 关闭连接
print('关闭连接')


