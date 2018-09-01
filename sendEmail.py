from email.mime.text import MIMEText
import smtplib


def load_eaddr(filename="emails.txt") -> list:
    emails = []
    with open(filename) as f:
        for line in f.readlines():
            # print(line.strip())
            emails.append(line.strip())
    return emails


def genHTML(news3: tuple) -> str:
    body = "<html><body>"

    for i in range(3):
        if len(news3[i]) == 0:
            continue
        if i == 0:
            body += "<div><h3 href=http://jwc.hnu.edu.cn/tzgg/xsfw.htm>%s</h3><ul>" % "学生服务"
        elif i == 1:
            body += "<div><h3 href=http://jwc.hnu.edu.cn/tzgg/zhfw.htm>%s</h3><ul>" % "综合服务"
        else:
            body += "<div><h3 href=http://csee.hnu.edu.cn/tzgg.htm>%s</h3><ul>" % "信息院信息"
        # List news
        for news in news3[i]:
            body += "<li><a href=%s>%s</a></li>" % (news[2], news[1])
        body += "</ul></div>"

    return body + "</body></html>"


def send_email(fromAddr: str, toAddr: list, subject: str, text: str, passwd: str):
    # 设置邮件内容
    msg = MIMEText(text, 'HTML', 'utf-8')
    msg['Subject'] = subject
    msg['From'] = fromAddr

    try:
        smtp = smtplib.SMTP_SSL('smtp.qq.com', port=465)
        smtp.login(fromAddr, passwd)
        smtp.sendmail(fromAddr, toAddr, msg.as_string())
    except smtplib.SMTPException as e:
        print("Failed: %s" % e)
    finally:
        smtp.quit()
