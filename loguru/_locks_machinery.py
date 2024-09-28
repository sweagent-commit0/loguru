import os
import threading
import weakref
if not hasattr(os, 'register_at_fork'):
else:
    logger_locks = weakref.WeakSet()
    handler_locks = weakref.WeakSet()
    os.register_at_fork(before=acquire_locks, after_in_parent=release_locks, after_in_child=release_locks)