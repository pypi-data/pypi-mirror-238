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


"""TODO"""

#from qdpy import algorithms, containers, plots
#from qdpy.base import ParallelismManager


import pathlib
import runpy
import sys
import pytest
import os

scripts = list(
          set(pathlib.Path(__file__, '..', 'bipedal_walker').resolve().glob('*bipedal_walker*.py'))
        | set(pathlib.Path(__file__, '..').resolve().glob('*rastrigin*.py'))
        | set(pathlib.Path(__file__, '..').resolve().glob('*eval*.py'))
        ) 


@pytest.mark.parametrize('script', scripts)
def test_script_execution(script):
    os.chdir(str(script.parent))
    sys.path.append(str(script.parent))
    sys.argv = [sys.argv[0]]
    runpy.run_path(str(script), run_name='__main__')


# MODELINE "{{{1
# vim:expandtab:softtabstop=4:shiftwidth=4:fileencoding=utf-8
# vim:foldmethod=marker
