import google.protobuf.message
import modal._output
import modal.functions
import modal.object
import modal_proto.api_pb2
import typing
import typing_extensions

T = typing.TypeVar("T")

class ClsMixin:
    @classmethod
    def __init_subclass__(cls):
        ...


def check_picklability(key, arg):
    ...


class _Obj:
    _functions: typing.Dict[str, modal.functions._Function]
    _inited: bool
    _entered: bool
    _local_obj: typing.Any
    _local_obj_constr: typing.Union[typing.Callable[[], typing.Any], None]

    def __init__(self, user_cls: type, output_mgr: typing.Union[modal._output.OutputManager, None], base_functions: typing.Dict[str, modal.functions._Function], args, kwargs):
        ...

    def get_obj(self):
        ...

    def get_local_obj(self):
        ...

    def enter(self):
        ...

    @property
    def entered(self):
        ...

    async def aenter(self):
        ...

    def __getattr__(self, k):
        ...


class Obj:
    _functions: typing.Dict[str, modal.functions.Function]
    _inited: bool
    _entered: bool
    _local_obj: typing.Any
    _local_obj_constr: typing.Union[typing.Callable[[], typing.Any], None]

    def __init__(self, user_cls: type, output_mgr: typing.Union[modal._output.OutputManager, None], base_functions: typing.Dict[str, modal.functions.Function], args, kwargs):
        ...

    def get_obj(self):
        ...

    def get_local_obj(self):
        ...

    def enter(self):
        ...

    @property
    def entered(self):
        ...

    async def aenter(self):
        ...

    def __getattr__(self, k):
        ...


class _Cls(modal.object._Object):
    _user_cls: typing.Union[type, None]
    _functions: typing.Dict[str, modal.functions._Function]

    def _initialize_from_empty(self):
        ...

    def _set_output_mgr(self, output_mgr: modal._output.OutputManager):
        ...

    def _hydrate_metadata(self, metadata: google.protobuf.message.Message):
        ...

    def _get_metadata(self) -> modal_proto.api_pb2.ClassHandleMetadata:
        ...

    @staticmethod
    def from_local(user_cls, base_functions: typing.Dict[str, modal.functions._Function]) -> _Cls:
        ...

    def get_user_cls(self):
        ...

    def get_base_function(self, k: str) -> modal.functions._Function:
        ...

    def __call__(self, *args, **kwargs) -> _Obj:
        ...

    async def remote(self, *args, **kwargs):
        ...

    def __getattr__(self, k):
        ...


class Cls(modal.object.Object):
    _user_cls: typing.Union[type, None]
    _functions: typing.Dict[str, modal.functions.Function]

    def __init__(self, *args, **kwargs):
        ...

    def _initialize_from_empty(self):
        ...

    def _set_output_mgr(self, output_mgr: modal._output.OutputManager):
        ...

    def _hydrate_metadata(self, metadata: google.protobuf.message.Message):
        ...

    def _get_metadata(self) -> modal_proto.api_pb2.ClassHandleMetadata:
        ...

    @staticmethod
    def from_local(user_cls, base_functions: typing.Dict[str, modal.functions.Function]) -> Cls:
        ...

    def get_user_cls(self):
        ...

    def get_base_function(self, k: str) -> modal.functions.Function:
        ...

    def __call__(self, *args, **kwargs) -> Obj:
        ...

    class __remote_spec(typing_extensions.Protocol):
        def __call__(self, *args, **kwargs):
            ...

        async def aio(self, *args, **kwargs):
            ...

    remote: __remote_spec

    def __getattr__(self, k):
        ...
