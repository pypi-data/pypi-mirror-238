# type: ignore
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

__all__ = ["TorchFeatureExtractionContainerDecorator", "TorchAE"]

########### IMPORTS ########### {{{1
import numpy as np
from typing import Optional, Tuple, List, Iterable, Iterator, Any, TypeVar, Generic, Union, Sequence, MutableSet, MutableSequence, Type, Callable, Generator, MutableMapping, Mapping, overload
import types
from timeit import default_timer as timer

from qdpy.utils import *
from qdpy.phenotype import *
from qdpy.base import *
from qdpy.metrics import novelty, novelty_local_competition, novelty_nn
from .base import *



########### FEATURE EXTRACTION CLASSES ########### {{{2


try:
    import torch
    import torch.nn as nn
    from torch.autograd import Variable
    from torch.utils.data import DataLoader


    class TorchAE(nn.Module):
        def __init__(self, input_size, latent_size=2):
            super().__init__()
            self.input_size = input_size
            self.latent_size = latent_size

            fst_layer_size = input_size//2 if input_size > 7 else 4
            snd_layer_size = input_size//4 if input_size > 7 else 2

            self.encoder = nn.Sequential(
                nn.Linear(input_size, fst_layer_size),
                nn.ReLU(True),
                nn.Linear(fst_layer_size, snd_layer_size),
                nn.ReLU(True),
                nn.Linear(snd_layer_size, latent_size))
            self.decoder = nn.Sequential(
                nn.Linear(latent_size, snd_layer_size),
                nn.ReLU(True),
                nn.Linear(snd_layer_size, fst_layer_size),
                nn.ReLU(True),
                nn.Linear(fst_layer_size, input_size), nn.Tanh())

            # Initialize weights
            def init_weights(m):
                if type(m) == nn.Linear:
                    torch.nn.init.normal_(m.weight, mean=0.0, std=0.3)
                    torch.nn.init.ones_(m.bias)
            self.encoder.apply(init_weights)
            self.decoder.apply(init_weights)


        def forward(self, x):
            x = self.encoder(x)
            x = self.decoder(x)
            return x



    # Unbound get_ind_features method of the ``DebugTorchFeatureExtractionContainerDecorator`` class
    def _TorchFeatureExtractionContainerDecorator_get_ind_features(self, individual: IndividualLike, *args, **kwargs) -> FeaturesLike:
        # Extracted features are already computed. Use the stored values.
        if f"extracted_{id(self)}_0" in individual.scores:
            latent_scores = []
            i = 0
            while f"extracted_{id(self)}_{i}" in individual.scores:
                latent_scores.append(individual.scores[f"extracted_{id(self)}_{i}"])
                i += 1
            return Features(latent_scores)

        #return self.compute_latent([individual])[0]
        # Calling ``compute_latent`` is too computationally expensive.
        # Instead, run a similar code, but only on one individual ``individual`` rather than a sequence of individuals:

        # Create model if none exists
        if self.model == None:
            self._create_default_model(individual)
            #print("DEBUG: created default model")
        # Identify base scores
        base_scores = self.base_scores
        if self.base_scores == None: # Not base scores specified, use all scores (except those created through feature extraction)
            base_scores = [x for x in individual.scores.keys() if not x.startswith("extracted_") ]
        # Get ``individual``'s base scores
        ind_scores = torch.empty(len(base_scores)) # type: ignore
        for i, s in enumerate(base_scores): # type: ignore
            ind_scores[i] = individual.scores[s] # TODO error message if individual does not have the specified score
        # Get latent representation of base scores
        latent_scores = self.model.encoder(ind_scores).tolist() # type: ignore
        # Store latent scores into ``individual``
        for i in range(len(latent_scores)):
            individual.scores[f"extracted_{id(self)}_{i}"] = latent_scores[i]
        #print("DEBUG scores:", individual, latent_scores) # XXX
        # Return final values
        return Features(latent_scores)


#    # Unbound add method of the ``DebugTorchFeatureExtractionContainerDecorator`` class
#    def _TorchFeatureExtractionContainerDecorator_add(self, individual: Any, raise_if_not_added_to_parents: bool = False) -> Any:
#        traceback.print_stack() #XXX
#        # Train and recomputed all features if necessary
#        training_inds = self._get_training_inds()
#        nb_training_inds = len(training_inds)
#        #print("DEBUG add !", nb_training_inds, self.training_period, self._last_training_nb_inds)
#        if nb_training_inds >= self.training_period and nb_training_inds % self.training_period == 0 and nb_training_inds != self._last_training_nb_inds:
#            self._last_training_nb_inds = nb_training_inds
#            try:
#                self.clear()
#                self.train(self.nb_epochs if nb_training_inds > self.training_period else self.initial_nb_epochs)
#                self.recompute_features_all_ind()
#            except Exception as e:
#                print("Training failed !")
#                traceback.print_exc()
#                raise e
#
#        # Add individual(s)
#        #res = self._orig_add(individual, raise_if_not_added_to_parents)
#        try:
#            #res = self.container.add(individual, raise_if_not_added_to_parents)
#            res = self._orig_add(individual, raise_if_not_added_to_parents)
#        #except IndexError as e:
#        #    pass
#        #except ValueError as e:
#        #    pass
#        except Exception as e:
#            traceback.print_exc()
#            raise e
#        return res
#

    @registry.register
    class TorchFeatureExtractionContainerDecorator(ContainerDecorator):
        """TODO""" # TODO

        training_containers: Sequence[ContainerLike]
        model: Optional[nn.Module]
        initial_nb_epochs: int
        nb_epochs: int
        batch_size: int
        learning_rate: float
        training_period: int
        base_scores: Optional[Sequence[str]]
        current_loss: float

        def __init__(self, container: ContainerLike,
                training_containers: Sequence[ContainerLike] = [],
                model: Optional[nn.Module] = None,
                initial_nb_epochs: int = 100,
                nb_epochs: int = 2, batch_size: int = 128,
                learning_rate: float = 1e-3,
                training_period: int = 100,
                base_scores: Optional[Sequence[str]] = None,
                **kwargs: Any) -> None:
            self.training_containers = training_containers
            self.model = model
            self.initial_nb_epochs = initial_nb_epochs
            self.nb_epochs = nb_epochs
            self.batch_size = batch_size
            self.learning_rate = learning_rate
            self.training_period = training_period
            self.base_scores = base_scores
            self.current_loss = np.nan
            self._last_training_nb_inds = 0
            super().__init__(container, **kwargs)
            self._init_methods_hooks()


        def _init_methods_hooks(self):
            # TODO create a bound method instead (with types.MethodType)
            # Replace container's `get_ind_features` method
            #self._orig_get_ind_features = self.container.get_ind_features
            #self.container.get_ind_features = partial(self.__get_ind_features, self) # type: ignore
            #self.get_ind_features = partial(self.__get_ind_features, container_self=self.container) # type: ignore
            self._orig_get_ind_features = self.container.get_ind_features
            self.container.get_ind_features = partial(_TorchFeatureExtractionContainerDecorator_get_ind_features, self) # type: ignore
            self.get_ind_features = partial(_TorchFeatureExtractionContainerDecorator_get_ind_features, self) # type: ignore

            # TODO create a bound method instead (with types.MethodType)
            # Replace container's `add` method
            ##self._orig_add = self.container.add
            ##self.container.add = partial(self.__add, self) # type: ignore
            ##self.add = partial(self.__add, container_self=self.container) # type: ignore
            #self._orig_add = self.container.add
            #self.container.add = partial(_TorchFeatureExtractionContainerDecorator_add, self) # type: ignore
            #self.add = partial(_TorchFeatureExtractionContainerDecorator_add, self) # type: ignore

        # Note: we change the ``get_ind_features`` and ``add`` methods of ``self.container``. So it's necessary to update them here when objects of this class are unpickled
        def __setstate__(self, state):
            if '_orig_get_ind_features' in state:
                del state['_orig_get_ind_features']
            if 'get_ind_features' in state['container'].__dict__:
                del state['container'].__dict__['get_ind_features']
            #del state['_orig_add']
            #del state['container'].__dict__['add']
            self.__dict__.update(state)
            self._init_methods_hooks()


        def compute_latent(self, inds: Sequence[IndividualLike]) -> Sequence[FeaturesLike]:
            assert(len(inds) > 0)
            if self.model == None:
                self._create_default_model(inds[0])

            # Identify base scores
            base_scores = self.base_scores
            if self.base_scores == None: # Not base scores specified, use all scores (except those created through feature extraction)
                base_scores = [x for x in inds[0].scores.keys() if not x.startswith("extracted_") ]

            # Get the base scores of every individuals
            ind_scores = torch.empty(len(inds), len(base_scores)) # type: ignore
            for i, ind in enumerate(inds):
                for j, s in enumerate(base_scores): # type: ignore
                    ind_scores[i, j] = ind.scores[s] # TODO error message if individual does not have the specified score

            # Get latent representation of base scores
            self.model.eval()
            latent_scores = self.model.encoder(ind_scores).tolist() # type: ignore

            # Store latent scores into each individual
            for ls, ind in zip(latent_scores, inds):
                for j, s in enumerate(ls):
                    ind.scores[f"extracted_{id(self)}_{j}"] = s

            #print("DEBUG scores:", latent_scores)
            # Return final values
            return [Features(ls) for ls in latent_scores]


#        def __get_ind_features(self, container_self, individual: IndividualLike, *args, **kwargs) -> FeaturesLike:
#            # Extracted features are already computed. Use the stored values.
#            if f"extracted_{id(self)}_0" in individual.scores:
#                latent_scores = []
#                i = 0
#                while f"extracted_{id(self)}_{i}" in individual.scores:
#                    latent_scores.append(individual.scores[f"extracted_{id(self)}_{i}"])
#                    i += 1
#                return Features(latent_scores)
#
#            #return self.compute_latent([individual])[0]
#            # Calling ``compute_latent`` is too computationally expensive.
#            # Instead, run a similar code, but only on one individual ``individual`` rather than a sequence of individuals:
#
#            #print("DEBUG: get_ind_features", id(container_self), id(self))
#            # Create model if none exists
#            if self.model == None:
#                self._create_default_model(individual)
#                #print("DEBUG: created default model")
#            # Identify base scores
#            base_scores = self.base_scores
#            if self.base_scores == None: # Not base scores specified, use all scores (except those created through feature extraction)
#                base_scores = [x for x in individual.scores.keys() if not x.startswith("extracted_") ]
#            # Get ``individual``'s base scores
#            ind_scores = torch.empty(len(base_scores)) # type: ignore
#            for i, s in enumerate(base_scores): # type: ignore
#                ind_scores[i] = individual.scores[s] # TODO error message if individual does not have the specified score
#            # Get latent representation of base scores
#            latent_scores = self.model.encoder(ind_scores).tolist() # type: ignore
#            # Store latent scores into ``individual``
#            for i in range(len(latent_scores)):
#                individual.scores[f"extracted_{id(self)}_{i}"] = latent_scores[i]
#            #print("DEBUG scores:", latent_scores)
#            # Return final values
#            return Features(latent_scores)


        def _create_default_model(self, example_ind: IndividualLike) -> None:
            #print("############# CREATE DEFAULT MODEL ###############")
            # Identify base scores
            if self.base_scores == None: # Not base scores specified, use all scores (except those created through feature extraction)
                base_scores = [str(x) for x in example_ind.scores.keys() if not x.startswith("extracted_") ]
            else:
                base_scores = self.base_scores # type: ignore
            # Find default model parameters
            input_size = len(base_scores)
            assert(self.container.features_domain != None)
            latent_size = len(self.container.features_domain) # type: ignore
            # Set extracted scores names as the default features of the container
            self.container.features_score_names = [f"extracted_{id(self)}_{j}" for j in range(latent_size)]
            # Create simple auto-encoder as default model
            self.model = TorchAE(input_size, latent_size)


        def _get_training_inds(self) -> Sequence[IndividualLike]:
            if len(self.training_containers) > 0:
                training_cont_as_lists = [list(p) for p in self.training_containers]
                all_training_inds = [i for sublist in training_cont_as_lists for i in sublist]
                return all_training_inds
            elif len(self.parents) > 0:
                return self.all_parents_inds()
            else:
                return list(self)


        def train(self, nb_epochs: int) -> None:
            #print("###########  DEBUG: training.. ###########")
            #start_time = timer() # XXX

            training_inds = self._get_training_inds()
            assert(len(training_inds) > 0)
            assert(self.model != None)

            # Identify base scores
            if self.base_scores == None: # Not base scores specified, use all scores (except those created through feature extraction)
                base_scores: List[Any] = [x for x in training_inds[0].scores.keys() if not x.startswith("extracted_") ]
            else:
                base_scores = self.base_scores # type: ignore

            # Build dataset
            data = torch.empty(len(training_inds), len(base_scores))
            for i, ind in enumerate(training_inds):
                for j, s in enumerate(base_scores):
                    data[i,j] = ind.scores[s]
            #dataset = torch.utils.data.TensorDataset(data)
            dataloader: Any = DataLoader(data, batch_size=self.batch_size, shuffle=True) # type: ignore

            # Create criterion and optimizer
            criterion = nn.MSELoss()
            optimizer = torch.optim.Adam(self.model.parameters(), lr=self.learning_rate, weight_decay=1e-5) # type: ignore

            # Train !
            for epoch in range(nb_epochs):
                for data in dataloader:
                    d = Variable(data)
                    output = self.model(d) # type: ignore
                    loss = criterion(d, output)
                    optimizer.zero_grad()
                    loss.backward()
                    optimizer.step()
                #print(f"loss: {loss}")
            self.current_loss = loss.item()

            #elapsed = timer() - start_time # XXX
            #print(f"# Training: final loss: {loss}  elapsed: {elapsed}")


        def recompute_features_all_ind(self, update_params={}) -> None:
            #print("DEBUG: features recomputed for all inds..")
            #start_time = timer() # XXX

            training_inds = self._get_training_inds()
            self.compute_latent(training_inds)
            #elapsed = timer() - start_time # XXX
            #print(f"# Features recomputed for {len(training_inds)} inds.. Elapsed={elapsed}") # XXX
            #start_time = timer() # XXX
            self.container.update(training_inds, **update_params)
            #for i in training_inds:
            #    try:
            #        #self.container.add(i)
            #        self._orig_add(i)
            #    except Exception:
            #        pass

            #elapsed = timer() - start_time # XXX
            #print(f"# Tried adding {len(training_inds)} inds back to the container: {len(self)} added.. Elapsed={elapsed}") # XXX


        def _train_and_recompute_if_needed(self, update_params=()):
            # Train and recomputed all features if necessary
            training_inds = self._get_training_inds()
            nb_training_inds = len(training_inds)
            #print("DEBUG add !", nb_training_inds, self.training_period, self._last_training_nb_inds)
            if nb_training_inds >= self.training_period and nb_training_inds % self.training_period == 0 and nb_training_inds != self._last_training_nb_inds:
                self._last_training_nb_inds = nb_training_inds
                try:
                    self.clear() # type: ignore
                    self.train(self.nb_epochs if nb_training_inds > self.training_period else self.initial_nb_epochs)
                    self.recompute_features_all_ind(update_params)
                except Exception as e:
                    print("Training failed !")
                    traceback.print_exc()
                    raise e



        def add(self, individual: IndividualLike, raise_if_not_added_to_parents: bool = False) -> Optional[int]:
            self._train_and_recompute_if_needed()

            return self.container.add(individual, raise_if_not_added_to_parents)
#            # Add individual(s)
#            try:
#                res = self.container.add(individual, raise_if_not_added_to_parents)
#                #res = self._orig_add(individual, raise_if_not_added_to_parents)
#            #except IndexError as e:
#            #    pass
#            #except ValueError as e:
#            #    pass
#            except Exception as e:
#                print("fitness:", individual.fitness, individual.fitness.valid)
#                print("features", individual.features)
#                print("scores", individual.scores)
#                print("get_ind_features", self.get_ind_features(individual))
#                traceback.print_exc()
#                raise e
#            return res

        def update(self, iterable: Iterable, ignore_exceptions: bool = True, issue_warning: bool = False) -> int:
            self._train_and_recompute_if_needed({'ignore_exceptions': ignore_exceptions, 'issue_warning': issue_warning})
            #return super().update(iterable, ignore_exceptions, issue_warning)
            res = self.container.update(iterable, ignore_exceptions, issue_warning)
            return res




except ImportError:
    class TorchAE():
        def __init__(self, *args, **kwargs):
            raise NotImplementedError("`TorchAE` needs the 'torch' package to be installed and importable.")

    @registry.register # type: ignore
    class TorchFeatureExtractionContainerDecorator(ContainerDecorator): # type: ignore
        def __init__(self, *args, **kwargs):
            raise NotImplementedError("`TorchFeatureExtractionContainerDecorator` needs the 'torch' package to be installed and importable.")




## MODELINE	"{{{1
## vim:expandtab:softtabstop=4:shiftwidth=4:fileencoding=utf-8
## vim:foldmethod=marker
