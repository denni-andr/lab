import socket

# File to be sent
filename = "sample.txt"

# Set up the client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 5001))

# Open the file and send its contents
with open(filename, "rb") as file:
    data = file.read(1024)
    while data:
        client_socket.send(data)
        data = file.read(1024)

print("File has been sent successfully.")

# Close the connection
client_socket.close()
