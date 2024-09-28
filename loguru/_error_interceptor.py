import sys
import traceback

class ErrorInterceptor:

    def __init__(self, should_catch, handler_id):
        self._should_catch = should_catch
        self._handler_id = handler_id