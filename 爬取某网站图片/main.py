import re
import requests
import os

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
}
response = requests.get('https://www.vmgirls.com/17081.html', headers=headers)
html = response.text
# print(response.text)
dir_name = re.findall('<h1 class="post-title mb-3">(.*?)</h1>', html)[-1]
if not os.path.exists(dir_name):
    os.makedirs(dir_name)
urls = re.findall('<a href="(.*?)" alt=".*?" title=".*?">', html)
print(urls)


# for url in urls:
#     # time.sleep(1)
#     file_name = url.split('/')[-1]
#     response = requests.get("https:" + url, headers=headers)
#     with open(dir_name + '/' + file_name, 'wb') as f:
#         f.write(response.content)

# 按间距中的绿色按钮以运行脚本。
# if __name__ == '__main__':
#     main()