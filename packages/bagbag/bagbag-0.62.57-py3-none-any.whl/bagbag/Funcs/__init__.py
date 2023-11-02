from typing import TYPE_CHECKING
from lazy_imports import LazyImporter
import sys

_import_structure = {
    "Wget_src": ["Wget"],
    "IPAddressConvert_src": ["Int2IP", "IP2Int"],
    "ResizeImage_src": ["ResizeImage", "ConvertImageFormate"],
    "GetPublicIP_src": ["GetPublicIP"],
    "Ping_src": ["Ping"],
    # "CutSentence_src": ["CutSentence"],
    "UUID_src": ["UUID", "UUID_Full"],
    # "Markdown_src": ["Markdown2Html", "Html2Markdown"],
    "FakeIdentity_src": ["FakeIdentity"],
}

if TYPE_CHECKING:
    from .Wget_src import Wget
    from .IPAddressConvert_src import Int2IP, IP2Int
    from .ResizeImage_src import ResizeImage, ConvertImageFormate
    from .GetPublicIP_src import GetPublicIP
    from .Ping_src import Ping
    # from .CutSentence_src import CutSentence
    from .UUID_src import UUID, UUID_Full
    # from .Markdown_src import Markdown2Html, Html2Markdown
    # from .FileType import FileType
    from .FakeIdentity_src import FakeIdentity
else:
    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        _import_structure,
        extra_objects={},
    )

from . import Format


