


import requests
import jsonpath
import parsel


for page in range(0,11):
    url = "https://www.dongchedi.com/motor/searchapi/search_content/?keyword=%E6%96%B0%E8%83%BD%E6%BA%90&offset={}0&count=10&cur_tab=1&city_name=%E6%B2%88%E9%98%B3&motor_source=pc&format=json".format(page)
    print(url)
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36',
        'cookie': 'tt_webid=6933103760962012680; MONITOR_WEB_ID=a84c2806-b6ea-41e8-99fc-64be0ffca2cb; UM_distinctid=177d824b9745cc-0c31c4176a17fe-73e356b-144000-177d824b975515; CNZZDATA1278124308=762550460-1614237319-https%253A%252F%252Fwww.baidu.com%252F%7C1614237319; xgplayer_device_id=66397566939; xgplayer_user_id=160743885262'
    }

    response = requests.get(url,headers=headers).json()
    # print(response)
    title_list = jsonpath.jsonpath(response,'$..share_info.share_text')
    # print(len(title_list))
    # print(title_list)

    cover_photo = jsonpath.jsonpath(response, '$..share_info.share_image')
    # print(cover_photo)

    link = jsonpath.jsonpath(response,'$..share_info.share_url')
    # print(link)
    for detail_link,title in zip(link,title_list):
        content = requests.get(detail_link).text
        # print(content)
        content_resp = parsel.Selector(content)
        code_content = content_resp.xpath('//article[@class="jsx-655012078"]').get()
        pa = "懂车帝"
        if pa in code_content:
            pa = "竞车"
        print(code_content)
        # p_list = content_resp.xpath('//article[@id="article"]/p')
        # print('标题：',title)
        # for p in p_list:
        #     # print(p)
        #     content = p.xpath('.//text()').get()
        #     if content == None:
        #         pass
        #     else:
        #         print(content)





