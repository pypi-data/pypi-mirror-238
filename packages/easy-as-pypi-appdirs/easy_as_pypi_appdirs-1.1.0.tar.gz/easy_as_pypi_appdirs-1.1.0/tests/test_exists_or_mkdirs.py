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

"""Tests the exists_or_mkdirs.py module."""

import os

from easy_as_pypi_appdirs import (
    must_ensure_directory_exists,
    must_ensure_file_path_dirred,
)


class TestMustEnsureDirectoryExists(object):
    """must_ensure_directory_exists test(s)."""

    def test_must_ensure_directory_exists(self, tmpdir):
        ensure_this_path = os.path.join(tmpdir, 'foo')
        assert not os.path.exists(ensure_this_path)
        must_ensure_directory_exists(ensure_this_path)
        assert os.path.exists(ensure_this_path)


class TestMustEnsureFilePathDirred(object):
    """must_ensure_file_path_dirred test(s)."""

    def test_must_ensure_file_path_dirred(self, tmpdir):
        ensure_this_path = os.path.join(tmpdir, 'foo')
        ensure_this_file = os.path.join(ensure_this_path, 'bar.bat')
        assert not os.path.exists(ensure_this_path)
        must_ensure_file_path_dirred(ensure_this_file)
        assert os.path.exists(ensure_this_path)

