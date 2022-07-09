import requests
from bs4 import BeautifulSoup as bs
import time
import re


def proxy_spider():
    url = 'https://free.kuaidaili.com/free/inha/'
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_3) AppleWebKit/605.1.15 (KHTML, like Gecko) '
                      'Version/14.1 Safari/605.1.15 '
    }
    r = requests.get(url=url, headers=headers)
    soup = bs(r.content, 'lxml')
    datas = soup.find_all(name='td', attrs={'data-title': ['IP', 'PORT', '类型']})

    i = 0
    j = 0
    x = 0
    ip = []
    port = []
    types = []
    for data in datas:
        soup_proxy_content = bs(str(data), 'lxml')
        soup_proxys = soup_proxy_content.find_all(name='td')
        if '.' in soup_proxys[0].string:
            ip.append(soup_proxys[0].string)
            i += 1
        elif 'HTTP' in soup_proxys[0].string:
            types.append(soup_proxys[0].string)
            j += 1
        else:
            port.append(soup_proxys[0].string)
            x += 1
    for y in range(0, i):
        proxy_check(ip[y], port[y], types[y])


def proxy_check(ip, port, types):
    # url = 'https://ip.tool.chinaz.com/'
    url = 'http://httpbin.org/ip'
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_3) AppleWebKit/605.1.15 (KHTML, like Gecko) '
                      'Version/14.1 Safari/605.1.15 ',

    }
    proxy = {}
    proxy[types.lower()] = '%s://%s:%s' % (types.lower(), ip, port)
    try:
        r = requests.get(url=url, headers=headers, proxies=proxy, timeout=6)
        html = r.text

        # 站长工具,不知道为什么总是显示自己IP
        # soup = bs(r.content, 'lxml')
        # ip_attr = soup.find_all(name='dd', attrs={'class': 'fz24'})
        # ip_content = ip_attr[0].string.strip()

        # httpbin.org/ip
        ip_attr = re.findall('"origin": "(.*?)"', html)
        ip_content = ip_attr[0]
        if ip == ip_content:
            print('%s:%s' % (ip, port))
            time.sleep(1)
    except Exception:
        pass


if __name__ == '__main__':
    proxy_spider()
