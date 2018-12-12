#!/usr/bin/python3
# coding=utf-8
#
# Copyright © 2016 Scott Severance
# Code mixed in from Caffeine Plus and Jacob Vlijm
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''The settings module.

The only public object is the get_config() function. Everything else should be
deemed private.
'''

import json
import os
from .lib.collection import Collection
__all__ = ['get_config']
_settings_obj = None

def get_config():
    '''Creates, if necessary, and returns the settings object, ensuring that only one such object exists.'''
    global _settings_obj
    if _settings_obj:
        obj = _settings_obj
    else:
        obj = _SettingsObject()
        _settings_obj = obj
    return obj

class _SettingsObject(Collection):
    '''The class which stores settings. Don't create an instance directly.
    instead, use get_config().'''
    
    def __str__(self):
        return '===============\nSettingsObject:\n' + '\n'.join(
            f'\t{k}: {str(v)}' for k, v in self
        ) + '\n==============='
    
    def __iter__(self):
        return self.keys()
