import requests
import parsel
from requests.adapters import HTTPAdapter
import concurrent.futures  # 线程模块  通过这个模块可以创建出一个线程池
import pymysql
import time
import re
import datetime



"""连接MySQL数据库"""
# conn = pymysql.connect(host="112.126.89.134", user="jgcdb", password="jgcdb123456", port=3306, db="jgcdb",charset="utf8")
conn = pymysql.connect(host="localhost", user="root", password="", port=3306, db="jdbc", charset="utf8")
curso = conn.cursor()  # 创建游标


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
    'Connection':'close'
}
# proxies = {  # 代理ip
#     "https": "https://221.122.91.61:9400",
#     # 'https':'https://134.209.13.16:8080'
# }
requests.adapters.DEFAULT_RETRIES = 6
s = requests.session()
s.mount('https://', HTTPAdapter(max_retries=20))
s.mount('http://', HTTPAdapter(max_retries=3))

def get_html(url):
    """发起请求"""
    resp_html = s.get(url=url,headers=headers,timeout=(30,60))
    if resp_html.status_code == 200:
        print("===========程序走到了请求函数============")
        return resp_html

def analysis(resp_html):
    """汽车之家车型数据解析"""
    resp_data = parsel.Selector(resp_html.text)
    """车系连接"""   #  /price/series-145.html
    # series_url = resp_data.xpath('//li[@class="current"]/dl/dd/a/@href').getall()
    series_url = resp_data.xpath('//li[@class="current"]/dl/dt/a/@href').getall()

    for i in series_url:
        """详情连接、拼接url"""
        series_size_link = 'https://car.autohome.com.cn' + i
        print(series_size_link)

        """对车系详情发起请求"""
        ret_detail = s.get(url=series_size_link, headers=headers, timeout=(30,70))
        series_data = parsel.Selector(ret_detail.text)
        print("===========程序走到了解析函数============")
        print(series_size_link)


        """品牌id"""
        # brand_id = ''.join(re.findall('\d+',str(series_data.xpath('//div[@class="column grid-16"]/div[@class="breadnav"]/a[3]/@href').get())))
        brand_id = ''.join(re.findall('\d+',str(series_data.xpath('//div[@class="column grid-16"]/div[@class="breadnav"]/a[3]/@href').get())))
        print('品牌id',brand_id)

        """产商id"""
        # contractor_idl = series_data.xpath('//div[@class="column grid-16"]/div[@class="breadnav"]/a[4]/@href').get()
        contractor_idl = series_data.xpath('//div[@class="cartab-title"]/h2[@class="fn-left cartab-title-name"]/a/@href').get()
        contractor_id = re.findall(r'\d+', contractor_idl)[-1]
        print('产商id',contractor_id)
        # print(contractor_idl)

        """产商名称"""
        # contractor_name = series_data.xpath('//div[@class="column grid-16"]/div[@class="breadnav"]/a[4]/text()').get()
        contractor_name = series_data.xpath('//div[@class="cartab-title"]/h2[@class="fn-left cartab-title-name"]/a/text()').get()
        print('产商名称',contractor_name)

        """最后一次更新时间"""
        last_sync_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(last_sync_time)

        yield contractor_id,contractor_name,brand_id,last_sync_time


def data_storage(details):
    """数据存储"""
    for detail in details:
        print(detail)
        data = (detail)
        # sql2 = "select series_id from t_car_category where series_id='{0}'".format(data[0])
        # curso.execute(sql2)
        # many = curso.fetchone()
        # if many:
        #     print('此数据表中已存在')
        # else:
        sql = "replace into t_car_contractor(contractor_id,contractor_name,brand_id,last_sync_time) value(%s,%s,%s,%s)"
        curso.execute(sql,data)
        conn.commit()  # 提交数据
        print('数据提交完成')



def main(brand_ids):
    """主函数"""
    # for i in range(1,2):
    # 创建多线程
    thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=12)  # 最大线程等于6
    for brand_id in brand_ids:
        url = 'https://car.autohome.com.cn/AsLeftMenu/As_LeftListNew.ashx?typeId=1%20&brandId={}'.format(brand_id)

        # get_data = get_html(url)
        thread_pool.submit(get_html,args=url)  # 将发起请求函数，添加到线程

        # analysis_data = analysis(get_data)
        # analysis(get_data)
        thread_pool.submit(analysis,args=get_html(url))  # 将解析数据函数，添加到线程

        data_storage(analysis(get_html(url)))
        # thread_pool.submit(data_storage, args=analysis(get_html(url)))  # 将存储数据函数，添加到线程

    thread_pool.shutdown()  # 待所有线程结束后关闭线程池

if __name__ == '__main__':
    start = time.time()
    """从数据库读取出品牌id"""
    sql = "select brand_id from t_car_brand"
    curso.execute(sql)
    brand_id = curso.fetchall()  # 得到品牌id数据
    brand_ids = []
    for id in brand_id:
        brand_ids.append(id[0])
    # print(brand_ids)
    main(brand_ids)

    print('关闭游标')
    curso.close()  # 关闭游标
    print('关闭数据库连接')
    conn.close()  # 关闭连接

    print('总耗时：%.5f秒' % float(time.time() - start))