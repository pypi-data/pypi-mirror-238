# -*- coding: utf-8; -*-
######################################################################
#
#  Messkit -- Generic-ish Data Utility App
#  Copyright © 2022-2023 Lance Edgar
#
#  This file is part of Messkit.
#
#  Messkit is free software: you can redistribute it and/or modify it
#  under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Messkit is distributed in the hope that it will be useful, but
#  WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with Messkit.  If not, see <http://www.gnu.org/licenses/>.
#
######################################################################
"""
Config extension for Messkit
"""

import os
import sys

from rattail.config import ConfigExtension


class MesskitConfig(ConfigExtension):
    """
    Rattail config extension for Messkit
    """
    key = 'messkit'

    def configure(self, config):

        # set some default config values
        config.setdefault('rattail', 'app_title', "Messkit")
        config.setdefault('rattail', 'app_class_prefix', 'Messkit')
        config.setdefault('rattail', 'app_table_prefix', 'messkit')
        config.setdefault('tailbone.menus', 'handler', 'messkit.web.menus:MesskitMenuHandler')
        config.setdefault('rattail', 'enum', 'messkit.enum')
        config.setdefault('rattail', 'model', 'messkit.db.model')
        # TODO: remove this when flag defaults to true
        config.setdefault('rattail.mail', 'emails.use_entry_points', 'true')
