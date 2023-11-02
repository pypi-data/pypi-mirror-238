# This file exists within 'easy-as-pypi-config':
#
#   https://github.com/tallybark/easy-as-pypi-config#🍐
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

"""Singleton metaclass."""

__all__ = ("Singleton",)


class Singleton(type):
    """A Singleton metaclass.

    For a healthy discussion on ways to implement Singleton in Python,
    and whether or not they're a good tool to use, read the long-standing
    and still-rolling *Creating a singleton in Python* article:

        https://stackoverflow.com/questions/6760685/creating-a-singleton-in-python
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """Return Singleton for specified class and optional arguments.

        Creates Singleton if necessary, or verifies specified arguments
        match previously-created Singleton for the same arguments.
        """
        fresh_cls = cls not in cls._instances
        if fresh_cls or args or kwargs:
            new_instance = super(Singleton, cls).__call__(*args, **kwargs)

        if fresh_cls:
            cls_instance = new_instance
            cls._instances[cls] = cls_instance
        else:
            cls_instance = cls._instances[cls]

        if (args or kwargs) and (new_instance != cls_instance):
            raise Exception("DEV: Singleton initialized again but differently")

        return cls_instance

    @classmethod
    def _reset_instances(cls):
        cls._instances = {}
