import datetime
import logging
import os


class Logger:
    def __init__(self, logger_name, level=logging.DEBUG, log_path='./logs'):
        self.__configure_logger(logger_name, level, log_path)

    def __configure_logger(self, logger_name, level, log_path):
        log_dir = log_path
        formatted_datetime = datetime.datetime.now().strftime('%Y_%m_%d__%H:%M:%S')

        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        log_file_name = f"{log_dir}/{logger_name}-{formatted_datetime}.log"

        with open(log_file_name, 'w') as f:
            f.write('')

        self.logger = logging.getLogger(logger_name)

        self.logger.setLevel(level)

        file_handler = logging.FileHandler(log_file_name)
        stream_handler = logging.StreamHandler()

        logging_format = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')

        file_handler.setFormatter(logging_format)
        stream_handler.setFormatter(logging_format)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(stream_handler)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)
