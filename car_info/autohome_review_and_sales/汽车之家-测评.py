# -*- coding:utf-8 -*-

import requests
import parsel
import pymysql





headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    'cookie': 'fvlid=1607490165095Jnd7Civ56e; sessionid=84C90528-375C-4E5B-BE53-11FC8F8B79B7%7C%7C2020-12-09+13%3A02%3A46.351%7C%7Cwww.baidu.com; autoid=c5f53b6ad00463b5b46ddb685e9bd33e; ahpau=1; __ah_uuid_ng=c_84C90528-375C-4E5B-BE53-11FC8F8B79B7; sessionuid=84C90528-375C-4E5B-BE53-11FC8F8B79B7%7C%7C2020-12-09+13%3A02%3A46.351%7C%7Cwww.baidu.com; _oname_v2=%E5%88%98%E5%85%88%E7%94%9F; _ophone_v2=18512439986; ASP.NET_SessionId=jqcme52aqqwry0wsxhuajs5s; Hm_lvt_9924a05a5a75caf05dbbfb51af638b07=1607490524,1608520555,1608617365; __utma=1.1759152834.1609215025.1609215025.1609215025.1; __utmc=1; __utmz=1.1609215025.1.1.utmcsr=autohome.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/; ahsids=65_692_121_5979_5999_4683; FootPrints=42882%7C2021-1-3%2C45297%7C2021-1-3%2C44994%7C2021-1-1%2C45050%7C2020-12-31%2C47956%7C2020-12-31%2C43097%7C2020-12-31%2C44086%7C2020-12-31%2C37352%7C2020-12-31%2C43461%7C2020-12-31%2C42502%7C2020-12-31%2C38557%7C2020-12-31%2C1009036%7C2020-12-28%2C1005332%7C2020-12-28%2C46747%7C2020-12-28%2C49184%7C2020-12-26%2C45048%7C2020-12-26%2C; cityId=615; cookieCityId=640100; Hm_lpvt_9924a05a5a75caf05dbbfb51af638b07=1609737579; area=210114; sessionip=223.101.43.228; sessionvid=27620697-6F3D-42B6-9F72-34E81FBB98ED; ahpvno=11; v_no=6; visit_info_ad=84C90528-375C-4E5B-BE53-11FC8F8B79B7||27620697-6F3D-42B6-9F72-34E81FBB98ED||-1||-1||6; ref=www.baidu.com%7C0%7C0%7C0%7C2021-01-07+21%3A18%3A25.608%7C2020-12-09+13%3A02%3A46.351; ahrlid=1610025501628i6bRDSMZnw-1610025729070'
}


data_list = []

def get_html(url):

        resp = requests.get(url,headers=headers)
        resp.encoding = 'gbk'
        response = parsel.Selector(resp.text)
        # print(response)  # <Selector xpath=None data='<html>\r\n<head>\r\n    <meta charset="gb231'>

        div_list = response.xpath('//div[@id="bestautocontent"]/div[@class="row"][position()>4]')
        # print(div_list)
        for div in div_list:
            try:
                # 车型id
                spec_id = div.xpath('.//div[@class="uibox-title uibox-title-border"]/a/@href').get().replace('/spec/','').replace('/', '')
                # print(spec_id)

                # 车型名称
                print(url)
                spec_name = div.xpath('.//div[@class="uibox-title uibox-title-border"]/a/text()').get()
                # print(spec_name)



                """评价"""

                # 评价时间
                evaluator_time = div.xpath('.//div[@class="tit"]/span[@class="mrleft"]/text()').get()
                # print(evaluator_time)

                dd_list = div.xpath('.//div[@class="tabbox2 tabbox-score"]/dl/dd')
                for dd in dd_list:

                    # print(url)
                    # 评价人
                    evaluator = dd.xpath('.//div[@class="dd-div1"]/a/text()|.//div[@class="dd-div1"]/span/text()').get()
                    if evaluator == None:
                        evaluator = '单杜诗'
                    # print(evaluator)

                    # 评价内容
                    evaluator_content = ''.join(dd.xpath('.//div[@class="dd-div3"]/div/text()').get().replace('\r\n','').split())
                    # print(evaluator_content)

                    data = (spec_id,spec_name,evaluator,evaluator_content,evaluator_time)
                    data_list.append(data)
                    # print(data)
            except AttributeError:
                continue

def data_storage():
    # 连接MySQL数据库
    conn = pymysql.connect(host="112.126.89.134", user="jgcdb", password="jingche0000", port=3306, db="jgcproddb",charset="utf8")
    # conn = pymysql.connect(host="localhost", user="root", password="", port=3306, db="jdbc", charset="utf8")
    cursor = conn.cursor()  # 创建游标
    for datas in data_list:
        data = datas
        insert_sql = 'insert into t_car_detail_city_evaluate(spec_id,spec_name,evaluator,evaluator_content,evaluator_time)values (%s,%s,%s,%s,%s)'
        cursor.execute(insert_sql, data)
        conn.commit()  # 提交数据
        print('数据提交完成')
    cursor.close()  # 关闭游标
    print('关闭游标')
    conn.close()  # 关闭连接
    print('关闭连接')


def main():
    for page in range(1,177):
        url = 'https://www.autohome.com.cn/bestauto/{}'.format(page)
        get_html(url)
    data_storage()

if __name__ == '__main__':
    main()


















