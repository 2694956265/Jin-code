print("欢迎您来到我们的银行，请问您是新用户还是老用户?")
# 下面是一个注册函数
def zhuce():
    print("请您注册一个账号，下面是您的用户id")
    import random
    id = random.randint(1,10000)
    print(f"您的id号为{id}")
    while True :
        set_mima = input("请设置您的密码")
        set_mima_again = input("请再次输入你的密码")
        if set_mima != set_mima_again :
            print("不好意思，两次密码不一致，请重新设置")
            continue
        else :
            break
    print("注册成功！")
    return (set_mima_again,id)
#下面是本银行的主页面，总共由四个部分组成，分别是查看余额，存钱，取钱，以及退出
def zhuye(id):
    global money
    rest = 0
    while True:
        print("请问您想进行什么操作，请输入'查看余额' '取钱' ’存钱‘ 或者 '退出'")
        opretion = input()
        if opretion == "查看余额":
            print(f"您在我们银行存入的资金为{rest}")
        if opretion == "取钱":
            x = int(input("请问您要取多少钱"))
            if x > rest :
                print("你银行没有这么多钱")
            else :
                rest -= x
                money += x
                print("取钱成功！")
        if opretion == "存钱":
            y = int(input("请问您要存多少钱"))
            if y <= money:
                rest += y
                money -= y
                print("存钱成功！")
            else :
                print("你哪来的这么多钱去存")
        if opretion == "退出":
            print("欢迎您下次光临")
            break
# 下面是本银行的登陆页面
def denglu(id):
    for i in range(1,10001):
        if id == i :
            x = 0
            while x < 5 :
                input_mima = input("请输入您的密码")
                if mima == input_mima :
                    print("登陆成功，即将进入主页面")
                    zhuye(id)
                    break
                else :
                    x += 1
                    print(f"密码错误啦，您还有{5 - x}次机会")
                    continue
            break


#主函数
if __name__ == '__main__':
    gid = 0
    money = 10000
    print("您的初始资金（还未存到银行）有10000元")
    new_or_old = input()
    if new_or_old == "新用户":
        mima,gid = zhuce()
    else:
        print("我还没学到数组了，等着银行后续完善吧")

print("请输入您的id，我们要进行登陆啦")

while True :
    id_number = int(input())
    if id_number == gid :
        denglu(id_number)
        break
    else :
        print("没有这个id号")
