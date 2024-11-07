# import socket
# import threading

# clients = []

# def handle_client(connection):
#     clients.append(connection)
#     try:
#         while True:
#             message = connection.recv(1024).decode('utf-8')
#             if not message:
#                 break
#             print(f"Client: {message}")
#             # Broadcast message to all clients except the sender
#             for client in clients:
#                 if client != connection:
#                     client.sendall(f"Broadcast from another client: {message}".encode('utf-8'))
#     finally:
#         clients.remove(connection)
#         connection.close()

# def simple_server():
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
#         server_socket.bind(('localhost', 5000))
#         server_socket.listen(5)
#         print("Server is listening on port 5000...")

#         while True:
#             connection, _ = server_socket.accept()
#             threading.Thread(target=handle_client, args=(connection,)).start()

# if __name__ == "__main__":
#     simple_server()

import socket
import threading

clients = []

def handle_client(connection, address):
    clients.append(connection)
    try:
        while True:
            message = connection.recv(1024).decode('utf-8')
            if not message:
                break
            if message.lower() == 'exit':
                print(f"Client {address} disconnected.")
                break
            
            print(f"Client {address}: {message}")
            
            # Broadcast message to all clients except the sender
            for client in clients:
                if client != connection:
                    try:
                        client.sendall(f"Broadcast from {address}: {message}".encode('utf-8'))
                    except Exception as e:
                        print(f"Failed to send to client {client}: {e}")
    except Exception as e:
        print(f"Connection error with client {address}: {e}")
    finally:
        clients.remove(connection)
        connection.close()
        # Notify remaining clients about disconnection
        for client in clients:
            try:
                client.sendall(f"Client {address} has left the chat.".encode('utf-8'))
            except Exception as e:
                print(f"Failed to send disconnect notice to client {client}: {e}")

def simple_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(('localhost', 5000))
        server_socket.listen(5)
        print("Server is listening on port 5000...")

        while True:
            connection, address = server_socket.accept()
            print(f"New connection from {address}")
            threading.Thread(target=handle_client, args=(connection, address)).start()

if __name__ == "__main__":
    simple_server()
