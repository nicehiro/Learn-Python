#


from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from email.header import Header
from email.utils import parseaddr, formataddr


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


from_addr = '17826856902@163.com'
password = 'w1234567'

to_addr = '8617826856902@kindle.cn'
smtp_server = 'smtp.163.com'

bookname = 'Python-Crawler.pdf'

msg = MIMEMultipart()
msg['From'] = _format_addr('The God <%s>' % from_addr)
msg['To'] = _format_addr('My kindle <%s>' % to_addr)
msg['Subject'] = Header('send book', 'utf-8').encode()

# 构造附件1，传送当前目录下的 test.txt 文件
att1 = MIMEText(open('/home/hiro/Documents/kindle/' + bookname,
                     'rb').read(), 'base64', 'utf-8')
att1["Content-Type"] = 'application/octet-stream'
# 这里的filename可以任意写，写什么名字，邮件中显示什么名字
att1["Content-Disposition"] = 'attachment; filename=bookname'
msg.attach(att1)

server = smtplib.SMTP(smtp_server, 25)
server.set_debuglevel(1)
server.login(from_addr, password)
server.sendmail(from_addr, [to_addr], msg.as_string())
server.quit()
