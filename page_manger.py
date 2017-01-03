# coding:utf8
import time
import urllib2
import json

#读取历史
class PageManager(object):
    def __init__(self):
        #用于直接存储page对象
        self.page = 0
        self.pages = []
        self.urls=[]
        self.enable = True

    def AddUrl(self,url):
        self.urls.append(url)

    #读取网页
    def ReadPageFromUrl(self,pageUrl):
        try:
            user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
            headers = {'User-Agent': user_agent}
            req = urllib2.Request(pageUrl, headers=headers)
            myResponse = urllib2.urlopen(req)
            myPage = myResponse.read()
            return myPage
        except Exception, e:
            print Exception, ":", e
            return None


    # 用于加载新的页面
    def LoadPage(self):
        startUrl='http://www.qiushibaike.com/history/'

        #如果为空，返回还是从首页开始？
        if(len(self.urls)<=0):
            #self.urls.append(startUrl)
            return
        #设置初始值
        pageUrl=startUrl

        while self.enable:
            # 如果pages数组中的内容小于2个
            # print len(self.pages)
            if len(self.pages) < 3:

                # region -------不用此段则是随机读取startUrl--------
                #使用指定下一页的方式，不能起到预读的效果，每次只缓存一页
                #指定读取下一页
                # if(len(self.urls)>0):
                # 读取待读列表第一个，并去除掉
                #     pageUrl = self.urls[0]
                #     del self.urls[0]
                # else:
                #     pageUrl=startUrl
                # endregion

                #读取网页内容
                myPage=self.ReadPageFromUrl(pageUrl)
                if(myPage):
                    self.pages.append(myPage)
                    self.page += 1
            else:
                time.sleep(2)
                #self.enable=False
        #print self.pages

#pageManager= PageManager();
#pageManager.LoadPage()