'服务端tcp通信并发'
from socket import *
import os,sys,signal
from multiprocessing import Process
from eledict_db import User

class OtherError(Exception):
    pass

ADDR = ('0.0.0.0',8888)
db = User(database='eledict')

def do_login(confd, data):
    datas = data.split(' ')
    mes = db.login(datas[1],datas[2])
    if mes:
        confd.send(b'OK')
    else:
        confd.send(b'Fail')
def do_register(confd, data):
    datas = data.split(' ')
    mes = db.register(datas[1], datas[2])
    if mes:
        confd.send(b'OK')
    else:
        confd.send(b'Fail')
def do_findmean(confd, data):
    datas = data.split(' ')
    mes = db.find_mean(datas[1], datas[2])
    confd.send(mes.encode())
def do_findhistory(confd, data):
    datas = data.split(' ')
    mes = db.find_hist(datas[1])
    if mes:
        total_mes = ''
        for item in mes:
            total_mes = '%s %s %s \n'%(item[1],item[2],item[3])
        confd.send(total_mes.encode())
    else:
        confd.send('没有查询记录'.encode())
def request(confd):
    '''
    登录   L 注册   R 查单词  F 历史记录  H 退出   Q
    '''
    db.create_cursor()  # 每个子进程有自己的游标
    while True:
        data = confd.recv(1024).decode()  # 接受请求
        if not data or data[0] == 'Q':
            sys.exit()  # 退出对应的子进程
        elif data[0] == 'R':
            do_register(confd, data)
        elif data[0] == 'L':
            do_login(confd, data)
        elif data[0] == 'F':
            do_findmean(confd, data)
        elif data[0] == 'H':
            do_findhistory(confd, data)
    confd.close()
# 搭建网络
def main():
    s= socket(AF_INET,SOCK_STREAM)
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    s.bind(ADDR)
    s.listen(5)

    signal.signal(signal.SIGCHLD,signal.SIG_IGN)
    print('wait to connect......')
    while True:
        try:
            c,addr = s.accept()
            print("connect from",addr)
        except KeyboardInterrupt:
            sys.exit('服务退出')
        except OtherError as e:
            print(e)
            continue
        p = Process(target=request,args=(c,))
        p.daemon = True
        p.start()
    s.close()
if __name__ == '__main__':
    main()