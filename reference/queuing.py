import threading
from queue import Queue

def do_stuff(q):
    while True:
        print(q.get())
        q.task_done()
        
q = Queue(maxsize=0)
num_threads = 10

for x in range(num_threads):
    worker = threading.Thread(target=do_stuff, args=(q,))
    worker.daemon = True
    worker.start()

for y in range (10):
    for x in range(100):
        q.put(x + y * 100)
    q.join()
    print("Batch " + str(y) + " Done")
    
""" waits until the queue is empty and all of the threads are done working 
 (which it knows because task_done() will have been called on every element of the queue)
 
 Tutorial: https://www.troyfawkes.com/learn-python-multithreading-queues-basics/
"""
