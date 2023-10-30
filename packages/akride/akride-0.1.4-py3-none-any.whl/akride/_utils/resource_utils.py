import importlib.resources

from akride.core import conf


def get_absolute_path(file_name):
    with importlib.resources.path(conf, file_name) as p:
        return str(p)
