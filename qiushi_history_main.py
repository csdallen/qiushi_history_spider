# -*- coding: utf-8 -*-
import thread
import time
from qiushi_history_spider import html_parser
from qiushi_history_spider import html_outputer
from qiushi_history_spider import txt_outputer
from qiushi_history_spider import page_manger
from qiushi_history_spider import mysql_outputer
from qiushi_history_spider import date_manager
import urllib2


# ----------- 加载处理糗事百科 -----------
class Spider_Model:
    # 声明self:含有page pages enabled
    def __init__(self):
        self.pagemanger = page_manger.PageManager()
        self.htmlparser = html_parser.HtmlParser()
        # self.outputer=html_outputer.HtmlOutputer()
        self.txtoutputer = txt_outputer.TxtOutputer()
        self.mysqlOutputer = mysql_outputer.MysqlOutputer()
        self.datemanager = date_manager.DateManager()
        self.page = 1
        self.pages = []
        self.storys = []
        self.enable = True
        self.maxPageNum = 400;

    def Start(self):
        self.enable = True
        page = self.page
        print u'正在加载中请稍候......'
        # 新建一个线程在后台加载段子并存储
        startUrl = 'http://www.qiushibaike.com/history/'
        self.pagemanger.AddUrl(startUrl)
        connection = self.mysqlOutputer.open_conneciton()  # 打开数据库连接
        self.datemanager.set_conn(connection)
        thread.start_new_thread(self.pagemanger.LoadPage, ())

        time.sleep(3)
        self.pages = self.pagemanger.pages
        # ----------- 加载处理糗事百科 -----------
        while self.enable:
            # 存储并检验是否到达预订页数
            if (page > self.maxPageNum):
                self.pagemanger.enable = False
                self.enable = False
                break

            # 如果self的page数组中存有元素
            # 等待，防止pagemanager尚未读取完毕
            time.sleep(2)
            if self.pages:
                if(len(self.pages)<=0):
                    continue
                nowPage = self.pages[0]

                if(nowPage==None):
                    del self.pages[0]
                    continue
                del self.pages[0]
                #读取内容
                self.storys, thisUrlCode, nextUrlCode, dateStr = self.htmlparser.GetStorys2(nowPage)

                # 判断是否重复
                nodump = self.datemanager.no_duplicate(thisUrlCode)
                if (nodump):
                    # region-----------保存当前日期的第一页---------------
                    self.datemanager.save_code(dateStr, thisUrlCode)

                    # 当前这一步没有用，现在的页面是不停的刷新‘穿越’页得到的
                    # print '存入待读列表：',startUrl + nextUrlCode
                    # self.pagemanger.AddUrl(startUrl + nextUrlCode)

                    dateStoryDic = {'story': self.storys, 'urlcode': thisUrlCode, 'date': dateStr, 'page': 1}
                    # print dateStoryDic
                    self.mysqlOutputer.collect_data(dateStoryDic)
                    self.PrintInfo(page, dateStr, thisUrlCode, nextUrlCode, 1)
                    page += 1
                    # endregion

                    # region-----------保存当前日期的第二页----------------
                    print "总页数:" + bytes(page), "日期:" + dateStr, "页码:" + bytes(2)
                    print "当前页Code:",thisUrlCode+'/page/2'
                    secondPageUrl = startUrl+thisUrlCode+'/page/2'
                    secondPage=self.pagemanger.ReadPageFromUrl(secondPageUrl)

                    if(secondPage==None):
                        print "加载此页失败！"
                        continue
                    self.storys, thisUrlCode, nextUrlCode, dateStr = self.htmlparser.GetStorys2(secondPage)
                    dateStoryDic = {'story': self.storys, 'urlcode': thisUrlCode, 'date': dateStr, 'page': 2}
                    self.mysqlOutputer.collect_data(dateStoryDic)

                    #page += 1
                    # endregion

                    self.mysqlOutputer.output_database()
            else:
                self.enable = False
                break

        self.mysqlOutputer.close_conneciton()

    # 打印输出 抓取的总页数,日期字符串，当前code，下一错的，当前日期第几页
    def PrintInfo(self, pagecount, datestr, thiscode, nextcode, pageIndex):
        print "总页数:" + bytes(pagecount), "日期:" + datestr, "页码:" + bytes(pageIndex)
        print "当前页Code:", thiscode
        #print "下一页Code：", nextcode


# ----------- 程序的入口处 -----------
# 1从数据库中读取所有id？
# 2每次从首页（history）读取
# 3首先获取当前页id，查重
# 4如无重复则解析 存储到数据库
# 5如果重复，直接读取下一页
# 6读取下一页，重复2-6

# Todolist:
# 1.读取当天的第二页第三页
# 2.输出mysql数据库中的数据到文件
# 3.把datecode从数据库中读出到数组，以后查重更快

myModel = Spider_Model()
myModel.Start()

# 否则 python错误Unhandled exception in thread started by Error in sys.excepthook
time.sleep(3)
