import requests
import parsel
import pymysql
from concurrent.futures import ThreadPoolExecutor
from faker import Factory
f = Factory.create()
ua = f.user_agent()


headers = {
    'User-Agent' : ua
}

conn = pymysql.connect(host="112.126.89.134", user="jgcdb", password="jingche0000", port=3306, db="jgcproddb",charset="utf8")
# conn = pymysql.connect(host="localhost", user="root", password="", port=3306, db="jdbc", charset="utf8")
cursor = conn.cursor()  # 创建游标


def cars_on_sale(url):
    try:
        first_page_data = requests.get(url,headers=headers).text
        on_spec_data = parsel.Selector(first_page_data)
        a_link = on_spec_data.xpath('//html/body/div[2]/div[1]/div[2]/div[7]/div/div[3]/div[1]/ul/li[1]/a/@href').get()
        if a_link == None:
            print(a_link)
        else:
            detail_url = 'https://car.autohome.com.cn' + a_link
            spec_data = requests.get(detail_url,headers=headers).text
            spec_id_data = parsel.Selector(spec_data)
            li_list = spec_id_data.xpath('//*[@id="divSeries"]/div/ul/li')
            print(a_link)
            for li in li_list:
                spec_id = li.xpath('./@data-value').get()
                print('在售',spec_id)
                with open("在售车型id.txt", "a") as fp:
                    fp.write(spec_id+","+"\n")
    except requests.exceptions.ConnectionError:
        print('___________________________报错了___________________________')
        cars_on_sale(url)

# 停售车型id
def stop_selling_cars(stop_url):
    try:
        spec_data = requests.get(stop_url,headers=headers).text
        print(stop_url)
        stop_spec_data = parsel.Selector(spec_data)
        li_list = stop_spec_data.xpath('//ul[@class="interval01-list"]/li')
        for li in li_list:
            spec_id = li.xpath('./@data-value').get()
            print('停售',spec_id)
            with open("停售车型id.txt", "a", encoding="utf-8") as fp:
                fp.write(spec_id+","+"\n")
        # 下一页
        next_page = stop_spec_data.xpath('//*[@id="brandtab-1"]/div[3]/div/a[4]/@href').get()
        if next_page:
            next_url = 'https://car.autohome.com.cn' + next_page
            spec_data_next = requests.get(next_url, headers=headers).text
            print('停售下一页', next_url)
            next_stop_spec_data = parsel.Selector(spec_data_next)
            li_list = next_stop_spec_data.xpath('//ul[@class="interval01-list"]/li')
            for li in li_list:
                spec_id = li.xpath('./@data-value').get()
                print('停售下一页',spec_id)
                with open("停售车型id.txt", "a", encoding="utf-8") as fp:
                    fp.write(spec_id+","+"\n")
    except requests.exceptions.ConnectionError:
        print('___________________________报错了___________________________')
        stop_selling_cars(stop_url)

# 预售车型id
def pre_sale_car(pre_url):
    try:
        spec_data = requests.get(pre_url,headers=headers).text
        pre_spec_data = parsel.Selector(spec_data)
        li_list = pre_spec_data.xpath('//ul[@class="interval01-list"]/li')
        for li in li_list:
            if li_list == False:
                continue
            spec_id = li.xpath('./@data-value').get()
            print('预售',spec_id)
            with open("预售车型id.txt", "a", encoding="utf-8") as fp:
                fp.write(spec_id+","+"\n")

    except requests.exceptions.ConnectionError:
        print('___________________________报错了___________________________')
        pre_sale_car(pre_url)

def main():

    """在售"""
    on_sql = "select series_id from t_car_category"
    cursor.execute(on_sql)
    series_ids = cursor.fetchall()  # 得到在售车系id数据
    for id in series_ids:
        sid = (id[0])
        # 在售
        url = 'https://car.autohome.com.cn/price/series-{}.html#pvareaid=2042205'.format(sid)
        cars_on_sale(url=url)

        # 停售
        stop_url = ('https://car.autohome.com.cn/price/series-{}-0-3-0-0-0-0-1.html'.format(sid))
        stop_selling_cars(stop_url=stop_url)

        # 预售
        pre_url = 'https://car.autohome.com.cn/price/series-{}-0-2-0-0-0-0-1.html'.format(sid)
        pre_sale_car(pre_url=pre_url)

if __name__ == '__main__':
    main()
    print('全部下载完成！')




# for sid in series_on_sale:
#     url = 'https://car.autohome.com.cn/price/series-{}-0-1-0-0-0-0-1.html'.format(sid)
#     cars_on_sale(url)


cursor.close()
conn.cursor()









