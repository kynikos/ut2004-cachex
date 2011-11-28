# UT2004 CacheX - Unreal Tournament 2004 cache extraction utility for Linux.
# Copyright (C) 2011 Dario Giovannetti <dev@dariogiovannetti.com>
#
# This file is part of UT2004 CacheX.
#
# UT2004 CacheX is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# UT2004 CacheX is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with UT2004 CacheX.  If not, see <http://www.gnu.org/licenses/>.

"""
UT2004 CacheX - This script moves the downloaded Unreal Tournament 2004 *.uxx
cache files from the specified Cache directory to the corresponding ut2004
subdirectories, renaming them with their real name.

@author: Dario Giovannetti
@copyright: Copyright (C) 2011 Dario Giovannetti <dev@dariogiovannetti.com>
@license: GPLv3
@version: 0.9
@date: 2011-11-28
"""

import argparse
import os
import sys

import configfile


class ShowVersion(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        print('''UT2004 CacheX 0.9 (2011-11-28)

Copyright (C) 2011 Dario Giovannetti <dev@dariogiovannetti.com>
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, you are welcome to redistribute it under the
conditions of the GNU General Public License version 3 or later.
See <http://gnu.org/licenses/gpl.html> for details.''')
        sys.exit()

config = configfile.ConfigFile(
    {
        # Any change to the default values here must be reflected in the help
        # descriptions of the add_argument's below
        'backupsN': '5',
        'cachedir': os.getenv('HOME') + '/.ut2004/Cache/',
        'configfile': 'utcachex.conf',
        'loglevel': '20',
        'logfile': 'utcachex.log',
        'targetdir': os.getenv('HOME') + '/.ut2004/',
    }
)

# Options -h and --help are automatically created
cliparser = argparse.ArgumentParser(
    description='Unreal Tournament 2004 cache extraction utility for Linux.'
)
cliparser.add_argument(
    '--auto',
    action='store_true',
    dest='autoinput',
    help='enable auto-input mode: all user input requests will be '
         'auto-answered with preset values always aimed at continuing '
         'operations; BEWARE, this won\'t give any possibility to cancel any '
         'operation'
)
cliparser.add_argument(
    '-b',
    '--backups',
    # Let this default to None
    type=int,
    metavar='N',
    dest='backupsN',
    help='keep only the latest %(metavar)s cache.ini backups; if set to 0, '
         'all existing backups will be deleted and none will be created; '
         'if set to -1, all backups will be kept (default: 5)'
)
cliparser.add_argument(
    '-c',
    '--cache',
    # Let this default to None
    metavar='PATH',
    dest='cachedir',
    help='set the cache folder to %(metavar)s: this is where the downloaded '
         'files and the cache.ini file are (default: ~/.ut2004/Cache/)'
)
cliparser.add_argument(
    '-o',
    '--config',
    # Let this default to None
    metavar='FILE',
    dest='configfile',
    help='set the configuration file name: a relative or full path can be '
         'specified (default: ./utcachex.conf)'
)
cliparser.add_argument(
    '-l',
    '--loglevel',
    # Let this default to None
    metavar='NN',
    dest='loglevel',
    help='a 2-digit number (in base 4, from 00 to 33) whose digits define the '
         'verbosity of, respectively, stdout and file log messages; '
         '0) disabled; 1) essential reports; 2) normal verbosity; '
         '3) debug mode; digits different from 0,1,2,3 will be converted to 3 '
         '(default: 20, see also --logfile option)'
)
cliparser.add_argument(
    '-f',
    '--logfile',
    # Let this default to None
    metavar='FILE',
    dest='logfile',
    help='set the log file name: a relative or full path can be specified '
         '(default: ./utcachex.log, see also --loglevel option)'
)
cliparser.add_argument(
    '-t',
    '--target',
    # Let this default to None
    metavar='PATH',
    dest='targetdir',
    help='set the target folder to %(metavar)s: this is where Maps, System, '
         'Textures... folders are (default: ~/.ut2004/)'
)
cliparser.add_argument(
    '-v',
    '--version',
    action=ShowVersion,
    nargs=0,
    dest='version',
    help='show program\'s version number, copyright and license information, '
         'then exit'
)
cliargs = cliparser.parse_args()

if cliargs.configfile == None and os.path.isfile(config.get('configfile')):
    config.update(config.get('configfile'))
elif cliargs.configfile != None:
    config.update(cliargs.configfile)

config['autoinput'] = str(cliargs.autoinput)
if cliargs.backupsN != None:
    config['backupsN'] = str(cliargs.backupsN)
if cliargs.cachedir != None:
    config['cachedir'] = cliargs.cachedir
if cliargs.loglevel != None:
    config['loglevel'] = cliargs.loglevel
if cliargs.logfile != None:
    config['logfile'] = cliargs.logfile
if cliargs.targetdir != None:
    config['targetdir'] = cliargs.targetdir
