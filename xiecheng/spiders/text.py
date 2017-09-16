# import requests
# from lxml import etree
#
#
# html=requests.get('http://flights.ctrip.com/booking/hot-city-flights-sitemap.html').text
#
#
# list=etree.HTML(str(html)).xpath('//*[@id="ctl00_MainContentPlaceHolder_Lb_HotFlightRout"]/a/@href')
#
# for i in list:
#     start=i[33:36]
#     ends=i[37:40]
#     print(start,'-----',ends)
