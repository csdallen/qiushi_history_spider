# coding:utf8
class DateManager(object):
    def __init__(self):
        self.fatherUrl="http://www.qiushibaike.com/history/"
        self.thisUrl=""
        self.thisDate=""
        self.thisUrlCode=""
        self.nextDate=""
        self.nextUrlCode=""
        self.cacheDates=[]
        self.sqlconn=None

    #设置连接
    def set_conn(self,sqlconn):
        self.sqlconn = sqlconn

    #检查没有重复的日期 code
    def no_duplicate(self,code):
        sql = "SELECT * FROM datecode \
               WHERE urlcode = '%s'" % (code)
        try:
            cursor = self.sqlconn.cursor()
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            if(len(results)>0):
                return False
            else:
                return True  #无重复
        except Exception,e:
            print "Error: unable to fecth data"
            print "Exception:",e
            return False

    #region--------快速查询有无重复日期Code-----------
    #Todo:有空再做
    #检查没有重复的日期Code：一次检索数据库存到列表中，后期追加到列表
    def no_duplicateFast(self,code):
        sql = "SELECT * FROM datecode"
        date_code_arr=[]
        try:
            cursor = self.sqlconn.cursor()
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            for row in results:
                for r in row:
                    print r
        except Exception,e:
            print "Error: unable to fecth data"
            print "Exception:",e
            return False
    #endregion

    #把code存进去
    def save_code(self,datestr,code):
        if self.sqlconn is None:
            print 'mysql connection is none'
            return

        cursor = self.sqlconn.cursor()
        sql = "INSERT INTO `datecode` (`datestr`, `urlcode`) \
               VALUES ('%s', '%s')" % \
              (datestr, code)
        try:
            cursor.execute(sql)
            self.sqlconn.commit()
        except Exception,e:
            self.sqlconn.rollback()

