import os
from multiprocessing import Process, Pipe, Queue

MAX_SIZE = 100

def parent_process(p2c_conn, c2p_conn, queue):
    # Parent sends a message to the child
    msg = input("Parent, enter your message: ")
    p2c_conn.send(msg)  # Send message to the child
    p2c_conn.close()  # Close the parent-to-child pipe after sending

    # Parent waits for child to signal that it's ready for the response
    queue.get()  # Block until child is ready for input
    
    # Prompt user for the child's response
    child_reply = input("Child, enter your response: ")
    c2p_conn.send(child_reply)  # Send the response to the parent process
    print("Parent received:", child_reply)
    c2p_conn.close()  # Close the child-to-parent pipe after sending

def child_process(p2c_conn, c2p_conn, queue):
    # Child reads the parent's message
    msg = p2c_conn.recv()  # Read from the parent-to-child pipe
    print("Child received:", msg)
    p2c_conn.close()  # Close the parent-to-child pipe after receiving

    # Notify the parent process that the child is ready for the response
    queue.put("ready")
    
    # Child receives the response back from the parent (simulating the child's reply)
    reply = c2p_conn.recv()
    # print("Child sends back:", reply)
    c2p_conn.close()  # Close the child-to-parent pipe after receiving

def main():
    # Create two pipes: one for parent-to-child (p2c) and one for child-to-parent (c2p)
    p2c_parent_conn, p2c_child_conn = Pipe()  # Pipe for Parent-to-Child communication
    c2p_parent_conn, c2p_child_conn = Pipe()  # Pipe for Child-to-Parent communication

    # Queue to signal readiness between processes
    queue = Queue()

    # Start the child process
    child = Process(target=child_process, args=(p2c_child_conn, c2p_child_conn, queue))
    child.start()

    # Run the parent process
    parent_process(p2c_parent_conn, c2p_parent_conn, queue)

    # Wait for the child to finish
    child.join()

if __name__ == "__main__":
    main()
