# -*- coding: utf-8 -*-

from __future__ import absolute_import

import os
from os.path import dirname, join

from cmake_test_utils import CMakeTestScripts


class Tests(CMakeTestScripts):
    base_dir = dirname(__file__)
    scripts_dir = join(base_dir, "cmake_scripts")

    tests = ["functional_utils"]
