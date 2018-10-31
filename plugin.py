# coding:utf8
import datetime
try:
    from .db import default_db
except:
    from db import default_db


def onQQMessage(bot, contact, member, content):
    # 当收到 QQ 消息时被调用
    # bot     : QQBot 对象，提供 List/SendTo/GroupXXX/Stop/Restart 等接口，详见文档第五节
    # contact : QContact 对象，消息的发送者
    # member  : QContact 对象，仅当本消息为 群或讨论组 消息时有效，代表实际发消息的成员
    # content : str 对象，消息内容
    if content == '--version' and getattr(member, 'uin') == bot.conf.qq:
        bot.SendTo(contact, 'QQbot-' + bot.conf.version)

    # 解析消息
    message = {
        "qq": bot.conf.qq,
        "group_name": contact.name,
        "member_name": member.name,
        "content": content,
        "gtime": datetime.datetime.now(),
    }
    default_db.add(message, table_name="qq_messages")
    return
