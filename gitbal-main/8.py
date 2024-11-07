import multiprocessing
import time
from multiprocessing import shared_memory, Queue

def writer(shared_mem_name, input_queue):
    # Access the existing shared memory
    existing_shm = shared_memory.SharedMemory(name=shared_mem_name)
    
    while True:
        # Retrieve message from the queue
        message = input_queue.get()
        
        # Check if the message is "exit"
        if message == "exit":
            # Write the exit message to shared memory
            existing_shm.buf[:len(message)] = message.encode()
            print("Writer: Exiting...")
            break

        # Write the message to shared memory
        existing_shm.buf[:len(message)] = message.encode()
        print(f"Writer: Data written to shared memory: {message}")
        
        # Small delay to allow reader to read
        time.sleep(1)
    
    # Close the shared memory access
    existing_shm.close()

def reader(shared_mem_name, size):
    # Access the existing shared memory
    existing_shm = shared_memory.SharedMemory(name=shared_mem_name)
    
    while True:
        # Read data from shared memory
        message = bytes(existing_shm.buf[:size]).decode().strip()
        # Check if the message is "exit"
        if "exit" in message:
            print("Reader: 'exit' received, stopping reader.")
            break
        
        # Print the read message
        if message:
            print(f"Reader: Data read from shared memory: {message}")
        
        # Small delay to allow writer to write
        time.sleep(5)
    
    # Close the shared memory access
    existing_shm.close()

if __name__ == "__main__":
    # Create a Queue to pass messages from main to the writer process
    input_queue = Queue()

    # Initial message for shared memory
    initial_message = " " * 100  # Allocate enough space for messages
    
    # Create a shared memory segment with a fixed size
    shm = shared_memory.SharedMemory(create=True, size=len(initial_message))
    
    # Start writer process with shared memory and input queue
    writer_process = multiprocessing.Process(target=writer, args=(shm.name, input_queue))
    writer_process.start()
    
    # Start reader process
    reader_process = multiprocessing.Process(target=reader, args=(shm.name, len(initial_message)))
    reader_process.start()
    
    # Main loop to get user input and send it to the writer process via the queue
    while True:
        message = input("Enter a message: ")
        input_queue.put(message)  # Send the message to the writer process
        
        if message == "exit":
            break

    # Wait for both processes to complete
    writer_process.join()
    reader_process.join()
    
    # Clean up the shared memory
    shm.close()
    shm.unlink()