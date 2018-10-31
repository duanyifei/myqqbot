# coding:utf8

from qqbot import _bot as bot


# 建表
def init():
    from db import default_db
    sql = """create table if not exists `qq_messages` (
      `id` integer,
      `qq` int(11) NULL,
      `group_name` varchar(255) NULL,
      `member_name` varchar(255) NULL,
      `content` varchar(255) NULL,
      `gtime` datetime(0) NULL,
      PRIMARY KEY (`id`)
    );"""
    default_db.cursor.execute(sql)
    default_db.db.commit()
    return


def main():
    init()
    #
    # 登录
    bot.Login(['-r', '-q', '1821367759'])

    # 插件
    bot.Plug("plugin")
    # 主循环
    bot.Run()
    return


if __name__ == '__main__':
    main()
