import logging

auth_logger = logging.getLogger("auth")
auth_logger.setLevel(logging.INFO)


file_handler = logging.FileHandler("auth.log")
formatter = logging.Formatter("%(acstime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

if not auth_logger.handlers:
    auth_logger.addHandler(file_handler)


task_logger = logging.getLogger("taskmanager")
task_logger.setLevel(logging.INFO)

task_file_handler  = logging.FileHandler("taskmanager.log")    

task_file_handler.setFormatter(formatter)

if not task_logger.handlers:
    task_logger.addHandler(task_file_handler) 