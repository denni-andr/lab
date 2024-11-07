import socket

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def process_request(request):
    parts = request.split()
    if len(parts) != 3:
        return "Invalid request format."

    command, a, b = parts
    try:
        a, b = int(a), int(b)
    except ValueError:
        return "Arguments must be integers."

    if command == "add":
        return str(add(a, b))
    elif command == "subtract":
        return str(subtract(a, b))
    else:
        return "Unknown command."

# Set up the server
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5000
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(1)
print(f"Server is listening on {SERVER_HOST}:{SERVER_PORT}")


client_socket, client_address = server_socket.accept()
print(f"Connection from {client_address} established.")

# Receive and process request
request = client_socket.recv(1024).decode()
print(f"Received request: {request}")
result = process_request(request)
print(f"Sending result: {result}")

# Send the result and close connection
client_socket.send(result.encode())
client_socket.close()
