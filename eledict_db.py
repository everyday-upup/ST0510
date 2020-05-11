'''
    数据库操作
'''
import pymysql,hashlib
import re
import time

# 加密处理
def jm(passwd):
    salt = "^&5#Az$"
    hash = hashlib.md5(salt.encode())  # 生产加密对象
    hash.update(passwd.encode())  # 加密处理
    return hash.hexdigest()

class User:

    def __init__(self, host='localhost',
                 port=3306,
                 user='root',
                 password='123456',
                 charset='utf8',
                 database=None):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.charset = charset
        self.database = database
        self.connect_db()

    # 链接数据库
    def connect_db(self):
        self.db = pymysql.connect(host = self.host,
                                  port = self.port,
                                  user=self.user,
                                  passwd=self.password,
                                  database=self.database,
                                  charset=self.charset)

    # 创建游标对象(cur=db.cursor())
    def create_cursor(self):
        self.cur = self.db.cursor()
    # 游标方法: cur.execute("insert ....")
    # 提交到数据库或者获取数据: db.commit() / db.fetchall()
    # 登录
    def login(self,name,password):
        password = jm(password)  # 加密处理
        sql = 'select * from user where name=%s and password=%s'
        self.cur.execute(sql,[name,password])
        logmes = self.cur.fetchone()
        return True if logmes else False
    # 注册
    def register(self,name,password):
        sql = 'select * from user where name=%s'
        self.cur.execute(sql,[name])
        regmes = self.cur.fetchone()
        if regmes:
            return False
        sql = 'insert into user(name,password) values(%s,%s)'
        password = jm(password)  # 加密处理
        try:
            self.cur.execute(sql,[name,password])
            self.db.commit()
            return True
        except:
            self.db.rollback()
            return False
    # 查单词含义
    # 查历史记录
    def find_mean(self,name,word):
        with open('dict.txt', 'r', encoding='utf-8') as file:
            for line in file:
                w = re.findall(r'(\S+)\s+(.*)',line)[0]
                if w[0] == word:
                    sql = 'insert into hist(name,word) values(%s,%s)'
                    try:
                        self.cur.execute(sql,[name,word])
                        self.db.commit()
                        return w[1]
                    except:
                        self.db.rollback()
                    return 'qi'
                else:
                    return '没有找到该单词'
    def find_hist(self,name):
        sql = 'select * from hist where name=%s order by time desc limit 10'
        self.cur.execute(sql, [name])
        return self.cur.fetchall()
    # 关闭游标对象 ：cur.close()
    # 断开数据库连接 ：db.close()
