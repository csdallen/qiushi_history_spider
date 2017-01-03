# coding:utf8
import pymysql.cursors
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

#mysql输出器
class MysqlOutputer:
    def __init__(self):
        self.pageDicArr=[]
        self.sqlconn=None

    #收集数据
    def collect_data(self, dataDict):
        if dataDict is None:
            return
        dict1= dict()
        dict1['story']=dataDict['story']
        dict1['urlcode']=dataDict['urlcode']
        dict1['date']=dataDict['date']
        dict1['page']=dataDict['page']

        self.pageDicArr.append(dict1)
    #将来是攒到一定数据，例如1000条写入一次，起用多线程

    #打开数据连接
    def open_conneciton(self):
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='mysql',
                                     db='qiushispider',
                                     charset='utf8mb4')
        self.sqlconn = connection
        return self.sqlconn

    #关闭数据连接
    def close_conneciton(self):
        if (self.sqlconn != None):
            self.sqlconn.close()

    #循环写入数据库，使用完后清空收集的数据
    def output_database(self):
         if(self.sqlconn is None):
             self.open_conneciton()
         sql=''

         try:
            # 循环每一页
            for pageDict in self.pageDicArr:
                storys = pageDict['story']
                urlCode = pageDict['urlcode']
                dateStr = pageDict['date']
                pageIndex=pageDict['page']

                #循环所有笑话
                for story in storys:
                    author = story[0]        #作者
                    storycontent = story[1]  #笑话内容
                    #story[2]是图片内容
                    commend = int(story[3])  # 推荐数

                    #storycontent常含有</br>和'
                    #'符号在sql变量中会导致与sql语句中的'混合
                    storycontent=storycontent.replace("<br/>","\r").replace("'","\"")

                    # 获得指针
                    cursor = self.sqlconn.cursor()
                    if self.sqlconn is None:
                        print 'mysql connection is none'
                        break

                    #整型数据插入不对
                    #sql = "insert into `storys` (`author`,`content`,`commend`,`datestr`,`pageindex`) values ('%s','%s',%i,'%s',%i)"
                    #cursor.execute(sql, (author, storycontent,commend,dateStr,1))

                    #sql = "insert into `storys` (`author`,`content`,`datestr`,`commend`,`pageindex`) \
                      #values ('"+author+"','"+storycontent+"','"+dateStr+"',"+commend+","+"1)"
                    #cursor.execute(sql)

                    sql = "INSERT INTO `storys` (`author`, \
                           `content`, `commend`, `datestr`, `pageindex`) \
                           VALUES ('%s', '%s', %d, '%s', %d )" % \
                          (author, storycontent, commend, dateStr, pageIndex)
                    cursor.execute(sql)

                    self.sqlconn.commit()
            print 'insert to database sucessful', ':', dateStr
         except Exception,e:
           self.sqlconn.rollback()
           print 'insert to database error!!!',':',dateStr
           print 'sql语句:',sql
           print "Exception:",e
         finally:
             #清空数据
             self.pageDicArr=[]