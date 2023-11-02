import importlib


def import_class(class_path: str) -> type:
    """Import class from module path

    :param class_path: path to class
    :type class_path: str
    :return: imported class
    """
    module_path, class_name = class_path.rsplit('.', 1)
    module = importlib.import_module(module_path)

    return getattr(module, class_name)
