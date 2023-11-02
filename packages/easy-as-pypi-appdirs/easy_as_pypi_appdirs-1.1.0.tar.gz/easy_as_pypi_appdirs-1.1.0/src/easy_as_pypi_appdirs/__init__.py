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

"""Top-level package for this CLI-based application."""

# Convenience import(s).

import appdirs  # noqa: F401

from .app_dirs import register_application  # noqa: F401
from .app_dirs_with_mkdir import AppDirsWithMkdir as AppDirs  # noqa: F401
from .exists_or_mkdirs import (  # noqa: F401
    must_ensure_directory_exists,
    must_ensure_file_path_dirred,
)
from .expand_and_mkdirs import must_ensure_appdirs_path  # noqa: F401

# This version value is substituted on poetry-build. See pyproject.toml:
#   [tool.poetry-dynamic-versioning.substitution]
# - So when installed in 'editable' mode, the substitution does not happen,
#   and __version__ remains "".
#   - But we only use __version__ for .github/workflows/release-smoke-test.yml
#     and not for anything else (otherwise we could check Git tags when
#     __version__ == "", if we assume an 'editable' mode install only happens
#     on a dev machine).
__version__ = "1.1.0"
