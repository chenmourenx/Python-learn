import requests
from bs4 import BeautifulSoup as bs
import threading
import queue
import urllib.request
import base64

url = 'http://jandan.net/pic/MjAyMjA3MDYtMTg2#comments'


def spider(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_3) AppleWebKit/605.1.15 (KHTML, like Gecko) '
                      'Version/14.1 '
                      'Safari/605.1.15',
    }
    r = requests.get(url=url, headers=headers)
    soup = bs(r.content, 'lxml')
    imgs = soup.find_all(name='img', attrs={})
    for img in imgs:
        if 'onload' in str(img):
            img = 'http:'+img['org_src']
        else:
            img = 'http:'+img['src']
        name = img.split('/')[-1]
        urllib.request.urlretrieve(img, filename='img/' + name)


class JianDan(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self._queue = queue

    def run(self):
        while not self._queue.empty():
            url1 = self._queue.get_nowait()
            spider(url1)


def main():
    queue1 = queue.Queue()
    s = str(base64.b64encode('20220706-'.encode("utf-8")), "utf-8")
    for i in range(100, 101):
        queue1.put('http://jandan.net/pic/' + s +
                   str(base64.b64encode(str(i).encode("utf-8")), "utf-8"))
    threads = []
    thread_count = 3

    for i in range(thread_count):
        threads.append(JianDan(queue1))

    for t in threads:
        t.start()

    for t in threads:
        t.join()


if __name__ == '__main__':
    main()
