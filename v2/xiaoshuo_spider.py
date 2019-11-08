import requests
import os
from bs4 import BeautifulSoup
import http
import time
#url请求地址
headers={
'user-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
}
urls=[0]
urls[0]=input("请输入爬取小说的第一章：")

time_start = time.time() #开始计时
for url in urls:
    #发起请求
    repage = requests.get(url,headers = headers)
    #utf-8编码
    repage.encoding = 'utf-8'
    #解释网页
    soup = BeautifulSoup(repage.text,'html.parser')
    ##位置
    names =soup.select('.bdsub dl dt a')
    name_text=names[5].string
    title =soup.select('.bdsub dd h1')
    next_links=soup.select('.bdsub dd h3 a')
    content=soup.select('#contents')
    title_text=(title[0].string)
    if(len(content)==0):
        time_end = time.time()    #结束计时
        time_sum= time_end - time_start
        print("小说<<:-"+name_text+">>-保存成功...")
        print("用时:{0}s",time_sum)
        break
    content_text=content[0].text
    next_url=next_links[2]['href']
    urls.append('https://www.ddxsku.com'+next_url)
    io = open('{0}.txt'.format(title_text), "ab+")
    io.write(content_text.encode('UTF-8')) 
    print(title_text+'-'+"保存成功...")
   
    if(url==""):
        time_end = time.time()    #结束计时
        time_sum= time_end - time_start
        print("小说<<:-"+name_text+">>-保存成功...")
        print("用时:{0}s",time_sum)
        break

    
    

 
