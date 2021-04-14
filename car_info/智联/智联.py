# -*- coding:utf-8 -*-

import requests
import jsonpath



for page in range(1,22):
    url = 'https://sou.zhaopin.com/?p={}&jl=536&kw=%E6%B1%BD%E8%BD%A6%E9%94%80%E5%94%AE&kt=3'.format(page)
    print(url)
    #  智联 沈阳销售顾问
    """
    https://sou.zhaopin.com/?p=1&jl=599&kw=%E6%B1%BD%E8%BD%A6%E9%94%80%E5%94%AE&kt=3
https://sou.zhaopin.com/?p=2&jl=599&kw=%E6%B1%BD%E8%BD%A6%E9%94%80%E5%94%AE&kt=3
https://sou.zhaopin.com/?p=3&jl=599&kw=%E6%B1%BD%E8%BD%A6%E9%94%80%E5%94%AE&kt=3
https://sou.zhaopin.com/?p=4&jl=599&kw=%E6%B1%BD%E8%BD%A6%E9%94%80%E5%94%AE&kt=3
https://sou.zhaopin.com/?p=5&jl=599&kw=%E6%B1%BD%E8%BD%A6%E9%94%80%E5%94%AE&kt=3
https://sou.zhaopin.com/?p=6&jl=599&kw=%E6%B1%BD%E8%BD%A6%E9%94%80%E5%94%AE&kt=3
https://sou.zhaopin.com/?p=7&jl=599&kw=%E6%B1%BD%E8%BD%A6%E9%94%80%E5%94%AE&kt=3
https://sou.zhaopin.com/?p=8&jl=599&kw=%E6%B1%BD%E8%BD%A6%E9%94%80%E5%94%AE&kt=3
https://sou.zhaopin.com/?p=9&jl=599&kw=%E6%B1%BD%E8%BD%A6%E9%94%80%E5%94%AE&kt=3
https://sou.zhaopin.com/?p=10&jl=599&kw=%E6%B1%BD%E8%BD%A6%E9%94%80%E5%94%AE&kt=3
https://sou.zhaopin.com/?p=11&jl=599&kw=%E6%B1%BD%E8%BD%A6%E9%94%80%E5%94%AE&kt=3
https://sou.zhaopin.com/?p=12&jl=599&kw=%E6%B1%BD%E8%BD%A6%E9%94%80%E5%94%AE&kt=3
https://sou.zhaopin.com/?p=13&jl=599&kw=%E6%B1%BD%E8%BD%A6%E9%94%80%E5%94%AE&kt=3
https://sou.zhaopin.com/?p=14&jl=599&kw=%E6%B1%BD%E8%BD%A6%E9%94%80%E5%94%AE&kt=3
https://sou.zhaopin.com/?p=15&jl=599&kw=%E6%B1%BD%E8%BD%A6%E9%94%80%E5%94%AE&kt=3
https://sou.zhaopin.com/?p=16&jl=599&kw=%E6%B1%BD%E8%BD%A6%E9%94%80%E5%94%AE&kt=3
https://sou.zhaopin.com/?p=17&jl=599&kw=%E6%B1%BD%E8%BD%A6%E9%94%80%E5%94%AE&kt=3
https://sou.zhaopin.com/?p=18&jl=599&kw=%E6%B1%BD%E8%BD%A6%E9%94%80%E5%94%AE&kt=3
https://sou.zhaopin.com/?p=19&jl=599&kw=%E6%B1%BD%E8%BD%A6%E9%94%80%E5%94%AE&kt=3
https://sou.zhaopin.com/?p=20&jl=599&kw=%E6%B1%BD%E8%BD%A6%E9%94%80%E5%94%AE&kt=3
    """

    # 智联 辽宁销售顾问
    """
    https://sou.zhaopin.com/?p=1&jl=535&kw=%E6%B1%BD%E8%BD%A6%E9%94%80%E5%94%AE&kt=3
https://sou.zhaopin.com/?p=2&jl=535&kw=%E6%B1%BD%E8%BD%A6%E9%94%80%E5%94%AE&kt=3
https://sou.zhaopin.com/?p=3&jl=535&kw=%E6%B1%BD%E8%BD%A6%E9%94%80%E5%94%AE&kt=3
https://sou.zhaopin.com/?p=4&jl=535&kw=%E6%B1%BD%E8%BD%A6%E9%94%80%E5%94%AE&kt=3
https://sou.zhaopin.com/?p=5&jl=535&kw=%E6%B1%BD%E8%BD%A6%E9%94%80%E5%94%AE&kt=3
https://sou.zhaopin.com/?p=6&jl=535&kw=%E6%B1%BD%E8%BD%A6%E9%94%80%E5%94%AE&kt=3
https://sou.zhaopin.com/?p=7&jl=535&kw=%E6%B1%BD%E8%BD%A6%E9%94%80%E5%94%AE&kt=3
https://sou.zhaopin.com/?p=8&jl=535&kw=%E6%B1%BD%E8%BD%A6%E9%94%80%E5%94%AE&kt=3
https://sou.zhaopin.com/?p=9&jl=535&kw=%E6%B1%BD%E8%BD%A6%E9%94%80%E5%94%AE&kt=3
https://sou.zhaopin.com/?p=10&jl=535&kw=%E6%B1%BD%E8%BD%A6%E9%94%80%E5%94%AE&kt=3
https://sou.zhaopin.com/?p=11&jl=535&kw=%E6%B1%BD%E8%BD%A6%E9%94%80%E5%94%AE&kt=3
https://sou.zhaopin.com/?p=12&jl=535&kw=%E6%B1%BD%E8%BD%A6%E9%94%80%E5%94%AE&kt=3
https://sou.zhaopin.com/?p=13&jl=535&kw=%E6%B1%BD%E8%BD%A6%E9%94%80%E5%94%AE&kt=3
https://sou.zhaopin.com/?p=14&jl=535&kw=%E6%B1%BD%E8%BD%A6%E9%94%80%E5%94%AE&kt=3
https://sou.zhaopin.com/?p=15&jl=535&kw=%E6%B1%BD%E8%BD%A6%E9%94%80%E5%94%AE&kt=3
https://sou.zhaopin.com/?p=16&jl=535&kw=%E6%B1%BD%E8%BD%A6%E9%94%80%E5%94%AE&kt=3
https://sou.zhaopin.com/?p=17&jl=535&kw=%E6%B1%BD%E8%BD%A6%E9%94%80%E5%94%AE&kt=3
https://sou.zhaopin.com/?p=18&jl=535&kw=%E6%B1%BD%E8%BD%A6%E9%94%80%E5%94%AE&kt=3
https://sou.zhaopin.com/?p=19&jl=535&kw=%E6%B1%BD%E8%BD%A6%E9%94%80%E5%94%AE&kt=3
https://sou.zhaopin.com/?p=20&jl=535&kw=%E6%B1%BD%E8%BD%A6%E9%94%80%E5%94%AE&kt=3
https://sou.zhaopin.com/?p=21&jl=535&kw=%E6%B1%BD%E8%BD%A6%E9%94%80%E5%94%AE&kt=3
https://sou.zhaopin.com/?p=22&jl=535&kw=%E6%B1%BD%E8%BD%A6%E9%94%80%E5%94%AE&kt=3
https://sou.zhaopin.com/?p=23&jl=535&kw=%E6%B1%BD%E8%BD%A6%E9%94%80%E5%94%AE&kt=3
https://sou.zhaopin.com/?p=24&jl=535&kw=%E6%B1%BD%E8%BD%A6%E9%94%80%E5%94%AE&kt=3
https://sou.zhaopin.com/?p=25&jl=535&kw=%E6%B1%BD%E8%BD%A6%E9%94%80%E5%94%AE&kt=3
https://sou.zhaopin.com/?p=26&jl=535&kw=%E6%B1%BD%E8%BD%A6%E9%94%80%E5%94%AE&kt=3
https://sou.zhaopin.com/?p=27&jl=535&kw=%E6%B1%BD%E8%BD%A6%E9%94%80%E5%94%AE&kt=3
https://sou.zhaopin.com/?p=28&jl=535&kw=%E6%B1%BD%E8%BD%A6%E9%94%80%E5%94%AE&kt=3
https://sou.zhaopin.com/?p=29&jl=535&kw=%E6%B1%BD%E8%BD%A6%E9%94%80%E5%94%AE&kt=3
https://sou.zhaopin.com/?p=30&jl=535&kw=%E6%B1%BD%E8%BD%A6%E9%94%80%E5%94%AE&kt=3
https://sou.zhaopin.com/?p=31&jl=535&kw=%E6%B1%BD%E8%BD%A6%E9%94%80%E5%94%AE&kt=3
https://sou.zhaopin.com/?p=32&jl=535&kw=%E6%B1%BD%E8%BD%A6%E9%94%80%E5%94%AE&kt=3
https://sou.zhaopin.com/?p=33&jl=535&kw=%E6%B1%BD%E8%BD%A6%E9%94%80%E5%94%AE&kt=3
https://sou.zhaopin.com/?p=34&jl=535&kw=%E6%B1%BD%E8%BD%A6%E9%94%80%E5%94%AE&kt=3
    """
    # 智联 吉林销售顾问
    """
    https://sou.zhaopin.com/?p=1&jl=536&kw=%E6%B1%BD%E8%BD%A6%E9%94%80%E5%94%AE&kt=3
https://sou.zhaopin.com/?p=2&jl=536&kw=%E6%B1%BD%E8%BD%A6%E9%94%80%E5%94%AE&kt=3
https://sou.zhaopin.com/?p=3&jl=536&kw=%E6%B1%BD%E8%BD%A6%E9%94%80%E5%94%AE&kt=3
https://sou.zhaopin.com/?p=4&jl=536&kw=%E6%B1%BD%E8%BD%A6%E9%94%80%E5%94%AE&kt=3
https://sou.zhaopin.com/?p=5&jl=536&kw=%E6%B1%BD%E8%BD%A6%E9%94%80%E5%94%AE&kt=3
https://sou.zhaopin.com/?p=6&jl=536&kw=%E6%B1%BD%E8%BD%A6%E9%94%80%E5%94%AE&kt=3
https://sou.zhaopin.com/?p=7&jl=536&kw=%E6%B1%BD%E8%BD%A6%E9%94%80%E5%94%AE&kt=3
https://sou.zhaopin.com/?p=8&jl=536&kw=%E6%B1%BD%E8%BD%A6%E9%94%80%E5%94%AE&kt=3
https://sou.zhaopin.com/?p=9&jl=536&kw=%E6%B1%BD%E8%BD%A6%E9%94%80%E5%94%AE&kt=3
https://sou.zhaopin.com/?p=10&jl=536&kw=%E6%B1%BD%E8%BD%A6%E9%94%80%E5%94%AE&kt=3
https://sou.zhaopin.com/?p=11&jl=536&kw=%E6%B1%BD%E8%BD%A6%E9%94%80%E5%94%AE&kt=3
https://sou.zhaopin.com/?p=12&jl=536&kw=%E6%B1%BD%E8%BD%A6%E9%94%80%E5%94%AE&kt=3
https://sou.zhaopin.com/?p=13&jl=536&kw=%E6%B1%BD%E8%BD%A6%E9%94%80%E5%94%AE&kt=3
https://sou.zhaopin.com/?p=14&jl=536&kw=%E6%B1%BD%E8%BD%A6%E9%94%80%E5%94%AE&kt=3
https://sou.zhaopin.com/?p=15&jl=536&kw=%E6%B1%BD%E8%BD%A6%E9%94%80%E5%94%AE&kt=3
https://sou.zhaopin.com/?p=16&jl=536&kw=%E6%B1%BD%E8%BD%A6%E9%94%80%E5%94%AE&kt=3
https://sou.zhaopin.com/?p=17&jl=536&kw=%E6%B1%BD%E8%BD%A6%E9%94%80%E5%94%AE&kt=3
https://sou.zhaopin.com/?p=18&jl=536&kw=%E6%B1%BD%E8%BD%A6%E9%94%80%E5%94%AE&kt=3
https://sou.zhaopin.com/?p=19&jl=536&kw=%E6%B1%BD%E8%BD%A6%E9%94%80%E5%94%AE&kt=3
https://sou.zhaopin.com/?p=20&jl=536&kw=%E6%B1%BD%E8%BD%A6%E9%94%80%E5%94%AE&kt=3
https://sou.zhaopin.com/?p=21&jl=536&kw=%E6%B1%BD%E8%BD%A6%E9%94%80%E5%94%AE&kt=3
    """



























