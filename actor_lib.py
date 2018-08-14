import requests
import xlsxwriter
from lxml import etree


USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
cookies = 'bid=VZlZKIlHcJk; ll="108288"; __yadk_uid=rYViaa5Z2fRXLiJiPeByWlusW9vh3f3m; _ga=GA1.2.1948961151.1514821665; ps=y; ue="at015z@163.com"; push_noty_num=0; push_doumail_num=0; __utmv=30149280.18264; _vwo_uuid_v2=D12A12A76FCE35A55CA7A879CD8117E1A|8874f1ae28ba57370c8dfa5ee71edbef; __utmz=30149280.1534145292.4.2.utmcsr=sogou.com|utmccn=(referral)|utmcmd=referral|utmcct=/link; ap=1; douban-fav-remind=1; __utma=30149280.1948961151.1514821665.1534171982.1534232179.6; __utmc=30149280; dbcl2="182649084:h5GEDbvffnA"; ck=1n_U; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1534257093%2C%22https%3A%2F%2Fwww.sogou.com%2Flink%3Furl%3DDSOYnZeCC_oPL4RhSawS82YvcrgiTSe0%22%5D; _pk_ses.100001.8cb4=*; _pk_id.100001.8cb4=9a840889a4540e21.1510935629.11.1534259066.1534243975.'

cookie = {}
for line in cookies.split(';'):
    name, value = cookies.strip().split('=', 1)
    cookie[name] = value

header = {'User-Agent': USER_AGENT, 'Connection': 'keep-alive'}


movieurl = 'https://www.douban.com/link2/?url=https%3A%2F%2Fmovie.douban.com%2Fsubject%2F26985127%2F&query=%E9%BB%84%E6%B8%A4&cat_id=1002&type=search&pos=0'
moviepage = requests.get(movieurl, headers=header, timeout=60)
selector = etree.HTML(moviepage.text)
director = selector.xpath('//*[@id="info"]/span[1]/span[2]/a/text()')
writer = selector.xpath('//*[@id="info"]/span[2]/span[2]/a[1]/text()')
actors = selector.xpath('//*[@id="info"]/span[@class="actor"]/span[2]/*[@rel="v:starring"]/text()')
movieclass = selector.xpath('//*[@id="info"]/span[@property="v:genre"]/text()')
IMDb = selector.xpath('//*[@id="info"]/a[@rel="nofollow"]/@href')
print(IMDb)


if IMDb:
    url = IMDb[0]
    imdbpage = requests.get(url, headers=header, timeout=60)
    print(imdbpage.text)
    selector = etree.HTML(imdbpage.text)
    imdbscore = selector.xpath('//*[@id="title-overview-widget"]/div[2]/div[2]/div/div[1]/div[1]/div[1]/strong/span/text()')
    print(imdbscore)