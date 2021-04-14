
import requests
import jsonpath
import parsel
import pymysql
import aiohttp  #导入异步模块
import asyncio
import datetime
import time


# url = 'https://dealer.autohome.com.cn/DealerList/GetAreasAjax?provinceId=0&cityId=210100&brandid=0&manufactoryid=0&seriesid=0&isSales=0'
#
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
# }
#
# response = requests.get(headers=headers,url=url).json()
# city_pinyin = jsonpath.jsonpath(response,'$..Pinyin')
# print(city_pinyin)
# 连接MySQL数据库
conn = pymysql.connect(host="112.126.89.134", user="jgcdb", password="jingche0000", port=3306, db="jgcproddb",charset="utf8")
# conn = pymysql.connect(host="localhost", user="root", password="", port=3306, db="jdbc", charset="utf8")
# 创建游标
cursor = conn.cursor()


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
    'Connection':'close',
    'cookie':'vlid=1598334632611x7bYbNr3JN; sessionid=BB0564B9-7B92-4628-A03D-6DE5063240D1%7C%7C2020-08-25+13%3A50%3A32.313%7C%7Cwww.baidu.com; autoid=edb260ee2f8896bcbe87a8bec00502e1; area=210106; ahpau=1; sessionuid=BB0564B9-7B92-4628-A03D-6DE5063240D1%7C%7C2020-08-25+13%3A50%3A32.313%7C%7Cwww.baidu.com; __ah_uuid_ng=c_BB0564B9-7B92-4628-A03D-6DE5063240D1; Hm_lvt_9924a05a5a75caf05dbbfb51af638b07=1598335812; jrsfvi=1598424705503IWzQEODWWC%7Cwww.autohome.com.cn%7C6841722; orderCount=eyJzaXRlSWQiOiI1MSIsImNhdGVnb3J5SWQiOiI4MjEiLCJzdWJDYXRlZ29yeUlkIjoiMTU0MjAiLCJ1c2VySWQiOiIiLCJwdmlkQ2hhaW4iOiIxMDE1OTQsMTAxNTk0LDEwMTU5NCwxMDE1OTQsNjg0MTcyMiIsImFjY2Vzc1R5cGUiOiIxIiwiYXBwS2V5IjoiIiwibG9jQ2l0eUlkIjoiMjEwMTAwIiwibG9jUHJvdmluY2VJZCI6IjIxMDAwMCIsImRldmljZUlkIjoiIiwibG9hZElkIjoiMTU5ODQyNDcwNTUwM0lXelFFT0RXV0MiLCJzZXNzaW9uSWQiOiJCQjA1NjRCOS03QjkyLTQ2MjgtQTAzRC02REU1MDYzMjQwRDF8fDIwMjAtMDgtMjUrMTM6NTA6MzIuMzEzfHx3d3cuYmFpZHUuY29tIiwidmlzaXRfaW5mbyI6IkJCMDU2NEI5LTdCOTItNDYyOC1BMDNELTZERTUwNjMyNDBEMXx8OTlFRDk2OTktQ0YzOC00MThBLUE0QTYtMTU1MUQxNERGRDg4fHwyMDIwMDUwOXx8MDF8fDYiLCJjdXJQdmFyZWFJZCI6IjY4NDE3MjIiLCJwdmFyZWFJZCI6IjY4NDE3MjIifQ==; Hm_lpvt_9924a05a5a75caf05dbbfb51af638b07=1598515794; ahsids=874_4745_5009_4105; FootPrints=45048%7C2020-8-27%2C44696%7C2020-8-27%2C37352%7C2020-8-27%2C38170%7C2020-8-27%2C45453%7C2020-8-27%2C; ahplid=1599162565800; ahpvno=94; sessionip=119.119.130.86; v_no=1; visit_info_ad=BB0564B9-7B92-4628-A03D-6DE5063240D1||58D95981-AAD3-41AA-A6C4-4824CC71D019||-1||-1||1; ref=www.baidu.com%7C0%7C0%7C0%7C2020-08-28+09%3A06%3A35.007%7C2020-08-25+13%3A50%3A32.313; sessionvid=58D95981-AAD3-41AA-A6C4-4824CC71D019; ahrlid=1598576794896Aidc0tZHac-1598576797201'
}
# city_pinyin = [
#         'beijing', 'shanghai', 'nanjing', 'hangzhou', 'guangzhou', 'shenzhen', 'tianjin', 'chongqing',
#         'hefei', 'wuhu', 'bangbu', 'huainan', 'maanshan', 'huaibei', 'tongling', 'anqing',
#         'huangshan', 'chuzhou', 'fu_yang', 'su_zhou', 'liuan', 'bozhou', 'chizhou', 'xuancheng', 'aomen',
#         'aomen', 'fuzhou', 'xiamen', 'putian', 'sanming', 'quanzhou', 'zhangzhou', 'nanping',
#         'longyan', 'ningde', 'guangzhou', 'shaoguan', 'shenzhen', 'zhuhai', 'shantou', 'foshan',
#         'jiangmen', 'zhanjiang', 'maoming', 'zhaoqing', 'huizhou', 'meizhou', 'shanwei', 'heyuan',
#         'yangjiang', 'qingyuan', 'dongguan', 'zhongshan', 'chaozhou', 'jieyang', 'yunfu',
#         'nanning', 'liuzhou', 'guilin', 'wuzhou', 'beihai', 'fangchenggang', 'qinzhou', 'guigang', 'yu_lin',
#         'baise', 'hezhou', 'hechi', 'laibin', 'chongzuo', 'guiyang', 'liupanshui', 'zunyi',
#         'anshun', 'bijie', 'tongren', 'xingyishi', 'kaili', 'duyunshi', 'lanzhou', 'jiayuguan',
#         'jinchang', 'baiyin', 'tianshui', 'wuwei', 'zhangye', 'pingliang', 'jiuquan', 'qingyang', 'dingxi',
#         'longnan', 'linxia', 'gannan', 'shijiazhuang', 'tangshan', 'qinhuangdao', 'handan',
#         'xingtai', 'baoding', 'zhangjiakou', 'chengde', 'cangzhou', 'langfang', 'hengshui',
#         'haerbin', 'qiqihaer', 'jixi', 'hegang', 'shuangyashan', 'daqing', 'yichun', 'jiamusi', 'qitaihe',
#         'mudanjiang', 'heihe', 'suihua', 'daxinganling','zhengzhou', 'kaifeng', 'luoyang',
#         'pingdingshan', 'anyang', 'hebi', 'xinxiang', 'jiaozuo', 'puyang', 'xuchang', 'luohe', 'sanmenxia',
#         'nanyang', 'shangqiu', 'xinyang', 'zhoukou', 'zhumadian', 'jiyuan', 'wuhan', 'huangshi',
#         'shiyan', 'yichang', 'xiangyang', 'ezhou', 'jingmen', 'xiaogan', 'jingzhou', 'huanggang', 'xianning',
#         'suizhou', 'enshi', 'xiantao', 'qianjiang', 'tianmen', 'shennongjia', 'changsha', 'zhuzhou',
#         'xiangtan', 'hengyang', 'shaoyang', 'yueyang', 'changde', 'zhangjiajie', 'yiyang', 'chenzhou',
#         'yongzhou', 'huaihua', 'loudi', 'xiangxi', 'haikou', 'sanya', 'sanshashi', 'danzhou',
#         'wuzhishan', 'qionghai', 'wenchang', 'wanning', 'dongfang', 'dingan', 'tunchang', 'chengmai',
#         'lingao', 'baisha', 'changjiang', 'ledong', 'lingshui', 'baoting', 'qiongzhong',
#         'changchun', 'jilinshi', 'siping', 'liaoyuan', 'tonghua', 'baishan', 'songyuan', 'baicheng',
#         'yanbian', 'nanjing', 'wuxi', 'xuzhou', 'changzhou', 'suzhou', 'nantong', 'lianyungang',
#         'huaian', 'yancheng', 'yangzhou', 'zhenjiang', 'tai_zhou', 'suqian',  'nanchang',
#         'jingdezhen', 'ping_xiang', 'jiujiang', 'xinyu', 'yingtan', 'ganzhou', 'jian', 'yi_chun', 'fu_zhou',
#         'shangrao', 'shenyang', 'dalian', 'anshan', 'fushun', 'benxi', 'dandong', 'jinzhou',
#         'yingkou', 'fuxin', 'liaoyang', 'panjin', 'tieling', 'chaoyang', 'huludao', 'namenggu', 'huhehaote',
#         'baotou', 'wuhai', 'chifeng', 'tongliao', 'eerduosi', 'hulunbeier', 'bayannaoer', 'wulanchabu',
#         'xinganmeng', 'xilinguolemeng', 'alashanmeng',  'yinchuan', 'shizuishan', 'wuzhong',
#         'guyuan', 'zhongwei', 'xining', 'haidong', 'haibei', 'huangnan', 'hai_nan', 'guoluo',
#         'yushu', 'haixi', 'taiyuan', 'datong', 'yangquan', 'changzhi', 'jincheng', 'shuozhou',
#         'jinzhong', 'yuncheng', 'xinzhou', 'linfen', 'lvliang','jinan', 'qingdao', 'zibo',
#         'zaozhuang', 'dongying', 'yantai', 'weifang', 'jining', 'taian', 'weihai', 'rizhao', 'laiwu',
#         'linyi', 'dezhou', 'liaocheng', 'binzhou', 'heze', 'sichuan', 'chengdu', 'zigong', 'panzhihua',
#         'luzhou', 'deyang', 'mianyang', 'guangyuan', 'suining', 'neijiang', 'leshan', 'nanchong', 'meishan',
#         'yibin', 'guangan', 'dazhou', 'yaan', 'bazhong', 'ziyang', 'aba', 'ganzi', 'liangshan',
#         'xian', 'tongchuan', 'baoji', 'xianyang', 'weinan', 'yanan', 'hanzhong', 'yulin', 'ankang',
#         'shangluo', 'taiwan', 'taiwan', 'lasa', 'rikaze', 'changdou', 'linzhi', 'shannan', 'naqu',
#         'ali', 'wulumuqi', 'kelamayi', 'tulufan', 'hami', 'changji', 'boertala', 'bayinguoleng',
#         'akesu', 'kezilesu', 'kashen', 'hetian', 'yili', 'tacheng', 'aletai', 'shihezi', 'alaer',
#         'tumushuke', 'wujiaqu', 'beitunshi', 'tiemenguanshi', 'shuangheshi', 'kekedalashi', 'kunyu',
#         'xianggang', 'xianggang', 'kunming', 'qujing', 'yuxi', 'baoshan', 'zhaotong', 'lijiang',
#         'puer', 'lincang', 'chuxiong', 'honghe', 'wenshan', 'xishuangbanna', 'dali', 'dehong', 'nujiang',
#         'diqing', 'hangzhou', 'ningbo', 'wenzhou', 'jiaxing', 'huzhou', 'shaoxing', 'jinhua',
#         'quzhou', 'zhoushan', 'taizhou', 'lishui']

city_pinyin = [
        'binzhou', 'heze', 'chengdu', 'zigong', 'panzhihua',
        'luzhou', 'deyang', 'mianyang', 'guangyuan', 'suining', 'neijiang', 'leshan', 'nanchong', 'meishan',
        'yibin', 'guangan', 'dazhou', 'yaan', 'bazhong', 'ziyang', 'aba', 'ganzi', 'liangshan',
        'xian', 'tongchuan', 'baoji', 'xianyang', 'weinan', 'yanan', 'hanzhong', 'yulin', 'ankang',
        'shangluo', 'taiwan', 'taiwan', 'lasa', 'rikaze', 'changdou', 'linzhi', 'shannan', 'naqu',
        'ali',  'wulumuqi', 'kelamayi', 'tulufan', 'hami', 'changji', 'boertala', 'bayinguoleng',
        'akesu', 'kezilesu', 'kashen', 'hetian', 'yili', 'tacheng', 'aletai', 'shihezi', 'alaer',
        'tumushuke', 'wujiaqu', 'beitunshi', 'tiemenguanshi', 'shuangheshi', 'kekedalashi', 'kunyu',
        'xianggang', 'xianggang', 'kunming', 'qujing', 'yuxi', 'baoshan', 'zhaotong', 'lijiang',
        'puer', 'lincang', 'chuxiong', 'honghe', 'wenshan', 'xishuangbanna', 'dali', 'dehong', 'nujiang',
        'diqing', 'hangzhou', 'ningbo', 'wenzhou', 'jiaxing', 'huzhou', 'shaoxing', 'jinhua',
        'quzhou', 'zhoushan', 'taizhou', 'lishui']


def get_html(fours_url):
    try:
        print('正在爬取的连接',fours_url)
        resp_html = requests.get(fours_url,headers=headers)
        resp_html.encoding = 'gbk'
        resp_data = parsel.Selector(resp_html.text)
        data_list = resp_data.xpath('//ul[@class="list-box"]/li[@class="list-item"]')
        for li in data_list:
            print(fours_url)
            """请求详情"""
            # 获取详情连接
            store_name_link = 'https:'+li.xpath('./ul[@class="info-wrap"]/li[1]/a/@href').get()
            # 对详情发起请求
            detail_resp = requests.get(headers=headers, url=store_name_link)
            detail_resp.encoding = 'gbk'
            # 转化响应
            detail_data = parsel.Selector(detail_resp.text)

            # 4s店名称
            store_name = detail_data.xpath('//div[@id="breadnav"]/p/span[2]/text()').get()
            # print(store_name)

            # 座机号
            telephone_number = detail_data.xpath('//div[@id="400set"]/span[@class="dealer-api"]/span/text()').get()
            # print(telephone_number)

            # 地址
            address = detail_data.xpath('//div[@id="dealerposi"]/div[@class="allagency-cont"]/p/@title').get()
            print(address)
            if address =='':
                continue
            # print(address)

            # 城市名称
            city_name = detail_data.xpath('//div[@id="breadnav"]/p/a/text()').get()
            # print('城市',city_name)

            # 城市id
            sql2 = "select city_id from national_cities where city_name ='{}'".format(city_name)
            cursor.execute(sql2)
            city_id = cursor.fetchone()[0]

            last_sync_time = datetime.datetime.now().strftime("%Y-%m-28 23:35:23")

            # 主营品牌
            brand_list = detail_data.xpath('//div[@class="brandtree"]/div/p[@class="text"]/text()').getall()
            print(brand_list)

            brand_name = ''
            for bname in brand_list:
                brand_name = bname
                if brand_name == '阿尔法·罗密欧':
                    brand_name = '阿尔法・罗密欧'

                if brand_name == '阿斯顿·马丁':
                    brand_name = '阿斯顿・马丁'
                # 品牌id
                sql2 = "select brand_id from t_car_brand where brand_name='{}'".format(brand_name)
                cursor.execute(sql2)
                brand_id = cursor.fetchone()[0]

                data = (brand_name,brand_id,store_name,telephone_number,address,city_name,city_id,last_sync_time)
                print(data)
                # t_mbr_role_storehouse
                # 存入数据
                # 根据 车型id 城市id 判断 车型是否存在  时间就是确保 库里只保留本月的数据
                sql = "select * from t_mbr_role_storehouse where brand_name='{}'and brand_id='{}'and store_name ='{}' and telephone_number ='{}' and address='{}'and city_name='{}'".format(
                    data[0], data[1], data[2], data[3], data[4], data[5])
                cursor.execute(sql)
                many = cursor.fetchone()
                if many:
                    print('此数据表中已存在')
                else:
                    insert_sql = "insert into t_mbr_role_storehouse(brand_name,brand_id,store_name,telephone_number,address,city_name,city_id,last_sync_time)values (%s,%s,%s,%s,%s,%s,%s,%s)"
                    cursor.execute(insert_sql, data)
                    conn.commit()  # 提交数据

                    print('数据提交完成')
    except TypeError:
        pass
def main():
    # 4s店url
    for pin in city_pinyin:
        for page in range(1,41):
            time.sleep(1)
            fours_url = 'https://dealer.autohome.com.cn/{}/0/0/0/0/{}/1/0/0.html'.format(pin,page)
            get_html(fours_url)
    cursor.close()
    conn.close()
    print('数据库已关闭')
if __name__ == '__main__':
        main()




