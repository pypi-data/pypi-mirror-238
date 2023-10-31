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
#from __future__ import annotations

__all__ = ["BackendLike", "SimpleOrderedSet", "ContainerLike", "Container", "ContainerDecorator"]

########### IMPORTS ########### {{{1
import sys
import warnings
import math
import numpy as np
from typing import Optional, Tuple, List, Iterable, Iterator, Any, TypeVar, Generic, Union, Sequence, MutableSet, MutableSequence, Type, Callable, Generator, MutableMapping, Mapping, overload
from typing_extensions import runtime, Protocol
import traceback
import deprecation
import functools
import sortedcollections

from qdpy.utils import *
from qdpy.phenotype import *
from qdpy.base import *
from qdpy.metrics import novelty, novelty_local_competition, novelty_nn



########### BACKEND CLASSES ########### {{{1


@registry.register
class SimpleOrderedSet(MutableSet[T], Sequence[T]):
    """A MutableSet variant that conserves entries order, and can be accessed like a Sequence.
    This implementation is not optimised, but does not requires the type ``T`` of items to be hashable.
    It also does not implement indexing by slices.

    Parameters
    ----------
    iterable: Optional[Iterable[T]]
        items to add to the SimpleOrderedSet
    """

    _items: List[T]    # Internal storage

    def __init__(self, iterable: Optional[Iterable] = None) -> None:
        self._items = []
        if iterable is not None:
            self.update(iterable)

    def __len__(self) -> int:
        return len(self._items)

    @overload
    def __getitem__(self, index: int) -> T: ...

    @overload
    def __getitem__(self, s: slice) -> Sequence[T]: ...

    def __getitem__(self, key):
        if isinstance(key, slice):
            raise NotImplementedError
        return self._items[key]

    def __contains__(self, key: Any) -> bool:
        return key in self._items

    def __iter__(self) -> Iterator[T]:
        return iter(self._items)

    def __reversed__(self) -> Iterator[T]:
        return reversed(self._items)

    def __repr__(self) -> str:
        if not self:
            return "%s()" % (self.__class__.__name__,)
        return "%s(%r)" % (self.__class__.__name__, list(self))

    def __delitem__(self, idx) -> None:
        del self._items[idx]

    def count(self, key: T) -> int:
        return 1 if key in self else 0

    def index(self, key: T, start: int = 0, stop: int = sys.maxsize) -> int:
        return self._items.index(key, start, stop)

    def add(self, key: T) -> None:
        """Add ``key`` to this SimpleOrderedSet, if it is not already present. """
        try:
            self._items.index(key)
        except ValueError:
            self._items.append(key)

    def discard(self, key: T) -> None:
        """Discard ``key`` in this SimpleOrderedSet. Does not raise an exception if absent."""
        try:
            self._items.remove(key)
        except ValueError:
            return

    def update(self, iterable: Iterable) -> None:
        """Add the items in ``iterable``, if they are not already present in the SimpleOrderedSet.  """
        try:
            for item in iterable:
                self.add(item)
        except TypeError:
            raise ValueError(f"Argument needs to be an iterable, got {type(iterable)}")



BackendLike = Union[MutableSequence[T], SimpleOrderedSet[T]]



########### CONTAINER CLASSES ########### {{{1

@runtime
class ContainerLike(Protocol):
    def all_parents_inds(self) -> Sequence[IndividualLike]: ...

    def add(self, individual: IndividualLike, raise_if_not_added_to_parents: bool = False) -> Optional[int]: ...
    def discard(self, individual: IndividualLike, also_from_parents: bool = False) -> None: ...
    def update(self, iterable: Iterable, ignore_exceptions: bool = True, issue_warning: bool = False) -> int: ...
    def clear(self, also_from_parents: bool = False) -> None: ...
    def novelty(self, individual: IndividualLike, **kwargs): ...
    def novelty_local_competition(self, individual: IndividualLike, **kwargs): ...
    def qd_score(self, normalized: bool = True) -> float: ...
    def to_grid(self, shape: Union[ShapeLike, int], max_items_per_bin: int = 1, capacity: Optional[float] = None, **kwargs: Any) -> Any: ...
    def __len__(self) -> int: ...
    def __iter__(self) -> Iterator: ...
    def get_ind_features(self, individual: IndividualLike, *args, **kwargs) -> FeaturesLike: ...
    def get_ind_fitness(self, individual: IndividualLike, *args, **kwargs) -> FitnessLike: ...
    def set_ind_fitness(self, individual: IndividualLike, fitness: FitnessLike, *args, **kwargs): ...
    @property
    def capacity(self) -> float: ...
    @property
    def free(self) -> float: ...
    @property
    def size(self) -> int: ...
    @property
    def best(self) -> Any: ...
    @property
    def best_fitness(self) -> Optional[FitnessLike]: ...
    @property
    def best_features(self) -> Optional[FeaturesLike]: ...
    @property
    def nb_discarded(self) -> int: ...
    @property
    def nb_added(self) -> int: ...
    @property
    def nb_rejected(self) -> int: ...
    @property
    def nb_operations(self) -> int: ...
    @property
    def fitness_extrema(self) -> Optional[Sequence[DomainLike]]: ...
    @property
    def features_extrema(self) -> Optional[Sequence[DomainLike]]: ...
    fitness_domain: Optional[Sequence[DomainLike]]
    features_domain: Optional[Sequence[DomainLike]]
    fitness_score_names: Sequence[str]
    features_score_names: Sequence[str]


# TODO verify that containers are thread-safe
@registry.register
class Container(ContainerLike, Sequence, Summarisable, Copyable, CreatableFromConfig):
    """TODO

    Parameters
    ----------
    iterable: Iterable[IndividualLike] or None
        TODO
    storage_type: Backend (MutableSet or MutableSequence)
        TODO
    parents: Sequence[Container]
        TODO
    fitness_domain: Sequence[DomainLike] (sequence of 2-tuple of numbers)
        TODO
    features_domain: Sequence[DomainLike] (sequence of 2-tuple of numbers)
        TODO
    """ # TODO

    name: Optional[str]
    items: BackendLike[IndividualLike]
    #depot: Optional[BackendLike[IndividualLike]]
    parents: Sequence[ContainerLike]
    fitness_domain: Optional[Sequence[DomainLike]]
    features_domain: Optional[Sequence[DomainLike]]
    fitness_score_names: Sequence[str]
    features_score_names: Sequence[str]
    recentness: MutableSequence[int]
    fitness_weights: Optional[FitnessValuesLike]
    _capacity: float
    _size: int
    _best: Optional[IndividualLike]
    _best_fitness: Optional[FitnessLike]
    _best_features: Optional[FeaturesLike]
    _nb_discarded: int
    _nb_added: int
    _nb_rejected: int

    def __init__(self, iterable: Optional[Iterable] = None,
            storage_type: Union[str,BackendLike,Type[BackendLike]] = list, parents: Sequence[ContainerLike] = [],
            fitness_domain: Optional[Sequence[DomainLike]] = None,
            features_domain: Optional[Sequence[DomainLike]] = None,
            fitness_score_names: Sequence[str] = [], features_score_names: Sequence[str] = [],
            fitness_weights: Optional[FitnessValuesLike] = None,
            capacity: Optional[float] = None, name: Optional[str] = None,
            only_add_accepted_inds_to_parents: bool = False,
            disable_parents_pickling: bool = True,
            **kwargs: Any) -> None:
        self.items = self._create_storage(storage_type)
        self.parents = parents
        self.only_add_accepted_inds_to_parents = only_add_accepted_inds_to_parents
        self.disable_parents_pickling = disable_parents_pickling
        self.fitness_domain = fitness_domain
        if self.fitness_domain is not None:
            for f in self.fitness_domain:
                if not is_iterable(f) or len(f) != 2:
                    raise ValueError("``fitness_domain`` must be a sequence of 2-tuples.")
        self.features_domain = features_domain
        if self.features_domain is not None:
            for f in self.features_domain:
                if not is_iterable(f) or len(f) != 2:
                    raise ValueError("``features_domain`` must be a sequence of 2-tuples.")
        self.fitness_score_names = fitness_score_names
        self.features_score_names = features_score_names
        self.fitness_weights = fitness_weights
        self.recentness = []
        self.name = name if name is not None else f"{self.__class__.__name__}-{id(self)}"
        self._capacity = math.inf if capacity is None else capacity
        self._size = 0
        self._best = None
        self._best_fitness = None
        self._best_features = None
        self._nb_discarded = 0
        self._nb_rejected = 0
        self._nb_added = 0
        if iterable is not None:
            self.update(iterable)

    def _create_storage(self, storage_type: Union[str,BackendLike,Type[BackendLike]] = list):
        if isinstance(storage_type, str):
            t = storage_type.lower()
            if t == "list":
                return list()
            elif t == "simpleorderedset":
                return SimpleOrderedSet()
            elif t == "orderedset":
                return sortedcollections.OrderedSet()
            elif t == "indexableset":
                return sortedcollections.IndexableSet()
            else:
                raise ValueError(f"Unknown class name specified for ``storage_type`` ({storage_type}). Known names include 'list', 'simpleorderedset', 'orderedset,' and 'indexableset'.")
        elif isinstance(storage_type, Type): # type: ignore
            return storage_type() # type: ignore
        else:
        #elif isinstance(storage_type, BackendLike):
            return storage_type
        #else:
            #raise ValueError("``storage_type`` must be either a BackendLike object or the class of a BackendLike or a string containing the name of the BackendLike class.")

    def __getstate__(self):
        odict = self.__dict__.copy()
        if odict['disable_parents_pickling'] and 'parents' in odict:
            del odict['parents']
        return odict

    @property
    def capacity(self) -> float:
        """Return the capacity of the container (i.e. maximal number of items/spots/bins/etc). Can be math.inf."""
        return self._capacity

    @property
    def free(self) -> float:
        """Return the number of free spots in the container. Can be math.inf."""
        return self._capacity - self._size

    @property
    def size(self) -> int:
        """Return the size of the container (i.e. number of items, spots, bins, etc)."""
        return self._size

    @property
    def best(self) -> Any:
        """Return the best individual. """
        return self._best

    @property
    def best_fitness(self) -> Optional[FitnessLike]:
        """Return the fitness values of the individual with the best quality, or None. """
        return self._best_fitness

    @property
    def best_features(self) -> Optional[FeaturesLike]:
        """Return the features values of the individual with the best quality, or None. """
        return self._best_features

    @property
    def nb_discarded(self) -> int:
        """Return the number of individuals discarded by the container since its creation. """
        return self._nb_discarded

    @property
    def nb_added(self) -> int:
        """Return the number of individuals added into the container since its creation. """
        return self._nb_added

    @property
    def nb_rejected(self) -> int:
        """Return the number of individuals rejected (when added) by the container since its creation. """
        return self._nb_rejected

    @property
    def nb_operations(self) -> int:
        """Return the number of adds, modifications and discards since the creation of this container. """
        return self._nb_added + self._nb_discarded


    @property
    def fitness_extrema(self) -> Optional[Sequence[DomainLike]]:
        """Return the extrema values of the fitnesses of the stored individuals."""
        if len(self) == 0:
            return None
        #maxima = np.array(self[0].fitness.values) # type: ignore
        #minima = np.array(self[0].fitness.values) # type: ignore
        maxima = minima = np.array(self.get_ind_fitness(self[0]).values) # type: ignore
        for ind in self:
            ind_f = np.array(self.get_ind_fitness(ind).values)
            for i in range(len(maxima)):
                if ind_f[i] > maxima[i]:
                    maxima[i] = ind_f[i]
                elif ind_f[i] < minima[i]:
                    minima[i] = ind_f[i]
        return tuple(zip(minima, maxima))


    @property
    def features_extrema(self) -> Optional[Sequence[DomainLike]]:
        """Return the extrema values of the features of the stored individuals."""
        if len(self) == 0:
            return None
        #maxima = np.array(self[0].features) # type: ignore
        #minima = np.array(self[0].features) # type: ignore
        maxima = np.array(self.get_ind_features(self[0])) # type: ignore
        minima = np.array(self.get_ind_features(self[0])) # type: ignore
        for ind in self:
            ind_f = self.get_ind_features(ind)
            for i in range(len(maxima)):
                if ind_f[i] > maxima[i]:
                    maxima[i] = ind_f[i]
                elif ind_f[i] < minima[i]:
                    minima[i] = ind_f[i]
        return tuple(zip(minima, maxima))


    def all_parents_inds(self) -> Sequence[IndividualLike]:
        return flatten_seq_of_seq(self.parents) # type: ignore


    def size_str(self) -> str:
        """Return a string describing the fullness of the container."""
        if math.isinf(self.capacity):
            return str(self.size)
        else:
            return "%i/%i" % (self.size, self.capacity)

    def __len__(self) -> int:
        return len(self.items)

    @overload
    def __getitem__(self, index: int) -> T: ...

    @overload
    def __getitem__(self, s: slice) -> Sequence[IndividualLike]: ...

    def __getitem__(self, key):
        if isinstance(key, slice):
            raise NotImplementedError
        return self.items[key]

    def __contains__(self, key: Any) -> bool:
        return key in self.items

    def __iter__(self) -> Iterator[IndividualLike]:
        return iter(self.items)

#    def __reversed__(self) -> Iterator[IndividualLike]:
#        return reversed(self.items)

    def __repr__(self) -> str:
        if not self:
            return "%s()" % (self.__class__.__name__,)
        return "%s(%r)" % (self.__class__.__name__, list(self))


    def _add_to_collection(self, collection: BackendLike[IndividualLike], individual: IndividualLike) -> Tuple[bool,int]:
        """Add ``individual`` to ``collection``.
        Return a tuple containing (added, index), with ``added`` a bool saying whether ``individual`` was added or not to ``collection``, and ``index`` the index in the ``collection``.
        ``collection`` can be a MutableSequence or an ordered set implementing Sequence and MutableSet."""
        old_len: int = len(collection)
        if isinstance(collection, MutableSet):
            collection.add(individual)
            if len(collection) == old_len:
                return False, collection.index(individual)
            else:
                return True, len(collection) - 1
        elif isinstance(collection, MutableSequence):
            added: bool = False
            try:
                index: int = collection.index(individual)
            except ValueError:
                collection.append(individual)
                index = len(collection) - 1
                added = True
            return added, index
        else:
            raise ValueError("collection must be an ordered set implementing MutableSet or a Sequence")


    def in_bounds(self, val: Any, domain: Any) -> bool:
        """TODO"""
        if domain is None or len(domain) == 0:
            return True
        return in_bounds(val, domain)

    def get_ind_features(self, individual: IndividualLike, *args, **kwargs) -> FeaturesLike:
        if len(self.features_score_names) == 0:
            return individual.features
        else:
            return individual.scores.to_features(self.features_score_names, *args, **kwargs)

    def get_ind_fitness(self, individual: IndividualLike, *args, **kwargs) -> FitnessLike:
        if len(self.fitness_score_names) == 0:
            if self.fitness_weights:
                individual.fitness.weights = self.fitness_weights
            return individual.fitness
        else:
            return individual.scores.to_fitness(self.fitness_score_names, *args, weights=self.fitness_weights, **kwargs)

    def set_ind_fitness(self, individual: IndividualLike, fitness: FitnessLike, *args, **kwargs):
        if len(self.fitness_score_names) == 0:
            individual.fitness = fitness
            if self.fitness_weights:
                individual.fitness.weights = self.fitness_weights
        else:
            for name,val in zip(self.fitness_score_names,fitness.values):
                individual.scores[name] = val

    def _check_if_can_be_added(self, individual: IndividualLike) -> None:
        """TODO"""
        # Retrieve features and fitness from individual
        #ind_fitness: FitnessValuesLike = self._get_fitness_from_ind(individual)
        #ind_features: FeaturesLike = self._get_features_from_ind(individual)
        exc = None
        fit = self.get_ind_fitness(individual)
        if not fit.valid:
            exc = ValueError(f"Fitness is not valid.")
        # Check if fitness and features are out of bounds
        if not self.in_bounds(fit.values, self.fitness_domain):
            exc = ValueError(f"fitness ({str(fit)}) out of bounds ({str(self.fitness_domain)}).")
        ft = self.get_ind_features(individual)
        if not self.in_bounds(ft, self.features_domain):
            #exc = ValueError(f"features ({str(ft)}) out of bounds ({str(self.features_domain)}).")
            exc = ValueError(f"features ({str(ft)}) out of bounds ({str(self.features_domain)}). fitness={fit}. scores={individual.scores}") # XXX
        if exc:
            self._nb_rejected += 1
            raise exc


    #def _add_internal(self, individual: T, raise_if_not_added_to_depot: bool, only_to_depot: bool, ind_fitness: FitnessLike, ind_features: FeaturesLike) -> Optional[int]:
    def _add_internal(self, individual: IndividualLike, raise_if_not_added_to_parents: bool, only_to_parents: bool) -> Optional[int]:
        """TODO"""
        # Verify if we do not exceed capacity
        if not only_to_parents and self.free < 1:
            self._nb_rejected += 1
            raise IndexError(f"No free slot available in this container.")
#        if raise_if_not_added_to_parents and len(self.parents) == 0:
#            self._nb_rejected += 1
#            raise ValueError(f"`raise_if_not_added_to_parents` can only be set to True if at least one parent is specified.")
        if only_to_parents and len(self.parents) == 0:
            self._nb_rejected += 1
            raise ValueError(f"`only_to_parents` can only be set to True if at least one parent is specified.")

        # Add to storage
        added = False
        exc_add: Optional[Exception] = None
        index = None
        if not only_to_parents:
            try:
                added, index = self._add_to_collection(self.items, individual)
                # Update best_fitness
                if added:
                    #if self._best is None or self._dominates(individual, self._best):
                    ind_fit = self.get_ind_fitness(individual)
                    if self._best is None or ind_fit.dominates(self._best_fitness):
                        self._best = individual
                        self._best_fitness = ind_fit
                        self._best_features = self.get_ind_features(individual)
                    self.recentness.append(self._nb_added)
                    self._size += 1
                    self._nb_added += 1
            except Exception as e:
                added = False
                exc_add = e

        # Add to parents, if needed
        added_parents = True
        exc_add_parents = None
        if not self.only_add_accepted_inds_to_parents or added:
            for p in self.parents:
                try:
                    p.add(individual, raise_if_not_added_to_parents=raise_if_not_added_to_parents)
                except Exception as e:
                    added_parents = False
                    exc_add_parents = e
                    break
            if raise_if_not_added_to_parents and not added_parents:
                self._nb_rejected += 1
                for p in self.parents:
                    try:
                        p.discard(individual, also_from_parents = True)
                    except Exception as e:
                        pass
                raise ValueError(f"Individual could not be added to the parents: {exc_add_parents}")

        # Raise if add raised an exception
        if exc_add != None:
            raise exc_add # type: ignore
        else:
            return index

#        # Add to parents, if needed
#        added_parents = True
#        exc_add_parents = None
#        for p in self.parents:
#            try:
#                p.add(individual, raise_if_not_added_to_parents=raise_if_not_added_to_parents)
#            except Exception as e:
#                added_parents = False
#                exc_add_parents = e
#                break
#        if raise_if_not_added_to_parents and not added_parents:
#            self._nb_rejected += 1
#            for p in self.parents:
#                try:
#                    p.discard(individual, also_from_parents = True)
#                except Exception as e:
#                    pass
#            raise ValueError(f"Individual could not be added to the parents: {exc_add_parents}")
#        if only_to_parents:
#            return None
#        else:
#            # Add to storage
#            added, index = self._add_to_collection(self.items, individual)
#            # Update best_fitness
#            if added:
#                #if self._best is None or self._dominates(individual, self._best):
#                ind_fit = self.get_ind_fitness(individual)
#                if self._best is None or ind_fit.dominates(self._best_fitness):
#                    self._best = individual
#                    self._best_fitness = ind_fit
#                    self._best_features = self.get_ind_features(individual)
#                self.recentness.append(self._nb_added)
#                self._size += 1
#                self._nb_added += 1
#            return index


    def add(self, individual: IndividualLike, raise_if_not_added_to_parents: bool = False) -> Optional[int]:
        """Add ``individual`` to the container, and returns its index, if successful, None elsewise. If ``raise_if_not_added_to_parents`` is True, it will raise and exception if it was not possible to add it also to the parents."""
        # Retrieve features and fitness from individual and check if they are not out-of-bounds
        self._check_if_can_be_added(individual)
        # Add
        return self._add_internal(individual, raise_if_not_added_to_parents, False)


    def _discard_by_index(self, individual: IndividualLike, idx: Optional[int] = None, also_from_parents: bool = False) -> None:
        """Remove ``individual`` of the container. If ``also_from_parents`` is True, discard it also from the parents, if they exist. Use the indexes ``idx`` if it is provided."""
        # Remove from parents
        if also_from_parents:
            try:
                for p in self.parents:
                    p.discard(individual, also_from_parents = True)
            except Exception as e:
                pass
        # Remove from container
        if idx is None:
            try:
                idx = self.items.index(individual)
            except KeyError:
                return
        del self.items[idx]
        del self.recentness[idx]
        self._size -= 1
        self._nb_discarded += 1
        if self._size < 0:
            raise RuntimeError("`self.size` < 0 !")


    def discard(self, individual: IndividualLike, also_from_parents: bool = False) -> None:
        """Remove ``individual`` of the container. If ``also_from_parents`` is True, discard it also from the parents, if they exist."""
        idx = None
        # Remove from container
        try:
            idx = self.items.index(individual)
        except KeyError:
            pass
        self._discard_by_index(individual, idx, also_from_parents)


    def update(self, iterable: Iterable, ignore_exceptions: bool = True, issue_warning: bool = False) -> int:
        """Add the individuals in ``iterable``, if they are not already present in the container.
        If ``ignore_exceptions`` is True, it will ignore exceptions raised when adding each individual, but issue warnings instead.
        Returns the number of elements inserted or updated."""
        nb_inserted: int = 0
        item_index: Optional[int] = None
        only_to_parents = False
        try:
            for item in iterable:
                try:
                    self._check_if_can_be_added(item)
                except Exception as e:
                    only_to_parents = True
                    if ignore_exceptions and issue_warning:
                        if isinstance(e,IndexError):
                            warnings.warn(f"Adding individual failed (index out of bounds): {str(e)}")
                        elif isinstance(e,ValueError):
                            warnings.warn(f"Adding individual failed (attribute out of bounds): {str(e)}")
                        else:
                            warnings.warn(f"Adding individual failed: {str(e)}")
                            traceback.print_exc()
                    elif not ignore_exceptions:
                        raise e
                if not only_to_parents or len(self.parents) > 0:
                    item_index = self._add_internal(item, True, only_to_parents)
                    if item_index is not None:
                        nb_inserted += 1

        except TypeError:
            raise ValueError(f"Argument needs to be an Iterable, got {type(Iterable)}")
        return nb_inserted


    def clear(self, also_from_parents: bool = False) -> None:
        """Clear all individual in the collection. If ``also_from_parents`` is the to True, also remove those individuals in the parent containers."""
        # Remove all individuals
        items = list(self) # Save individuals (cannot iterate a list while its items are deleted)
        for e in items:
            self.discard(e, also_from_parents)
        #for e in items:
        #    try:
        #        self.discard(e, also_from_parents)
        #    except Exception as ex:
        #        print("ERROR WHILE DISCARDING", e)
        #        traceback.print_exc()
        #        #raise ex

        # Clear recentness and best
        self.recentness = []
        self._best = None
        self._best_fitness = None
        self._best_features = None


    @deprecation.deprecated(deprecated_in="0.1.3", removed_in="0.2.0",
                        current_version=qdpy.__version__,
                        details="Use 'self.clear(also_from_parents=True)' instead.")
    def clear_all(self) -> None:
        """Clear all individual in the collection, and clear also those individuals in the parent containers."""
        self.clear(also_from_parents = True)


    def novelty(self, individual: IndividualLike, **kwargs):
        """Returns the novelty score of `individual`, using the parents as archive. TODO""" # TODO
        if len(self.parents) == 0:
            raise RuntimeError(f"At least one parent is necessary to assess novelty.")
        return novelty(individual, self.all_parents_inds(), **kwargs)

    def novelty_local_competition(self, individual: IndividualLike, **kwargs):
        """Returns the novelty and local competition scores of `individual`, using the parents as archive. TODO""" # TODO
        if len(self.parents) == 0:
            raise RuntimeError(f"At least one parent is necessary to assess novelty.")
        return novelty_local_competition(individual, self.all_parents_inds(), **kwargs)


    def to_grid(self, shape: Union[ShapeLike, int],
            max_items_per_bin: int = 1,
            capacity: Optional[float] = None, **kwargs: Any) -> Any:
        """Return a grid representation of this container, with `shape` the shape of the grid.

        Parameters
        ----------
        :param shape: Union[ShapeLike, int]
            The shape of the grid.
        :param max_items_per_bin: int
            The maximal number of entries stored in each bin of the grid. Defaults to 1.
        :param fitness_domain: Optional[Sequence[DomainLike]]
            The domain of the fitness of the individual of this grid. Default to `self.fitness_extrema`.
        :param features_domain: Optional[Sequence[DomainLike]]
            The domain of the features of the individual of this grid. Default to `self.features_extrema`.
        :param capacity: Optional[float] = None
            The capacity (i.e. maximal number of entries) of the returned grid representation. Default to None (i.e. no limit).
        :param storage_type: Type[BackendLike]
            How individuals are stored internally. Defaults to list.

        Return
        ------
        grid: Grid
            Grid representation of this container.
        """
        if not 'fitness_domain' in kwargs:
            kwargs['fitness_domain'] = self.fitness_domain if self.fitness_domain is not None else self.fitness_extrema
        if not 'features_domain' in kwargs:
            kwargs['features_domain'] = self.features_domain if self.features_domain is not None else self.features_extrema
        if not 'fitness_score_names' in kwargs:
            kwargs['fitness_score_names'] = self.fitness_score_names
        if not 'features_score_names' in kwargs:
            kwargs['features_score_names'] = self.features_score_names
        if not 'fitness_weights' in kwargs:
            kwargs['fitness_weights'] = self.fitness_weights
        return qdpy.containers.Grid(self, shape=shape, max_items_per_bin=max_items_per_bin, capacity=capacity, **kwargs) # type: ignore


    def qd_score(self, normalized: bool = True) -> float:
        """Return the QD score of this container. It corresponds to the sum of the fitness values of all individuals in the container.

        Parameters
        ----------
        :param normalized: bool = True
            Normalize fitness values. If False, the returned QD score is computed by just summing all fitness values.
            If True, all fitness values are normalized depending on the domain of the fitness values, and on their weight (i.e., minimization vs maximization). Each fitness value is normalized as follow:
                if weight < 0.:
                    normalized_fitness_value = (bounds[1] - fitness_value) / (bounds[1] - bounds[0])
                else:
                    normalized_fitness_value = (fitness_value - bounds[0]) / (bounds[1] - bounds[0])
            Then, the returned QD is computed by summing all normalized fitness values.

        Return
        ------
        qd_score: float
            QD score of this container.
        """
        score: float = 0.
        if normalized:
            if self.fitness_domain is None:
                raise RuntimeError(f"'fitness_domain' must be set to compute normalized QD scores.")
            else:
                for ind in self:
                    ind_fit = self.get_ind_fitness(ind)
                    for v, w, bounds in zip(ind_fit.values, ind_fit.weights, self.fitness_domain):
                        d = (bounds[1] - bounds[0]) if bounds[1] > bounds[0] else 1
                        if w < 0.:
                            score += (bounds[1] - v) / (d)
                        else:
                            score += (v - bounds[0]) / (d)
        else:
            for ind in self:
                ind_fit = self.get_ind_fitness(ind)
                score += np.sum(ind_fit.values)
        return score



########### DECORATOR CLASSES ########### {{{2


@registry.register
class ContainerDecorator(ContainerLike, Sequence, Summarisable, Copyable, CreatableFromConfig):
    """TODO""" # TODO

    container: ContainerLike
    name: Optional[str]

    def __init__(self, container: ContainerLike,
            name: Optional[str] = None,
            **kwargs: Any) -> None:
        self.container = container
        self.name = name if name is not None else f"{self.__class__.__name__}-{id(self)}"

    def __getstate__(self):
        odict = self.__dict__.copy()
        return odict

    def __setstate__(self, state):
        self.__dict__.update(state)

    def __setattr__(self, attr, value):
        if attr in self.__dict__:
            self.__dict__[attr] = value
        elif "container" in self.__dict__:
            setattr(self.container, attr, value)
        else:
            self.__dict__[attr] = value

    def __getattr__(self, attr):
        if attr in self.__dict__:
            return getattr(self, attr)
        if "container" not in self.__dict__:
            raise AttributeError
        return getattr(self.container, attr)


    def __len__(self) -> int:
        return self.container.__len__()

    @overload
    def __getitem__(self, index: int) -> T: ...

    @overload
    def __getitem__(self, s: slice) -> Sequence[IndividualLike]: ...

    def __getitem__(self, key):
        return self.container.__getitem__(key)


    def all_parents_inds(self) -> Sequence[IndividualLike]:
        return self.container.all_parents_inds()

    def add(self, individual: IndividualLike, raise_if_not_added_to_parents: bool = False) -> Optional[int]:
        return self.container.add(individual, raise_if_not_added_to_parents)

    def discard(self, individual: IndividualLike, also_from_parents: bool = False) -> None:
        return self.container.discard(individual, also_from_parents)

    update = functools.partialmethod(Container.update) # type: ignore
    clear = functools.partialmethod(Container.clear) # type: ignore

    def novelty(self, individual: IndividualLike, **kwargs):
        return self.container.novelty(individual, **kwargs)

    def novelty_local_competition(self, individual: IndividualLike, **kwargs):
        return self.container.novelty_local_competition(individual, **kwargs)

    def qd_score(self, normalized: bool = True) -> float:
        return self.container.qd_score(normalized)

    def to_grid(self, shape: Union[ShapeLike, int], max_items_per_bin: int = 1, capacity: Optional[float] = None, **kwargs: Any) -> Any:
        return self.container.to_grid(shape, max_items_per_bin, capacity, **kwargs)

    def __iter__(self) -> Iterator:
        return self.container.__iter__()

    def get_ind_features(self, individual: IndividualLike, *args, **kwargs) -> FeaturesLike:
        return self.container.get_ind_features(individual, *args, **kwargs)

    def get_ind_fitness(self, individual: IndividualLike, *args, **kwargs) -> FitnessLike:
        return self.container.get_ind_fitness(individual, *args, **kwargs)

    def set_ind_fitness(self, individual: IndividualLike, fitness: FitnessLike, *args, **kwargs):
        self.container.set_ind_fitness(individual, fitness, *args, **kwargs)

    @property
    def capacity(self) -> float:
        return self.container.capacity

    @property
    def free(self) -> float:
        return self.container.free

    @property
    def size(self) -> int:
        return self.container.size

    @property
    def best(self) -> Any:
        return self.container.best

    @property
    def best_fitness(self) -> Optional[FitnessLike]:
        return self.container.best_fitness

    @property
    def best_features(self) -> Optional[FeaturesLike]:
        return self.container.best_features

    @property
    def nb_discarded(self) -> int:
        return self.container.nb_discarded

    @property
    def nb_added(self) -> int:
        return self.container.nb_added

    @property
    def nb_rejected(self) -> int:
        return self.container.nb_rejected

    @property
    def nb_operations(self) -> int:
        return self.container.nb_operations

    @property
    def fitness_extrema(self) -> Optional[Sequence[DomainLike]]:
        return self.container.fitness_extrema

    @property
    def features_extrema(self) -> Optional[Sequence[DomainLike]]:
        return self.container.features_extrema



## MODELINE	"{{{1
## vim:expandtab:softtabstop=4:shiftwidth=4:fileencoding=utf-8
## vim:foldmethod=marker
