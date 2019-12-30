import csv
import time
import poplib
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr


def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value


def guess_charset(msg):
    charset = msg.get_charset()
    if charset is None:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    return charset


# indent用于缩进显示:
def print_info(msg, indent=0):
    list_msg = []

    if indent == 0:
        for header in ['Date', 'From', 'To', 'Subject']:
            value = msg.get(header, '')
            if value:
                # if header == 'Subject':
                value = decode_str(value)
                '''else:
                    hdr, addr = parseaddr(value)
                    name = decode_str(hdr)
                    value = u'%s <%s>' % (name, addr)'''
            # print('%s%s: %s' % ('  ' * indent, header, value))
            list_msg.append(value)
    if msg.is_multipart():
        parts = msg.get_payload()
        for n, part in enumerate(parts):
            # print('%spart %s' % ('  ' * indent, n))
            # print('%s--------------------' % ('  ' * indent))
            print_info(part, indent + 1)
    else:
        content_type = msg.get_content_type()
        if content_type == 'text/plain' or content_type == 'text/html':
            content = msg.get_payload(decode=True)
            charset = guess_charset(msg)
            if charset:
                content = content.decode(charset)
            # print('%sText: %s' % ('  ' * indent, content + '...'))
            list_msg.append(content)
        else:
            # print('%sAttachment: %s' % ('  ' * indent, content_type))
            list_msg.append(content_type)

    return list_msg


def receive_msg(update_time):
    list_allmsg = []
    with open("temporary.csv", 'r') as temp_f:
        reader = csv.reader(temp_f)
        for row in reader:
            list_info = row

    # get login information
    username = list_info[1]
    password = list_info[2]

    pop3_host = 'pop.qq.com'
    pop3_server = poplib.POP3(pop3_host)

    pop3_server.user(username)
    pop3_server.pass_(password)

    resp, mails, octets = pop3_server.list()

    index = len(mails)

    for i in range((index - 10), (index + 1)):
        resp, lines, octets = pop3_server.retr(i)

        try:
            msg_content = b'\r\n'.join(lines).decode('utf-8')
            msg = Parser().parsestr(msg_content)
            list_msg = print_info(msg)
            list_allmsg.append(list_msg)
        except UnicodeDecodeError:
            pass
        except LookupError:
            pass

    pop3_server.quit()

    # Save MSG _______________
    with open('group.csv', 'r') as read_csv:
        reader = csv.reader(read_csv)
        for row in reader:
            member_name = row[0]

            with open('msg.csv', 'w', newline='') as f:
                writer = csv.writer(f)
                for l_msg in list_allmsg:
                    try:
                        date = l_msg[0][5:25]
                        time_stamp = time.mktime(time.strptime(date, '%d %b %Y %H:%M:%S'))

                    except ValueError:
                        date = l_msg[0][4:24]
                        time_stamp = time.mktime(time.strptime(date, '%d %b %Y %H:%M:%S'))

                    if member_name in l_msg[1] and time_stamp-update_time > 0:
                        writer.writerow(l_msg)
                        # print('writen')


# receive_msg(time.time())
