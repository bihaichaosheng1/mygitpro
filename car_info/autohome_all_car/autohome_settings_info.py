# -*- coding:utf-8 -*-

import parsel
import jsonpath
import json
import re
from datetime import datetime
import aiohttp
import asyncio
import aiofiles
import aiomysql
from aiomysql import create_pool




async def get_html(sid):

    url = 'https://carif.api.autohome.com.cn/Car/Spec_ParamListBySpecList.ashx?speclist={}&_=1599033601180&_callback=__param1'.format(sid)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            dic = await resp.text('gbk')
            dic = dic.replace('__param1(','').replace('})','}')
            car_detail_info = json.loads(dic)

            key_name = jsonpath.jsonpath(car_detail_info, '$..paramitems..name')
            if key_name == False:
                pass
            value_name = jsonpath.jsonpath(car_detail_info, '$..paramitems..valueitems..value')
            item = {}
            # for k,v in zip(key_name,value_name):
            item.update(dict(zip(key_name, value_name)))
            # print(item)


        spec_data_url = f'https://www.autohome.com.cn/spec/{sid}/'
        # 对汽车图片url发起请求
        async with session.get(spec_data_url) as spec_data:
            spec_data = await spec_data.text('gbk')
            resp_data = parsel.Selector(spec_data)
            # print(spec_data_url)

            car_logo = 'https:' +resp_data.xpath('/html/body/div[1]/div[3]/div[4]/div[1]/div[1]/div[2]/div[1]/div[1]/a/span[1]/img/@src').get()
            # print('汽车图片',car_logo)

            car_category_id = resp_data.xpath(
                '//div[@class="container athm-sub-nav article-sub-nav"]/div[@class="athm-sub-nav__car"]/div[@class="athm-sub-nav__car__name"]/a/@href').get().replace(
                '/', '')
            # print('车系id',car_category_id)


            spec_id = str(sid)
            # print('车型id', spec_id)

            car_fullname = jsonpath.jsonpath(item, '$..车型名称')[0]
            # print(car_fullname)

            # 厂商指导价
            car_price = jsonpath.jsonpath(item, '$..厂商指导价(元)')[0].replace('万', '')
            if '~' in car_price:
                car_price = ''.join(re.findall('[0-9.]*~', car_price)).replace('~', '')
            if car_price == '暂无报价':
                car_price = '0.00'
            # print(car_price)

            # 年款
            car_yeartype = ''.join(re.findall('[0-9]*款', car_fullname)).replace('款', '')
            # print(car_yeartype)

            # 在售状态
            sale_type = ''
            """在售车型id"""
            async with aiofiles.open(r'./all_spec_id/autohome_on_spec_id.txt','r')as f:
                async for id in f:
                    if spec_id in id:
                        # print(spec_id)
                        sale_type='在售'

            """停售车型id"""
            async with aiofiles.open(r'./all_spec_id/autohome_halt_spec_id.txt', 'r')as f:
                async for id in f:
                    if spec_id in id:
                        # print(spec_id)
                        sale_type = '停售'

            """预售车型id"""
            async with aiofiles.open(r'./all_spec_id/autohome_pre_spec_id.txt', 'r')as f:
                async for id in f:
                    if spec_id in id:
                        # print(spec_id)
                        sale_type = '预售'

            # print(sale_type)

            envir_standard = jsonpath.jsonpath(item, '$..环保标准')
            if envir_standard == False:
                envir_standard = ['-']
            # print(envir_standard)

            displacement = jsonpath.jsonpath(item, '$..排量(L)')
            if displacement == False:
                displacement = ['-']
            # print(displacement)

            maximum_torque = jsonpath.jsonpath(item, '$..最大扭矩(N・m)')
            if maximum_torque == False:
                maximum_torque = ['-']
            # print(maximum_torque)

            gearbox = jsonpath.jsonpath(item, '$..变速箱')
            if gearbox == False:
                gearbox = ['-']
            # print(gearbox)

            engine = jsonpath.jsonpath(item, '$..发动机')
            if engine == False:
                engine = ['-']
            # print(engine)

            car_size = jsonpath.jsonpath(item, '$..级别')
            if car_size == False:
                car_size = ['-']
            # print(car_size)

            accelerate = jsonpath.jsonpath(item, '$..官方0-100km/h加速(s)')
            if accelerate == False:
                accelerate = ['-']
            # print(accelerate)

            fuel_consumption = jsonpath.jsonpath(item, '$..工信部综合油耗(L/100km)')
            if fuel_consumption == False:
                fuel_consumption = ['-']
            # print(fuel_consumption)

            energy_type = jsonpath.jsonpath(item, '$..能源类型')
            if energy_type == False:
                energy_type = ['-']
            # print(energy_type)

            length_width_height = jsonpath.jsonpath(item, '$..长*宽*高(mm)')
            if length_width_height == False:
                length_width_height = ['-']
            # print(length_width_height)

            maxhorse_power = jsonpath.jsonpath(item, '$..最大马力(Ps)')
            if maxhorse_power == False:
                maxhorse_power = ['-']
            # print(maxhorse_power)

            # last_sync_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            last_sync_time = datetime.now().strftime("%Y-%m-28 23:35:23")
            # print(last_sync_time)

            data = (spec_id, car_fullname, car_logo, car_category_id, car_price, car_yeartype, sale_type, car_size[0],
                    envir_standard[0],
                    displacement[0] + 'L', maximum_torque[0] + 'N.m', maxhorse_power[0] + 'Ps', length_width_height[0],
                    fuel_consumption[0] + 'L/100km', energy_type[0], accelerate[0], engine[0], gearbox[0], last_sync_time)

            print(data)


            # 异步链接数据库
            async with create_pool(host='127.0.0.1', user='root', password='', port=3306, db='jdbc') as pool:
                async with pool.get() as conn:
                    async with conn.cursor() as cur:

                        sql2 = "select * from t_car_detail where spec_id='{}'".format(data[0])
                        await cur.execute(sql2)
                        many = await cur.fetchone()
                        if many:
                            # print('此数据表中已存在')
                            sql = "UPDATE  t_car_detail SET  sale_type='{}' ,fuel_consumption='{}', last_sync_time='{}' WHERE spec_id='{}'".format(
                                data[6], data[13], data[18], data[0])
                            await cur.execute(sql)
                            await conn.commit()
                            # print('数据已更新')
                        else:

                            insert_sql = 'insert into t_car_detail(spec_id, car_fullname, car_logo, car_category_id, car_price, car_yeartype, sale_type, car_size, envir_standard,displacement, maximum_torque, maxhorse_power,length_width_height,fuel_consumption, energy_type, accelerate, engine, gearbox,last_sync_time) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                            await cur.execute(insert_sql, data)
                            await conn.commit()  # 提交数据
                            # print('数据提交完成')

        cur.close()
        conn.close()
        print('数据库连接已关闭')

async def main():
    async with aiofiles.open(r'./all_spec_id/autohome_spec_id.txt') as f:
        async for id in f:
            id_list = id.replace(' ','').split(',')

    for sid in id_list:
        tasks = []
        tasks.append(get_html(sid))
        await asyncio.wait(tasks)

if __name__ == '__main__':
    asyncio.run(main())
    print('全部下载完成')

