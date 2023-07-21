#!/usr/bin/env python

from serpent.Serpent import execute
import socket,subprocess,shlex

# 绑定的IP地址和端口号
SERVER_IP = '127.0.0.1'
SERVER_PORT = 8848


from serpent.Serpent import initialize_game

def UDP():


    # 创建UDP套接字
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # 将套接字绑定到指定的IP地址和端口号
    server_socket.bind((SERVER_IP, SERVER_PORT))

    print('UDP服务器已启动，等待客户端连接...')
    game_name = "MLA"

    game = initialize_game(game_name)

    while True:
        # 接收客户端发送的数据和客户端地址
        data, client_address = server_socket.recvfrom(1024)
        print('从客户端', client_address, '接收到数据:', data.decode()[:-1])
        zl = data.decode()[:-1]
        if zl == "10":
            break
        elif zl == "1": # 测试函数
            subprocess.call(shlex.split(f"python Serpent.py  launch  {game_name}"))
        elif zl == "2": # 从游戏中捕捉帧
            subprocess.call(shlex.split(f"python Serpent.py capture frame {game_name} 1"))
        elif zl == "3":
            subprocess.call(shlex.split(f"python Serpent.py dashboard"))
        elif zl == "4":
            game.launch() # 启动游戏
        elif zl == "5":
            game.launch(dry_run=True) # 激活窗口
        elif zl == "6":
            game.printscreen()

        response = 'Hello, client!'
        server_socket.sendto(response.encode(), client_address)


def main():
    print("控制台启动")
    # execute()
    UDP()

if __name__ == "__main__":
    main()


'''
##分别运行以下两行命令
 
docker run -dit --name emqx -p 18083:18083 -p 1883:1883 -p 8083:8083 -p 8084:8084 emqx/emqx:latest
 
docker exec -it  emqx /bin/sh

'''