import asyncio
import logging
import weakref
from ._asyncio_loop import get_running_loop, get_task_loop

class StreamSink:

    def __init__(self, stream):
        self._stream = stream
        self._flushable = callable(getattr(stream, 'flush', None))
        self._stoppable = callable(getattr(stream, 'stop', None))
        self._completable = asyncio.iscoroutinefunction(getattr(stream, 'complete', None))

class StandardSink:

    def __init__(self, handler):
        self._handler = handler

class AsyncSink:

    def __init__(self, function, loop, error_interceptor):
        self._function = function
        self._loop = loop
        self._error_interceptor = error_interceptor
        self._tasks = weakref.WeakSet()

    def __getstate__(self):
        state = self.__dict__.copy()
        state['_tasks'] = None
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self._tasks = weakref.WeakSet()

class CallableSink:

    def __init__(self, function):
        self._function = function