import threading
import random

LOWER_NUM = 1
UPPER_NUM = 10000
BUFFER_SIZE = 100
MAX_COUNT = 10000

buffer = []
lock = threading.Lock()
producer_finished = False
consumers_finished = False

class Producer(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        global producer_finished
        for _ in range(MAX_COUNT):
            num = random.randint(LOWER_NUM, UPPER_NUM)
            with lock:
                buffer.append(num)
                with open("all.txt", "a") as f:
                    f.write(str(num) + "\n")
        producer_finished = True

class Consumer(threading.Thread):
    def __init__(self, is_even):
        super().__init__()
        self.is_even = is_even

    def run(self):
        global consumers_finished
        while not producer_finished or buffer:
            with lock:
                if buffer:
                    num = buffer.pop()
                    if (num % 2 == 0 and self.is_even) or (num % 2 != 0 and not self.is_even):
                        filename = "even.txt" if self.is_even else "odd.txt"
                        with open(filename, "a") as f:
                            f.write(str(num) + "\n")
                elif not buffer:
                    continue
        consumers_finished = True

if __name__ == "__main__":
    producer_thread = Producer()
    consumer_even_thread = Consumer(is_even=True)
    consumer_odd_thread = Consumer(is_even=False)

    producer_thread.start()
    consumer_even_thread.start()
    consumer_odd_thread.start()

    producer_thread.join()
    consumer_even_thread.join()
    consumer_odd_thread.join()

    print("All threads finished.")
