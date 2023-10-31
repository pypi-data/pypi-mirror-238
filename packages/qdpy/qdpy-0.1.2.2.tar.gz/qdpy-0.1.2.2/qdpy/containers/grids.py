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

__all__ = ["Grid", "CVTGrid", "AutoScalingGrid"]

########### IMPORTS ########### {{{1
import math
from functools import reduce
import operator
import numpy as np
from typing import Optional, Tuple, List, Iterable, Iterator, Any, TypeVar, Generic, Union, Sequence, MutableSet, MutableSequence, Type, Callable, Generator, MutableMapping, Mapping, overload
import random
#import traceback

from qdpy.utils import *
from qdpy.phenotype import *
from qdpy.base import *
from qdpy.metrics import novelty, novelty_local_competition, novelty_nn
from .base import *




########### GRID-BASED CLASSES ########### {{{2

# Custom types
GridSolutionsLike = MutableMapping[GridIndexLike, MutableSequence]
GridItemsPerBinLike = MutableMapping[GridIndexLike, int]
GridFitnessLike = MutableMapping[GridIndexLike, MutableSequence[FitnessLike]]
GridFeaturesLike = MutableMapping[GridIndexLike, MutableSequence[FeaturesLike]]
GridQualityLike = MutableMapping[GridIndexLike, Optional[FitnessLike]]
GridRecentnessPerBinLike = MutableMapping[GridIndexLike, MutableSequence[int]]


@registry.register
class Grid(Container):
    """TODO""" # TODO

    fitness_domain: Sequence[DomainLike]
    features_domain: Sequence[DomainLike]

    _shape: ShapeLike
    _max_items_per_bin: int
    _filled_bins: int
    _solutions: GridSolutionsLike
    _nb_items_per_bin: GridItemsPerBinLike
    _fitness: GridFitnessLike
    _features: GridFeaturesLike
    _quality: GridQualityLike
    _quality_array: np.array
    _bins_size: Sequence[float]
    _nb_bins: int
    recentness_per_bin: GridRecentnessPerBinLike
    history_recentness_per_bin: GridRecentnessPerBinLike
    activity_per_bin: np.array
    discard_random_on_bin_overload: bool


    def __init__(self, iterable: Optional[Iterable] = None,
            shape: Union[ShapeLike, int] = (1,), max_items_per_bin: int = 1,
            fitness_domain: Optional[Sequence[DomainLike]] = ((0., np.inf),),
            discard_random_on_bin_overload = False,
            **kwargs: Any) -> None:
        self._shape = tuplify(shape)
        self._max_items_per_bin = max_items_per_bin
        self.discard_random_on_bin_overload = discard_random_on_bin_overload
        super().__init__([], fitness_domain=fitness_domain, **kwargs)
        if self.features_domain is None or len(self.features_domain) == 0:
            raise ValueError("`features_domain` must be specified and have a length > 0.")
        if self.fitness_domain is None or len(self.fitness_domain) == 0:
            raise ValueError("`fitness_domain` must be specified and have a length > 0.")
        #if len(self.features_domain) != len(self.shape):
        #    raise ValueError("`features_domain` must have the same shape as `shape`.")
        self._init_grid()
        if not "capacity" in kwargs:
            self._capacity = self._nb_bins * self._max_items_per_bin
        if iterable is not None:
            self.update(iterable)


    def _init_grid(self) -> None:
        """Initialise the grid to correspond to the shape `self.shape`."""
        self._solutions = {x: [] for x in self._index_grid_iterator()}
        self._nb_items_per_bin = np.zeros(self._shape, dtype=int) #{x: 0 for x in self._index_grid_iterator()}
        self._fitness = {x: [] for x in self._index_grid_iterator()}
        self._features = {x: [] for x in self._index_grid_iterator()}
        self._quality = {x: None for x in self._index_grid_iterator()}
        self._quality_array = np.full(self._shape + (len(self.fitness_domain),), np.nan)
        self._bins_size = [(self.features_domain[i][1] - self.features_domain[i][0]) / float(self.shape[i]) for i in range(len(self.shape))]
        self._filled_bins = 0
        self._nb_bins = reduce(operator.mul, self._shape)
        self.recentness_per_bin = {x: [] for x in self._index_grid_iterator()}
        self.history_recentness_per_bin = {x: [] for x in self._index_grid_iterator()}
        self.activity_per_bin = np.zeros(self._shape, dtype=int)


    @property
    def shape(self) -> ShapeLike:
        """Return the shape of the grid."""
        return self._shape

    @property
    def max_items_per_bin(self) -> int:
        """Return the maximal number of items stored in a bin of the grid."""
        return self._max_items_per_bin

    @property
    def filled_bins(self) -> int:
        """Return the number of filled bins of the container."""
        return self._filled_bins

    @property
    def solutions(self) -> GridSolutionsLike:
        """Return the solutions in the grid."""
        return self._solutions

    @property
    def nb_items_per_bin(self) -> GridItemsPerBinLike:
        """Return the number of items stored in each bin of the grid."""
        return self._nb_items_per_bin

    @property
    def fitness(self) -> GridFitnessLike:
        """Return the fitness values in the grid."""
        return self._fitness

    @property
    def features(self) -> GridFeaturesLike:
        """Return the features values in the grid."""
        return self._features

    @property
    def quality(self) -> GridQualityLike:
        """Return the best fitness values in the grid."""
        return self._quality

    @property
    def quality_array(self) -> np.array:
        """Return the best fitness values in the grid, as a numpy array."""
        return self._quality_array

    @property
    def best_index(self) -> Optional[GridIndexLike]:
        """Return the index of the individual with the best quality, or None. """
        if self._best_features is None:
            return None
        else:
            return self.index_grid(self._best_features)


    def filled_str(self) -> str:
        """Return a string describing the fullness of the grid (not the container itself, which is handled by ``Container.size_str``)."""
        return "%i/%i" % (self.filled_bins, self._nb_bins)


    def _index_grid_features(self, features: FeaturesLike) -> GridIndexLike:
        """Get the index in the grid of a given individual with features ``features``, raising an IndexError if it is outside the grid. """
        index: List[int] = []
        if len(features) != len(self.shape):
            raise IndexError(f"Length of parameter ``features`` ({len(features)}) does not corresponds to the number of dimensions of the grid ({len(self.shape)}).")
        for i in range(len(features)):
            normalised_feature: float = features[i] - self.features_domain[i][0]
            if normalised_feature == self.features_domain[i][1] - self.features_domain[i][0]:
                partial: int = self.shape[i] - 1
            elif normalised_feature > self.features_domain[i][1] - self.features_domain[i][0]:
                raise IndexError(f"``features`` ({str(features)}) out of bounds ({str(self.features_domain)})")
            else:
                partial = int(normalised_feature / self._bins_size[i])
            index.append(partial)
        return tuple(index)


    @overload
    def index_grid(self, features: FeaturesLike) -> GridIndexLike: ...

    @overload
    def index_grid(self, scores: ScoresDictLike) -> GridIndexLike: ...

    @overload
    def index_grid(self, ind: IndividualLike) -> GridIndexLike: ...

    def index_grid(self, param):
        """Get the index in the grid of object ``param``, raising an IndexError if it is outside the grid.

        Parameters
        ----------
        :param param: Union[FeaturesLike, ScoresDictLike, IndividualLike]:
            The target object this method should return the index of. It can be either an individual object, or a features or scores object.

        Return
        ------
        index: GridIndexLike
            Index of object ``param`` in the grid.
        """
        if isinstance(param, ScoresDictLike):
            if len(self.features_score_names) == 0:
                raise RuntimeError(f"'features_score_names' must be set to compute an individual grid index from scores.")
            features = param.to_features(self.features_score_names)
        elif isinstance(param, IndividualLike):
            features = self.get_ind_features(param)
        elif hasattr(param, "features"):
            features = param.features
        else:
            features = param
        return self._index_grid_features(features)


    def _index_grid_iterator(self) -> Generator[GridIndexLike, None, None]:
        """Return an iterator of the index of the grid, based on ``self.shape``."""
        val: List[int] = [0] * len(self._shape)
        yield tuple(val)
        while True:
            for i in reversed(range(len(self._shape))):
                val[i] += 1
                if val[i] >= self._shape[i]:
                    if i == 0:
                        return
                    val[i] = 0
                else:
                    yield tuple(val)
                    break

    def _update_quality(self, ig: GridIndexLike) -> None:
        """Update quality in bin ``ig`` of the grid."""
        if self._nb_items_per_bin[ig] == 0:
            val: Optional[FitnessLike] = None
        elif self._nb_items_per_bin[ig] == 1:
            val = self.fitness[ig][0]
        else:
            best: IndividualLike = self.solutions[ig][0]
            fit_best = self.get_ind_fitness(best)
            for s in self.solutions[ig][1:]:
                fit_s = self.get_ind_fitness(s)
                if fit_s.dominates(fit_best):
                    best = s
                    fit_best = self.get_ind_fitness(best)
            val = fit_best
        self.quality[ig] = val
        if val is None:
            self.quality_array[ig] = math.nan
        else:
            self.quality_array[ig] = val.values


    def _add_internal(self, individual: IndividualLike, raise_if_not_added_to_parents: bool, only_to_parents: bool) -> Optional[int]:
        # Check if individual can be added in grid, if there are enough empty spots
        can_be_added: bool = False
        if not only_to_parents:
            try:
                # Find corresponding index in the grid
                ig = self.index_grid(individual) # Raise exception if features are out of bounds

                
                if self._nb_items_per_bin[ig] < self.max_items_per_bin:
                    can_be_added = True
                else:
                    if self.discard_random_on_bin_overload:
                        idx_to_discard = random.randint(0, len(self.solutions[ig])-1)
                        Container.discard(self, self.solutions[ig][idx_to_discard])
                        self._discard_from_grid(ig, idx_to_discard)
                        can_be_added = True
                    else:
                        worst_idx = 0
                        worst: IndividualLike = self.solutions[ig][worst_idx]
                        fit_worst = self.get_ind_fitness(worst)
                        if self._nb_items_per_bin[ig] > 1:
                            for i in range(1, self._nb_items_per_bin[ig]):
                                s = self.solutions[ig][i]
                                fit_s = self.get_ind_fitness(s)
                                if fit_worst.dominates(fit_s):
                                    worst = s
                                    worst_idx = i
                                    fit_worst = self.get_ind_fitness(worst)
                        fit_ind = self.get_ind_fitness(individual)
                        if fit_ind.dominates(fit_worst):
                            Container.discard(self, self.solutions[ig][worst_idx])
                            self._discard_from_grid(ig, worst_idx)
                            can_be_added = True
            except:
                pass

        # Add individual in grid, if there are enough empty spots
        if can_be_added:
            if self._nb_items_per_bin[ig] == 0:
                self._filled_bins += 1
            # Add individual in container
            old_len: int = self._size
            index: Optional[int] = super()._add_internal(individual, raise_if_not_added_to_parents, False)
            if index == old_len: # Individual was not already present in container
                self._solutions[ig].append(individual)
                ind_fit = self.get_ind_fitness(individual)
                self._fitness[ig].append(ind_fit)
                ind_ft = self.get_ind_features(individual)
                self._features[ig].append(ind_ft)
                self.recentness_per_bin[ig].append(self._nb_added)
                self.history_recentness_per_bin[ig].append(self._nb_added)
                self._nb_items_per_bin[ig] += 1
                self.activity_per_bin[ig] += 1
            # Update quality
            self._update_quality(ig)
            return index
        else:
            # Only add to parents
            if len(self.parents) > 0:
                super()._add_internal(individual, raise_if_not_added_to_parents, True)
            return None


    def _discard_from_grid(self, ig: GridIndexLike, index_in_bin: int) -> None:
        # Remove individual from grid
        del self._solutions[ig][index_in_bin]
        self._nb_items_per_bin[ig] -= 1
        del self._fitness[ig][index_in_bin]
        del self._features[ig][index_in_bin]
        del self.recentness_per_bin[ig][index_in_bin]
        # Update quality
        self._update_quality(ig)
        # Update number of filled bins
        if self._nb_items_per_bin[ig] == 0:
            self._filled_bins -= 1


    def discard(self, individual: IndividualLike, also_from_parents: bool = False) -> None:
        """Remove ``individual`` of the container. If ``also_from_parents`` is True, discard it also from the parents, if they exist."""
        old_len: int = self._size
        # Remove individual from container
        Container.discard(self, individual, also_from_parents)
        if self._size == old_len:
            return
        # Remove individual from grid
        ig = self.index_grid(individual) # Raise exception if features are out of bounds
        index_in_bin = self.solutions[ig].index(individual)
        self._discard_from_grid(ig, index_in_bin)

    def _get_best_inds(self):
        best_inds = []
        for idx, inds in self.solutions.items():
            if len(inds) == 0:
                continue
            best = inds[0]
            best_fit = self.get_ind_fitness(best)
            for ind in inds[1:]:
                ind_fit = self.get_ind_fitness(ind)
                if ind_fit.dominates(best_fit):
                    best = ind
                    best_fit = self.get_ind_fitness(best)
            best_inds.append(best)
        return best_inds


    def qd_score(self, normalized: bool = True) -> float:
        """Return the QD score of this grid. It corresponds to the sum of the fitness values of the best individuals of each bin of the grid.

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
                best_inds = self._get_best_inds()
                for ind in best_inds:
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





from sklearn.cluster import KMeans
from sklearn.gaussian_process import GaussianProcessRegressor

@registry.register
class CVTGrid(Grid):
    """TODO""" # TODO

    _grid_shape: ShapeLike
    _nb_sampled_points: int
    cluster_centers: np.array

    def __init__(self, iterable: Optional[Iterable] = None,
            shape: Union[ShapeLike, int] = (1,), max_items_per_bin: int = 1,
            grid_shape: Union[ShapeLike, int] = (1,), nb_sampled_points: int = 50000, **kwargs: Any) -> None:
        self._grid_shape = tuplify(grid_shape)
        self._nb_sampled_points = nb_sampled_points
        super().__init__(iterable, shape, max_items_per_bin, **kwargs)
        if len(self.shape) != 1:
            raise ValueError("Using CVTGrid, `shape` must be a scalar or a sequence of length 1.")
        if nb_sampled_points <= 0:
            raise ValueError("`nb_sampled_points` must be positive and greatly superior to `shape` and `grid_shape`.")
        self._init_clusters()

    def _init_clusters(self) -> None:
        """Initialise the clusters and tessellate the grid."""
        sample = np.random.uniform(0.0, 1.0, (self.nb_sampled_points, len(self.grid_shape)))
        for i, d in enumerate(self.features_domain):
            sample[:, i] = d[0] + (d[1] - d[0]) * sample[:, i]
        kmeans = KMeans(init="k-means++", n_clusters=self.shape[0], n_init=1, n_jobs=1, verbose=0)
        kmeans.fit(sample)
        self.cluster_centers = kmeans.cluster_centers_

    @property
    def grid_shape(self) -> ShapeLike:
        """Return the shape of the grid."""
        return self._grid_shape

    @property
    def nb_sampled_points(self) -> int:
        """Return the number of sampled points to identify cluster centers."""
        return self._nb_sampled_points

    def _index_grid_features(self, features: FeaturesLike) -> GridIndexLike:
        """Get the index in the cvt of a given individual with features ``features``, raising an IndexError if it is outside the cvt. """
        dists = np.empty(self._shape[0])
        for i in range(len(dists)):
            dists[i] = math.sqrt(np.sum(np.square(self.cluster_centers[i] - features)))
        return (np.argmin(dists),)




@registry.register
class AutoScalingGrid(Grid):
    """ A Grid-based container that automatically scale the fitness and/or feature descriptors domains to match the fitness/features descriptors extrema encountered so far.
It can be used in problems where the domain of feature descriptors is not known in advance.
Each time that a recaling takes place, the autoscaling grid container will be reinitialized. First all individuals will be removed from the grid,
then all individuals from parent containers will be added to the grid. As such, autoscaling grids need to rely on at least one other container
to store all previously encountered individuals.
    """ # TODO

    scaling_containers: Sequence[Container]
    fitness_scaling: bool
    features_scaling: bool
    rescaling_period: int

    def __init__(self, iterable: Optional[Iterable] = None,
            shape: Union[ShapeLike, int] = (1,), max_items_per_bin: int = 1,
            scaling_containers: Sequence[Container] = [],
            fitness_scaling: bool = True,
            features_scaling: bool = True,
            rescaling_period: int = 1,
            **kwargs: Any) -> None:
        self.scaling_containers = scaling_containers
        self.fitness_scaling = fitness_scaling
        self.features_scaling = features_scaling
        self.rescaling_period = rescaling_period # max(rescaling_period, 1)
        self._nb_rescaled = 0
        self._last_nb_rescaled = 0
        super().__init__(iterable, shape, max_items_per_bin, **kwargs)


    def rescale(self, fitness_domain: Sequence[DomainLike], features_domain: Sequence[DomainLike]) -> None:
        #print(f"# rescale {features_domain} {len(self)}")
        # Identify which individuals should be added after the rescaling
        if len(self.scaling_containers) > 0:
            inds = flatten_seq_of_seq(self.scaling_containers)
        elif len(self.parents) > 0:
            inds = self.all_parents_inds()
        else:
            inds = list(self)

        # Rescale the container
        self.clear()
        self.fitness_domain = fitness_domain
        self.features_domain = features_domain
        self._init_grid()
        for i in inds:
            try:
                super().add(i)
            except Exception:
                pass
        #print(f"# rescale flatten: {len(flatten_seq_of_seq(self.scaling_containers))} {len(self)}")


    def _recompute_fitness_extrema(self, new_ind_fits: Sequence[FitnessLike]) -> Sequence[DomainLike]:
        assert(len(new_ind_fits) > 0)
        maxima = np.array(new_ind_fits[0])
        minima = np.array(new_ind_fits[0])
        for ind in self:
            ind_f = np.array(self.get_ind_fitness(ind).values)
            for i in range(len(maxima)):
                if ind_f[i] > maxima[i]:
                    maxima[i] = ind_f[i]
                elif ind_f[i] < minima[i]:
                    minima[i] = ind_f[i]
        for f in new_ind_fits:
            ind_f = np.array(f)
            for i in range(len(maxima)):
                if ind_f[i] > maxima[i]:
                    maxima[i] = ind_f[i]
                elif ind_f[i] < minima[i]:
                    minima[i] = ind_f[i]
        return tuple(zip(minima, maxima))

    def _recompute_features_extrema(self, new_ind_fts: Sequence[FeaturesLike]) -> Sequence[DomainLike]:
        assert(len(new_ind_fts) > 0)
        maxima = np.array(new_ind_fts[0])
        minima = np.array(new_ind_fts[0])
        for ind in self:
            ind_f = np.array(self.get_ind_features(ind))
            for i in range(len(maxima)):
                if ind_f[i] > maxima[i]:
                    maxima[i] = ind_f[i]
                elif ind_f[i] < minima[i]:
                    minima[i] = ind_f[i]
        for f in new_ind_fts:
            ind_f = np.array(f)
            for i in range(len(maxima)):
                if ind_f[i] > maxima[i]:
                    maxima[i] = ind_f[i]
                elif ind_f[i] < minima[i]:
                    minima[i] = ind_f[i]
        return tuple(zip(minima, maxima))


    def _add_rescaling(self, inds: Sequence[IndividualLike]) -> None:
#        self._nb_rescaled += len(inds)
#        if self.rescaling_period <= 0 or self._nb_rescaled - self._last_nb_rescaled < self.rescaling_period:
#            return
#
        fits = []
        fts = []
        valid_inds = []
        # Iterate and find valid inds, their fitness and feature descriptors
        for ind in inds:
            fit = self.get_ind_fitness(ind)
            ft = self.get_ind_features(ind)
            if not fit.valid:
                continue
            # If needed, check if fitness and features are within bounds
            if not self.fitness_scaling and not self.in_bounds(fit.values, self.fitness_domain):
                continue
            if not self.features_scaling and not self.in_bounds(ft, self.features_domain):
                continue
            valid_inds.append(ind)
            fits.append(fit)
            fts.append(ft)
        if len(valid_inds) == 0:
            return

        # Rescale grid
        new_fit_domain = self.fitness_domain
        new_ft_domain = self.features_domain
        rescale = False
        if self.fitness_scaling:
            new_fit_domain = self._recompute_fitness_extrema(fits)
            rescale = new_fit_domain != self.fitness_extrema
        if self.features_scaling:
            new_ft_domain = self._recompute_features_extrema(fts)
            rescale = new_ft_domain != self.features_extrema
        if rescale:
            self.rescale(new_fit_domain, new_ft_domain)
            self._last_nb_rescaled = self._nb_rescaled


    def add(self, individual: IndividualLike, raise_if_not_added_to_parents: bool = False) -> Optional[int]:
        # Rescale grid if needed
        self._nb_rescaled += 1
        if self.rescaling_period > 0 and self._nb_rescaled - self._last_nb_rescaled >= self.rescaling_period:
            self._add_rescaling([individual])
        # Add new individual
        return super().add(individual, raise_if_not_added_to_parents)


    def update(self, iterable: Iterable, ignore_exceptions: bool = True, issue_warning: bool = False) -> int:
        # Rescale grid if needed
        self._nb_rescaled += len(iterable) # type: ignore
        if self.rescaling_period > 0 and self._nb_rescaled - self._last_nb_rescaled >= self.rescaling_period:
            self._add_rescaling(iterable) # type: ignore
        # Add new individual
        return super().update(iterable, ignore_exceptions, issue_warning)





## MODELINE	"{{{1
## vim:expandtab:softtabstop=4:shiftwidth=4:fileencoding=utf-8
## vim:foldmethod=marker
