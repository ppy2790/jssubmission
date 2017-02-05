#coding=utf-8

from scrapy.spiders import CrawlSpider
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector

from jssubmission.items import JssubmissionItem

import json
import time
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

class JssubmissionSpider(CrawlSpider):

    name = 'submission'

    start_urls=[
        'http://www.jianshu.com/trending/monthly'

    ]

    cookies={
        ## your cookies
    }

    def start_requests(self):

        url = 'http://www.jianshu.com/collections/V2CqjW/collection_submissions.json?state=&page=1'

        return [FormRequest(url,cookies=self.cookies,callback=self.parse)]

    def parse(self, response):

        item = JssubmissionItem()
        selector = Selector(response)

        data = json.loads(response.body)
        collect = data['collection_submissions']

        if len(collect) > 0:
            for cc in collect:
                item['state']= cc['state']
                create_x = int(cc['created_at'])
                create_x = time.localtime(create_x)
                item['create_time'] = time.strftime('%Y-%m-%d %H:%M:%S', create_x)

                title = cc['note']['title']
                item['title'] = title
                nickname = cc['note']['user']['nickname']
                item['nickname'] = nickname
                x = int(cc['note']['first_shared_at'])

                #转化时间戳
                x = time.localtime(x)
                item['sub_time'] = time.strftime('%Y-%m-%d %H:%M:%S', x)

                yield item



        for i in range(2,2676):
            nexturl = 'http://www.jianshu.com/collections/V2CqjW/collection_submissions.json?state=&page=%s'%i

            yield FormRequest(nexturl,cookies=self.cookies,callback=self.parse)





