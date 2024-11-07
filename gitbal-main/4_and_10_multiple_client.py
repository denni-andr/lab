import socket

def simple_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 5000))

    try:
        while True:
            message = input("You: ")
            if message.lower() == 'exit':
                client_socket.sendall(message.encode('utf-8'))
                print("Disconnected from server...")
                break
            client_socket.sendall(message.encode('utf-8'))
            response = client_socket.recv(1024).decode('utf-8')
            print(response)
    except Exception as e:
        print(f"Connection error: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    simple_client()
