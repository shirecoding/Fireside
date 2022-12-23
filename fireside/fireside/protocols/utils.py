__all__ = ["as_deserialized_pdict", "as_serialized_pdict"]

from typing import TYPE_CHECKING

from fireside.utils import import_path_to_function

if TYPE_CHECKING:
    from .defs import ProtocolDict


def as_deserialized_pdict(pdict: "ProtocolDict"):
    """
    Ensures pdict values are `Protocol`s
    """
    from fireside.protocols import Protocol

    return {
        pkey: import_path_to_function(pd.klass)(**pd.dict())
        if isinstance(pd, Protocol)
        else import_path_to_function(pd["klass"])(**pd)
        for pkey, pd in pdict.items()
    }


def as_serialized_pdict(pdict: "ProtocolDict"):
    """
    Ensures pdict values are python dictionaries
    """
    from fireside.protocols import Protocol

    return {
        pkey: pd.dict() if isinstance(pd, Protocol) else pd
        for pkey, pd in pdict.items()
    }
