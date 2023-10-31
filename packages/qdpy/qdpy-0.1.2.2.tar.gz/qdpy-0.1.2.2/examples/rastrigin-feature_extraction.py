#!/usr/bin/env python3
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


"""An example illustrating how QD algorithms can automatically discover the feature descriptors of a Grid container.
Here we use a methodology similar to the AURORA algorithm (Cully2019: https://arxiv.org/pdf/1905.11874.pdf) where an autoencoder is continuously trained during the optimization process on all individuals found so far. The latent space of this autoencoder is used as the feature descriptors of the grid.
In order to achieve that, grids have to periodically recompute the feature descriptors of all individual found so far. So it implies that all individuals should be stored in additional container. This is achieved in QDpy by using hierarchies of containers, where a (child) container can forward all individuals it encounters to a parent container. Here, the child container is the main Grid, and the parent is an archive containing all individuals found so far.
See the configuration file "examples/conf/rastrigin-feature_extraction.yaml" for more details.
"""

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

from qdpy.algorithms import *
from qdpy.containers import *
from qdpy.benchmarks import *
from qdpy.base import *
from qdpy.plots import *
from qdpy import tools

import os
import numpy as np
import random
from functools import partial
import yaml
import torch



if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--seed', type=int, default=None, help="Numpy random seed")
    parser.add_argument('-p', '--parallelismType', type=str, default='none', help = "Type of parallelism to use (none, concurrent, scoop)")
    parser.add_argument('-c', '--configFile', type=str, default='conf/rastrigin-feature_extraction-pytorch.yaml', help = "Path of the configuration file")
    parser.add_argument('-o', '--outputDir', type=str, default=None, help = "Path of the output log files")
    parser.add_argument('-v', '--verbose', default=False, action='store_true', help = "Enable verbose mode")
    args = parser.parse_args()


    # Retrieve configuration from configFile
    config = yaml.safe_load(open(args.configFile))
    print("Retrieved configuration:")
    print(config)
    print("\n------------------------\n")

    # Find where to put logs
    log_base_path = config.get("log_base_path", ".") if args.outputDir is None else args.outputDir

    # Find random seed
    if args.seed is not None:
        seed = args.seed
    elif "seed" in config:
        seed = config["seed"]
    else:
        seed = np.random.randint(1000000)

    # Update and print seed
    np.random.seed(seed)
    random.seed(seed)
    print("Seed: %i" % seed)
    # Update torch seed
    torch.manual_seed(seed)


    # Create containers and algorithms from configuration 
    factory = Factory()
    assert "containers" in config, f"Please specify configuration entry 'containers' containing the description of all containers."
    factory.build(config["containers"])
    assert "algorithms" in config, f"Please specify configuration entry 'algorithms' containing the description of all algorithms."
    factory.build(config["algorithms"])
    assert "main_algorithm_name" in config, f"Please specify configuration entry 'main_algorithm' containing the name of the main algorithm."
    algo = factory[config["main_algorithm_name"]]
    container = algo.container

    # Define evaluation function
    eval_fn = partial(illumination_rastrigin_normalised, nb_features = 4)

    # Create a logger to pretty-print everything and generate output data files
    logger = TQDMAlgorithmLogger(algo, log_base_path=log_base_path, config=config)
    stat_loss = LoggerStat("loss", lambda algo: f"{algo.container.current_loss:.4f}", True)
    stat_training = LoggerStat("training_size", lambda algo: f"{len(algo.container._get_training_inds())}", True)
    logger.register_stat(stat_loss, stat_training)

    # Run illumination process !
    with ParallelismManager(args.parallelismType) as pMgr:
        best = algo.optimise(eval_fn, executor = pMgr.executor, batch_mode=False, verbose=args.verbose) # Disable batch_mode (steady-state mode) to ask/tell new individuals without waiting the completion of each batch


    # Print results info
    print("\n------------------------\n")
    print(algo.summary())

    # Plot the results
    default_plots_grid(logger)

    print("All results are available in the '%s' pickle file." % logger.final_filename)
    print(f"""
To open it, you can use the following python code:
    import pickle
    # You may want to import your own packages if the pickle file contains custom objects

    with open("{logger.final_filename}", "rb") as f:
        data = pickle.load(f)
    # ``data`` is now a dictionary containing all results, including the final container, all solutions, the algorithm parameters, etc.

    grid = data['container']
    print(grid.best)
    print(grid.best.fitness)
    print(grid.best.features)
    """)

# MODELINE "{{{1
# vim:expandtab:softtabstop=4:shiftwidth=4:fileencoding=utf-8
# vim:foldmethod=marker
