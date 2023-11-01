import hashlib
import os
import sys
import traceback


def import_class(import_str):
    mod_str, _sep, class_str = import_str.rpartition(".")
    __import__(mod_str)
    try:
        return getattr(sys.modules[mod_str], class_str)
    except AttributeError:
        raise ImportError(
            f"Class {class_str} cannot be found ({traceback.format_exception(*sys.exc_info())})"
        )


def zero_copy(in_fd, out_fd):
    ret = 0
    offset = 0
    while True:
        ret = os.sendfile(in_fd, out_fd, offset, 65536)
        offset += ret
        if ret == 0:
            break


def md5_content_hex(path):
    md5 = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            md5.update(chunk)
    return md5.hexdigest()
