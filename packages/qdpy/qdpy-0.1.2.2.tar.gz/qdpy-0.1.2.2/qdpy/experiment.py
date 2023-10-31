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

"""The :mod:`qdpy.experiment` module contains classes providing a standard way of performing a QD Experiment """

__all__ = ["QDExperiment"]

#from collections.abc import Iterable
#from typing import Optional, Tuple, TypeVar, Union, Any, MutableSet, Mapping, MutableMapping, Sequence, MutableSequence, Callable, Tuple
#from typing_extensions import runtime, Protocol
#import inspect

from qdpy.algorithms import *
from qdpy.containers import *
from qdpy.plots import *
from qdpy.base import *
from qdpy import tools
import qdpy

import yaml
import random
import datetime
import pathlib
import traceback
import deprecation

from typing import Optional, Tuple, List, Iterable, Iterator, Any, TypeVar, Generic, Union, Sequence, MutableSet, MutableSequence, Type, Callable, Generator, Mapping, MutableMapping, overload


class QDExperiment(object):
    def __init__(self, config_filename, parallelism_type = "concurrent", seed = None, base_config = None):
        self._loadConfig(config_filename)
        if base_config is not None:
            self.config = {**self.config, **base_config}
        self.parallelism_type = parallelism_type
        self.config['parallelism_type'] = parallelism_type
        self._init_seed(seed)
        self.reinit()

    def __getstate__(self):
        odict = self.__dict__.copy()
        del odict['algo']
        del odict['container']
        return odict


    def _loadConfig(self, config_filename):
        self.config_filename = config_filename
        self.config_name = os.path.splitext(os.path.basename(config_filename))[0]
        self.config = yaml.safe_load(open(config_filename))

    def set_defaultconfig_entry(self, path, val):
        d = self.config
        for p in path[:-1]:
            d = d[p]
        insert_dict(d, path[-1], val)


    def _get_features_list(self):
        fitness_list = []
        assert not ('fitness_list' in self.config and 'fitness_type' in self.config), f"'fitness_list' and 'fitness_type' cannot both be specified at the same time."
        if 'fitness_type' in self.config:
            fitness_list.append(self.config['fitness_type'])
        elif 'fitness_list' in self.config:
            fitness_list += self.config['fitness_list']

        features_list = []
        assert not ('features_list' in self.config and 'feature_type' in self.config), f"'features_list' and 'feature_type' cannot both be specified at the same time."
        if 'feature_type' in self.config:
            features_list.append(self.config['feature_type'])
        elif 'features_list' in self.config:
            features_list += self.config['features_list']
        return features_list, fitness_list

    @property # type: ignore
    @deprecation.deprecated(deprecated_in="0.1.3", removed_in="0.2.0",
                        current_version=qdpy.__version__,
                        details="Use 'self.fitness_list' instead.")
    def fitness_type(self):
        return self.fitness_list[0] if len(self.fitness_list) > 0 else None

    def _define_domains(self):
        self.features_list, self.fitness_list = self._get_features_list()
        self.config['features_domain'] = []
        for feature_name in self.features_list:
            val = self.config['%s%s' % (feature_name, "Domain")]
            self.config['features_domain'] += [tuple(val)]
        self.config['fitness_domain'] = []
        for fitness_name in self.fitness_list:
            val = self.config['%s%s' % (fitness_name, "Domain")]
            self.config['fitness_domain'] += [tuple(val)]
        #self.config['fitness_domain'] = tuple(self.config['%s%s' % (self.fitness_type, "Domain")]),

    def _init_seed(self, rnd_seed = None):
        # Find random seed
        if rnd_seed is not None:
            seed = rnd_seed
        elif "seed" in self.config:
            seed = self.config["seed"]
        else:
            seed = np.random.randint(1000000)

        # Update and print seed
        np.random.seed(seed)
        random.seed(seed)
        print("Seed: %i" % seed)


    def reinit(self):
        # Name of the expe instance based on the current timestamp
        self.instance_name = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        # Identify and create result data dir
        if not self.config.get('dataDir'):
            resultsBaseDir = self.config.get('resultsBaseDir') or "./results/"
            dataDir = os.path.join(os.path.expanduser(resultsBaseDir), os.path.splitext(os.path.basename(self.config_filename))[0])
            self.config['dataDir'] = dataDir
        pathlib.Path(self.config['dataDir']).mkdir(parents=True, exist_ok=True)

        # Find the domains of the fitness and features
        self._define_domains()
        default_config = {}
        if self.config['fitness_domain'] != None and len(self.config['fitness_domain']) > 0:
            default_config["fitness_domain"] = self.config['fitness_domain']
        if self.config['features_domain'] != None and len(self.config['features_domain']) > 0:
            default_config["features_domain"] = self.config['features_domain']
        if len(self.fitness_list) > 0:
            default_config["fitness_score_names"] = self.fitness_list
        if len(self.features_list) > 0:
            default_config["features_score_names"] = self.features_list
        #print(default_config)

        # Create containers and algorithms from configuration
        factory = Factory()
        assert "containers" in self.config, f"Please specify configuration entry 'containers' containing the description of all containers."
        factory.build(self.config["containers"], default_config)
        assert "algorithms" in self.config, f"Please specify configuration entry 'algorithms' containing the description of all algorithms."
        factory.build(self.config["algorithms"])
        assert "main_algorithm_name" in self.config, f"Please specify configuration entry 'main_algorithm' containing the name of the main algorithm."
        self.algo = factory[self.config["main_algorithm_name"]]
        self.container = self.algo.container

        self.batch_mode = self.config.get('batch_mode', False)
        self.log_base_path = self.config['dataDir']

        # Create a logger to pretty-print everything and generate output data files
        self.iteration_filenames = os.path.join(self.log_base_path, "iteration-%i_" + self.instance_name + ".p")
        self.final_filename = os.path.join(self.log_base_path, "final_" + self.instance_name + ".p")
        self.save_period = self.config.get('save_period', 0)
        logger_type = self.config.get('logger_type', "tqdm").lower()
        if logger_type == "tqdm":
            self.logger = TQDMAlgorithmLogger(self.algo,
                    iteration_filenames=self.iteration_filenames, final_filename=self.final_filename, save_period=self.save_period,
                    config=self.config)
        elif logger_type == "basic":
            self.logger = AlgorithmLogger(self.algo,
                    iteration_filenames=self.iteration_filenames, final_filename=self.final_filename, save_period=self.save_period,
                    config=self.config)
        else:
            raise ValueError(f"Unknown value for `logger_type`: {logger_type}. It can be either 'tqdm' or 'basic'.")


    def run(self):
        verbose = self.config.get('verbose', False)
        send_several_suggestions_to_fn = self.config.get('send_several_suggestions_to_fn', False)
        max_nb_suggestions_per_call = self.config.get('max_nb_suggestions_per_call', 10)
        eval_fn = self.several_eval_fn if send_several_suggestions_to_fn else self.eval_fn
        # Run illumination process !
        with ParallelismManager(self.parallelism_type) as pMgr:
            best = self.algo.optimise(eval_fn, executor = pMgr.executor, batch_mode=self.batch_mode, verbose=verbose, send_several_suggestions_to_fn=send_several_suggestions_to_fn, max_nb_suggestions_per_call=max_nb_suggestions_per_call)

        print("\n------------------------\n")
        print(self.algo.summary())

        to_grid_parameters = self.config.get('to_grid_parameters', {})
        default_plots_grid(self.logger, self.log_base_path, suffix=f"-{self.instance_name}", to_grid_parameters=to_grid_parameters)
        print("\nA plot of the performance grid was saved in '%s'." % os.path.abspath(os.path.join(self.log_base_path, f"performancesGrid-{self.instance_name}.pdf")))
        print("\nA plot of the activity grid was saved in '%s'." % os.path.abspath(os.path.join(self.log_base_path, f"activityGrid-{self.instance_name}.pdf")))
        print("All results are available in the '%s' pickle file." % self.logger.final_filename)


    def _removeTmpFiles(self, fileList):
        keepTemporaryFiles = self.config.get('keepTemporaryFiles')
        if not keepTemporaryFiles:
            for f in fileList:
                try:
                    if os.path.isfile(f):
                        os.remove(f)
                    else:
                        shutil.rmtree(f)
                except:
                    pass

    def several_eval_fn(self, inds):
        res = []
        for ind in inds:
            res.append(self.eval_fn(ind))
        return res

    def eval_fn(self, ind):
        #print(ind.name)
        fitness = [np.random.uniform(x[0], x[1]) for x in self.config['fitness_domain']]
        features = [np.random.uniform(x[0], x[1]) for x in self.config['features_domain']]
        scores = {f"{i}": v for i, v in enumerate(features)}
        scores['perf'] = fitness[0]
        return fitness, features, scores


# MODELINE	"{{{1
# vim:expandtab:softtabstop=4:shiftwidth=4:fileencoding=utf-8
# vim:foldmethod=marker
