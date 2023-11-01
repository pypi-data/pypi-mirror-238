"""
ThreadPool class, which supports run tasks with timeout.
"""

import ctypes
import time
from queue import Queue
from threading import Thread
from typing import List


class WorkerThread:
    name: str
    thread: Thread = None
    start_time: int = 0
    task_timeout: int = 0
    task_queue: Queue

    def __init__(self, name: str, task_queue: Queue) -> None:
        self.name = name
        self.task_queue = task_queue

    def is_alive(self) -> bool:
        if self.thread is not None:
            return self.thread.is_alive()
        return False

    def is_busy(self) -> bool:
        return self.start_time > 0

    def activate(self):
        self.task_timeout = 0
        self.start_time = 0
        self.busy = False
        self.thread = Thread(target=self.watch, daemon=True, name=self.name)
        self.thread.start()

    def shutdown(self):
        if not self.is_alive() or self.thread.ident is None:
            return
        try:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(self.thread.ident), ctypes.py_object(SystemExit))
        except:
            pass

    def watch(self):
        """工作线程的守护程序，从任务队列中读取任务，每次执行任务前，同步执行开始时间，任务超时限额，线程名称"""
        while True:
            if self.task_queue is None:
                break

            func, task_name, timeout, args, kwargs = self.task_queue.get()

            self.start_time = time.time()
            self.task_timeout = timeout
            self.thread.setName(f"{self.name}_{task_name}")

            func(*args, **kwargs)

            self.start_time = 0
            self.task_timeout = 0
            self.thread.setName(self.name)


class ThreadPool:
    """
    ThreadPool class, which supports run tasks with timeout.
    """

    busy_count: int = 0

    def __init__(
        self,
        num_workers: int = 1,
        timeout: float = 0,
        name_prefix: str = "Thread",
        enable_shutdown: bool = False,
    ) -> None:
        self.num_workers = num_workers
        self.timeout = timeout
        self.name_prefix = name_prefix
        self.enable_shutdown = enable_shutdown

        self.tasks = Queue()
        self.pool: List[WorkerThread] = [
            WorkerThread(name=f"{self.name_prefix}_{i}", task_queue=self.tasks) for i in range(num_workers)
        ]
        self.water_thread = Thread(target=self.watch, daemon=True, name=f"{self.name_prefix}_watcher")
        self.water_thread.start()

    def watch(self):
        """
        watch thread pool, if thread is timeout, kill it and create a new thread.
        """

        while True:
            if self.tasks is None:
                break

            busy_count = 0
            # 检查线程执行是否超时或结束。
            for worker in self.pool:
                if not worker.is_alive():
                    worker.activate()
                elif worker.is_busy():
                    busy_count += 1
                    # 判断是否超时
                    timeout = worker.task_timeout if worker.task_timeout > 0 else self.timeout
                    if self.enable_shutdown and time.time() - worker.start_time > timeout:
                        worker.shutdown()
                        worker.activate()

            self.busy_count = busy_count
            time.sleep(0.01)

    def submit(self, func, task_name: str = "", time: int = 0, *args, **kwargs) -> None:
        """
        run a task without timeout.

        Args:
            func: target function.
            task_name: task name.
            *args:  function args.
            **kwargs: function kwargs.
        """
        if self.tasks is None:
            return
        self.tasks.put([func, task_name, time, args, kwargs])

    @property
    def size(self) -> int:
        """
        count of thread pool which is alive..

        Returns:
            int: the count.
        """

        return self.busy_count

    @property
    def empty(self) -> bool:
        """
        whether empty the thread pools.

        Returns:
            bool: the result of whether all the thread tasks are done.
        """
        return self.busy_count == 0 and (self.tasks is None or self.tasks.empty())

    @property
    def names(self) -> list:
        """
        return names of cur pool.
        """
        names = []
        for thread in self.pool:
            names.append(thread.name)
        return names

    def shutdown(self):
        """shutdown the thread pool."""
        self.tasks = None

        for worker in self.pool:
            worker.shutdown()
            del worker
        self.pool.clear()
