
import socket

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        message = input("Enter a string (type 'exit' to close): ")
        
        # If user types 'exit', break the loop and close the connection
        if message.lower() == "exit":
            print("Closing connection...")
            break
        
        s.sendall(message.encode())  # Send the message to the server
        data = s.recv(1024)  # Receive data from the server

        print(f"Received {data.decode()}")  # Display the received message
