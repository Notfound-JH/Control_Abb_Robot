import socket
import time
import errno

if __name__ == "__main__":
    server_address = ('192.168.125.10', 3000)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(server_address)
    server_socket.listen(1)
    print(f"服务器正在监听 {server_address}...")

    # 设置超时时间而非非阻塞模式（更简单可靠）
    server_socket.settimeout(1.0)
    client_socket = None

    try:
        while True:
            # 等待客户端连接
            if client_socket is None:
                try:
                    print("等待客户端连接...")
                    client_socket, client_address = server_socket.accept()
                    # 设置客户端超时
                    client_socket.settimeout(1.0)
                    print(f"客户端 {client_address} 已连接")
                except socket.timeout:
                    continue  # 继续等待连接
                except Exception as e:
                    print(f"接受连接时出错: {e}")
                    time.sleep(1)
                    continue

            try:
                # 接收客户端消息
                data = client_socket.recv(4096)
                if not data:  # 客户端主动关闭连接
                    print("客户端断开连接")
                    client_socket.close()
                    client_socket = None
                    continue

                timesteps = time.time()
                message = data.decode('utf-8')
                print(f"{timesteps} steps 收到消息: {message}")

                # 准备响应
                response = f"服务器已收到: {message}"

                # 使用普通send配合循环，更可控
                total_sent = 0
                while total_sent < len(response):
                    try:
                        sent = client_socket.send(response[total_sent:].encode('utf-8'))
                        total_sent += sent
                    except socket.timeout:
                        print("发送超时，尝试重新连接")
                        client_socket.close()
                        client_socket = None
                        break
                    except socket.error as e:
                        if e.errno in (errno.EAGAIN, errno.EWOULDBLOCK):
                            time.sleep(0.01)  # 短暂等待并重试
                        else:
                            print(f"发送错误: {e}")
                            client_socket.close()
                            client_socket = None
                            break

                if client_socket:
                    print("数据发送成功")

            except socket.timeout:
                # 可以选择发送心跳包或忽略
                continue
            except socket.error as e:
                if e.errno == errno.ECONNRESET:
                    print("连接被客户端重置")
                else:
                    print(f"通信错误: {e}")
                if client_socket:
                    client_socket.close()
                    client_socket = None
            except Exception as e:
                print(f"未知错误: {e}")
                if client_socket:
                    client_socket.close()
                    client_socket = None

            time.sleep(0.01)  # 避免CPU占用过高

    except KeyboardInterrupt:
        print("\n程序被用户中断")
    finally:
        if client_socket:
            client_socket.close()
        server_socket.close()
        print("连接已关闭")
