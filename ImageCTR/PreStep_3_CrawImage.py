
# coding: utf-8

# In[4]:


import requests
import re, time


# In[5]:


def getpageurl():
    page_list = []
    #进行列表页循环
    for page in range(1001,2000):
        url="http://jandan.net/ooxx/page-"+str(page)+"#comments"
        #把生成的url加入到page_list中
        page_list.append(url)
    return page_list


# In[8]:


def geturllist(url):
    url_list=[]
    print(url)

    #head是我们自己构造的一个字典，里面保存了user-agent
    head = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36'}
    # html = requests.get('http://jp.tingroom.com/yuedu/yd300p/')
    html = requests.get(url, headers = head)
    text = html.text
    #正则匹配，匹配其中的图片
    pic_urls = re.findall('</a><br /><img src="(.*?).jpg" /></p>', text)
    for i in pic_urls:
        image = "http://" + i.lstrip("//") + '.jpg'
        #print 'image url = ' + image
        url_list.append(image)
    return url_list


# In[10]:


if __name__ == '__main__':

    pageurl = getpageurl()[:-1]
    #进行图片下载
    count = 0
    for url in pageurl:
        url_list = geturllist(url)

        i = 0

        for each in url_list:
            print('now downloading:' + each)
            pic = requests.get(each)
            name=re.sub('.+?/','',each)
            fp = open("data\\ImageData\\" + name , 'wb')
            fp.write(pic.content)
            fp.close()
            i+=1
            time.sleep(0.5)
            count += 1
        if(count > 10000):
        	exit()

