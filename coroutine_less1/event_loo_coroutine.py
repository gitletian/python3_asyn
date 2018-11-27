# coding: utf-8
# __author__: ""


from bisect import insort
from collections import deque
from coroutine_less1.fib import timed_fib
from functools import partial
from time import time
import selectors
import sys
import types
import pdb


class sleep_for_seconds(object):
    """
    Yield an object of this type from a coroutine to have it "sleep" for the
    given number of seconds.
    """
    def __init__(self, wait_time):
        self._wait_time = wait_time


class EventLoop(object):
    """
    Implements a simplified coroutine-based event loop as a demonstration.
    Very similar to the "Trampoline" example in PEP 342, with exception
    handling taken out for simplicity, and selectors added to handle file IO
    """
    def __init__(self, *tasks):
        self._running = False
        self._selector = selectors.DefaultSelector()
        # Queue of functions scheduled to run
        self._tasks = deque(tasks)
        # (coroutine, stack) pair of tasks waiting for input from stdin
        self._tasks_waiting_on_stdin = []
        # List of (time_to_run, task) pairs, in sorted order
        self._timers = []
        # Register for polling stdin for input to read
        self._selector.register(sys.stdin, selectors.EVENT_READ)

    def resume_task(self, coroutine, value=None, stack=()):
        result = coroutine.send(value)
        print("===========result type = {0}".format(type(result)))
        if isinstance(result, types.GeneratorType):
            print("==============GeneratorType")
            self.schedule(result, None, (coroutine, stack))
        elif isinstance(result, sleep_for_seconds):
            print("==============sleep_for_seconds")
            self.schedule(coroutine, None, stack, time() + result._wait_time)
        elif result is sys.stdin:
            print("==============sys.stdin")
            self._tasks_waiting_on_stdin.append((coroutine, stack))
        elif stack:
            self.schedule(stack[0], result, stack[1])
            print("==============stack")

    def schedule(self, coroutine, value=None, stack=(), when=None):
        """
        Schedule a coroutine task to be run, with value to be sent to it, and
        stack containing the coroutines that are waiting for the value yielded
        by this coroutine.
        """
        # Bind the parameters to a function to be scheduled as a function with
        # no parameters.
        task = partial(self.resume_task, coroutine, value, stack)

        if when:
            insort(self._timers, (when, task))
        else:
            self._tasks.append(task)

        print("==========len(self._timers) == {0}".format(len(self._timers)))
        print("==========len(self._tasks) == {0}".format(len(self._tasks)))

    def stop(self):
        self._running = False

    def do_on_next_tick(self, func, *args, **kwargs):
        self._tasks.appendleft(partial(func, *args, **kwargs))

    def run_forever(self):
        self._running = True
        while self._running:
            # First check for available IO input
            for key, mask in self._selector.select(0):
                line = key.fileobj.readline().strip()
                for task, stack in self._tasks_waiting_on_stdin:
                    self.schedule(task, line, stack)
                self._tasks_waiting_on_stdin.clear()
            # Next, run the next task
            if self._tasks:
                task = self._tasks.popleft()
                task()
            # Finally run time scheduled tasks
            while self._timers and self._timers[0][0] < time():
                task = self._timers[0][1]
                del self._timers[0]
                task()
        self._running = False


def print_every(message, interval):
    """
    Coroutine task to repeatedly print the message at the given interval
    (in seconds)
    """
    while True:
        print("{} - {}".format(int(time()), message))
        yield sleep_for_seconds(interval)


def read_input(loop):
    """
    Coroutine task to repeatedly read new lines of input from stdin, treat
    the input as a number n, and calculate and display fib(n).
    """
    while True:
        line = yield sys.stdin
        if line == 'exit':
            loop.do_on_next_tick(loop.stop)
            continue
        n = int(line)
        print("fib({}) = {}".format(n, timed_fib(n)))


def main():
    loop = EventLoop()
    hello_task = print_every('Hello world!', 3)
    fib_task = read_input(loop)
    loop.schedule(hello_task)
    loop.schedule(fib_task)
    loop.run_forever()


if __name__ == '__main__':
    main()

