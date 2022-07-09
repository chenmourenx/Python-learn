import requests #数据请求模块
import re #正则
import os #文件操作


filename='music\\'
#如果没有这个文件夹，就创建
if not os.path.exists(filename):
    os.mkdir(filename)

url = 'https://music.163.com/discover/toplist?id=3778678'
headers = {
    'user_agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
}
response = requests.get(url, headers=headers)
#print (response.text)

#通过正则表达式提取出歌曲的ID和歌名
html_data=re.findall('<li><a href="/song\?id=(\d+)">(.*?)</a>',response.text)
#print (html_data)
for num_id,title in html_data:
    #获取音乐url的api
    music_url=f'http://music.163.com/song/media/outer/url?id=(num_id).mp3'
    #对音乐url发送请求，获取字节流
    music_content=requests.get(url=music_url,headers=headers).content
    with open(filename+title+'.mp3',mode='wb') as f:
        f.write(music_content)
    print (num_id,title)