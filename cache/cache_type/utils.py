import sys
import typing as _t

from werkzeug.utils import ImportStringError


def import_string(import_name: str, silent: bool = False) -> _t.Any:
    import_name = import_name.replace(":", ".")
    try:
        try:
            __import__(import_name)
            print(import_name)
        except ImportError:
            if "." not in import_name:
                raise
        else:
            return sys.modules[import_name]

        module_name, obj_name = import_name.rsplit(".", 1)
        module = __import__(module_name, globals(), locals(), [obj_name])
        try:
            return getattr(module, obj_name)
        except AttributeError as e:
            raise ImportError(e) from None

    except ImportError as e:
        if not silent:
            raise ImportStringError(import_name, e).with_traceback(
                sys.exc_info()[2]
            ) from None

    return None
