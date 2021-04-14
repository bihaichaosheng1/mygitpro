# -*- coding:utf-8 -*-
import requests
import parsel
import pinyin
import datetime
import re
import pymysql


conn = pymysql.connect(host="112.126.89.134", user="jgcdb", password="jingche0000", port=3306, db="jgcproddb",charset="utf8")
# conn = pymysql.connect(host="localhost", user="root", password="", port=3306, db="jdbc", charset="utf8")
cursor = conn.cursor()  # 创建游标


headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
        'Connection': 'close'
    }


url = "https://car.autohome.com.cn/AsLeftMenu/As_LeftListNew.ashx?typeId=1%20&brandId"

resp = requests.get(url=url,headers=headers)

response = parsel.Selector(resp.text)



# 品牌id
ids = response.xpath('//body/ul/li/@id').getall()

base_url = 'https://car.autohome.com.cn/AsLeftMenu/As_LeftListNew.ashx?typeId=1%20&brandId'

for var in ids:
    id = var.replace('b', '=')
    base_url= url + id
    base_response = requests.get(base_url,headers=headers)
    base_response.encoding='gbk'
    base_resp = parsel.Selector(base_response.text)
    # print(base_resp)
    # 厂商id
    brand_link = base_resp.xpath('//body/ul/li/dl/dt/a/@href').getall()
    for link in brand_link:
        detail_url = 'https://car.autohome.com.cn/'+link

        # print(detail_url)

        detail_resp = requests.get(detail_url,headers=headers)
        detail_data = parsel.Selector(detail_resp.text)
        # 厂商名称
        brand_name = detail_data.xpath('//div[@class="cartab-title"]/h2/a/text()').get()
        # print(brand_name)


        # 厂商首字母
        da = pinyin.get_initial(brand_name, delimiter="").upper()
        brand_initial = da[0:1]

        # 品牌id
        contain_brand_link = detail_data.xpath('//div[@class="breadnav"]/a[3]/@href').get()
        contain_brand_id = "".join(re.findall('\d+', contain_brand_link))
        # print(contain_brand_link)

        # 厂商id
        brand_link = detail_data.xpath('//div[@class="cartab-title"]/h2/a/@href').get()
        brand_id = '100' + contain_brand_id + "".join(re.findall('\d+\.', brand_link)).replace('.', '')
        print(brand_link)

        # 品牌名称
        contain_brand_name = detail_data.xpath('//div[@class="breadnav"]/a[3]/text()').get()
        # print(contain_brand_name)

        # 产商首字母
        da = pinyin.get_initial(contain_brand_name, delimiter="").upper()
        contain_brand_initial = da[0:1]


        # 品牌logo
        # 拼接logo所在的url
        logo_url = 'https://car.autohome.com.cn' + contain_brand_link
        brand_logo_data = requests.get(logo_url)
        logo_data = parsel.Selector(brand_logo_data.text)
        contain_brand_logo = 'https:' + logo_data.xpath( '//div[@class="uibox-con contbox"]/div[@class="carbrand"]/div[@class="carbradn-pic"]/img/@src').get()


        # # 段位
        # brandone = ['宝马', '奥迪', '阿尔法・罗密欧', '阿斯顿・马丁', '奔驰', '布加迪', '宾利', '保时捷', '法拉利', '悍马', '捷豹', 'smart', 'Jeep',
        #             '凯迪拉克', '兰博基尼', '路虎', '路特斯', '林肯', '雷克萨斯', '劳斯莱斯', '迈巴赫', 'MINI', '玛莎拉蒂', '欧宝', '讴歌', '帕加尼', '日产',
        #             '沃尔沃', '英菲尼迪', '威兹曼', '科尼赛克', 'KTM', 'GMC', '光冈', 'AC Schnitzer', 'Lorinser', '迈凯伦', '特斯拉', '巴博斯',
        #             '卡尔森', '摩根', 'DS', 'Icona', '泰卡特', '乔治・巴顿', '卡升', '斯达泰克', 'LOCAL MOTORS', 'ALPINA', '罗夫哈特', 'Karma',
        #             '捷尼赛思', '迈莎锐', 'SHELBY', '铂驰', 'IMSA英飒']
        #
        # brandtwo = ['大众', '丰田', '福特', '克莱斯勒', '雷诺', '菲亚特', '现代', '标致', '本田', '别克', '道奇', '铃木', '马自达', '起亚', '萨博', '斯巴鲁',
        #             '世爵', '斯柯达', '三菱', '双龙', '雪佛兰', '雪铁龙', '红旗', '大发', '西雅特', '依维柯', '五十铃', '之诺', '小鹏汽车', '领克', '蔚来',
        #             '威马汽车', '理想汽车', '捷达', ]
        #
        # brandthree = ['荣威', '名爵', '中华', '哈飞', '吉利汽车', '奇瑞', '北京', '东风', '中兴', '比亚迪', '长安', '长城', '猎豹汽车', '北汽昌河', '力帆汽车',
        #               '东南', '广汽传祺', '金杯', '江淮', '华普', '海马', '华泰', '陆风', '莲花汽车', '双环', '永源', '众泰', '奔腾', '福田', '黄海',
        #               '开瑞', '威麟', '瑞麒', '广汽吉奥', '一汽', '野马汽车', '东风风神', '五菱汽车', '江铃', '宝骏', '启辰', '理念', '纳智捷', '福迪',
        #               '东风小康', '北汽威旺', '金龙', '欧朗', '陕汽通家', '海格', '九龙', '观致', '北汽制造', '上汽大通MAXUS', '腾势', '思铭', '长安欧尚',
        #               '恒天', '东风风行', 'BEIJING汽车', '如虎', '金旅', '哈弗', '华骐', '新凯', '东风风度', '潍柴英致', '成功汽车', '福汽启腾', '卡威',
        #               '北汽幻速', '陆地方舟', '赛麟', '知豆', '北汽新能源', '骐铃汽车', '开沃汽车', '凯翼', '雷丁', '全球鹰', '华颂', '宝沃', '御捷', '前途',
        #               '华凯', '东风风光', '华泰新能源', '驭胜', '汉腾汽车', 'SWM斯威汽车', '江铃集团新能源', '比速汽车', 'ARCFOX', '电咖', 'WEY', '云度',
        #               '长安凯程', '瑞驰新能源', '君马汽车', '宇通客车', '长安跨越', '北汽道达', '国金汽车', 'SRM鑫源', '裕路', 'Polestar极星', '哪吒汽车',
        #               '庆铃汽车', '广汽新能源', '云雀汽车', '零跑汽车', '捷途', '新特汽车', 'SERES赛力斯', '东风・瑞泰特', '爱驰', '广汽集团', '思皓', '欧拉',
        #               'LITE', '红星汽车', '容大智造', '天际汽车', '大乘汽车', '领途汽车', '星途', '宝骐汽车', '钧天', '车驰汽车', '国机智骏', '几何汽车',
        #               '银隆新能源', 'HYCAN合创', 'AUXUN傲旋', '迈迈', '远程汽车', '汉龙汽车', '比德文汽车', '潍柴汽车', '新宝骏', '野马新能源', '一汽凌河',
        #               '天美汽车', '上喆', '大运', '东风富康', '枫叶汽车', '金冠汽车', '凌宝汽车', '神州', '速达','ARCFOX极狐']
        #
        cata = ''
        # for brand in brandone:
        #     if contain_brand_name == brand:
        #         cata = 1
        #
        # for brand in brandtwo:
        #     if contain_brand_name == brand:
        #         cata = 2
        #
        # for brand in brandthree:
        #     if contain_brand_name == brand:
        #         cata = 3

        # 最后更新时间
        last_sync_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # print('更新时间', last_sync_time)

        print(brand_name,brand_id,contain_brand_id,contain_brand_name,contain_brand_initial,contain_brand_logo,brand_initial,last_sync_time)

        data = (brand_name,brand_id,contain_brand_id,contain_brand_name,contain_brand_initial,contain_brand_logo,brand_initial,last_sync_time)
        sql3 = "select * from t_car_brand_all where brand_id='{0}'".format(data[1])
        cursor.execute(sql3)
        many = cursor.fetchone()
        if many:
            print('此数据表中已存在')
            # sql2 = "UPDATE  t_car_brand_all SET contain_brand_initial='{}' WHERE brand_id='{}'".format(data[4],data[1])
            # cursor.execute(sql2)
            # conn.commit()  # 提交数据
            # print('已更新')
        else:
            sql = "insert into t_car_brand_all(brand_name,brand_id,contain_brand_id,contain_brand_name,contain_brand_initial,contain_brand_logo,brand_initial,last_sync_time) value(%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, data)
            conn.commit()  # 提交数据
            print('数据已提交')
cursor.close()  # 关闭游标
conn.close()  # 关闭连接

