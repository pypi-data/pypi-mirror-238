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

__all__ = ["NoveltyArchive"]

########### IMPORTS ########### {{{1
from typing import Optional, Tuple, List, Iterable, Iterator, Any, TypeVar, Generic, Union, Sequence, MutableSet, MutableSequence, Type, Callable, Generator, MutableMapping, Mapping, overload

from qdpy.utils import *
from qdpy.phenotype import *
from qdpy.base import *
from qdpy.metrics import novelty, novelty_local_competition, novelty_nn
from .base import *




########### ARCHIVE-BASED CLASSES ########### {{{1

@registry.register
class NoveltyArchive(Container):
    """TODO""" # TODO

    #depot: BackendLike[IndividualLike]

    k: int
    threshold_novelty: float
    novelty_distance: Union[str, Callable]

    def __init__(self, iterable: Optional[Iterable] = None,
            k: int = 15, threshold_novelty: float = 0.01, novelty_distance: Union[str, Callable] = "euclidean",
            parents: Sequence[ContainerLike] = [], **kwargs: Any) -> None:
        self.k = k
        self.threshold_novelty = threshold_novelty
        self.novelty_distance = novelty_distance
        if len(parents) == 0:
            raise ValueError("``parents`` must contain at least one parent container to create an archive container.")
        super().__init__(iterable, parents=parents, **kwargs)


    def _add_internal(self, individual: IndividualLike, raise_if_not_added_to_parents: bool, only_to_parents: bool) -> Optional[int]:
        # Find novelty of this individual, and its nearest neighbour
        all_parents = self.all_parents_inds()
        novelty, nn = novelty_nn(individual, all_parents, k=self.k, nn_size=1, dist=self.novelty_distance, ignore_first=False)
        if novelty > self.threshold_novelty:
            # Add individual
            return super()._add_internal(individual, raise_if_not_added_to_parents, only_to_parents)
        else:
            ind_nn = all_parents[nn[0]]
            ind_nn_fit = self.get_ind_fitness(ind_nn)
            ind_fit = self.get_ind_fitness(individual)
            if len(nn) > 0 and ind_fit.dominates(ind_nn_fit):
                #self.discard(nn[0])
                #self._discard_by_index(ind_nn, idx_depot=nn[0])
                self._discard_by_index(ind_nn)
                return super()._add_internal(individual, raise_if_not_added_to_parents, only_to_parents)
            else:
                #return None
                return super()._add_internal(individual, raise_if_not_added_to_parents, True)



## MODELINE	"{{{1
## vim:expandtab:softtabstop=4:shiftwidth=4:fileencoding=utf-8
## vim:foldmethod=marker
