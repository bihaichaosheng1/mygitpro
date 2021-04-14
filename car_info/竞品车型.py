


import requests
import jsonpath
import json
import pymysql
from openpyxl import Workbook
wb = Workbook()
ws = wb.active
ws.append(['车型','竞品车型'])

# 连接MySQL数据库
conn = pymysql.connect(host="112.126.89.134", user="jgcdb", password="jingche0000", port=3306, db="jgcproddb",charset="utf8")
# conn = pymysql.connect(host="localhost", user="root", password="", port=3306, db="jdbc", charset="utf8")
cursor = conn.cursor()  # 创建游标

while 1:
    print('+++++++++++++++++++++++++++++++++++')
    try:
        try:
            brand_name = input('请输入要查询的品牌：')
            brand_sql = f"select brand_id from t_car_brand where brand_name = '{brand_name}'"
            cursor.execute(brand_sql)
            brand_id = cursor.fetchone()[0]
            sql = f"select series_id,category_fullname from t_car_category where sale_type = '在售' and car_brand_id = '{brand_id}'"
            cursor.execute(sql)
            series_idlist = cursor.fetchall()  # 得到车系id数据
            for id in series_idlist:
                sid = id[0]
                sname = id[1]
                url = 'https://data.autohome.com.cn/rcm/RelativeRecommend/common?uid=0&datatype=1&appid=0&source=pc&sessionid=E3225414-EC36-4FF8-A653-29E2571ABDE4&seriesid={}&seriesnum=6'.format(sid)
                print('_______________________________')
                resp = requests.get(url).text
                # print(url)
                resp = resp.replace('cainixihuan(','').replace('})','}')
                resp_dict = json.loads(resp)
                # 车系名称
                seriesname = jsonpath.jsonpath(resp_dict,'$..seriesname')
                # print(seriesname)
                # 车系id
                seriesid = jsonpath.jsonpath(resp_dict,'$..seriesid')
                # print(seriesid)
                for name,id in zip(seriesname,seriesid):
                    print(sname,name)
                    line = [sname,name]
                    ws.append(line)
                path = r'C:\Users\Public\Documents\{}.xlsx'.format(brand_name)
                wb.save(path)
            print('下载完成：文件保存在' + r'C:\Users\Public\Documents\{}.xlsx'.format(brand_name))
        except TypeError:

            series_name = input('请输入汽车厂商：')
            series_sql = f"select brand_id from t_car_brand_all where brand_name like '%{series_name}%'"
            cursor.execute(series_sql)
            car_series_id = cursor.fetchone()[0]
            print(car_series_id)
            sql = f"select series_id,category_fullname from t_car_category where sale_type = '在售' and car_series_id = '{car_series_id}'"
            cursor.execute(sql)
            series_idlist = cursor.fetchall()  # 得到车系id数据
            for id in series_idlist:
                sid = id[0]
                sname = id[1]
                url = 'https://data.autohome.com.cn/rcm/RelativeRecommend/common?uid=0&datatype=1&appid=0&source=pc&sessionid=E3225414-EC36-4FF8-A653-29E2571ABDE4&seriesid={}&seriesnum=6'.format(
                    sid)
                print('_______________________________')
                resp = requests.get(url).text
                # print(url)
                resp = resp.replace('cainixihuan(', '').replace('})', '}')
                resp_dict = json.loads(resp)
                # 车系名称
                seriesname = jsonpath.jsonpath(resp_dict, '$..seriesname')
                # print(seriesname)
                # 车系id
                seriesid = jsonpath.jsonpath(resp_dict, '$..seriesid')
                # print(seriesid)
                for name, id in zip(seriesname, seriesid):
                    print(sname, name)
                    line = [sname, name]
                    ws.append(line)
                path = r'C:\Users\Public\Documents\{}.xlsx'.format(series_name)
                wb.save(path)
            print('下载完成：文件保存在'+r'C:\Users\Public\Documents\{}.xlsx'.format(series_name))
    except TypeError:
        print('输入错误请重新输入，是否类似 “一汽-大众” 要加 “-” ！！！')




