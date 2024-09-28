import builtins
import inspect
import io
import keyword
import linecache
import os
import re
import sys
import sysconfig
import tokenize
import traceback
if sys.version_info >= (3, 11):
else:
    try:
        from exceptiongroup import ExceptionGroup
    except ImportError:

class SyntaxHighlighter:
    _default_style = {'comment': '\x1b[30m\x1b[1m{}\x1b[0m', 'keyword': '\x1b[35m\x1b[1m{}\x1b[0m', 'builtin': '\x1b[1m{}\x1b[0m', 'string': '\x1b[36m{}\x1b[0m', 'number': '\x1b[34m\x1b[1m{}\x1b[0m', 'operator': '\x1b[35m\x1b[1m{}\x1b[0m', 'punctuation': '\x1b[1m{}\x1b[0m', 'constant': '\x1b[36m\x1b[1m{}\x1b[0m', 'identifier': '\x1b[1m{}\x1b[0m', 'other': '{}'}
    _builtins = set(dir(builtins))
    _constants = {'True', 'False', 'None'}
    _punctation = {'(', ')', '[', ']', '{', '}', ':', ',', ';'}
    _strings = {tokenize.STRING}
    _fstring_middle = None
    if sys.version_info >= (3, 12):
        _strings.update({tokenize.FSTRING_START, tokenize.FSTRING_MIDDLE, tokenize.FSTRING_END})
        _fstring_middle = tokenize.FSTRING_MIDDLE

    def __init__(self, style=None):
        self._style = style or self._default_style

class ExceptionFormatter:
    _default_theme = {'introduction': '\x1b[33m\x1b[1m{}\x1b[0m', 'cause': '\x1b[1m{}\x1b[0m', 'context': '\x1b[1m{}\x1b[0m', 'dirname': '\x1b[32m{}\x1b[0m', 'basename': '\x1b[32m\x1b[1m{}\x1b[0m', 'line': '\x1b[33m{}\x1b[0m', 'function': '\x1b[35m{}\x1b[0m', 'exception_type': '\x1b[31m\x1b[1m{}\x1b[0m', 'exception_value': '\x1b[1m{}\x1b[0m', 'arrows': '\x1b[36m{}\x1b[0m', 'value': '\x1b[36m\x1b[1m{}\x1b[0m'}

    def __init__(self, colorize=False, backtrace=False, diagnose=True, theme=None, style=None, max_length=128, encoding='ascii', hidden_frames_filename=None, prefix=''):
        self._colorize = colorize
        self._diagnose = diagnose
        self._theme = theme or self._default_theme
        self._backtrace = backtrace
        self._syntax_highlighter = SyntaxHighlighter(style)
        self._max_length = max_length
        self._encoding = encoding
        self._hidden_frames_filename = hidden_frames_filename
        self._prefix = prefix
        self._lib_dirs = self._get_lib_dirs()
        self._pipe_char = self._get_char('│', '|')
        self._cap_char = self._get_char('└', '->')
        self._catch_point_identifier = ' <Loguru catch point here>'