import logging
import sys

formatter = logging.Formatter('[%(levelname)s]: %(asctime)s - %(name)s - %(message)s')

koppeltaal_logger = logging.getLogger(__name__)
koppeltaal_logger.setLevel(logging.DEBUG)

console_logger = logging.StreamHandler(sys.stdout)
console_logger.setLevel(logging.DEBUG)
console_logger.setFormatter(formatter)

file_logger = logging.FileHandler(r'koppeltaal.log')  # FIXME: make optional
file_logger.setLevel(logging.INFO)
file_logger.setFormatter(formatter)

koppeltaal_logger.addHandler(console_logger)
koppeltaal_logger.addHandler(file_logger)


class NoopLogger:
    def critical(self, msg, **kwargs):
        ...

    def debug(self, msg, **kwargs):
        ...

    def error(self, msg, **kwargs):
        ...

    def exception(self, msg, **kwargs):
        ...

    def fatal(self, msg, **kwargs):
        ...

    def info(self, msg, **kwargs):
        ...

    def log(self, msg, **kwargs):
        ...

    def warning(self, msg, **kwargs):
        ...

    def warn(self, msg, **kwargs):
        ...


noop_koppeltaal_logger = NoopLogger()
