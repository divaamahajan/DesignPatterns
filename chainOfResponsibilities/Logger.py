from abc import ABC, abstractmethod

class Logger(ABC):
    INFO = 1
    DEBUG = 2
    ERROR = 3

    def __init__(self, next_logger=None):
        self.next_logger = next_logger

    def set_next(self, next_logger):
        self.next_logger = next_logger

    def log_message(self, level, message):
        if self._log(level, message):
            return
        if self.next_logger:
            self.next_logger.log_message(level, message)

    @abstractmethod
    def _log(self, level, message):
        pass

class InfoLogger(Logger):
    def _log(self, level, message):
        if level == Logger.INFO:
            print(f"INFO: {message}")
            return True
        return False

class DebugLogger(Logger):
    def _log(self, level, message):
        if level == Logger.DEBUG:
            print(f"DEBUG: {message}")
            return True
        return False

class ErrorLogger(Logger):
    def _log(self, level, message):
        if level == Logger.ERROR:
            print(f"ERROR: {message}")
            return True
        return False

class LoggerChain:
    def __init__(self):
        self.error_logger = ErrorLogger()
        self.debug_logger = DebugLogger(self.error_logger)
        self.info_logger = InfoLogger(self.debug_logger)

    def get_logger_chain(self):
        return self.info_logger

# Example Usage
if __name__ == "__main__":
    logger_chain = LoggerChain().get_logger_chain() #info logger

    logger_chain.log_message(Logger.INFO, "This is an info message.")
    logger_chain.log_message(Logger.DEBUG, "This is a debug message.")
    logger_chain.log_message(Logger.ERROR, "This is an error message.")
 