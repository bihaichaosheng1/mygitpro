import requests
import parsel
from requests.adapters import HTTPAdapter
import concurrent.futures  # 线程模块  通过这个模块可以创建出一个线程池
import pymysql
import time
import re
import datetime
import jsonpath
import json
import urllib3
urllib3.disable_warnings()

"""连接MySQL数据库"""
conn = pymysql.connect(host="112.126.89.134", user="jgcdb", password="jingche0000", port=3306, db="jgcproddb",charset="utf8")
# conn = pymysql.connect(host="localhost", user="root", password="", port=3306, db="jdbc", charset="utf8")
cursor = conn.cursor()  # 创建游标


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
    'Connection':'close'
}

requests.adapters.DEFAULT_RETRIES = 6
s = requests.session()
s.mount('https://', HTTPAdapter(max_retries=60))

def get_html(url):
    """发起请求"""
    resp_html = s.get(url=url,headers=headers,timeout=(30,60),verify=False)
    if resp_html.status_code == 200:
        print("===========程序走到了请求函数============")
        return resp_html

def analysis(resp_html):
    """汽车之家车型数据解析"""
    resp_data = parsel.Selector(resp_html.text)
    """车系连接"""   #  /price/series-145.html
    series_url = resp_data.xpath('//li[@class="current"]/dl/dd/a/@href').getall()

    """车系状态"""
    # sale_type = resp_data.xpath('//li[@class="current"]/dl/dd/a/em/text()').getall()
    # print(sale_type)
    # print(series_url)

    """
    根据车系连接  发起请求 得到详情响应 获得字段数据，不同页面的
    """
    for i in series_url:
        """详情连接、拼接url"""
        series_size_link = 'https://car.autohome.com.cn' + i

        """对车系详情发起请求"""
        ret_detail = s.get(url=series_size_link, headers=headers, timeout=(30,70),verify=False)
        series_data = parsel.Selector(ret_detail.text)
        print("===========程序走到了解析函数============")
        print(series_size_link)
        """车系id"""
        series_id = "".join(re.findall('\d+/',str(series_data.xpath('//div[@class="list-cont-main"]/div[@class="main-title"]//a/@href').get()))).replace('/','')
        if series_id == None:
            continue
        # print(series_id)

        """车系状态"""
        time.sleep(0.5)
        on_link = 'https://car.autohome.com.cn/price/series-{}-0-1-0-0-0-0-1.html'.format(series_id)

        print(on_link)
        on_spec = s.get(on_link,headers=headers,verify=False)
        on_spec_data = parsel.Selector(on_spec.text)
        sale_type = on_spec_data.xpath(
            '//div[@class="tab-nav border-t-no"]/ul[@data-trigger="click"]/li[@class="current"]/a/text()').get()
        # print(sale_type)

        """车系名称"""
        category_fullname = series_data.xpath('//div[@class="list-cont-main"]/div[@class="main-title"]/a/text()').get()
        # print(category_fullname)

        """车系logo"""

        category_spec_id =  series_data.xpath('//ul[@class="interval01-list"]/li/@data-value').get()
        # print(category_spec_id)
        logo_url = 'https://j.api.autohome.com.cn/api/item/getSolutionBySpecId?specId={}&cityId=210100&_appid=cms&callback=callBack'.format(category_spec_id)
        logo_url_two = 'https://songshuopen.autohome.com.cn/adfront/v1/_mget?clientIp=127.0.0.1&callback=jQuery172046023604672150675_1604285238533&appKey=autohome.com.cn&advId=100248&systemType=2&B7E022A6-8421-4E7E-AC1E-6A077BA471E1&cityId=210100&ProvinceId=210000&specId={}'.format(category_spec_id)
        logo_json = s.get(logo_url,headers=headers, timeout=(30,70),verify=False)
        logo_json_data = logo_json.text.replace('callBack(','').replace(')','')
        # print(logo_json_data)
        logo_json_data = json.loads(logo_json_data)
        # time.sleep(1)
        category_logo = ''
        try:
            category_logo = "".join(jsonpath.jsonpath(logo_json_data,'$..minDownpayIp.picUrl'))

            if category_logo == None:
                category_logo = '暂无'
            if category_logo == False:
                logo_json = s.get(logo_url_two, headers=headers, timeout=(30, 70),verify=False)
                logo_json_datas = logo_json.text.replace('jQuery172046023604672150675_1604285238533(', '').replace(')', '')
                # print(logo_json_datas)
                logo_json_data = json.loads(logo_json_datas)
                category_logo_html = ''.join(jsonpath.jsonpath(logo_json_data, '$..content'))
                # print(category_logo_html)
                content_data = parsel.Selector(category_logo_html)
                category_logo = content_data.xpath('//img/@src').get()
            # print('图片：', category_logo)

        except TypeError:
            pass


        """品牌id"""
        car_brand_id = ''.join(re.findall('\d+',str(series_data.xpath('//div[@class="column grid-16"]/div[@class="breadnav"]/a[3]/@href').get())))
        # print(car_brand_id)

        """车系等级"""
        size_type = series_data.xpath('//div[@class="main-lever-left"]/ul[@class="lever-ul"]/li[1]/span/text()').get()
        # print(size_type)

        """价格"""
        car_price = series_data.xpath('//div[@class="main-lever-right"]/div/span[@class="lever-price red"]/span/text()').get()


        """隶属产商"""
        car_series = series_data.xpath('//div[@class="column grid-16"]/div[@class="breadnav"]/a[4]/text()').get()
        # print(car_series)

        """产商id（"""
        car_series_id = '100' + ''.join(re.findall('\d+',str(series_data.xpath('//div[@class="column grid-16"]/div[@class="breadnav"]/a[4]/@href').get())))
        print('产商id', car_series_id)

        """最后一次更新时间"""
        last_sync_time = datetime.datetime.now().strftime("%Y-%m-28 23:35:23")
        # print(last_sync_time)

        yield series_id,category_fullname,sale_type,category_logo,car_brand_id,size_type,car_price,car_series,car_series_id,last_sync_time


def data_storage(details):
    """数据存储"""
    for detail in details:
        data = (detail)
        print(data)
    #     # sql = "select * from t_car_category where series_id='{}' and sale_type='{}' and last_sync_time='{}'".format(data[0],data[2],data[8])
    #     sql = "select * from t_car_category where series_id='{}'".format(data[0])
    #     cursor.execute(sql)
    #     many = cursor.fetchone()
    #     print('many',many)  # None
    #     if many:
    #         sql2 = "UPDATE t_car_category SET sale_type='{}',last_sync_time='{}' WHERE series_id='{}'".format(data[2],data[8],data[0])
    #         print(sql2)
    #         cursor.execute(sql2)
    #         conn.commit()  # 提交数据
    #         print('数据已更新')
    #     elif many == None:
    #         sql3 = "insert into t_car_category(series_id,category_fullname,sale_type,category_logo,car_brand_id,size_type,car_price,car_series,last_sync_time) value (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    #         print(sql3)
    #         # sql = "insert into t_car_category(series_id,category_fullname,sale_type,category_logo,car_brand_id,size_type,car_price,car_series,last_sync_time) value(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    #         cursor.execute(sql3,data)
    #         conn.commit()  # 提交数据
    #         print('数据提交完成')

        # sql = "select * from t_car_category where series_id='{}' and sale_type='{}' and last_sync_time='{}'".format(data[0],data[2],data[8])
        """添加厂商id"""
        sql = "select * from t_car_category where series_id='{}'".format(data[0])
        cursor.execute(sql)
        many = cursor.fetchone()
        print('many',many)  # None
        if many:
            pass
            sql2 = "UPDATE t_car_category SET sale_type='{}' WHERE series_id='{}'".format(data[2],data[0])
            print(sql2)
            cursor.execute(sql2)
            conn.commit()  # 提交数据
            print('数据已更新')
        elif many == None:
            sql3 = "insert into t_car_category(series_id,category_fullname,sale_type,category_logo,car_brand_id,size_type,car_price,car_series,car_series_id,last_sync_time) value (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            print(sql3)
            # sql = "insert into t_car_category(series_id,category_fullname,sale_type,category_logo,car_brand_id,size_type,car_price,car_series,last_sync_time) value(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql3,data)
            conn.commit()  # 提交数据
            print('数据提交完成')



def main(brand_ids):
    """主函数"""
    # for i in range(1,2):
    # 创建多线程
    thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=6)  # 最大线程等于6
    for brand_id in brand_ids:
        url = 'https://car.autohome.com.cn/AsLeftMenu/As_LeftListNew.ashx?typeId=1%20&brandId={}'.format(brand_id)

        get_data = get_html(url)
        thread_pool.submit(get_html,url)  # 将发起请求函数，添加到线程

        # analysis_data = analysis(get_data)
        thread_pool.submit(analysis,get_html(url))  # 将解析数据函数，添加到线程

        thread_pool.submit(data_storage(analysis(get_html(url))))

    thread_pool.shutdown()  # 待所有线程结束后关闭线程池



if __name__ == '__main__':
    start = time.time()
    """从数据库读取出品牌id"""
    sql = "select brand_id from t_car_brand"
    cursor.execute(sql)
    brand_id = cursor.fetchall()  # 得到品牌id数据
    brand_ids = []
    for id in brand_id:
        brand_ids.append(id[0])
    print(brand_ids)
    # brand_ids = [33]

    main(brand_ids)

    print('关闭游标')
    cursor.close()  # 关闭游标
    print('关闭连接')
    conn.close()  # 关闭连接

    print('总耗时：%f' % float(time.time() - start))

    # """定时程序"""
    # def doSth():
    #     start = time.time()
    #     """从数据库读取出品牌id"""
    #     sql = "select brand_id from t_car_brand"
    #     cursor.execute(sql)
    #     brand_id = cursor.fetchall()  # 得到品牌id数据
    #     brand_ids = []
    #     for id in brand_id:
    #         brand_ids.append(id[0])
    #
    #     main(brand_ids)
    #     cursor.close()  # 关闭游标
    #     print('关闭游标')
    #     conn.close()  # 关闭连接
    #     print('关闭连接')
    #     print('总耗时：%.5f秒' % float(time.time() - start))
    #
    # def main_o(h=12,m=0):
    #     while True:
    #         # 判断是否达到设定时间，例如0:00
    #         while True:
    #             now_time = datetime.datetime.now()
    #             print(now_time.hour, now_time.minute)
    #             # 到达设定时间，结束内循环
    #             if now_time.hour == h and now_time.minute == m:
    #                 break
    #             # 不到时间就等60秒之后再次检测
    #             time.sleep(60)
    #             # 做正事，一天做一次
    #         doSth()
    # main_o()






























