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

"""Public fixtures."""

import os
from unittest import mock

import pytest

from easy_as_pypi_appdirs.app_dirs_with_mkdir import AppDirsWithMkdir
from easy_as_pypi_appdirs.expand_and_mkdirs import must_ensure_directory_exists

__all__ = (
    "tmp_appdirs",
    "xdg_appdirs",
    # PRIVATE:
    #  'ensure_appdir_exists',
)

# XDG_* mapping as seen in appdirs source:
#  $(virtualenvwrapper_get_site_packages_dir)/appdirs.py
APPDIRS_DIRS = (
    ("user_data", "XDG_DATA_HOME"),
    ("site_data", "XDG_DATA_DIRS"),
    ("user_config", "XDG_CONFIG_HOME"),
    ("site_config", "XDG_CONFIG_DIRS"),
    ("user_cache", "XDG_CACHE_HOME"),
    ("user_state", "XDG_STATE_HOME"),
    ("user_log", ""),  # {XDG_CACHE_HOME}/log
)


@pytest.fixture
def tmp_appdirs(mocker, tmpdir):
    """Provide mocked AppDirs whose paths share a common base tmpdir."""

    def _tmp_appdirs():
        for appdir_dir_def in APPDIRS_DIRS:
            mocker_patch_app_dirs(mocker, tmpdir, appdir_dir_def[0])

        return AppDirsWithMkdir()

    def mocker_patch_app_dirs(mocker, tmpdir, appdir_dir):
        tmp_appdir = ensure_appdir_exists(tmpdir, appdir_dir)
        pkg_path = "easy_as_pypi_appdirs.app_dirs_with_mkdir.AppDirsWithMkdir"
        prop_name = "{}_dir".format(appdir_dir)
        target = "{}.{}".format(pkg_path, prop_name)
        mocker.patch(target, new_callable=mock.PropertyMock(return_value=tmp_appdir))

    return _tmp_appdirs()


@pytest.fixture
def xdg_appdirs(mocker, tmpdir):
    """Provide mocked AppDirs whose paths use tmpdir via XDG_* environs."""

    def _xdg_appdirs():
        for appdir_dir, xdg_environ in APPDIRS_DIRS:
            environ_patch_app_dirs(mocker, tmpdir, appdir_dir, xdg_environ)

        return AppDirsWithMkdir()

    def environ_patch_app_dirs(mocker, tmpdir, appdir_dir, xdg_environ):
        if not xdg_environ:
            return

        tmp_appdir = ensure_appdir_exists(tmpdir, appdir_dir)
        mocker.patch.dict(os.environ, {xdg_environ: tmp_appdir})

    return _xdg_appdirs()


def ensure_appdir_exists(tmpdir, appdir_dir):
    tmp_appdir = os.path.join(tmpdir.mkdir(appdir_dir).strpath, "easy-as-pypi-appdirs")
    # Because mocking property, which is wrapped by @mkdir_side_effect, do same,
    # albeit preemptively. (lb): Seriously, such a smelly side effect.
    must_ensure_directory_exists(tmp_appdir)
    return tmp_appdir
