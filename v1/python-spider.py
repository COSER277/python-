import requests
import os
from bs4 import BeautifulSoup
import http
import time
import random

#请求头
headers={
    'user-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8',
    'Cookie': 'Hm_lvt_ce0cbeec14a385423f05b3b8791b5042=1572934891,1573125046; Hm_lpvt_ce0cbeec14a385423f05b3b8791b5042=1573138556'
}

#网站地址
path="dingdianxiaoshuodizhi 你懂得"
#分类列表
categoryList=[]
#小说列表
storyList=[]
#小说的章节地址
urls=[]
# 设置存储目录
def setDir(bookname):
    _dir="stories"
    _filedir="{0}".format(bookname)
    if _dir not in os.listdir('./'):
        Dir=_dir+"/"+_filedir
        os.makedirs(Dir)
    if _filedir not in os.listdir('./stories/'):
       os.makedirs(_dir+"/"+_filedir) 
        
#1获取分类
def GetCategories(url):
    IPS=[
        {'HTTPS':'https://115.237.16.200:8118'},
        {'HTTPS':'https://42.49.119.10:8118'},
        {'HTTPS':'https://60.174.74.40:8118'}
    ]
    IP=random.choice(IPS)
    res=requests.get(url,headers=headers,proxies=IP)
    res.encoding='utf-8'
    html=res.text
    page=BeautifulSoup(html,'html.parser')
    categories=page.select('.m_menu ul li a')
    #除去0 1
    del categories[0]
    del categories[len(categories)-1]
    for item in categories:
        categoryList.append(path+item['href'])
#2获取小说
def GetStories(url):
    IPS=[
        {'HTTPS':'https://115.237.16.200:8118'},
        {'HTTPS':'https://42.49.119.10:8118'},
        {'HTTPS':'https://60.174.74.40:8118'}
    ]
    IP=random.choice(IPS)
    res=requests.get(url,headers=headers,proxies=IP)
    res.encoding='utf-8'
    html=res.text
    page=BeautifulSoup(html,'html.parser')
    stories=page.select(".bdsub #content table tr")
    del stories[0]
    for story in stories:
        link=story.find("td").select("a")[0]["href"]
        name=story.find("td").text
        link=link[:-5]
        link=path+"/files/article/html/88"+link[len(path)+len("/xiaoshuo"):]
        obj={"link":link,"name":name}
        storyList.append(obj)
    print("获取所有小说成功...\n")
    #print(storyList)
#3获取小说章节
def GetStoryUrls(url):
    IPS=[
        {'HTTPS':'https://115.237.16.200:8118'},
        {'HTTPS':'https://42.49.119.10:8118'},
        {'HTTPS':'https://60.174.74.40:8118'}
    ]
    IP=random.choice(IPS)
    res=requests.get(url,headers=headers,proxies=IP)
    res.encoding='utf-8'
    html=res.text
    page=BeautifulSoup(html,'html.parser')
    bookname=page.select(".bdsub dl h1")[0].text
    Nurls=page.select(".bdsub table a")
    for nurl in Nurls:
        title=""+nurl.text
        link=nurl["href"]
        obj={"title":title,"link":link}
        urls.append(obj)
    #print("获取所有章节成功...\n")
    #print(urls)
   


#4获取章节内容
def GetContent(url):
    IPS=[
        {'HTTPS':'https://115.237.16.200:8118'},
        {'HTTPS':'https://42.49.119.10:8118'},
        {'HTTPS':'https://60.174.74.40:8118'}
    ]
    IP=random.choice(IPS)
    res=requests.get(url["link"],headers=headers,proxies=IP)
    res.encoding='utf-8'
    html=res.text
    page=BeautifulSoup(html,'html.parser')
    title=url["title"]
    content=page.select(".bdsub dl #contents")
    return (title,content)


#5 保存文件
def saveFile(bookname,title,content):
    filename="%s.txt"%title
    io=open('./stories/{0}/{1}'.format(bookname,filename),'a',encoding='utf-8')
    io.write(content)
    #print("====保存成功===")

#6 下载
def download():
    for story in storyList:   
        print("正在获取小说<<{0}>>...\n".format(story["name"]))
        GetStoryUrls(story["link"])
        count=0
        time_start = time.time() #开始计时
        for url in urls:
            title,content=GetContent(url)
            process=count/len(urls)*100
            message=str(story["name"])+"下载进度为"
            print('%-9s   %0.2f%%\n'%(message,process))
            count=count+1
            setDir(str(story["name"]))
            saveFile(str(story["name"]),str(title),str(content))            
        print("{0}-小说保存成功!".format(str(story["name"])))
        time_end = time.time()    #结束计时
        time_sum= time_end - time_start
        print("用时:{0}s\n",time_sum)
        
#6 main
def mymain():
    GetCategories(path)
    #获取前2页
    print("============================程序开始==========================\n")
    for page in "12":
        print("============================分页start==========================\n")
        print("正在获取第一个分类的第{0}页".format(page))
        GetStories(categoryList[0][:-6]+page+".html")
        download()
        print("============================分页end==========================\n")
    print("============================程序结束==========================\n")

mymain()


 
