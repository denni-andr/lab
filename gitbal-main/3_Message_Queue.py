from multiprocessing import Process, Queue
import time

def sender(queue):
    message = "Hello from Sender"
    message1="hello from s2"
    queue.put(message)  # Sending message to the queue
    queue.put(message1)
    print("Sender Process: Sent message:", message)
    print("Sender Process: Sent message:", message1)

def receiver(queue):
    time.sleep(1)  # Wait for sender to send message
    message = queue.get()  # Receiving message from the queue
    m2=queue.get()
    print("Receiver Process: Received message:", message)
    print("Receiver Process: Received message:", m2)
    

if __name__ == "__main__":
    queue = Queue()

    sender_process = Process(target=sender, args=(queue,))
    receiver_process = Process(target=receiver, args=(queue,))

    sender_process.start()
    receiver_process.start()

    sender_process.join()
    receiver_process.join()




# 3-msg-copy

# from multiprocessing import Process, Queue
# import time

# def sender(queue):
#     messages = ["Message 1 from sender", "Message 2 from sender", "Message 3 from sender", "STOP"]
    
#     for message in messages:
#         queue.put(message)
#         print(f"Sender: Sent '{message}' to the queue.")
#         time.sleep(1)  # Simulate some delay between messages

# def receiver(queue):
#     while True:
#         # Wait for a message from the queue
#         message = queue.get()
#         print(f"Receiver: Received '{message}' from the queue.")
        
#         # Break the loop if the termination message is received
#         if message == "STOP":
#             print("Receiver: Termination signal received. Stopping.")
#             break

# if __name__ == "__main__":
#     # Create a queue for inter-process communication
#     queue = Queue()

#     # Create the sender and receiver processes
#     sender_process = Process(target=sender, args=(queue,))
#     receiver_process = Process(target=receiver, args=(queue,))

#     # Start the processes
#     sender_process.start()
#     receiver_process.start()

#     # Wait for both processes to complete
#     sender_process.join()
#     receiver_process.join()

