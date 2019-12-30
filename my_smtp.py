import csv
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart


def w_email(text, from_nick, to_nick, subject):
    msg = MIMEText(text, 'plain', 'utf-8')
    msg['From'] = Header(from_nick)
    msg['To'] = Header(to_nick)
    msg['Subject'] = Header(subject)
    return msg


def sent_mail(text, subject):
    with open("temporary.csv", 'r') as temp_f:
        reader = csv.reader(temp_f)
        for row in reader:
            list_info = row

    # get login information
    nickname = list_info[0]
    from_addr = list_info[1]
    password = list_info[2]

    smtp_server = 'smtp.qq.com'
    server = smtplib.SMTP_SSL(smtp_server)
    server.connect(smtp_server, 465)
    server.login(from_addr, password)

    # Read group member
    with open('group.csv', 'r') as read_csv:
        reader = csv.reader(read_csv)
        for row in reader:
            member_name = row[0]
            member_email = row[1]
            # Check email
            try:
                server.sendmail(from_addr, member_email, w_email(text, nickname, member_name, subject).as_string())
            except smtplib.SMTPRecipientsRefused:
                pass

    server.quit()
