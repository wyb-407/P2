import requests
import xlsxwriter
from lxml import etree


# 设置请求头
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
cookies = 'bid=VZlZKIlHcJk; ll="108288"; __yadk_uid=rYViaa5Z2fRXLiJiPeByWlusW9vh3f3m; _ga=GA1.2.1948961151.1514821665; ps=y; ue="at015z@163.com"; push_noty_num=0; push_doumail_num=0; __utmv=30149280.18264; _vwo_uuid_v2=D12A12A76FCE35A55CA7A879CD8117E1A|8874f1ae28ba57370c8dfa5ee71edbef; __utmz=30149280.1534145292.4.2.utmcsr=sogou.com|utmccn=(referral)|utmcmd=referral|utmcct=/link; ap=1; douban-fav-remind=1; __utma=30149280.1948961151.1514821665.1534171982.1534232179.6; __utmc=30149280; dbcl2="182649084:h5GEDbvffnA"; ck=1n_U; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1534257093%2C%22https%3A%2F%2Fwww.sogou.com%2Flink%3Furl%3DDSOYnZeCC_oPL4RhSawS82YvcrgiTSe0%22%5D; _pk_ses.100001.8cb4=*; _pk_id.100001.8cb4=9a840889a4540e21.1510935629.11.1534259066.1534243975.'

cookie = {}
for line in cookies.split(';'):
    name, value = cookies.strip().split('=', 1)
    cookie[name] = value

header = {'User-Agent': USER_AGENT, 'Connection': 'keep-alive'}


# 抓取网页上的演员对应的电影以及电影评分
movies = []
for i in range(0, 1000, 20):
    url = "https://www.douban.com/j/search?q=%E9%BB%84%E6%B8%A4&start={}&cat=1002".format(i)

    req = requests.get(url, headers=header, timeout=60)
    lists = list(req.json()['items'])
    if len(lists) == 0:
        print(i)
        break

    # 使用xpath提取电影名与评分，列表形式写入movies
    for u in lists:
        movie = []
        selector = etree.HTML(u)
        if selector.xpath('/html/body/div[@class="result"]/div[2]/div/h3/span/text()') == ['[电影]']:
            score = selector.xpath('/html/body/div[@class="result"]/div[2]/div/div/span[2]/text()')
            if score == ['(暂无评分)'] or score == ['(尚未上映)']:
                continue
            title = selector.xpath('/html/body/div[@class="result"]/div[2]/div/h3/a/text()')
            # 提取电影的详情页
            movieurl = selector.xpath('/html/body/div[@class="result"]/div[2]/div/h3/a/@href')
            # actors = selector.xpath('')
            for k, j in zip(title, score):
                print(k, j)
                k = k.strip()
                j = float(j)
                movies.append([k, j, movieurl[0]])

print(movies)


# 提取电影详情页中的主要演员
actorslist = []
moviedetails = {}
for i in range(len(movies)):
    moviedetail = {}
    movieurl = movies[i][2]
    moviepage = requests.get(movieurl, headers=header, timeout=60)
    selector = etree.HTML(moviepage.text)
    director = selector.xpath('//*[@id="info"]/span[1]/span[2]/a/text()')
    writer = selector.xpath('//*[@id="info"]/span[2]/span[2]/a[1]/text()')
    actors = selector.xpath('//*[@id="info"]/span[@class="actor"]/span[2]/*[@rel="v:starring"]/text()')
    movieclass = selector.xpath('//*[@id="info"]/span[@property="v:genre"]/text()')
    IMDb = selector.xpath('//*[@id="info"]/a[@rel="nofollow"]/@href')
    actorslist.append(actors)
    moviedetail['director'] = '/'.join(director)
    moviedetail['writer'] = '/'.join(writer)
    moviedetail['actors'] = '/'.join(actors)
    moviedetail['movieclass'] = '/'.join(movieclass)
    moviedetail['IMDbscore'] = ''
    moviedetail['IMDb'] = ''.join(IMDb)
    moviedetails[movies[i][0]] = moviedetail

    if len(moviedetail['IMDb']) > 0:
        url = moviedetail['IMDb']
        try:
            imdbpage = requests.get(url, headers=header, timeout=60)
        except:
            continue
        selector = etree.HTML(imdbpage.text)
        IMDbscore = selector.xpath('//*[@id="title-overview-widget"]/div[2]/div[2]/div/div[1]/div[1]/div[1]/strong/span/text()')
        if IMDbscore:
            moviedetail['IMDbscore'] = float(IMDbscore[0])
    print(moviedetail)

    moviedetails[movies[i][0]] = moviedetail

print(moviedetails)


# 将数据(movies)写入excel
workbook = xlsxwriter.Workbook("./actors/huanbo.xlsx") # 创建一个新的工作薄
worksheet1 = workbook.add_worksheet() # 新增一个工作表,可传入表名，不传默认为sheet1
# 插入数据，传入三个参数
worksheet1.write(0, 0, "movie") # 三个参数分别为：行，列，数据。注意行列索引值从零开始。
worksheet1.write(0, 1, "score")
worksheet1.write(0, 2, "director")
worksheet1.write(0, 3, "writer")
worksheet1.write(0, 4, "actors")
worksheet1.write(0, 5, "movieclass")
worksheet1.write(0, 6, "IMDbscore")
worksheet1.write(0, 7, "IMDb")
worksheet1.write(0, 8, "url")

line = 1
for i in range(len(movies)):
    worksheet1.write(line, 0, movies[i][0])
    worksheet1.write(line, 1, movies[i][1])
    worksheet1.write(line, 2, moviedetails[movies[i][0]]['director'])
    worksheet1.write(line, 3, moviedetails[movies[i][0]]['writer'])
    worksheet1.write(line, 4, moviedetails[movies[i][0]]['actors'])
    worksheet1.write(line, 5, moviedetails[movies[i][0]]['movieclass'])
    if moviedetails[movies[i][0]]['IMDbscore']:
        worksheet1.write(line, 6, moviedetails[movies[i][0]]['IMDbscore'])
    worksheet1.write(line, 7, moviedetails[movies[i][0]]['IMDb'])
    worksheet1.write(line, 8, movies[i][2])
    line += 1

# 关闭工作薄，完成数据的保存
workbook.close()


print('finish')
