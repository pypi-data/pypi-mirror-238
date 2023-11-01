import threading
import queue


class Worker(threading.Thread):
    def __init__(self, queue):
        super().__init__()
        self.queue = queue
        self.daemon = True  # Set as a daemon so it will close when the main thread closes

    def run(self):
        while True:
            # Get a job from the queue and block indefinitely until a job is available
            func, args = self.queue.get()

            # Execute the job with provided arguments
            func(*args)

            # Mark the task as done in the queue
            self.queue.task_done()


class ThreadPool:
    def __init__(self, n_workers):
        self.queue = queue.Queue()
        self.workers = []

        for _ in range(n_workers):
            worker = Worker(self.queue)
            self.workers.append(worker)
            worker.start()

    def add_job(self, func, args=()):
        self.queue.put((func, args))
