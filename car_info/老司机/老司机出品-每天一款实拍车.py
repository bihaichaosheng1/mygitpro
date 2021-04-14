

"""
老司机出品-每天一款实拍车
"""

import requests
import parsel
import jsonpath


# post请求
url = 'https://www.laosiji.com/api/hotShow/program'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36',
    'Cookie': 'sogouPlatform=null; dubaReferer=null; LSJCITYOBJ=%7B%22code%22%3A131%2C%22name%22%3A%22%E5%8C%97%E4%BA%AC%22%7D; OdStatisticsToken=0d641b24-32c4-45d7-8bcc-ea311d88aa5f-1612771815683; LSJLOGCOOKIE=11911911946108971111151051061054699111109-17265661-1612771816005; UM_distinctid=17780b0f24d956-0ca508e565698d-33e3567-144000-17780b0f24e204; Hm_lvt_9fa8070d0f1a747dc1fd8cc5bdda4088=1612771816; _ga=GA1.2.205457555.1612771842; _gid=GA1.2.527094914.1612771842; CNZZDATA1261736092=1008066312-1612768801-https%253A%252F%252Fwww.baidu.com%252F%7C1612772277; Hm_lpvt_9fa8070d0f1a747dc1fd8cc5bdda4088=1612774277; JSESSIONID=2ED8245E746757AFA5FDF05B6864FB66'
}

for page in range(1,11):
    data = {
        'hotShowId': '128',
        'sort': '1',
        'pageNo': page
    }

    # 发起请求
    response = requests.post(url=url,headers=headers,data=data).json()

    video_url = jsonpath.jsonpath(response,'$..bdinfo..url')
    # print(video_url)

    publishtime = jsonpath.jsonpath(response,'$..publishtime')
    # print(publishtime)

    title = jsonpath.jsonpath(response,'$..sns.list..title')[0::2]
    # print(title)

    head_portrait = jsonpath.jsonpath(response,'$..sns.list..user.image.url')
    # print(head_portrait)

    letterAndName = jsonpath.jsonpath(response,'$..sns.list..user.letterAndName')
    # print(letterAndName)

    cover_photo = jsonpath.jsonpath(response,'$..list..image.url')[0::3]
    # print(cover_photo)

    type = '10'

    for t,v,p,h,l,c in zip(title,video_url,publishtime,head_portrait,letterAndName,cover_photo):
        print(t,v,p,h,l,c,type)




