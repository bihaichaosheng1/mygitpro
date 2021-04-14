
import requests
import parsel
import pymysql
from xpinyin import Pinyin

"""
获得 汽车之家城市ip

"""

url = "https://buy.autohome.com.cn/210000/210400/selectcity.html?back=https%3A//buy.autohome.com.cn/210000/210400/car_614_34816_1.html%23pvareaid%3D2113201"

resp = requests.get(url=url)

html_data = parsel.Selector(resp.text)

dd_list = html_data.xpath('//div[@id="divCityList"]/dl')
for dd in dd_list:
    # 城市首字母
    city_initials = dd.xpath('./dt/span/text()').get()
    # print(city_initials)
    # 城市_cid
    city_id = dd.xpath('./dd/a/@data-cityid').getall()
    # print(city_id)
    # 城市名
    city_name = dd.xpath('./dd/a/text()').getall()
    # print(city_name)
    # p = Pinyin()
    # full_pin = []
    # for name in city_name:
    #     pin = p.get_pinyin(name,' ')
    #     full_pin.append(pin)

    for c_id,c_name,pin in zip(city_id,city_name):
        data = (city_initials,c_id,c_name,pin)
        print(data)
        # conn = pymysql.connect(host="112.126.89.134",user="jgcdb",password="jingche000",port=3306,db="jgcdb",charset="utf8")
        conn = pymysql.connect(host="localhost", user="root", password="", port=3306, db="jdbc", charset="utf8")
        cursor = conn.cursor()  # 创建游标
        # sql语句---xiaoshuo是表明，括号里面是字段，对应四个百分号
        sql2 = "select city_name from national_cities where city_name='{0}'".format(data[2])
        cursor.execute(sql2)
        many = cursor.fetchone()
        if many:
            print('此数据表中已存在')
        else:
            sql = "insert into national_cities(city_initials,city_id,city_name,full_pin) value(%s,%s,%s,%s)"
            cursor.execute(sql,data)
            conn.commit()   # 提交数据
            cursor.close()  # 关闭游标
            conn.close()    # 关闭连接

















