from enum import Enum


class LogLevel(Enum):
    INFO = "INFO"
    WARN = "WARN"
    ERROR = "ERROR"
    WARNING = "WARNING"
    DEBUG = "DEBUG"
    TRACE = "TRACE"

class LogSection(Enum):
    PLAN = 'plan'
    APPLY = 'apply'
