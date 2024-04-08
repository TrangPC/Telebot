'''
ĐỊnh nghĩa các env sẽ sử dụng trong service
=> sau này triển khai service lên hệ thống service sẽ nhận được env đựợc config trên hệ thống
'''
import argparse
import os

SETTINGS = [
    ("--service-name", "service_name", "telegram_bot", "name of service"),
    ("--service-host", "service_host", "localhost", "host of service"),
    ("--service-port", "service_port", "8000", "port of service")

]

parser = argparse.ArgumentParser(description="Config running params for telegram bot service")

for argument in SETTINGS:
    parser.add_argument(argument[0], dest=argument[1], default=argument[2])
args = vars(parser.parse_known_args()[0])


def get_os_env():
    """
    Get environment variables and update to args if not None.

    Returns: None

    """
    for param_name in args.keys():
        param_value = os.environ.get(param_name.upper())
        if param_value is not None:
            args[param_name] = param_value


get_os_env()


def get_argument():
    """get config argument from terminal.

    Returns:
        (dict): config argument
    """
    return args
