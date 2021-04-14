# # -*- coding:utf-8 -*-
#
# """
# 汽车之家，所有车型配置
# """
#
# import requests
# import jsonpath
# import numpy as np
# import json
# import pymongo
# import re
# import pinyin.cedict
#
# # 连接 mongoDB
# client = pymongo.MongoClient(host='127.0.0.1',port=27017)
#
# db = client.autohome_pk    # 选择库
#
# p = db.pk    # 选择库中的集合
#
# """从文件中读取车型id数据"""
# data = np.loadtxt('C:/mypythonfile/car_info/autohome_all_car/autohome_spec_id.txt', delimiter=',')
# # 输出结果是numpy中数组格式
# id_list = []
# for num in data:
#     num1 = str(num).replace('.0', '')
#     id_list.append(num1)
# print(len(id_list))
#
#
#
# headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
#         'Connection': 'close'
#     }
# car_info_list = []
# for id in id_list:
#     url = 'https://carif.api.autohome.com.cn/Car/Spec_ParamListBySpecList.ashx?speclist={}&_=1599033601180&_callback=__param1'.format(id)
#
#     resp = requests.get(url,headers=headers)
#
#     car_detail = resp.text
#
#     car_detail_infop = car_detail.replace('__param1(', '')
#
#     car_detail_infoq = car_detail_infop.replace('})', '}')
#
#     car_detail_info = json.loads(car_detail_infoq)
#
#     print('---------------------------------------------------------------------------------------')
#     print('正在获取的url',url)
#
#     # 解析获取数据
#     try:
#         spec_id = jsonpath.jsonpath(car_detail_info['result']['paramtypeitems'][0]['paramitems'][0], '$..specid').pop()
#         # print('车型id',spec_id)
#
#         # 所有 name
#         name = jsonpath.jsonpath(car_detail_info['result']['paramtypeitems'], '$..paramitems..name')
#         # print(name)
#
#         # 所有 value
#         value = jsonpath.jsonpath(car_detail_info['result']['paramtypeitems'], '$..value')
#         print('所有value',value)
#         # print(len(value))
#
#
#
#
#         # 对车型配置后半段抓取
#         wer = 'https://carif.api.autohome.com.cn/Car/v2/Config_ListBySpecIdList.ashx?speclist={}&_=1600826349285&_callback=__config3'.format(id)
#         resp_h = requests.get(wer,headers=headers)
#         car_detail_h = resp_h.text
#
#         car_detail_info_h = car_detail_h.replace('__config3(', '')
#
#         car_detail_info_h_q = car_detail_info_h.replace('})', '}')
#
#         car_detail_h_info = json.loads(car_detail_info_h_q)['result']['configtypeitems']
#
#         print('后半部分请求的url',wer)
#
#
#         name_h = jsonpath.jsonpath(car_detail_h_info,'$..configitems..name')
#         print(name_h)
#         name_s_h = []
#         for n in name_h:
#             ret = re.sub(u"&nbsp", "", n).replace('.','。')
#             name_s_h.append(ret)
#
#         value_h = jsonpath.jsonpath(car_detail_h_info,'$..value')
#
#
#         value_h_s = jsonpath.jsonpath(car_detail_h_info,'$..sublist')
#
#
#         value_half = []
#         for va,vas in zip(value_h,value_h_s):
#             va = va.replace('&nbsp','').replace(';','')
#
#             if va == '':
#                 va = jsonpath.jsonpath(vas,'$..subname')
#                 if va == False:
#                     va = '-'
#                 value_half.append(va)
#
#
#         """后半部分配置信息"""
#         car_configuration_h = {}
#         car_configuration_h.update(dict(zip(name_s_h, value_half)))
#         # print(car_configuration_h)
#
#
#         """前半部分配置信息"""
#         car_configuration_d = {}
#         car_configuration_d['车型id'] = str(spec_id)
#         car_configuration_d.update(dict(zip(name,value)),)
#
#         """将后半部分配置信息于牵绊部分信息拼接"""
#         car_configuration_d.update(car_configuration_h)
#
#         # print(car_configuration_d)
#
#
#         # 取出字典的第一对值
#         one_keyandvalue = car_configuration_d['车型id']
#         # print('第一对键值',one_keyandvalue)
#
#         # 入库前判断 存在跳出本次循环，否则出入数据库
#         # res = p.count_documents({'车型id':one_keyandvalue})  # 在数据库中出现的次数
#         # print(res)
#         # if res != 0:
#         #     print("有")
#         #     # continue
#         # else:
#         #     # 向mongo插入数据
#         #     ret = p.insert_one(car_configuration_d)
#         #     print('正在向mongo插入数据')
#     except IndexError as e:
#         print('输出错误：',e)
#         continue
#





















