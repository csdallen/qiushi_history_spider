# coding:utf8
from qiushi_history_spider import mysql_outputer
import pymysql.cursors
import os

class Mysql2Texts:
    def __init__(self):
        #self.date_storys=[]
        self.datestrs=[]
        self.date_name=''
        self.connection=None
        self.outfolder='out_text_files'

    #打开数据连接
    def open_conneciton(self):
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='mysql',
                                     db='qiushispider',
                                     charset='utf8mb4')
        self.sqlconn = connection
        return self.sqlconn

    #查询所有的日期
    def query_alldates(self):
        sql = "SELECT datestr FROM datecode"
        date_strs=[]
        try:
            cursor = self.sqlconn.cursor()
            cursor.execute(sql)
            # 获取所有记录列表
            result_rows = cursor.fetchall()
            for row in result_rows:
                date_strs.append(row[0])
        except Exception, e:
            print "Error: unable to fecth data"
            print "Exception:", e
        return date_strs

    #查询指定日期的段子
    def query_storys_bydate(self,datestr):
        sql = "SELECT content FROM storys WHERE datestr = '%s'" % (datestr)
        date_storys=[]
        try:
            cursor = self.sqlconn.cursor()
            cursor.execute(sql)
            # 获取所有记录列表
            result_rows = cursor.fetchall()
            for row in result_rows:
                date_storys.append(row[0])
        except Exception, e:
            print "Error: unable to fecth data"
            print "Exception:", e
        return date_storys

    #输出某个日期的段子
    def out_storys_bydate(self,datestr,storys):
        #最好声明为encoding='utf-8输出
        outfileName=datestr
        fout = open(self.outfolder+'\\'+outfileName + '.txt', 'w')  # 如果output目录不存在会报错

        # 输出每个段子
        for data in storys:
            #这是为什么要这样处理字符串？不需要encode了
            fout.write("%s"%data.replace("<span class=\"contentForAll\">查看全文","").replace("</span>",""))
            fout.write("\r\n")
        fout.close()
        return

    #开始输出
    def start_main(self):
        #创建文件夹
        if(not os.path.exists(self.outfolder)):
            os.makedirs(self.outfolder)

        self.connection=self.open_conneciton();
        print self.connection
        date_strs=self.query_alldates()
        print date_strs
        date_count=0;
        for datestr in  date_strs:
            #测试 输出几个时中止
            #date_count=date_count+1
            #if(date_count>100):
                #break
            date_storys=self.query_storys_bydate(datestr)
            print datestr
            #print date_storys
            self.out_storys_bydate(datestr,date_storys)

        self.connection.close()
        print '导出完成'

#主函数部分
mysql2texts= Mysql2Texts()
mysql2texts.start_main()