def add_one(number):
    return number + 1

def login():
    while True:
        choice = input("请输入选项（1表示登录，2表示退出）：")
        if choice == "1":
            name = input("请输入您的姓名：")
            print(f"欢迎您，{name}！")
            break
        elif choice == "2":
            print("密码错误，请重新输入。")
        else:
            print("无效选项，请重新输入。")



