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

"""Tests the app_dirs_with_mkdir.py module and AppDirsWithMkdir class."""

import os
from unittest import mock

import pytest

from easy_as_pypi_appdirs import app_dirs


class TestAppDirsWithMkdir(object):
    """AppDirsWithMkdir tests."""

    @pytest.fixture(autouse=True)
    def set_app_name(self, app_name):
        self.app_name = app_name

    def _test_app_dir_returns_directoy(self, app_dirname, tmpdir, **kwargs):
        """Make sure method returns directory."""
        path = tmpdir.strpath
        with mock.patch(
            'appdirs.{}'.format(app_dirname),
            new_callable=mock.PropertyMock,
        ) as mock_app_dir:
            mock_app_dir.return_value = path

            appdir = app_dirs.register_application(self.app_name)

            assert getattr(appdir, app_dirname) == path

            kwargs['version'] = None
            mock_app_dir.assert_called_once_with(self.app_name, None, **kwargs)

    def _test_app_dir_creates_file(self, app_dirname, create, tmpdir, faker, **kwargs):
        """Make sure that path creation depends on ``create`` attribute."""
        path = os.path.join(tmpdir.strpath, '{}'.format(faker.word()))
        # We want NarkAppDirs's call to appdirs.{}_dir to return our tmp path.
        with mock.patch(
            'appdirs.{}'.format(app_dirname),
            new_callable=mock.PropertyMock,
            return_value=path,
        ) as mock_app_dir:
            appdir = app_dirs.register_application(self.app_name)
            appdir.create = create
            # FYI: When testing, if this assert fires and you're running
            # `python -m pytest --pdb`, entering e.g., `appdir.user_data_dir` at the
            # pdb prompt shows the non-mocked value! But if you capture the
            # value first and print it, it's correct. So in code you'd have:
            #   show_actual = appdir.user_data_dir
            # And in pdb you'd type:
            #   (pdb) show_actual
            #   '/tmp/pytest-of-user/pytest-1142/test_user_data_dir_creates_fil0/relationship/'
            #   (pdb) appdir.user_data_dir
            #   '/home/user/.local/share/easy-as-pypi-appdirs-tests'
            assert os.path.exists(getattr(appdir, app_dirname)) is create
            kwargs['version'] = None
            mock_app_dir.assert_called_once_with(self.app_name, None, **kwargs)

    # ***

    def test_user_data_dir_returns_directoy(self, tmpdir):
        """Make sure method returns directory."""
        self._test_app_dir_returns_directoy(
            'user_data_dir', tmpdir, roaming=False,
        )

    @pytest.mark.parametrize('create', [True, False])
    def test_user_data_dir_creates_file(self, tmpdir, faker, create):
        """Make sure that path creation depends on ``create`` attribute."""
        self._test_app_dir_creates_file(
            'user_data_dir', create, tmpdir, faker, roaming=False,
        )

    # ---

    def test_site_data_dir_returns_directoy(self, tmpdir):
        """Make sure method returns directory."""
        self._test_app_dir_returns_directoy(
            'site_data_dir', tmpdir, multipath=False,
        )

    @pytest.mark.parametrize('create', [True, False])
    def test_site_data_dir_creates_file(self, tmpdir, faker, create):
        """Make sure that path creation depends on ``create`` attribute."""
        self._test_app_dir_creates_file(
            'site_data_dir', create, tmpdir, faker, multipath=False,
        )

    # ---

    def test_user_config_dir_returns_directoy(self, tmpdir):
        """Make sure method returns directory."""
        self._test_app_dir_returns_directoy(
            'user_config_dir', tmpdir, roaming=False,
        )

    @pytest.mark.parametrize('create', [True, False])
    def test_user_config_dir_creates_file(self, tmpdir, faker, create):
        """Make sure that path creation depends on ``create`` attribute."""
        self._test_app_dir_creates_file(
            'user_config_dir', create, tmpdir, faker, roaming=False,
        )

    # ---

    def test_site_config_dir_returns_directoy(self, tmpdir):
        """Make sure method returns directory."""
        self._test_app_dir_returns_directoy(
            'site_config_dir', tmpdir, multipath=False,
        )

    @pytest.mark.parametrize('create', [True, False])
    def test_site_config_dir_creates_file(self, tmpdir, faker, create):
        """Make sure that path creation depends on ``create`` attribute."""
        self._test_app_dir_creates_file(
            'site_config_dir', create, tmpdir, faker, multipath=False,
        )

    # ---

    def test_user_cache_dir_returns_directoy(self, tmpdir):
        """Make sure method returns directory."""
        self._test_app_dir_returns_directoy('user_cache_dir', tmpdir)

    @pytest.mark.parametrize('create', [True, False])
    def test_user_cache_dir_creates_file(self, tmpdir, faker, create):
        """Make sure that path creation depends on ``create`` attribute."""
        self._test_app_dir_creates_file('user_cache_dir', create, tmpdir, faker)

    # ---

    def test_user_state_dir_returns_directoy(self, tmpdir):
        """Make sure method returns directory."""
        self._test_app_dir_returns_directoy('user_state_dir', tmpdir)

    @pytest.mark.parametrize('create', [True, False])
    def test_user_state_dir_creates_file(self, tmpdir, faker, create):
        """Make sure that path creation depends on ``create`` attribute."""
        self._test_app_dir_creates_file('user_state_dir', create, tmpdir, faker)

    # ---

    def test_user_log_dir_returns_directoy(self, tmpdir):
        """Make sure method returns directory."""
        self._test_app_dir_returns_directoy('user_log_dir', tmpdir)

    @pytest.mark.parametrize('create', [True, False])
    def test_user_log_dir_creates_file(self, tmpdir, faker, create):
        """Make sure that path creation depends on ``create`` attribute."""
        self._test_app_dir_creates_file('user_log_dir', create, tmpdir, faker)

