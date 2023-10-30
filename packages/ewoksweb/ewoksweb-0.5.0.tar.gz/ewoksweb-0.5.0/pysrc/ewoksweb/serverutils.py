import os


def get_static_root() -> str:
    return os.path.join(os.path.dirname(__file__), "static")


def get_test_config() -> str:
    return os.path.join(os.path.dirname(__file__), "tests", "resources", "config.py")
