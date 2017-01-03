# coding:utf8
import re

class HtmlParser(object):
    # 将所有的段子都扣出来，添加到列表中并且返回列表
    def __init__(self):
        self.storys=[]
        self.keywords=[]
        self.nextUrlCode=''

    #获得笑话正文、当前页Code、下一页Code
    def GetStorys(self,page):
        # print myPage
        unicodePage = page.decode("utf-8")
        # 找出所有class="content"的div标记
        #re.S是任意匹配模式，也就是.可以匹配换行符
        #myItems = re.findall('<div.*?class="content">(.*?)</div>',unicodePage,re.S)
        myItems = re.findall('<div.*?class="content">\n\n+<span>(.*?)</span>\n\n+</div>',unicodePage,re.S)
        thisUrlCode=re.findall('<link rel="canonical" href="http://www.qiushibaike.com/history/(.*?)/">',unicodePage,re.S)[0]
        nextUrlCode=re.findall('<a class="random" href="/history/(.*?)/".*?',unicodePage,re.S)[0]

        return myItems,thisUrlCode,nextUrlCode

    #获得笑话正文(作者赞数)、当前页Code、下一页Code
    def GetStorys2(self,pageContent):
        try:
            unicodePage= pageContent.decode("utf-8")
            pattern = re.compile('<div class="author clearfix">.*?<h2>(.*?)</h2>.*?<div.*?' +'content">\n\n+<span>(.*?)</span>\n\n+</div>(.*?)<span class="stats-vote"><i class="number">(.*?)</i>',re.S)
			
			#items三个要素依次为用户名、段子内容、赞数
            items = re.findall(pattern, pageContent)

            for item in items:
                #去除段子内容中的查看全文
                item[1].replace("<span class=\"contentForAll\">查看全文","").replace("</span>","").replace("'","\"")
                #除去含有图片的
                haveImg = re.search("img", item[3])
                if  haveImg:
                    print item
                    del item
					
			#可以将这三个合并到上一个提高效率
            thisUrlCode = re.findall('<link rel="canonical" href="http://www.qiushibaike.com/history/(.*?)/">', unicodePage, re.S)[0]
            nextUrlCode = re.findall('<a class="random" href="/history/(.*?)/".*?', unicodePage, re.S)[0]
            dateStrs = re.findall('<meta name="keywords" content="(.*?)" />', unicodePage, re.S)[0]

            return items,thisUrlCode,nextUrlCode,dateStrs
        except Exception, e:
            print Exception, ":", e