# coding:utf8

class TxtOutputer(object):

    def __init__(self):
        self.datas=[]

    def collect_data(self, data):
        if data is None:
            return
        self.datas.extend(data)

    #循环写文件
    def output_txt(self):
        #最好声明为encoding='utf-8输出
        outfileName='outdata'
        fout = open(outfileName + '.txt', 'w')  # 如果output目录不存在会报错

        # 输出每个段子
        for data in self.datas:
            #这是为什么要这样处理字符串？不需要encode了
            fout.write("%s"%data[0].replace("<br/>","\r"))
            fout.write("\r")
            fout.write("%s"%data[1].replace("<br/>","\r"))
            fout.write("\r")
            fout.write("%s"%data[2].replace("<br/>","\r"))
            #fout.write("<div>%s</div>"%data['time'].encode('utf-8'))
            fout.write("\r\n")
        fout.close()
