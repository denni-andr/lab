from multiprocessing import Process, Value
import time

def writer(shared_data):
    shared_data.value = 42  # Writing data into shared memory
    print("Writer Process: Written data:", shared_data.value)

def reader(shared_data):
    time.sleep(1)  # Wait for writer to write data
    print("Reader Process: Read data:", shared_data.value)

if __name__ == "__main__":
    shared_data = Value('i', 0)  # Initialize shared memory (integer)

    writer_process = Process(target=writer, args=(shared_data,))
    reader_process = Process(target=reader, args=(shared_data,))

    writer_process.start()
    reader_process.start()

    writer_process.join()
    reader_process.join()


# code for using string in shared memory above is for integer

# from multiprocessing import Process, Array
# import ctypes
# import time

# def writer(shared_data):
#     data = "Hello, World!"  # The string you want to write
#     shared_data.value = data.encode()  # Write the encoded string to shared memory
#     print("Writer Process: Written data:", shared_data.value.decode())

# def reader(shared_data):
#     time.sleep(1)  # Wait for writer to write data
#     print("Reader Process: Read data:", shared_data.value.decode())

# if __name__ == "__main__":
#     # Initialize shared memory for a string of 100 characters
#     shared_data = Array(ctypes.c_char, 100)

#     writer_process = Process(target=writer, args=(shared_data,))
#     reader_process = Process(target=reader, args=(shared_data,))

#     writer_process.start()
#     reader_process.start()

#     writer_process.join()
#     reader_process.join()
#     reader_process.start()

#     # Wait for both processes to complete
#     writer_process.join()
#     reader_process.join()
