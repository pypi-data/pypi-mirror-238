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

"""Functions to ensure directories exist."""

import os

__all__ = (
    "must_ensure_directory_exists",
    "must_ensure_file_path_dirred",
)


def must_ensure_directory_exists(directory):
    """Ensure that the passed path to a directory exists."""
    # Note that os.makedirs raises for at least 3 good reasons:
    # - PermissionError: [Errno 13] Permission denied.
    #   For instance, `mkdir foo && chmod 550 foo && mkdir foo/bar`.
    # - FileExistsError: [Errno 17] File exists.
    #   E.g., if isdir() says False, but directory specifies file,
    #   for instance, `touch foo && mkdir foo`.
    # - NotADirectoryError: [Errno 20] Not a directory.
    #   E.g., if part of directory path is file,
    #   for instance, `touch foo && mkdir -p foo/bar`.
    if not os.path.isdir(directory):
        os.makedirs(directory)
    return directory


def must_ensure_file_path_dirred(filename):
    """Ensure parent directory for passed path exists, if not just a filename."""
    # This function assumes the path exists to the current working directory,
    # so if filename is empty or just a filename, and doesn't specify a path
    # with a directory in it, this function doesn't do anything. If it did
    # call must_ensure_directory_exists, os.makedirs raises FileNotFoundError
    # when passed the empty string.
    configfile_dir = os.path.dirname(filename)
    if configfile_dir:
        must_ensure_directory_exists(configfile_dir)
