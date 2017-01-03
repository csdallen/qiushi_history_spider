# coding:utf8
from array import array

class HtmlOutputer(object):

    def __init__(self):
        self.datas=[]

    def collect_data(self, data):
        if data is None:
            return
        self.datas.extend(data)

    #循环写文件
    def output_html(self):
        #最好声明为encoding='utf-8输出
        outfileName='outhtml'
        fout = open(outfileName + '.html', 'w')  # 如果output目录不存在会报错
        fout.write("<html>")
        fout.write("<head>")
        fout.write("<meta charset=""UTF-8"">")
        fout.write("</head>")
        fout.write("<body>")

        # 输出每个段子
        for data in self.datas:
            fout.write("<div>%s</div>"%data.encode("utf-8"))
            #fout.write("<div>%s</div>"%str(data).replace('u\'','\'').decode("unicode-escape").encode("utf-8"))
            fout.write("<br />")

        fout.write("</body>")
        fout.write("</html>")
        fout.close()
