from abc import ABC
from collections.abc import Mapping, Sequence
from typing import Generic, Optional, Union

from atoti_core import EMPTY_MAPPING

from ..directquery import MultiColumnArrayConversion, MultiRowArrayConversion
from ._external_table import ExternalTableT_co


class ExternalTableOptions(Generic[ExternalTableT_co], ABC):
    def __init__(
        self,
        *,
        array_conversion: Optional[
            Union[MultiColumnArrayConversion, MultiRowArrayConversion]
        ] = None,
        keys: Optional[Sequence[str]] = None,
        options: Mapping[str, object] = EMPTY_MAPPING,
    ) -> None:
        super().__init__()

        self._array_conversion = array_conversion
        self._keys = keys
        self._options = options
