#!/usr/bin/env python

# ---------------------------------------------------------------------------
# Copyright © 2017 Brian M. Clapper
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.
# ---------------------------------------------------------------------------

import sys
from shutil import *
import os
import re

def msg(message):
    print(f'{message}')

def copy_files(path):
    for dir in ('files', 'lib', 'scripts'):
        msg(f'Upgrading "{dir}" directory.')

        if not os.path.isdir(dir):
            msg(f'Creating local "{dir}" directory.')
            os.mkdir(dir)
        else:
            msg(f'Cleaning local "{dir}" directory.')
            for f in os.listdir(dir):
                if f.startswith('.'):
                    continue
                p = os.path.join(dir, f)
                if os.path.isdir(p):
                    rmtree(p)
                else:
                    os.unlink(p)

        new_dir = os.path.join(path, dir)
        msg(f'Copying files from "{new_dir}" to local "{dir}".')
        for f in os.listdir(new_dir):
            if f.startswith('.') or f.startswith('__pycache'):
                continue
            p = os.path.join(new_dir, f)
            if os.path.isdir(p):
                msg(f'--- directory "{p}"')
                copytree(p, os.path.join(dir, f))
            else:
                msg(f'--- file "{p}"')
                copy(p, dir)

    msg('Upgrading build script.')
    copy(os.path.join(path, 'build'), '.')

    msg('Copying upgrade.py (because, why not?).')
    copy(os.path.join(path, 'upgrade.py'), '.')

def upgrade(path):
    if os.path.exists('./build'):
        msg('Running: ./build clobber')
        if os.system('./build clobber') != 0:
            sys.exit(1)

    copy_files(path)

    VERSION_PAT = re.compile(r'^\s*VERSION\s*=\s*([^\s]+)$')
    version = "unknown"
    with open('./build') as build:
        for line in build.readlines():
            m = VERSION_PAT.match(line)
            if m:
                version = m.group(1)
                break

    msg(f'Upgraded to: {version}')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.stderr.write('Usage: upgrade.py path-to-new-tools\n')
        sys.exit(1)

    upgrade(sys.argv[1])
