#    This file is part of qdpy.
#
#    qdpy is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of
#    the License, or (at your option) any later version.
#
#    qdpy is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with qdpy. If not, see <http://www.gnu.org/licenses/>.

"""TODO"""

__all__ = ["Population"]

########### IMPORTS ########### {{{1
import numpy as np
from typing import Optional, Tuple, List, Iterable, Iterator, Any, TypeVar, Generic, Union, Sequence, MutableSet, MutableSequence, Type, Callable, Generator, MutableMapping, Mapping, overload

from qdpy.utils import *
from qdpy.phenotype import *
from qdpy.base import *
from qdpy.metrics import novelty, novelty_local_competition, novelty_nn
from .base import *


@registry.register
class Population(Container):
    """Container that simulates the behaviour of a population. The capacity is fixed. When an individual is added to a completely filled Population, the oldest individual is discarded.""" # TODO

    def __init__(self, iterable: Optional[Iterable] = None,
            capacity: Optional[float] = None,
            **kwargs: Any) -> None:
        assert(capacity is not None and not np.isinf(capacity))
        super().__init__(iterable, capacity=capacity, **kwargs)

    def _add_internal(self, individual: IndividualLike, raise_if_not_added_to_parents: bool, only_to_parents: bool) -> Optional[int]:
        # Check if there is enough space
        if self.free < 1:
            # Remove the oldest individual (index = 0)
            self.discard(self[0])
        # Add
        return super()._add_internal(individual, raise_if_not_added_to_parents, only_to_parents)




## MODELINE	"{{{1
## vim:expandtab:softtabstop=4:shiftwidth=4:fileencoding=utf-8
## vim:foldmethod=marker
