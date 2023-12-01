# _*_ coding : utf-8 _*_
# @Time : 2023/11/28 0:22
# @Author : 姚乐毅
# @File : test
# @Project : douban


from bs4 import BeautifulSoup #网页解析获取数据
import re   #正则表达式
import urllib.request, urllib.error #指定URL，获取网页数据
import xlwt #进行excel操作
import sqlite3  #进行数据库操作
print("你好 世界\n")


def main():
    baseurl = "https://movie.douban.com/top250?start="
    #1.爬取网页
    datalist = get_data(baseurl)

    #2.保存数据
    savepath =  '.\\豆瓣电影Top250.xls'
    save_data(datalist, savepath)
    print("爬取完毕\n")

#创建一个正则表达式对象，用于查找超链接
find_link = re.compile(r'<a href="(.*?)">')
#影片图像
find_img = re.compile(r'img alt=".*src="(.*?)"', re.S)
#影片片名
find_name = re.compile(r'<span class="title">(.*?)</span>')
#影片评分人数
find_judge_num = re.compile(r'<span>(\d*)人评价</span>')
#影片评分
find_judge = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
#影片概括
find_inq = re.compile(r'<span class="inq">(.*?)</span>')
#影片相关内容
find_bd = re.compile(r'<p class="">(.*?)</p>', re.S)


#爬取网页
def get_data(baseurl):
    datalist = []

    #获取网页信息
    for i in range(0, 10):
        url = baseurl + str(i * 25)
        html = askURL(url)

        #逐一解析数据
        soup = BeautifulSoup(html, "html.parser")
        #查找符合要求的字符串形成列表
        for item in soup.find_all('div', class_='item'):
            data = []   #保存一部电影所有信息
            item = str(item)

            #获取影片的超链接
            link = re.findall(find_link, item)[0]   #通过正则表达式查找指定的字符串
            data.append(link)

            #获取并保存图片
            img = re.findall(find_img, item)[0]
            data.append(img)

            #获取并保存片名
            name = re.findall(find_name, item)
            if len(name) == 2: #可能有外国名
                c_name = name[0]
                data.append(c_name)
                o_name = name[1].replace('/', "")
                data.append(o_name)
            else:
                c_name = name[0]
                data.append(c_name)
                o_name = ""
                data.append(o_name) #外国名留空

            #获取并保存评分
            judge = re.findall(find_judge, item)[0]
            data.append(judge)

            #获取并保存评分人数
            judge_num = re.findall(find_judge_num, item)[0]
            data.append(judge_num)

            #获取并保存概括
            inq = re.findall(find_inq, item)
            if len(inq) != 0:
                inq = inq[0].replace('。', '')   #去掉句号
                data.append(inq)
            else:
                data.append(" ")

            #获取并保存相关内容
            bd = re.findall(find_bd, item)[0]
            bd = re.sub('<br(\s+)?/>(\s+)?', " ", bd)   #去掉 <br/s>
            bd = re.sub('/', " ", bd)
            data.append(bd.strip()) #去掉前后空格

            datalist.append(data)   #吧处理好的一部电影的信息放入datalist

    return datalist

#得到指定的utl网页的内容
def askURL(url):
    head = {    #模拟浏览器头部信息，向服务器发送消息
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0'
    }   #用户代理，高速服务器，我们是什么类型的机器，可以接收什么水平的数据

    request = urllib.request.Request(url, headers = head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode('utf-8')
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html

#保存数据
def save_data(datalist, savepath):
    print("save...")
    #创建workbook对象
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)
    #创建工作表
    sheet = book.add_sheet('豆瓣电影250', cell_overwrite_ok=True)
    #添加列名
    col = ("电影详情链接", "图片链接", "影片中文名", "影片外文名", "评分", "评价数", "概况", "相关信息")
    for i in range(0, 8):
        sheet.write(0, i, col[i])
    #将内容保存本地
    for i in range(250):
        print(f"第{i + 1}条")
        data = datalist[i]
        for j in range(0, 8):
            sheet.write(i + 1, j, data[j])
    book.save(savepath)

if __name__ == "__main__":
    #调用函数
    main()












