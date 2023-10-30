"""
thread_utils.py - Thread Utilities Module

This module provides utility functions for working with threads in Python.

Usage:
    import abstract_utilities.thread_utils as thread_utils

Example:
    # Creating a thread
    my_thread = thread_utils.get_thread(target=my_function, args=(arg1, arg2), daemon=True)

    # Starting the thread
    thread_utils.start_thread(my_thread)

    # Verifying if a given object is a valid thread
    is_valid = thread_utils.verify_thread(my_thread)

    # Checking if a thread is alive
    if thread_utils.thread_alive(my_thread):
        print("Thread is alive")
    else:
        print("Thread is not alive")

This module is part of the `abstract_utilities` package.

Author: putkoff
Date: 10/25/2023
Version: 0.1.2
"""
import threading
import queue
from . import create_new_name,get_last_comp_list
class ThreadedEvent:
    def __init__(self, target_function,wait_function=None,termination_result=None,function_args={}):
        self._event = threading.Event()
        self._queue = queue.Queue()  # Add a queue for return values
        self._thread = threading.Thread(target=self._run, args=(target_function,wait_function,termination_result,function_args))
    def _run(self, target_function, wait_function, termination_result, function_args):
        print(f"Thread starting with event status: {self._event.is_set()}")
        while not self._event.is_set():
            print(f"In loop. Event status: {self._event.is_set()}")
            result = target_function(**function_args)
            if result:
                self._queue.put(result)  # Store the return value in the queue
            self._event.wait(1)  # This will wait for 1 second or until interrupted by calling `stop`.
        print(f"Thread {self._thread.name} is exiting.")
    def get_result(self):
        """Retrieve the result from the queue. Returns None if no result available."""
        if not self._queue.empty():
            return self._queue.get()
        return None
    def start(self):
        """Starts the thread."""
        self._thread.start()
    def stop(self):
        print(f"Attempting to stop thread {self._thread.name}")
        self._event.set()
        #  # Optionally, you can wait for the thread to finish.
    def wait(self,n=0):
        self._thread.wait(n)
    def join(self):
        self._thread.join()
    def is_alive(self):
        """Returns whether the thread is still running."""
        return self._thread.is_alive()
class ThreadManager:
    def __init__(self):
        self.threads = {}
        self.thread_name_list=[]
    def add_thread(self,name=None,target_function=None,wait_function=None,termination_result=None,function_args={},overwrite=False,make_default=True):
        if name == None:
            if make_default:
                name = 'Default_Thread_name'
            else:
                print('thread_name not provided and make_default is False... Aborting....')
                return
        if target_function == None:
            print('No Target Function... Aborting....')
            return
        if overwrite==False:
            name=create_new_name(name=name,names_list=self.all_thread_names())
        if name in self.thread_name_list:
            self.thread_name_list.remove(name)
        self.thread_name_list.append(name)
        """Add a thread with a name and target function."""
        self.threads[name] = ThreadedEvent(target_function=target_function,wait_function=wait_function,termination_result=termination_result,function_args=function_args)
        print(f"thread {name} added")
    def start(self, name,overwrite=False):
        """Start a specific thread by name."""
        if self.is_alive(name)==False:
            self.threads[name].start()
            print(f'thread {name} started')
    def wait(self,name,n=0):
        self.threads[name].wait(n)
    def join(self,name):
        self.threads[name].join()
    def stop(self, name, result=None):
        print(f"Attempting to stop thread with name: {name}")
        if self.check_name(name):
            if result:
                self.threads[name]._queue.put(result)
            self.threads[name].stop()
            print(f"Signal sent to stop thread {name}")
            print(f"Event status immediately after: {self.threads[name]._event.is_set()}")

        print(f'thread {name} stopped')
        return True
    def stop_last(self,name=None,result=None):
        str_name = f"for {name}" if name else ""
        print(f'stop_last: checking {str_name} to stopt it')
        if name ==None:
            name=get_last_comp_list(name,self.all_thread_names())
        if self.check_name(name):
            return self.stop(name,result=result)
        print(f'last_thread thread {name} not stopped')
        return False
    def start_all(self):
        """Start all threads."""
        for thread in self.threads.values():
            thread.start()

    def stop_all(self):
        """Stop all threads."""
        for thread in self.threads.values():
            thread.stop()

    def is_alive(self, name):
        """Check if a specific thread is alive by name."""
        print(f'checking if {name} is alive')
        if self.check_name(name):
            status = self.threads[name].is_alive()
            print(f'thread {name} is {"" if status else "not"} alive')
            return status
        return False
    def all_alive(self):
        """Return a dictionary indicating if each thread is alive."""
        return {name: thread.is_alive() for name, thread in self.threads.items()}
    def all_thread_names(self):
        return self.threads.keys()
    def get_last_result(self,name=None):
        str_name = f"for {name}" if name else ""
        print(f'getting last result {str_name} from thread name list')
        result = None
        if name:
            result_name=get_last_comp_list(name,self.all_thread_names())
            if self.check_name(name):
                result = self.threads[result_name].get_result()
        elif len(self.thread_name_list)>0:
            result = self.threads[self.thread_name_list[-1]].get_result()
        return result
    def check_name(self,name):
        print(f'checking name {name}')
        if name in self.all_thread_names():
            print(f'thread {name} found in thread_names')
            return True
        print(f'thread {name} not found in thread_names')
        return False
