import time
import requests
import traceback
from lxml import etree
from sendEmail import send_email
from sendEmail import genHTML
from sendEmail import load_eaddr

# Email
from_addr = "1021924274@qq.com"
to_addr = []
smtp_server = "smtp.qq.com"
pwd = "kflcjiiotlylbffd"

# URLs
buff = []
root_jwc = "http://jwc.hnu.edu.cn/"
root_csee = "http://csee.hnu.edu.cn/"
xsfw_url = "http://jwc.hnu.edu.cn/tzgg/xsfw.htm"
zhfw_url = "http://jwc.hnu.edu.cn/tzgg/zhfw.htm"    # /html/body/div[5]/div[2]/div[2]/ul/li
csee_url = "http://csee.hnu.edu.cn/tzgg.htm"        # /html/body/div[3]/div[2]/div[2]/ul/li


def get_news_lis(url):
    page = requests.get(url)
    #page.raise_for_status()
    page.encoding = page.apparent_encoding
    selector = etree.HTML(page.text)
    return selector.xpath('/html/body/div/div[2]/div[2]/ul/li')


def get_news_cess(lis):
    news = []
    for li in lis:
        # link
        link = root_csee + li.xpath("./a")[0].values()[0]
        # date
        date = li.xpath("./span")[0].text.split('-')
        for i in range(3):
            date[i] = int(date[i])
        date = tuple(date)
        # information
        info = li.xpath("./a")[0].text
        # add
        news.append((date, info, link))
    return news


def get_news_jwc(lis: list) -> list:
    news = []
    for li in lis:
        # link
        link = li.xpath('./a')[0].values()[0]   # '../info/1022/3610.htm'
        link = root_jwc + link[2:]
        # date
        dd = li.xpath("./a/div[1]/span[@class='dd']")[0].text
        yy = li.xpath("./a/div[1]/span[@class='yy']")[0].text
        date = yy + '-' + dd  # 2018-03-07
        date = date.split('-')
        for i in range(3):
            date[i] = int(date[i])
        date = tuple(date)
        # information
        info = li.xpath("./a/div[2]")[0].text
        # add
        news.append((date, info, link))
    return news


def latest_news(news: list, today: tuple) -> list:
    latest = []
    for info in news:
        if info[0] == today and info not in buff:
            latest.append(info)
            buff.append(info)
    return latest


def printNews():
    clock = time.localtime()
    today = (clock.tm_year, clock.tm_mon, clock.tm_mday)
    latest_xsfw = latest_news(get_news_jwc(get_news_lis(xsfw_url)), today)  # 获取教务处“学生服务”
    latest_zhfw = latest_news(get_news_jwc(get_news_lis(zhfw_url)), today)  # 获取教务处“综合服务”
    latest_csee = latest_news(get_news_cess(get_news_lis(csee_url)), today)  # 信息院
    print(latest_xsfw, '\n', latest_zhfw, '\n', latest_csee)


def call(frequence=1):
    print("Loading user emails...")
    to_addr = load_eaddr()
    print(to_addr)

    while True:
        clock = time.localtime()
        today = (clock.tm_year, clock.tm_mon, clock.tm_mday)
        if clock.tm_hour == 0 and clock.tm_min == 1:
            buff.clear()    # 新的一天开始了
            to_addr = load_eaddr()

        latest_xsfw = latest_news(get_news_jwc(get_news_lis(xsfw_url)), today)  # 获取教务处“学生服务”
        latest_zhfw = latest_news(get_news_jwc(get_news_lis(zhfw_url)), today)  # 获取教务处“综合服务”
        latest_csee = latest_news(get_news_cess(get_news_lis(csee_url)), today)  # 信息院

        if len(latest_csee) + len(latest_zhfw) + len(latest_xsfw) > 0:
            all_news = latest_xsfw, latest_zhfw, latest_csee
            with open('infos.txt', 'w+') as f:
                f.write(str(all_news) + '\n')
            print(all_news)
            msg_page = genHTML(all_news)
            send_email(from_addr, to_addr, "又双叒叕出新通知啦", msg_page, pwd)

        time.sleep(60 * frequence - time.localtime().tm_sec)


if __name__ == '__main__':
    print("Running...")
    try:
        call(frequence=15)
    except Exception as e:
        print(e)
        err = str(traceback.print_exc())
        send_email(from_addr, ["1021924274@qq.com", ], "(＃°Д°)崩溃鸟", err, pwd)
