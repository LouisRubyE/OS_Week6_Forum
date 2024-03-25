import threading
import random
import time

LOWER_NUM = 1
UPPER_NUM = 10000
BUFFER_SIZE = 100
MAX_COUNT = 10000

buffer = []
lock = threading.Lock()
producer_finished = False
consumers_finished = False

def producer():
    global producer_finished
    for _ in range(MAX_COUNT):
        num = random.randint(LOWER_NUM, UPPER_NUM)
        with lock:
            buffer.append(num)
            with open("all.txt", "a") as f:
                f.write(str(num) + "\n")
    producer_finished = True

def consumer_even():
    global consumers_finished
    while not producer_finished or buffer:
        with lock:
            if buffer and buffer[-1] % 2 == 0:
                num = buffer.pop()
                with open("even.txt", "a") as f:
                    f.write(str(num) + "\n")
            elif not buffer:
                continue
            else:
                continue
    consumers_finished = True

def consumer_odd():
    global consumers_finished
    while not producer_finished or buffer:
        with lock:
            if buffer and buffer[-1] % 2 != 0:
                num = buffer.pop()
                with open("odd.txt", "a") as f:
                    f.write(str(num) + "\n")
            elif not buffer:
                continue
            else:
                continue
    consumers_finished = True

if __name__ == "__main__":
    start_time = time.time()

    producer_thread = threading.Thread(target=producer)
    consumer_even_thread = threading.Thread(target=consumer_even)
    consumer_odd_thread = threading.Thread(target=consumer_odd)

    producer_thread.start()
    consumer_even_thread.start()
    consumer_odd_thread.start()

    producer_thread.join()
    consumer_even_thread.join()
    consumer_odd_thread.join()

    end_time = time.time()

    print("All threads finished.")
    print("Execution time:", end_time - start_time)
