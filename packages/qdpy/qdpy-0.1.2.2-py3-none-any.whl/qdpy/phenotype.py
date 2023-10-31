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

"""Some base classes, stubs and types."""
#from __future__ import annotations

#__all__ = ["jit"]


########### IMPORTS ########### {{{1
from typing import Optional, Tuple, List, Iterable, Iterator, Any, TypeVar, Generic, Union, Sequence, MutableSet, MutableSequence, Type, Callable, Generator, MutableMapping, overload
from typing_extensions import runtime, Protocol
from operator import mul, truediv
import math
import sys
import importlib
import pickle
import textwrap
import copy
from inspect import signature
from functools import partial
import warnings
import numpy as np

import os
import psutil
import signal
import deprecation
import traceback

from qdpy.utils import *
from qdpy.base import *
import qdpy


########### INTERFACES AND STUBS ########### {{{1
ScoreValuesLike = Union[Sequence[Any], np.ndarray]
FitnessValuesLike = ScoreValuesLike # Union[Sequence[T], np.ndarray]
#FeaturesLike = Union[Sequence[Any], np.ndarray]
FeaturesValuesLike = ScoreValuesLike # Union[Sequence[Any], np.ndarray]

@runtime
class ScoreLike(Protocol):
    """Protocol describing a generic score, that could be used as a fitness score or as a feature descriptor score."""
    def dominates(self, other: Any, obj: Any = slice(None), weights: Optional[ScoreValuesLike] = None) -> bool: ...
    @property
    def values(self) -> ScoreValuesLike: ...
    @values.setter
    def values(self, values: ScoreValuesLike) -> None: ...
    @values.deleter
    def values(self) -> None: ...
    @property
    def valid(self) -> bool: ...
    def reset(self) -> None: ...
    def __getitem__(self, key) -> Any: ...
    def __setitem__(self, idx, value) -> None: ...
    def __len__(self) -> int: ...

@runtime
class FitnessLike(ScoreLike, Protocol):
    """Fitness protocol inspired from (and compatible with) DEAP Fitness class."""
    weights: FitnessValuesLike
#    def dominates(self, other: Any, obj: Any = slice(None), weights: Optional[ScoreValuesLike] = None) -> bool: ...
#    def getValues(self) -> FitnessValuesLike: ...
#    def setValues(self, values: FitnessValuesLike) -> None: ...
#    def delValues(self) -> None: ...
    @property
    def values(self) -> FitnessValuesLike: ...
    @values.setter
    def values(self, values: FitnessValuesLike) -> None: ...
    @values.deleter
    def values(self) -> None: ...
#    @property
#    def valid(self) -> bool: ...
#    def reset(self) -> None: ...
#    @overload
#    def __getitem__(self, i: int) -> Any: ...
#    @overload
#    def __getitem__(self, s: slice) -> Sequence[Any]: ...
#    def __len__(self) -> int: ...


@runtime
class FeaturesLike(ScoreLike, Protocol):
    """Features protocol similar to the ``FitnessLike`` protocol."""
    pass
#    def getValues(self) -> FeaturesValuesLike: ...
#    def setValues(self, values: FeaturesValuesLike) -> None: ...
#    def delValues(self) -> None: ...
#    @property
#    def values(self) -> FeaturesValuesLike: ...
#    @values.setter
#    def values(self, values: FeaturesValuesLike) -> None: ...
#    @values.deleter
#    def values(self) -> None: ...
#    @property
#    def valid(self) -> bool: ...
#    def reset(self) -> None: ...
#    def __getitem__(self, key) -> Any: ...
#    def __len__(self) -> int: ...



@runtime
class ScoresDictLike(Protocol):
    """Protocol containing a map of scores values, which could then be selected as fitness scores or as feature descriptor scores."""
    def clear(self) -> None: ...
    def select(self, names: Sequence[str]) -> Sequence[Any]: ...
    def to_fitness(self, names: Sequence[str], *args, **kwargs) -> FitnessLike: ...
    def to_features(self, names: Sequence[str], *args, **kwargs) -> FeaturesLike: ...
    def __getitem__(self, key) -> Any: ...
    def __setitem__(self, key, value) -> None: ...
    def __contains__(self, value) -> bool: ...
    def items(self) -> Any: ...
    def keys(self) -> Any: ...
    def values(self) -> Any: ...


@runtime
class IndividualLike(Protocol):
    name: str
    #fitness: FitnessLike
    @property
    def fitness(self) -> FitnessLike: ...
    @fitness.setter
    def fitness(self, fit: FitnessLike) -> None: ...
    #features: FeaturesLike
    @property
    def features(self) -> FeaturesLike: ...
    @features.setter
    def features(self, ft: FeaturesLike) -> None: ...
    #scores: ScoresDictLike
    @property
    def scores(self) -> ScoresDictLike: ...
    @scores.setter
    def scores(self, scores: ScoresDictLike) -> None: ...
    elapsed: float
    def dominates(self, other: Any) -> bool: ...
    def reset(self) -> None: ...
    def __setitem__(self, key, values) -> None: ...



#FitnessLike = Sequence
FitnessGetter = Callable[[T], FitnessLike]
FeaturesGetter = Callable[[T], FeaturesLike]
GridIndexLike = ShapeLike



########### BASE OPTIMISATION CLASSES ########### {{{1

class Score(ScoreLike, Sequence[Any]):
    """Score implementation inspired from DEAP Fitness class. It can be used without problem with most (propably all) DEAP methods either as a fitness or as a feature descriptor."""
    _values: ScoreValuesLike

    def __init__(self, values: ScoreValuesLike=(), *args, **kwargs) -> None:
        self._values = values

    def weighted_values(self, weights: ScoreValuesLike) -> ScoreValuesLike:
        return tuple(map(mul, self, weights))
    def inv_weighted_values(self, weights: ScoreValuesLike) -> ScoreValuesLike:
        return tuple(map(truediv, self, weights))

    # Inspired by the dominates method from DEAP
    def dominates(self, other: Any, obj: Any = slice(None), weights: Optional[ScoreValuesLike] = None) -> bool:
        """Return true if each objective of ``self`` is not strictly worse than
        the corresponding objective of ``other`` and at least one objective is
        strictly better.
        """
#    :param obj: Slice indicating on which objectives the domination is
#                tested. The default value is `slice(None)`, representing
#                every objectives.  """
        self_wvalues = self.weighted_values(weights)[obj] if weights else self._values[obj]
        other_wvalues = other.weighted_values(weights)[obj] if weights else other._values[obj]
        not_equal: bool = False
        for self_wvalue, other_wvalue in zip(self_wvalues, other_wvalues):
            if self_wvalue > other_wvalue:
                not_equal = True
            elif self_wvalue < other_wvalue:
                return False
        return not_equal

    @property
    def valid(self) -> bool:
        """Assess if a Score is valid or not."""
        return len(self._values) != 0

    @property
    def values(self) -> ScoreValuesLike:
        return self._values

    @values.setter
    def values(self, values: ScoreValuesLike) -> None:
        self._values = values

    @values.deleter
    def values(self) -> None:
        self._values = ()

    def reset(self) -> None:
        self._values = (np.nan,) * len(self._values)

    def __len__(self) -> int:
        return len(self.values)

#    @overload
#    def __getitem__(self, index: int) -> T: ...
#
#    @overload
#    def __getitem__(self, s: slice) -> Sequence: ...

    def __getitem__(self, key):
        return self.values[key]

    def __setitem__(self, idx, value):
        self._values[idx] = value
        #if idx == slice(None, None, None):
        #    self.add_sample(value)
        #else:
        #    self._values[idx] = value

    def __contains__(self, key: Any) -> bool:
        return key in self.values

    def __iter__(self) -> Iterator:
        return iter(self.values)

    def __reversed__(self) -> Iterator:
        return reversed(self.values)


    def __hash__(self) -> int:
        return hash(self.values)

    def __gt__(self, other: Any) -> bool:
        return not self.__le__(other)

    def __ge__(self, other: Any) -> bool:
        return not self.__lt__(other)

    def __le__(self, other: Any) -> bool:
        return self.values <= other.values

    def __lt__(self, other: Any) -> bool:
        return self.values < other.values

    def __eq__(self, other: Any) -> bool:
        return self.values == other.values

    def __ne__(self, other: Any) -> bool:
        return not self.__eq__(other)

    def __str__(self) -> str:
        #return str(self.values if self.valid else tuple())
        return str(self.values)

    def __repr__(self) -> str:
        if not self:
            return "%s()" % (self.__class__.__name__,)
        return "%s(%r)" % (self.__class__.__name__, tuple(self))



class Fitness(Score, FitnessLike):
    """Fitness implementation inspired from DEAP Fitness class. It can be used without problem with most (propably all) DEAP methods."""

    weights: FitnessValuesLike = ()
    #wvalues: FitnessValuesLike = ()

    def __init__(self, values: FitnessValuesLike=(), weights: Optional[FitnessValuesLike]=None) -> None:
        if weights is None:
            if len(self.weights) == 0: # If weights was NOT initialized by DEAP `creator.create method`
                self.weights = tuple([-1.0 for _ in range(len(values))]) # Defaults to minimisation
        else:
            self.weights = weights
#        if len(self.weights) != len(values):
#            raise ValueError(f"``values`` and ``weights`` must have the same length ({len(values)} vs {len(self.weights)}).")
        self.values = values

    @property
    def values(self) -> FitnessValuesLike:
        return tuple(map(truediv, self._values, self.weights))

    @values.setter
    def values(self, values: FitnessValuesLike) -> None:
#        if len(self.weights) != len(values):
#            raise ValueError(f"``values`` and ``weights`` must have the same length ({len(values)} vs {len(self.weights)}).")
        try:
            self._values = tuple(map(mul, values, self.weights))
        #except TypeError:
        except Exception as e:
            raise ValueError("Invalid ``values`` parameter. Make sure that ``values`` and ``weights`` have the same length.")

    @values.deleter
    def values(self) -> None:
        self._values = ()

    @deprecation.deprecated(deprecated_in="0.1.3", removed_in="0.2.0",
                        current_version=qdpy.__version__,
                        details="Use 'foo = fitness.values' instead.")
    def getValues(self) -> FitnessValuesLike:
        return self.values

    @deprecation.deprecated(deprecated_in="0.1.3", removed_in="0.2.0",
                        current_version=qdpy.__version__,
                        details="Use 'fitness.values = (42,)' instead.")
    def setValues(self, values: FitnessValuesLike) -> None:
        self.values = values

    @deprecation.deprecated(deprecated_in="0.1.3", removed_in="0.2.0",
                        current_version=qdpy.__version__,
                        details="Use 'del fitness.values' instead.")
    def delValues(self) -> None:
        del self.values

#    def dominates(self, other: Any, obj: Any = slice(None), weights: Optional[ScoreValuesLike] = None) -> bool:
#        """Return true if each objective of ``self`` is not strictly worse than
#        the corresponding objective of ``other`` and at least one objective is
#        strictly better.
#        """
##    :param obj: Slice indicating on which objectives the domination is
##                tested. The default value is `slice(None)`, representing
##                every objectives.  """
#        return super().dominates(other, None, obj)



class Features(Score, FeaturesLike):
    @deprecation.deprecated(deprecated_in="0.1.3", removed_in="0.2.0",
                        current_version=qdpy.__version__,
                        details="Use 'foo = features.values' instead. ")
    def getValues(self) -> FeaturesValuesLike:
        return self.values

    @deprecation.deprecated(deprecated_in="0.1.3", removed_in="0.2.0",
                        current_version=qdpy.__version__,
                        details="Use 'features.values = (42,)' instead. ")
    def setValues(self, values: FeaturesValuesLike) -> None:
        self.values = values

    @deprecation.deprecated(deprecated_in="0.1.3", removed_in="0.2.0",
                        current_version=qdpy.__version__,
                        details="Use 'del features.values' instead. ")
    def delValues(self) -> None:
        del self.values



class ScoresDict(dict, ScoresDictLike):
    def select(self, names: Sequence[str]) -> Sequence[Any]:
        #if isinstance(names, str):
        #    names = [names]
        res = []
        for n in names:
            res.append(self.get(n, np.nan))
        return res

    def to_fitness(self, names: Sequence[str], *args, **kwargs) -> FitnessLike:
        return Fitness(self.select(names), *args, **kwargs)

    def to_features(self, names: Sequence[str], *args, **kwargs) -> FeaturesLike:
        return Features(self.select(names), *args, **kwargs)



class Individual(list, IndividualLike):
    """Qdpy Individual class. Note that containers and algorithms all use internally either the QDPYIndividualLike Protocol or the IndividualWrapper class, so you can easily declare an alternative class to Individual. TODO""" # TODO

    name: str
    _fitness: FitnessLike
    _features: FeaturesLike
    _scores: ScoresDictLike
    elapsed: float = math.nan

    def __init__(self, iterable: Optional[Iterable] = None,
            name: Optional[str] = None,
            fitness: Optional[FitnessLike] = None, features: Optional[FeaturesLike] = None,
            scores: Optional[ScoresDictLike] = None) -> None:
        if iterable is not None:
            self.extend(iterable)
        self.name = name if name else ""
        self._scores = scores if scores is not None else ScoresDict({})
        self.fitness = fitness if fitness is not None else Fitness()
        self.features = features if features is not None else Features([])

    def __repr__(self) -> str:
        if not self:
            return "%s()" % (self.__class__.__name__,)
        return "%s(%r)" % (self.__class__.__name__, list(self))

    @property
    def fitness(self) -> FitnessLike:
        return self._fitness
#        return self.scores.setdefault("fitness", Fitness())
    @fitness.setter
    def fitness(self, fit: FitnessLike) -> None:
        #self._scores["fitness"] = fit
        self._fitness = fit

    @property
    def features(self) -> FeaturesLike:
        #return self._scores.setdefault("features", Features())
        return self._features
    @features.setter
    def features(self, ft: FeaturesLike) -> None:
        #self._scores["features"] = ft
        self._features = ft

    @property
    def scores(self) -> ScoresDictLike:
        return self._scores
    @scores.setter
    def scores(self, scores: ScoresDictLike) -> None:
        if isinstance(scores, ScoresDictLike):
            self._scores = scores
        else:
            self._scores = ScoresDict(scores)

    def dominates(self, other: Any, score_name: Optional[str] = None) -> bool:
        """Return true if ``self`` dominates ``other``. """
        if score_name is None:
            return self.fitness.dominates(other.fitness)
        else:
            return self._scores[score_name].dominates(other._scores[score_name])

    def reset(self) -> None:
        self._scores.clear()
        self.fitness.reset()
        #self._scores["fitness"] = self._fitness
        self.features.reset()
        #self._scores["features"] = self._features
        self.elapsed = math.nan


    # TODO : improve performance ! (quick and dirty solution !)
    def __hash__(self):
        return hash(tuple(self))

    def __eq__(self, other):
        return (self.__class__ == other.__class__ and tuple(self) == tuple(other))


@registry.register # type: ignore
class GenIndividuals(CreatableFromConfig):
    def __init__(self, *args, **kwargs):
        pass
    def __iter__(self):
        return self
    def __next__(self):
        return Individual()
    def __call__(self):
        while(True):
            yield self.__next__()



# MODELINE	"{{{1
# vim:expandtab:softtabstop=4:shiftwidth=4:fileencoding=utf-8
# vim:foldmethod=marker
