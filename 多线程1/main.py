import requests
import json
import threading
import time


def spider(data):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0 Waterfox/56.6.2022.06'
    }
    url = 'https://www.ichunqiu.com/courses/ajaxCourses'
    r = requests.post(url=url, headers=headers, data=data)
    # print(r.status_code)
    datas = json.loads(r.content)

    for data in datas['course']['result']:
        print(data['courseName'], data['producerName'])


for i in range(1, 10):
    data = 'courseTag=&courseDiffcuty=&IsExp=&producerId=&orderField=&orderDirection=&pageIndex=2&tagType=&isOpen=' + \
           str(i)
    threading._start_new_thread(spider, (data,))
    time.sleep(0.1)
