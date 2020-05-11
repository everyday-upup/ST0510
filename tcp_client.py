'客户端tcp通信并发'
from socket import *
import sys
import getpass

ADDR =('127.0.0.1',8888)
def do_login(s):
    name = input('name:')
    password = input('password:')
    data = 'L ' + name + ' ' + password
    s.send(data.encode())

    data = s.recv(128).decode()  # 反馈
    if data == 'OK':
        print("登录成功")
        login(s,name)
    else:
        print("登录失败")
def do_register(s):
    while True:
        name = input('name:')
        pwd = getpass.getpass()
        pwd1 = getpass.getpass('password again:')
        if pwd != pwd1:
            print("两次密码不一致！")
            continue
        if (' ' in name) or (' ' in pwd):
            print("用户名或密码不能含有空格")
            continue

        msg = "R %s %s"%(name,pwd)
        s.send(msg.encode()) # 发送请求

        data = s.recv(128).decode() # 反馈
        if data == 'OK':
            print("注册成功")
            login(s,name)
        else:
            print("注册失败")
        return
def do_findmean(s,name):
    word = input('word:')
    data = 'F %s %s' %(name,word)
    s.send(data.encode())

    data = s.recv(1024).decode()  # 反馈
    print(data)
def do_findhistory(s,name):
    data = 'H %s' %name
    s.send(data.encode())

    data = s.recv(2048).decode()  # 反馈
    print(data)
def login(s,name):
    while True:
        print("""
            ==============%s Query ============
              1.查单词     2.历史记录     3.注销
            ===================================
            """ % name)
        cmd = input("选项(1,2,3):")
        if cmd == '1':
            do_findmean(s,name)
        elif cmd == '2':
            do_findhistory(s,name)
        elif cmd == '3':
            return  # 二级界面结束
        else:
            print("请输入正确命令")
def request(s):
    while True:
        print("""
         ========== Welcome ============
           1.注册     2.登录     3.退出
         ===============================
         """)
        cmd = input("选项(1,2,3):")
        if cmd == '1':
            do_register(s)
        elif cmd == '2':
            do_login(s)
        elif cmd == '3':
            s.send(b'Q')
            sys.exit("谢谢使用")
        else:
            print("请输入正确命令")

def main():
    s= socket(AF_INET,SOCK_STREAM)
    s.connect(ADDR)
    request(s)
    s.close()

if __name__ == '__main__':
    main()
