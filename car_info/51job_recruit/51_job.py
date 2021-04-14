# -*- coding:utf-8 -*-

import requests
import parsel
import json
import jsonpath
import pymysql
import xlwt
import re


"""
问题 未去除贝壳广告  已解决

将数据 进行可视化

"""

# 连接MySQL数据库
# conn = pymysql.connect(host="112.126.89.134", user="jgcdb", password="jgcdb123456", port=3306, db="jgcproddb",charset="utf8")
conn = pymysql.connect(host="localhost", user="root", password="", port=3306, db="jdbc", charset="utf8")
cursor = conn.cursor()  # 创建游标



for page in range(1,30):

    url = 'https://search.51job.com/list/230200,000000,0000,00,9,99,%25E6%25B1%25BD%25E8%25BD%25A6%25E9%2594%2580%25E5%2594%25AE,2,{}.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare='.format(page)
    res = requests.get(url)
    # print(res.text)
    resp = parsel.Selector(res.text)
    content = resp.xpath('//script[@type="text/javascript"][2]/text()').get()
    # print(type(content))  # <class 'str'>
    content_data = content.replace('window.__SEARCH_RESULT__ = ','')
    # print(content_data)

    # 将 字符串 转 json
    json_data = json.loads(content_data)
    # print(type(json_data))  # <class 'dict'>

    # 提取 数据
    # 公司名名称
    company_name = jsonpath.jsonpath(json_data, '$..company_name')
    # print(company_name)

    # 工作
    job_name = jsonpath.jsonpath(json_data,'$..job_name')
    # print(job_name)

    # 薪资
    providesalary = jsonpath.jsonpath(json_data,'$..providesalary_text')
    # print(providesalary)

    # 福利待遇
    jobwelf = jsonpath.jsonpath(json_data,'$..jobwelf')
    # print(jobwelf)

    # 要求
    attribute = jsonpath.jsonpath(json_data, '$..attribute_text')
    # print(attribute_text)

    for jname,cname,pro,jb,att in zip(job_name,company_name,providesalary,jobwelf,attribute):

        print('进入循环')
        # if '房地产'or '人寿' or '不动产' or '猎头' in cname:
        if '房地产'in cname:
            print(cname,'淘汰')
            continue
        if '人寿'in cname:
            print(cname,'淘汰')
            continue
        if '不动产'in cname:
            print(cname,'淘汰')
            continue
        if '猎头'in cname:
            print(cname,'淘汰')
            continue
        attr = ",".join(att)
        data = (jname,cname,pro,jb,attr)
        print(data)
        insert_sql = "insert into 51job_recruit(jobname,companyname,providesalary,jobwelf,attribute ) value (%s,%s,%s,%s,%s)"
        cursor.execute(insert_sql,data)
        conn.commit()
        print('数据提交完成')

cursor.close()
conn.close()
print('数据库已关闭')
