# Copyright Open Logistics Foundation
#
# Licensed under the Open Logistics Foundation License 1.3.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: OLFL-1.3

from collections import OrderedDict
from typing import Any, Generic, Optional, TypeVar

KT = TypeVar("KT")
VT = TypeVar("VT")


# Type for OrderedDict can not be provided since this would break python3.8 compatibility.
# Therefore, add a workaround for being a generic class.
class SizedDict(OrderedDict, Generic[KT, VT]):  # type: ignore[type-arg]
    """
    OrderedDict with a limited size
    """

    def __init__(self, max_size: Optional[int] = None) -> None:
        self.max_size: Optional[int] = max_size
        super(OrderedDict, self).__init__()

    def __setitem__(self, key: KT, item: VT, *args: Any, **kwargs: Any) -> None:
        OrderedDict.__setitem__(self, key, item)  # type: ignore[assignment]
        if self.max_size is not None and len(self) > self.max_size:
            self.popitem(last=False)
