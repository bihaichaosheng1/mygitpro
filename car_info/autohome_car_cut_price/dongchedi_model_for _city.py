# -*- coding:utf-8 -*-


"""
懂车帝--东北三省（省会）汽车降价数据
"""
from requests.adapters import HTTPAdapter
import requests
import jsonpath
import time
from decimal import Decimal
import pymysql
import re
import json
import concurrent.futures
from multiprocessing import Process,Lock

# 解决ssl证书警告
requests.packages.urllib3.disable_warnings()

# 解决超过最大链接
srequest = requests.session()
srequest.mount('https://', HTTPAdapter(max_retries=10))

# 解决重连
srequest.keep_alive = False
srequest.adapters.DEFAULT_RETRIES = 6
# 头部信息
headers = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
    'cookie':'UM_distinctid=1740f8c59ba7a6-05a4da24d8a412-3323767-144000-1740f8c59bbaa0; _ga=GA1.2.702845436.1597988692; tt_webid=6865841188574905870; CNZZDATA1278124308=1364508085-1597983626-https%253A%252F%252Fwww.baidu.com%252F%7C1598577288; _gid=GA1.2.1717526056.1598578239; _gat_gtag_UA_138671306_1=1; SLARDAR_WEB_ID=bea9ad8b-e827-4bdf-91ed-6effa54d2789'
}
ip_list = ['115.226.247.160:5412','114.107.151.72:3617','175.173.222.94:3617','223.215.24.189:894','180.113.9.169:5412','115.151.19.250:5412','114.238.85.132:894','175.173.223.168:766','60.166.105.164:766','180.113.48.220:766','111.72.144.150:894','114.223.179.218:3617','124.113.240.226:5412','223.240.242.25:5412','223.215.175.42:36410','117.57.20.241:36410','222.189.191.141:23564','183.160.35.59:23564','222.190.222.110:894','180.113.112.155:23564']
# for i in ip_list:
#
#     proxies = {  # 代理ip
#         'https://':'https://'+i
#     }

# 连接MySQL数据库
conn = pymysql.connect(host="112.126.89.134", user="jgcdb", password="jingche0000", port=3306, db="jgcproddb",charset="utf8")
# conn = pymysql.connect(host="localhost", user="root", password="", port=3306, db="jdbc", charset="utf8")
# 创建游标
cursor = conn.cursor()

# address = ['长春', '沈阳', '哈尔滨']  大连，吉林市，佳木斯,'齐齐哈尔','牡丹江','大庆','鸡西','双鸭山','伊春','七台河','鹤岗','黑河','绥化'


url = 'https://www.dcdapp.com/motor/brand/m/v1/select/series/?city_name=沈阳'

# address = ['合肥','安庆','蚌埠','池州','阜阳','淮北','淮南','六安','马鞍山','铜陵','芜湖','宣城','滁州','黄山', '宿州', '亳州', '北京', '福州', '厦门', '龙岩', '漳州', '莆田', '泉州', '南平', '宁德', '三明', '兰州', '定西', '平凉', '酒泉', '张掖', '庆阳', '武威', '天水', '嘉峪关', '金昌', '白银', '陇南', '甘南', '广州', '深圳', '珠海', '东莞', '中山', '汕头', '潮州', '韶关', '湛江', '肇庆', '茂名', '梅州', '佛山', '惠州', '江门', '揭阳', '清远', '云浮', '阳江', '河源', '汕尾', '南宁', '柳州', '桂林', '北海', '百色', '贺州', '河池', '贵港', '玉林', '钦州', '梧州', '防城港', '来宾', '崇左', '贵阳', '遵义', '安顺', '六盘水', '黔东南', '黔南', '毕节', '黔西南', '铜仁', '海口', '琼海', '三亚', '五指山', '儋州', '文昌', '万宁', '东方', '石家庄', '唐山', '邢台', '秦皇岛', '廊坊', '邯郸', '衡水', '沧州', '保定', '张家口', '承德', '郑州', '洛阳','大兴安岭', '武汉', '十堰', '襄阳', '随州', '仙桃', '天门', '宜昌', '黄石', '荆门', '荆州', '鄂州', '咸宁', '潜江', '孝感', '黄冈', '神农架', '长沙', '郴州', '常德', '衡阳', '怀化', '娄底', '株洲', '岳阳', '湘潭', '邵阳', '永州', '益阳', '张家界', '湘西', '通化', '辽源', '白山', '白城', '松原', '延边', '南京', '苏州', '无锡', '常州', '淮安', '连云港', '南通', '盐城', '扬州', '镇江', '泰州', '徐州', '宿迁', '南昌', '上饶', '萍乡', '新余', '宜春', '九江', '赣州', '吉安', '景德镇', '抚州', '鹰潭', '四平', '丹东', '抚顺', '阜新', '葫芦岛', '朝阳', '本溪', '鞍山', '锦州', '辽阳', '营口', '盘锦', '铁岭', '呼和浩特', '包头', '赤峰', '通辽', '乌海', '鄂尔多斯', '呼伦贝尔', '兴安盟', '巴彦淖尔', '乌兰察布', '锡林郭勒', '阿拉善盟', '银川', '吴忠', '固原', '石嘴山', '中卫', '西宁', '海北', '黄南', '果洛', '玉树', '海西', '海东', '海南', '济南', '青岛', '烟台', '威海', '潍坊', '泰安', '枣庄', '淄博', '东营', '菏泽', '滨州', '聊城', '临沂', '济宁', '日照', '莱芜', '太原', '大同', '晋城', '晋中', '临汾', '长治', '运城', '忻州', '阳泉', '朔州', '吕梁', '西安', '咸阳', '渭南', '榆林', '宝鸡', '安康', '汉中', '延安', '铜川', '商洛', '上海', '成都', '绵阳', '遂宁', '攀枝花', '宜宾', '雅安', '自贡', '资阳', '广元', '德阳', '乐山', '南充', '眉山', '巴中', '泸州', '内江', '广安', '达州', '阿坝', '甘孜', '凉山', '天津', '拉萨', '日喀则', '山南', '那曲', '阿里', '昌都', '林芝', '乌鲁木齐', '克拉玛依', '石河子', '博乐', '库尔勒', '伊犁', '阿拉尔', '图木舒克', '五家渠', '喀什', '阿克苏', '和田', '塔城', '吐鲁番', '哈密', '阿勒泰', '克州', '昆明', '玉溪', '曲靖', '保山', '临沧', '文山', '西双版纳', '昭通', '丽江', '红河', '德宏', '怒江', '迪庆', '普洱', '杭州', '宁波', '温州', '嘉兴', '金华', '丽水', '湖州', '衢州', '台州', '绍兴', '舟山', '重庆', '恩施', '三沙', '定安县', '屯昌县', '澄迈县', '临高县', '白沙黎族自治县', '昌江黎族自治县', '乐东黎族自治县', '陵水黎族自治县', '保亭黎族苗族自治县', '琼中黎族苗族自治县', '楚雄', '大理', '临夏', '昌吉', '北屯', '铁门关', '双河', '可克达拉', '昆玉', '台湾', '香港', '澳门']
address = [  '吕梁', '西安', '咸阳', '渭南','榆林', '宝鸡', '安康', '汉中', '延安', '铜川',
           '商洛', '上海', '成都', '绵阳', '遂宁', '攀枝花', '宜宾', '雅安', '自贡', '资阳', '广元', '德阳', '乐山', '南充', '眉山', '巴中', '泸州',
           '内江', '广安', '达州', '阿坝', '甘孜', '凉山', '天津', '拉萨', '日喀则', '山南', '那曲', '阿里', '昌都', '林芝','乌鲁木齐', '克拉玛依',
           '石河子', '博乐', '库尔勒', '伊犁', '阿拉尔', '图木舒克', '五家渠', '喀什', '阿克苏', '和田', '塔城', '吐鲁番', '哈密', '阿勒泰', '克州',
           '昆明', '玉溪', '曲靖', '保山', '临沧', '文山', '西双版纳', '昭通', '丽江', '红河', '德宏', '怒江', '迪庆', '普洱', '杭州', '宁波', '温州',
           '嘉兴', '金华', '丽水', '湖州', '衢州', '台州', '绍兴', '舟山', '重庆', '恩施', '三沙', '定安县', '屯昌县', '澄迈县', '临高县', '白沙黎族自治县',
           '昌江黎族自治县', '乐东黎族自治县', '陵水黎族自治县', '保亭黎族苗族自治县', '琼中黎族苗族自治县', '楚雄', '大理', '临夏', '昌吉', '北屯', '铁门关', '双河',
           '可克达拉','昆玉', '台湾', '香港', '澳门']

for a in address:
    for num in range(1, 154):
        data = {
            'offset': '{}'.format(num),
            'limit': '20',
            'is_refresh': '1',
            'city_name': '{}'.format(a)
        }
        try:
            resp_json = srequest.post(url=url, data=data, headers=headers,verify=False).json()
        except :
            continue
        # resp_json = srequest.post(url=url, data=data, headers=headers).json()
        time.sleep(1.5)
        series_id_list = jsonpath.jsonpath(resp_json, '$..id')
        for series_id in series_id_list:
            # print(series_id)
            spec_link = 'https://www.dcdapp.com/motor/car_page/m/v1/series_all_json/?series_id={}&city_name={}&show_city_price=1&m_station_dealer_price_v=1'.format(series_id, a)

            print('spec_link', spec_link)
            try:
                spec_data = srequest.get(url=spec_link, headers=headers,verify=False).json(strict=False)['data']
                time.sleep(1.5)

                # 车系名称
                series_name = jsonpath.jsonpath(spec_data, '$[online]..series_name')
                print('车系名称',series_name)
                # if series_name == False:
                #     continue
                # print(series_name)

                # 车型名称
                spec_names = jsonpath.jsonpath(spec_data, '$[online]..info.name')
                print(spec_names)
                if spec_names == False:
                    continue
                for name in spec_names:
                    if "马力" in name:
                        spec_names.remove(name)  # 删除带有马力的分类名称，留下车型名称
                # 车系名称与车型名称进行拼接
                spec_name_list = []
                for i in range(0, len(series_name)):
                    spec_name_list.append(series_name[i] + ' ' + spec_names[i])
                # 提取年框 拼接到名称最后
                spec_name_list2 = []  # 车型名称
                for name in spec_name_list:
                    s_name = "".join(re.findall(r'[0-9]{4}款*', name))
                    sp_name = name.replace(s_name + " ", '')
                    spec_namess = sp_name + s_name
                    spec_name_list2.append(spec_namess)
                # print('车型名称',spec_name_list2)

                # 手动
                spec_name_shou = []
                for name in spec_name_list2:
                    name1 = name.replace('手动', '手动 ')
                    spec_name_shou.append(name1)
                # print(spec_name_shou)
                # 更改后   # 自动
                spec_name = []
                for name in spec_name_shou:
                    name1 = name.replace('自动', '自动 ')
                    spec_name.append(name1)
                print('车型名称',spec_name)

                # 获取城市id
                city_id = "".join(re.findall('[\u4e00-\u9fa5]', spec_link))
                print(city_id)
                # for c_name in city_id:
                sql = "select city_id from national_cities_yiche where city_name='{}'".format(city_id)
                cursor.execute(sql)
                city_ids = cursor.fetchone()  # 得到品牌id数据
                city_id = []
                for id in city_ids:
                    print(id)
                    city_id.append(id)
                print('城市名称', city_id)

                """价格信息"""
                # 指导价列表
                guidance_price = []
                # 现价列表
                price = []
                # 计算降价数据使用的列表
                guidance_list = []
                price_list = []

                price_info_list = jsonpath.jsonpath(spec_data, '$[online]..price_info')
                # print('价格信息', price_info_list)
                try:
                    for i in price_info_list:
                        # 指导价
                        guidance = i['official_price']
                        guidance_list.append(guidance)

                        # 现价
                        p_price = i['dealer_price']
                        price_list.append(p_price)
                except TypeError:
                    continue
                # 降价列表
                cut_price = []
                cut_price_list = (list(map(lambda x, y: x - y, guidance_list, price_list)))
                # print('降价', cut_price_list)

                for g in guidance_list:
                    guidance_price.append(str(g) + '万')
                print('指导价', guidance_price)

                for p in price_list:
                    price.append(str(p) + '万')
                print('现价',price)

                for money in cut_price_list:
                    money = str(money)
                    if money == 0.00:
                        money = 'null'
                    cut_p = str(Decimal(money).quantize(Decimal('0.00'))) + '万'
                    cut_price.append(cut_p)
                print('降价',cut_price)
                # 来源（app）
                app_id = '5'  # 懂车帝

                # 最后一次更新时间
                # last_sync_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                # last_sync_time = datetime.datetime.now().strftime("%Y-%m-%d")
                last_sync_time = '2020-8-30 23:35:23'
                print('更新时间',last_sync_time)

                # 存储数据
                for ser_name, s_name, g_price, c_price, p_price in zip(series_name, spec_name, guidance_price, cut_price, price):
                    data = (ser_name, s_name, city_id[0], g_price, c_price, p_price, last_sync_time, app_id)
                    print(data)

                    # 若 mysql 连接失败就重新连接
                    conn.ping(reconnect=True)

                    print('这是即将存到数据库的data', data)
                    try:

                        sql2 = "select * from t_car_cut_price_to_app where spec_name='{}'and city_id='{}'and price='{}'and last_sync_time".format(data[1], data[2], data[3],data[6])
                        cursor.execute(sql2)
                        many = cursor.fetchone()
                        if many:
                            print('此数据表中已存在')
                        else:
                            sql_yiche_car_detail_city = "replace into t_car_cut_price_to_app(series_name,spec_name, city_id, guidance_price, cut_price, price, last_sync_time, app_id) value(%s,%s,%s,%s,%s,%s,%s,%s) "
                            cursor.execute(sql_yiche_car_detail_city, data)
                            # 若 mysql 连接失败就重新连接
                            conn.ping(reconnect=True)
                            conn.commit()  # 提交数据
                            print('数据提交完成')
                    except pymysql.err:
                        conn.ping(True)

            except :
                # continue
                print('geg')

cursor.close()  # 关闭游标
print('关闭游标')
conn.close()  # 关闭连接
print('关闭连接')