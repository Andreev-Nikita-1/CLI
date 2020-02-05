import os


def get_value(name):
    return os.environ[name] if name in os.environ else ""


def add_value(name, value):
    os.environ[name] = value



