import requests
import parsel


url = 'https://www.autohome.com.cn/ev/1/#liststart'

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36',
    'cookie': 'ASP.NET_SessionId=l4ohql3wyvqqta4ncmq3xsy5; fvlid=1613958532248TAolwCopX7; sessionid=E3225414-EC36-4FF8-A653-29E2571ABDE4%7C%7C2021-02-22+09%3A48%3A53.371%7C%7Cwww.baidu.com; autoid=1056bc400f38f087aeb6d17ac3004740; ahpau=1; sessionuid=E3225414-EC36-4FF8-A653-29E2571ABDE4%7C%7C2021-02-22+09%3A48%3A53.371%7C%7Cwww.baidu.com; __ah_uuid_ng=c_E3225414-EC36-4FF8-A653-29E2571ABDE4; Hm_lvt_9924a05a5a75caf05dbbfb51af638b07=1614044481; __utma=1.937942048.1614052392.1614052392.1614052392.1; __utmc=1; __utmz=1.1614052392.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); FootPrints=46809%7C2021-2-23%2C43101%7C2021-2-22%2C43097%7C2021-2-22%2C43099%7C2021-2-22%2C41184%7C2021-2-22%2C; cookieCityId=210100; cityId=375; sessionip=119.119.143.39; area=210106; ahsids=5273_6004_4908_5527_5336_5084; sessionvid=BE691684-2FD3-4571-9B7C-0BCADB8C3F55; Hm_lpvt_9924a05a5a75caf05dbbfb51af638b07=1614244618; pvidchain=3311667,3311667,3311246,3311229; ahpvno=489; v_no=6; visit_info_ad=E3225414-EC36-4FF8-A653-29E2571ABDE4||BE691684-2FD3-4571-9B7C-0BCADB8C3F55||-1||-1||6; ref=www.baidu.com%7C0%7C0%7C0%7C2021-02-25+17%3A18%3A53.454%7C2021-02-22+09%3A48%3A53.371'
}

response = requests.get(url,headers=headers).text
resp = parsel.Selector(response)

li_list = resp.xpath('//div[@id="auto-channel-lazyload-article"]/ul/li')
for li in li_list:
    link = 'https:'+li.xpath('./a/@href').get()
    # print(link)
    title = li.xpath('./a/h3/text()').get()
    print(title)

    response = requests.get(link).text
    resp = parsel.Selector(response)
    content = "".join(resp.xpath('//div[@id="articleContent"]/p/text()').getall())

    print(content)














