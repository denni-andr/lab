import os

MAX_SIZE = 100

def main():
    # Create two pipes: one for parent-to-child (p2c) and one for child-to-parent (c2p)
    p2c = os.pipe()  # Parent-to-Child
    c2p = os.pipe()  # Child-to-Parent

    # Fork the process
    pid = os.fork()

    if pid > 0:  # Parent process
        os.close(p2c[0])  # Close read end of p2c
        os.close(c2p[1])  # Close write end of c2p

        # Parent sends a message to the child
        msg = input("Parent, enter your message: ")
        os.write(p2c[1], msg.encode())  # Send message to the child
        os.close(p2c[1])  # Close write end after sending

        # Parent reads the child's response
        reply = os.read(c2p[0], MAX_SIZE).decode()
        print("Parent received:", reply)
        os.close(c2p[0])  # Close read end after receiving

    else:  # Child process
        os.close(p2c[1])  # Close write end of p2c
        os.close(c2p[0])  # Close read end of c2p

        # Child reads the parent's message
        reply = os.read(p2c[0], MAX_SIZE).decode()
        print("Child received:", reply)
        os.close(p2c[0])  # Close read end after receiving

        # Child sends a response back to the parent
        msg = input("Child, enter your response: ")
        os.write(c2p[1], msg.encode())  # Send response to the parent
        os.close(c2p[1])  # Close write end after sending

if __name__ == "__main__":
    main()
