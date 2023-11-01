import threading
import queue


class Worker(threading.Thread):
    def __init__(self, queue):
        super().__init__()
        self.queue = queue
        self.daemon = True  # Set as a daemon so it will close when the main thread closes

    def run(self):
        while True:
            try:
                # Get a job from the queue
                func, args = self.queue.get(timeout=3)  # Wait for 3 seconds to get a job
                if func is None:
                    # If the job is None, break the loop and end the worker
                    break
                # Execute the job with provided arguments
                func(*args)
            except queue.Empty:
                continue
            finally:
                # Mark the task as done in the queue
                self.queue.task_done()


class Parallelism:
    def __init__(self, n_workers):
        self.queue = queue.Queue()
        self.workers = []

        for _ in range(n_workers):
            worker = Worker(self.queue)
            self.workers.append(worker)
            worker.start()

    def add_job(self, func, args=()):
        self.queue.put((func, args))

    def wait_completion(self):
        # Wait until the queue is empty and all tasks are done
        self.queue.join()

        # Stop all worker threads after all tasks are done
        for _ in self.workers:
            self.queue.put((None, None))
        for worker in self.workers:
            worker.join()