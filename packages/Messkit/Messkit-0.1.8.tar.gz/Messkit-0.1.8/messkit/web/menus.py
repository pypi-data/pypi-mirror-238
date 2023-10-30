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
Web Menus
"""

from tailbone import menus as base


class MesskitMenuHandler(base.MenuHandler):
    """
    Messkit menu handler
    """

    def make_menus(self, request, **kwargs):

        people_menu = {
            'title': "People",
            'type': 'menu',
            'items': [
                {
                    'title': "All People",
                    'route': 'people',
                    'perm': 'people.list',
                },
            ],
        }

        reports_menu = self.make_reports_menu(request, include_poser=True)

        admin_menu = self.make_admin_menu(request, include_stores=False)

        menus = [
            people_menu,
            reports_menu,
            admin_menu,
        ]

        return menus
