'''
    视图界面
'''
class View:
    def login():
        while True:
            print("\n=========Command==============")
            print("*****      查单词        *****")
            print("*****      记录        *****")
            print("*****      注销        *****")
            print("===============================")
            cmd = input("Command:")
            if cmd == "查单词":
                pass
            elif cmd == "记录":
                pass
            elif cmd == '注销':
                break
            else:
                print('输入有误')


    while True:
        print("\n=========Command==============")
        print("*****    登录/注册      *****")
        print("*****      退出        *****")
        print("===============================")
        cmd = input("Command:")
        if cmd == "登录" or cmd == '注册':
            login()
        elif cmd == '退出':
            break
        else:
            print('输入有误')