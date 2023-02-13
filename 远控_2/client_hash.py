import os
import socket
import struct


def receive_file(server_socket, file_name):
    with open(file_name, 'wb') as f:
        while True:
            # # 接收并解析文件长度
            file_size_bytes = server_socket.recv(4)
            # 输出调试信息
            print(f'[DEBUG] received file size bytes: {file_size_bytes}')
            # 如果接收到的字节数为0，说明文件传输已结束
            if not file_size_bytes:
                break
            # 将字节数组解包为整数，即文件大小
            file_size = struct.unpack('!I', file_size_bytes)[0]

            # 接收文件内容
            while file_size > 0:
                # 接收文件内容
                data = server_socket.recv(4096)
                # 输出调试信息
                print(f'[DEBUG] received data: {data}')
                # 如果接收到的字节数为0，说明文件传输已结束
                if not data:
                    break
                # 减少剩余的字节数
                file_size -= len(data)
                # 将接收到的数据写入文件
                f.write(data)
    # 输出成功接收文件的消息
    print(f'[+] Received file: {file_name}')


def send_file(server_socket, file_name):
    with open(file_name, 'rb') as f:
        file_size = os.path.getsize(file_name)
        file_size_bytes = struct.pack('!I', file_size)

        # 发送文件长度
        server_socket.sendall(file_size_bytes)

        # 发送文件内容
        while file_size > 0:
            data = f.read(4096)
            if not data:
                break
            file_size -= len(data)
            server_socket.sendall(data)
    print(f'[+] Sent file: {file_name}')


def execute_command(server_socket, command):
    # 发送命令并打印输出
    command = command.strip()
    server_socket.sendall(command.encode())
    output = server_socket.recv(4096).decode()
    print(output)


def execute_get_command(server_socket, command):
    # Get file from server
    command_parts = command.split()
    file_name = " ".join(command_parts[1:])
    receive_file(server_socket, file_name)


def execute_put_command(server_socket, command):
    # Put file on server
    command_parts = command.split()
    file_name = " ".join(command_parts[1:])
    send_file(server_socket, file_name)


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect(('127.0.0.1', 8080))
    response = server_socket.recv(4096).decode()
    print(response)
    if response != '[+] Access granted.':
        server_socket.close()
        return
    while True:
        command = input('>>> ')
        if command == 'exit':
            server_socket.close()
            break
        parts = command.split()
        if len(parts) == 0:
            continue
        elif command.startswith('get'):
            file_name = command.split()[1]
            receive_file(server_socket, file_name)
            # execute_get_command(server_socket, command)
        elif command.startswith('put'):
            file_name = command.split()[1]
            send_file(server_socket, file_name)
            # execute_put_command(server_socket, command)
        else:
            execute_command(server_socket, command)


if __name__ == '__main__':
    main()
