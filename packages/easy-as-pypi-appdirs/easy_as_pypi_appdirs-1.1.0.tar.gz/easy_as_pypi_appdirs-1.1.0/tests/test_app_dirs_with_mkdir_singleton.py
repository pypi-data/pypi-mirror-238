# This file exists within 'easy-as-pypi-appdirs':
#
#   https://github.com/doblabs/easy-as-pypi-appdirs#🛣
#
# Copyright © 2018-2020 Landon Bouma. All rights reserved.
#
# Permission is hereby granted,  free of charge,  to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge,  publish,  distribute, sublicense,
# and/or  sell copies  of the Software,  and to permit persons  to whom the
# Software  is  furnished  to do so,  subject  to  the following conditions:
#
# The  above  copyright  notice  and  this  permission  notice  shall  be
# included  in  all  copies  or  substantial  portions  of  the  Software.
#
# THE  SOFTWARE  IS  PROVIDED  "AS IS",  WITHOUT  WARRANTY  OF ANY KIND,
# EXPRESS OR IMPLIED,  INCLUDING  BUT NOT LIMITED  TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE  FOR ANY
# CLAIM,  DAMAGES OR OTHER LIABILITY,  WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE,  ARISING FROM,  OUT OF  OR IN  CONNECTION WITH THE
# SOFTWARE   OR   THE   USE   OR   OTHER   DEALINGS  IN   THE  SOFTWARE.

"""Tests the AppDirsWithMkdir class init branches."""

import pytest

from easy_as_pypi_appdirs import AppDirs
from easy_as_pypi_appdirs.singleton import Singleton


class FooAppDirs(AppDirs, metaclass=Singleton):
    pass


class BarAppDirs(AppDirs, metaclass=Singleton):
    pass


class TestAppDirsWithMkdirSingleton(object):

    @pytest.fixture(autouse=True)
    def resets_instances(self):
        yield  # run the test_().
        Singleton._reset_instances()

    def test_raises_on_instantiation_without_initialization(self):
        # Because other tests call register_application, must reset.
        Singleton._reset_instances()

        with pytest.raises(Exception):
            AppDirs()

    def test_raises_on_instantiation_twice_with_different_appnames(self):
        AppDirs('foo')
        with pytest.raises(Exception):
            AppDirs('bar')

    def test_returns_separate_instances_with_different_classes(self):
        foo = FooAppDirs('baz')
        bar = BarAppDirs('baz')
        assert foo is not bar

    def test_returns_same_instance_after_being_initialized(self):
        foo = AppDirs('baz')
        bar = AppDirs()
        baz = AppDirs()
        assert foo is bar
        assert bar is baz

