import socket

# Set up the client
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5000

# Connect to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_HOST, SERVER_PORT))

# Send a function call request
request = input("Enter request (e.g., 'add 5 3' or 'subtract 10 4'): ")
client_socket.send(request.encode())

# Receive and display the result
result = client_socket.recv(1024).decode()
print(f"Result from server: {result}")

# Close the connection
client_socket.close()
