import html
import re
import time

import bleach
import pymysql
import requests
import telegram
from bs4 import BeautifulSoup

from config import cfg


def clean_html(dirty_html):
    dirty_html = bleach.clean(str(dirty_html), tags=['a'], strip=True)
    dirty_html = re.sub(r'(<a href="[^"]+?")(?:.+?)>', r'\1>', dirty_html)
    dirty_html = re.sub(r'href="//', 'href="https://', dirty_html)
    return dirty_html


req = requests.get(cfg['url'])
page_html = req.text

bot = telegram.Bot(cfg['telegram']['token'])

soup = BeautifulSoup(page_html, 'html.parser')

db = pymysql.connect(host=cfg['database']['host'],
                     user=cfg['database']['user'],
                     passwd=cfg['database']['passwd'],
                     db=cfg['database']['db'],
                     charset=cfg['database']['charset'])
cur = db.cursor()
cur.execute(
    """SELECT `mid`, `html` FROM `{0}message`""".format(cfg['database']['table_prefix']))
rows = cur.fetchall()
old_message = {}
for row in rows:
    old_message[row[1]] = row[0]
print(old_message)

for li in soup.find_all('li'):
    btype = li.find('span', class_='bulletin-type').text
    prefix = clean_html(li.find('span', class_='bulletin-prefix'))
    suffix = clean_html(li.find('span', class_='bulletin-suffix'))
    for item in li.find_all('span', class_='bulletin-item'):
        links = item.find_all('a')
        btext = item.text

        if re.search(cfg['hide_bulletin_regex'], btext):
            continue

        itemhtml = clean_html(item)
        message = '{0} {1}{2}{3}'.format(
            html.escape(btype),
            prefix,
            itemhtml,
            suffix
        )

        print(message)

        if message in old_message:
            del old_message[message]
            continue

        res = cur.execute(
            """INSERT INTO `{0}message` (`html`) VALUES (%s)""".format(
                cfg['database']['table_prefix']),
            (message))
        db.commit()
        mid = cur.lastrowid

        for chat_id in cfg['telegram']['chats']:
            chat = cfg['telegram']['chats'][chat_id]

            send_text = chat['new'].format(message)

            message_id = None
            for i in range(5):
                try:
                    print('send to {}'.format(chat_id))
                    sent_message = bot.send_message(
                        chat_id=chat_id,
                        text=send_text,
                        parse_mode=telegram.ParseMode.HTML,
                        disable_web_page_preview=True)
                    message_id = sent_message.message_id
                    break
                except telegram.error.TimedOut as e:
                    print('send to {} failed: TimedOut: {}'.format(
                        chat_id, e))
                    time.sleep(1)
                except telegram.error.BadRequest as e:
                    print('send to {} failed: BadRequest: {}'.format(
                        chat_id, e))
                    break
                except Exception as e:
                    print('send to {} failed: {}'.format(
                        chat_id, e))

            if message_id is None:
                continue

            res = cur.execute(
                """INSERT INTO `{0}record` (`mid`, `chat_id`, `message_id`) VALUES (%s, %s, %s)""".format(
                    cfg['database']['table_prefix']),
                (mid, chat_id, message_id))
            db.commit()

for message in old_message:
    mid = old_message[message]

    cur.execute(
        """SELECT `chat_id`, `message_id` FROM `{0}record` WHERE `mid` = %s""".format(
            cfg['database']['table_prefix']), (mid))
    rows = cur.fetchall()

    for row in rows:
        chat_id = row[0]
        message_id = row[1]

        if chat_id not in cfg['telegram']['chats']:
            continue

        chat = cfg['telegram']['chats'][chat_id]
        old_text = chat['new'].format(message)
        new_text = chat['archive'].format(message)
        if old_text != new_text:
            for i in range(5):
                try:
                    print('edit {} in {}'.format(message_id, chat_id))
                    bot.edit_message_text(
                        chat_id=chat_id,
                        message_id=message_id,
                        text=new_text,
                        parse_mode=telegram.ParseMode.HTML,
                        disable_web_page_preview=True)
                    break
                except telegram.error.TimedOut as e:
                    print('edit {} in {} failed: TimedOut: {}'.format(
                        message_id, chat_id, e))
                    time.sleep(1)
                except telegram.error.BadRequest as e:
                    print('edit {} in {} failed: BadRequest: {}'.format(
                        message_id, chat_id, e))
                    break
                except Exception as e:
                    print('edit {} in {} failed: {}'.format(
                        message_id, chat_id, e))

    res = cur.execute(
        """DELETE FROM `{0}message` WHERE `mid` = %s""".format(
            cfg['database']['table_prefix']),
        (mid))
    db.commit()
