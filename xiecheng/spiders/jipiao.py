# -*- coding: utf-8 -*-
import json
from lxml import etree
import time
import scrapy
from scrapy import Request
from xiecheng.items import Xiechengitem


class JipiaoSpider(scrapy.Spider):
    name = 'jipiao'
    allowed_domains = ['www.xiecheng.com']
    url='http://flights.ctrip.com/domesticsearch/search/SearchFirstRouteFlights?DCity1={startcity}&ACity1={destination}&SearchType=S&DDate1={date}&IsNearAirportRecommond=0&LogToken=277dded647224a66991ef3ff148242a7&rk=9.263879129561538094159&CK=D94A15198037F57D1DC5318B9A1156CE&r'+\
        '=0.4356206129208536792212'
    # startct='BJS'
    # destination='SHA'

    #tomorrow time
    date=str(time.strftime('%Y-%m-%d+1',time.localtime(time.time())))
    cookie={'_abtest_userid':'2356fe41-ed44-4471-bd8a-e8b5cdd2228e',' adscityen':'Guangzhou',' Customer':'HAL=ctrip_cn',' _ctm_t':'ctrip',' Session':'smartlinkcode=U135371&smartlinklanguage=zh&SmartLinkKeyWord=&SmartLinkQuary=&SmartLinkHost=',' Union':'AllianceID=4899&SID=135371&OUID=&Expires=1504660817981',' appFloatCnt':'1',' manualclose':'1',' DomesticUserHostCity':'CAN|%b9%e3%d6%dd',' FD_SearchHistorty':{"type":"S","data":"S%24%u5317%u4EAC%28BJS%29%24BJS%242017-09-02%24%u4E0A%u6D77%28SHA%29%24SHA"},' _bfa':'1.1504056015251.1zfab6.1.1504056015251.1504056015251.1.29',' _bfs':'1.29',' page_time':'1504058770846%2C1504059419727%2C1504059420028%2C1504059519723%2C1504059520024%2C1504060705007%2C1504060705248%2C1504060714929%2C1504060715215%2C1504061060640%2C1504061061692%2C1504061072128%2C1504061072386%2C1504061078207%2C1504061078454%2C1504061088321%2C1504061088582%2C1504061111166%2C1504061111448%2C1504061669077%2C1504061669745%2C1504061746001%2C1504061746271%2C1504061756285%2C1504061756528',' _RF1':'14.30.97.87',' _RSG':'2DaECPsqRZAcrKc2eSy4c9',' _RGUID':'a8dbd366-4c3a-4342-9984-f1ca02994d66',' _ga':'GA1.2.480365116.1504056018',' _gid':'GA1.2.1937278920.1504056018',' __zpspc':'9.1.1504056018.1504061759.22%233%7Cwww.google.com%7C%7C%7C%7C%23',' MKT_Pagesource':'PC',' _jzqco':'%7C%7C%7C%7C1504056082082%7C1.1145258682.1504056018064.1504061748939.1504061759279.1504061748939.1504061759279.undefined.0.0.22.22',' _bfi':'p1%3D101027%26p2%3D101027%26v1%3D29%26v2%3D28'}
    hotflylist='http://flights.ctrip.com/booking/hot-city-flights-sitemap.html'


    user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'

    def start_requests(self):

        yield Request(self.hotflylist,cookies=self.cookie,callback=self.parse1)

    def parse2(self,response):
        name=response.url[78:81]
        ID=response.url[89:92]
        # nameid=str(name)+'----'+str(ID)
        html=json.loads(response.text)

        fis=html['fis']
        for f in fis:
            flight=f['fn']
            fly_time=f['dt']
            arrival_time=f['at']
            fly_station=f['dpbn']
            arrival_station=f['apbn']
            depart_brigdge=json.loads(f['confort'])['DepartBridge']
            History_Puntuality=json.loads(f['confort'])['HistoryPunctuality']
            tax=f['tax']



            #保存到items一下
            航班=flight
            起飞时间=fly_time
            到达时间=arrival_time
            廊桥率=depart_brigdge
            准点率=History_Puntuality
            出发站台=fly_station
            到达站台=arrival_station
            民航发展基金= tax
            xcitems = Xiechengitem()
            for field in xcitems.fields:
                try:
                    xcitems[field]=eval(field)
                except NameError:
                    print('Field is not Defined',field)
            yield xcitems


            
            # print("航班:",flight)
            # print("起飞时间:",fly_time)
            # print("到达时间:",arrival_time)
            # print("廊桥率：",depart_brigdge)
            # print("准点率:",History_Puntuality)
            # print("出发站台:",fly_station)
            # print("到达站台:",arrival_station)
            # print("民航发展基金：",tax)
            # priecs=f['scs']
            # for price in priecs:
            #     alt_price = price['salep']
            #     print("可选价位:",alt_price)
            # print("=========================================")


    def parse1(self,response):
        html=response.text
        name=etree.HTML(str(html)).xpath('//*[@id="ctl00_MainContentPlaceHolder_Lb_HotFlightRout"]/a/text()')
        list = etree.HTML(str(html)).xpath('//*[@id="ctl00_MainContentPlaceHolder_Lb_HotFlightRout"]/a/@href')
        for li in list:

            startct = li[33:36]
            destination = li[37:40]
            yield Request(self.url.format(startcity=startct, destination=destination, date=self.date),
                          cookies=self.cookie, callback=self.parse2,dont_filter=True)


