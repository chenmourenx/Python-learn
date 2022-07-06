import requests
import threading
import queue
import base64


def spider(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_3) AppleWebKit/605.1.15 (KHTML, like Gecko) '
                      'Version/14.1 '
                      'Safari/605.1.15',
    }
    r = requests.get(url=url, headers=headers)
    print(r.status_code, len(r.content))


class JianDna(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self._queue = queue

    def run(self):
        while not self._queue.empty():
            url = self._queue.get_nowait()
            spider(url)


def main():
    queue1 = queue.Queue()
    s = str(base64.b64encode('20220706-'.encode("utf-8")), "utf-8")
    for i in range(2000, 2050):
        queue1.put('http://jandan.net/pic/' + s +
                   str(base64.b64encode(str(i).encode("utf-8")), "utf-8"))

    threads = []
    thread_count = 3

    for i in range(thread_count):
        threads.append(JianDna(queue1))

    for t in threads:
        t.start()

    for t in threads:
        t.join()


if __name__ == '__main__':
    main()
