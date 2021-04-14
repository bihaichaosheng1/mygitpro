

from requests.adapters import HTTPAdapter
import pinyin
import parsel
import datetime
import requests
import pymysql
import concurrent.futures



"""
汽车之家品牌数据

"""

conn = pymysql.connect(host="112.126.89.134", user="jgcdb", password="jingche0000", port=3306, db="jgcproddb",charset="utf8")
# conn = pymysql.connect(host="localhost", user="root", password="", port=3306, db="jdbc", charset="utf8")
cursor = conn.cursor()  # 创建游标

# url = "https://www.autohome.com.cn/car/"
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
        'Connection': 'close'
    }
# 解决最大重连次数
res = requests.session()
res.mount('https://', HTTPAdapter(max_retries=8))

def re_url(url):
    # 请求函数
    resp = res.get(url,headers=headers)
    return resp

def parse_data(resp):
    # 解析函数
    respdata = parsel.Selector(resp.text)

    # 品牌id
    brand_id = []
    brand_id_list = respdata.xpath('//ul/li/@id').getall()
    for id in brand_id_list:
        id = id.replace('b','')
        brand_id.append(id)


    # 品牌名称
    brand_name = respdata.xpath('//ul/li/h3/a/text()').getall()


    # 品牌首字母
    brand_ini = []
    for i in brand_name:
        if i == '上��':
            i = '上喆'
        da = pinyin.get_initial(i, delimiter="").upper()
        da2 = da[0:1]
        brand_ini.append(da2)

    # 品牌logo
    brand_logo = []
    logo_link = respdata.xpath('//ul/li/h3/a/@href').getall()
    for link in logo_link:
        # 拼接logo所在的url
        logo_url = 'https://car.autohome.com.cn' + link
        brand_logo_data = res.get(logo_url)
        logo_data = parsel.Selector(brand_logo_data.text)
        logo = 'https:'+logo_data.xpath('//div[@class="uibox-con contbox"]/div[@class="carbrand"]/div[@class="carbradn-pic"]/img/@src').get()
        brand_logo.append(logo)
    print('品牌logo',brand_logo)

    # 最后更新时间
    last_sync_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print('更新时间',last_sync_time)
    return brand_id,brand_ini,brand_name,brand_logo,last_sync_time

def store_data(brand_data):
    # 存储函数
    brand_id = brand_data[0]
    brand_ini = brand_data[1]
    brand_name = brand_data[2]
    brand_logo = brand_data[3]
    last_sync_time = brand_data[4]
    for b_id,b_i,b_name,b_l in zip(brand_id,brand_ini,brand_name,brand_logo):
        data = (b_id,b_i,b_name,b_l,last_sync_time)
        print(data)
        print(data[2])
        sql2 = "select brand_name from t_car_brand where brand_id='{0}'".format(data[0])
        cursor.execute(sql2)
        many = cursor.fetchone()
        if many:
            print('此数据表中已存在')
            sql = "UPDATE  t_car_brand SET brand_initial='{}',brand_name='{}',brand_logo='{}',last_sync_time='{}' WHERE brand_id='{}'".format(data[1],data[2],data[3],data[4],data[0])
            cursor.execute(sql)
            conn.commit()   # 提交数据
            print('数据已提交')
        else:
            sql = "insert into t_car_brand(brand_id,brand_initial,brand_name,brand_logo,last_sync_time) value(%s,%s,%s,%s,%s)"
            cursor.execute(sql,data)
    cursor.close()  # 关闭游标
    conn.close()    # 关闭连接

def main():
    # 主函数
    url = "https://car.autohome.com.cn/AsLeftMenu/As_LeftListNew.ashx?typeId=1%20&brandId"
    # 创建线程池
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=6)  # 最大线程等于6
    respdata = re_url(url)
    executor.submit(parse_data(respdata))
    # brand_data = parse_data(respdata)
    executor.submit(store_data(parse_data(respdata)))
    # store_data(brand_data)
    # 待所有线程结束后关闭线程池
    executor.shutdown()

if __name__ == '__main__':
    main()









# proxies = {  # 代理ip
#     "http://": "221.122.91.61:9400"
# }
#
#
#
# resp = requests.get(url=url,headers=headers,proxies=proxies)
# # html = str(resp_data, encoding="unicode_escape")
# # html.Unicode='gb2312'
# # html_data = parsel.Selector(html)
# # 获取品牌首字母
# resp_data = parsel.Selector(resp.text)
# div_list = resp_data.xpath('//div[@id="tab-content"]/div[@id="tab-content-item2"]/div[@class="find fn-clear"]')
#
# for li in div_list:
#     # print(li)
#     # 提取品牌id
#     brand_id = li.xpath('./div[@class="clear brand-series"]/dl[@class="clearfix brand-series__item"]/dd/a/@vos').getall()
#     print('这是品牌id',brand_id)
#     # 品牌名称
#     brand_names = []
#     brand_name = li.xpath('./div[@class="clear brand-series"]/dl[@class="clearfix brand-series__item"]/dd/a/@cname').getall()  # 品牌名称
#     print('这是品牌名称',brand_name)
#     # 提取品牌首字母
#     brand_ini = []
#     for i in brand_name:
#         if i == '上��':
#             i = '上喆'
#         brand_names.append(i)
#         da = pinyin.get_initial(i, delimiter="").upper()
#         da2 = da[0:1]
#         brand_ini.append(da2)
#     print('这是首字母',brand_ini)
#     # 品牌logo
#     brand_logo = []
#     brand_logo_link = li.xpath('./div[@class="clear brand-series"]/dl[@class="clearfix brand-series__item"]/dd/a/em/img/@src').getall()  # 品牌logo
#     for i in brand_logo_link:
#         logo = 'https:'+ i
#         brand_logo.append(logo)
#     print(brand_logo)
#     # 获取当前时间
#     dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     print('最后一次更新时间',dt)
#
#
#     for b_id,b_i,b_name,b_l in zip(brand_id,brand_ini,brand_names,brand_logo):
#         data = (b_id,b_i,b_name,b_l,dt)
#         print(data)
#         print(data[2])
#         sql2 = "select brand_name from t_car_brand where brand_name='{0}'".format(data[2])
#         cursor.execute(sql2)
#         many = cursor.fetchone()
#         if many:
#             print('此数据表中已存在')
#         else:
#             # sql语句---xiaoshuo是表明，括号里面是字段，对应四个百分号
#             sql = "insert into t_car_brand(brand_id,brand_initial,brand_name,brand_logo,last_sync_time) value(%s,%s,%s,%s,%s)"
#             cursor.execute(sql,data)
#             conn.commit()   # 提交数据
#             print('数据已提交')
# cursor.close()  # 关闭游标
# conn.close()    # 关闭连接



