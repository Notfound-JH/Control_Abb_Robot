import socket
import time
import errno

if __name__ == "__main__":
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('192.168.125.10', 3000)
    server_socket.bind(server_address)
    server_socket.listen(1)
    print(f"服务器正在监听 {server_address}...")
    
    # 设置为非阻塞模式
    server_socket.setblocking(0)
    
    client_socket = None
    
    try:
        while True:
            # 尝试接受连接
            if client_socket is None:
                try:
                    client_socket, client_address = server_socket.accept()
                    client_socket.setblocking(0)  # 设置客户端为非阻塞
                    print(f"客户端 {client_address} 已连接")
                except socket.error as e:
                    if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                        raise
                    time.sleep(0.01)
                    continue
            
            # 尝试接收数据
            try:
                data = client_socket.recv(4096)
                if not data:
                    print("客户端断开连接")
                    client_socket.close()
                    client_socket = None
                    continue
                
                timesteps = time.time()
                message = data.decode('utf-8')
                print(f"{timesteps} steps 收到消息: {message}")
                
                # 准备响应
                response = f"服务器已收到: {message}"
                
                # 发送响应（非阻塞方式）
                total_sent = 0
                while total_sent < len(response):
                    try:
                        sent = client_socket.send(response[total_sent:].encode('utf-8'))
                        total_sent += sent
                    except socket.error as e:
                        if e.errno == errno.EAGAIN or e.errno == errno.EWOULDBLOCK:
                            time.sleep(0.01)  # 等待缓冲区可用
                            continue
                        else:
                            raise
                
                print("数据发送成功")
                
            except socket.error as e:
                if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                    print(f"通信错误: {e}")
                    if client_socket:
                        client_socket.close()
                        client_socket = None
                time.sleep(0.01)
    
    # except KeyboardInterrupt:
    #     print("\n程序被用户中断")
    finally:
        if client_socket:
            client_socket.close()
        server_socket.close()
        print("连接已关闭")
