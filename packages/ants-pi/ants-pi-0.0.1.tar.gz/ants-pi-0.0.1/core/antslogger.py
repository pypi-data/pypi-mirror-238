import os
import logging


class AntsLogger:
    def __init__(self):
        super(AntsLogger, self).__init__()
        self.log_path = os.path.join(os.path.dirname(os.getcwd()), 'logs')  # log storage path
        os.makedirs(self.log_path, exist_ok=True)  # make log storage
        self.logger = logging.getLogger()  # make logger
        self.logger.setLevel(logging.INFO)  # set logging severity
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')  # print format
        self.file_handler = logging.FileHandler(os.path.join(self.log_path, 'logs.log'))  # make log file
        self.file_handler.setFormatter(self.formatter)  # set log format
        self.logger.addHandler(self.file_handler)

    def throw_error(self, err_code, err_msg):
        self.logger.error(f'%s :: %s', err_code, err_msg)

    def throw_warning(self, warn_code, warn_msg):
        self.logger.warning(f'%s :: %s', warn_code, warn_msg)


# automatic initiation
logger_handler = AntsLogger()
