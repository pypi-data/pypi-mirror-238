import abc

from sona.core.messages import Context
from sona.utils.common import import_class


class MiddlewareBase:
    def __call__(self, on_context):
        def func(ctx: Context):
            return self.wrapper_func(ctx, on_context)

        return func

    @abc.abstractmethod
    def wrapper_func(self, ctx: Context, on_context):
        return NotImplemented

    @classmethod
    def load_class(cls, import_str):
        _cls = import_class(import_str)
        if _cls not in cls.__subclasses__():
            raise Exception(f"Unknown middleware class: {import_str}")
        return _cls
