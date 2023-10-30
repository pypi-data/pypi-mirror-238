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
Messkit commands
"""

import os
import sys
import subprocess

from rattail import commands

from messkit import __version__


def main(*args):
    """
    Main entry point for Messkit command system
    """
    args = list(args or sys.argv[1:])
    cmd = Command()
    cmd.run(*args)


class Command(commands.Command):
    """
    Main command for Messkit
    """
    name = 'messkit'
    version = __version__
    description = "Messkit (Generic Data App)"
    long_description = ''


class Install(commands.InstallSubcommand):
    """
    Install the Messkit app
    """
    name = 'install'
    description = __doc__.strip()

    # nb. these must be explicitly set b/c config is not available
    # when running normally, e.g. `messkit -n install`
    app_title = "Messkit"
    app_package = 'messkit'
    app_eggname = 'Messkit'
    app_pypiname = 'Messkit'

    def do_install_steps(self):

        # first all normal steps
        super(Install, self).do_install_steps()

        # we also install poser..for now..?
        self.install_poser()

    def put_settings(self, **kwargs):

        rattail = [os.path.join(sys.prefix, 'bin', 'rattail'),
                   '-c', os.path.join(sys.prefix, 'app', 'silent.conf')]

        # set falafel theme
        cmd = rattail + ['setting-put', 'tailbone.theme', 'falafel']
        subprocess.check_call(cmd)

        # hide theme picker
        cmd = rattail + ['setting-put', 'tailbone.themes.expose_picker', 'false']
        subprocess.check_call(cmd)

        # set main image
        cmd = rattail + ['setting-put', 'tailbone.main_image_url', '/messkit/img/messkit.png']
        subprocess.check_call(cmd)

        # set header image
        cmd = rattail + ['setting-put', 'tailbone.header_image_url', '/messkit/img/messkit-small.png']
        subprocess.check_call(cmd)

        # set favicon image
        cmd = rattail + ['setting-put', 'tailbone.favicon_url', '/messkit/img/messkit-small.png']
        subprocess.check_call(cmd)

        # set default grid page size
        cmd = rattail + ['setting-put', 'tailbone.grid.default_pagesize', '20']
        subprocess.check_call(cmd)

    def install_poser(self):
        if not self.basic_prompt("make poser dir?", True, is_bool=True):
            return False

        self.rprint()

        # make poser dir
        poser_handler = self.app.get_poser_handler()
        poserdir = poser_handler.make_poser_dir()

        self.rprint("\n\tposer dir created:  [bold green]{}[/bold green]".format(
            poserdir))
        return True
