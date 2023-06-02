# -*- coding:utf-8 -*-

from nebula3.Config import Config
from nebula3.gclient.net import ConnectionPool

config = Config()
config.max_connection_pool_size = 10
# 初始化连接池
connection_pool = ConnectionPool()
# --addr=10.1.32.86 --port=9669 --user=root --password=123456
ok = connection_pool.init([("10.1.32.86", 9669)], config)

# 方法1：控制连接自行释放。
# 从连接池中获取会话
session = connection_pool.get_session("root", "123456")

pass
# 选择图空间
