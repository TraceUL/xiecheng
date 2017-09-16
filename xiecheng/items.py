# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
from scrapy import Item,Field


class Xiechengitem(Item):
    table_name='jipiao'


    # nameid=Field()
    航班 = Field()
    起飞时间 =Field()
    到达时间 = Field()
    出发站台 = Field()
    到达站台 = Field()
    廊桥率 = Field()
    准点率 = Field()
    民航发展基金 = Field()
