import logging

auth_logger = logging.getLogger("auth")
auth_logger.setLevel(logging.INFO)


file_handler = logging.FileHandler("auth.log")
formatter = logging.Formatter("%(acstime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

if not auth_logger.handlers:
    auth_logger.addHandler(file_handler)