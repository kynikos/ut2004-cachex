# UT2004 CacheX - Unreal Tournament 2004 cache extraction utility for Linux.
# Copyright (C) 2011 Dario Giovannetti <dev@dariogiovannetti.net>
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
@copyright: Copyright (C) 2011-2013 Dario Giovannetti <dev@dariogiovannetti.net>
@license: GPLv3
@version: 0.10
@date: 2013-03-26
"""

import logging

# loggingext is used indirectly in logger configuration
import loggingext

from cliargparse import config

loglevel = {'console': config.get('loglevel')[0],
                                            'file': config.get('loglevel')[1:]}

if loglevel['console'] not in ('0', '1', '2', '3'):
    loglevel['console'] = '2'
if loglevel['file'] not in ('0', '1', '2', '3'):
    loglevel['file'] = '0'
for k in loglevel:
    loglevel[k] = int(loglevel[k])

logconfig = {
    'version': 1,
    'formatters': {
        'simple': {
            'format': '%(asctime)s <%(relativeCreated)d> %(levelname)s: '
                                                                 '%(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'simplecol_cyan': {
            'format': '\033[1;36m%(levelname)s:\033[0m %(message)s'
        },
        'simplecol_info': {
            'format': '\033[1;34m::\033[0m %(message)s'
        },
        'simplecol_yellow': {
            'format': '\033[1;33m%(levelname)s:\033[0m %(message)s'
        },
        'simplecol_red': {
            'format': '\033[1;31m%(levelname)s:\033[0m %(message)s'
        },
        'simplecol_default': {
            'format': '%(levelname)s: %(message)s'
        },
        'verbose': {
            'format': '%(asctime)s <%(relativeCreated)d> [%(pathname)s '
                                      '%(lineno)d] %(levelname)s: %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'verbosecol_cyan': {
            'format': '%(relativeCreated)d [%(module)s %(lineno)d] '
                                  '\033[1;36m%(levelname)s:\033[0m %(message)s'
        },
        'verbosecol_info': {
            'format': '%(relativeCreated)d [%(module)s %(lineno)d] '
                                              '\033[1;34m::\033[0m %(message)s'
        },
        'verbosecol_yellow': {
            'format': '%(relativeCreated)d [%(module)s %(lineno)d] '
                                  '\033[1;33m%(levelname)s:\033[0m %(message)s'
        },
        'verbosecol_red': {
            'format': '%(relativeCreated)d [%(module)s %(lineno)d] '
                                  '\033[1;31m%(levelname)s:\033[0m %(message)s'
        },
        'verbosecol_default': {
            'format': '%(relativeCreated)d [%(module)s %(lineno)d] '
                                                   '%(levelname)s: %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'loggingext.StreamHandler',
            'level': ('CRITICAL', 'ERROR', 'INFO', 'DEBUG')[loglevel['console']
                                                                              ],
            'formatter': ('simplecol_default', 'simplecol_default',
                          'simplecol_default', 'verbosecol_default')[loglevel[
                                                                    'console']],
        },
        'file': {
            'class': 'loggingext.RotatingFileHandler',
            'level': ('CRITICAL', 'WARNING', 'INFO', 'DEBUG')[loglevel['file']],
            'formatter': ('simple', 'simple', 'simple', 'verbose')[loglevel[
                                                                       'file']],
            'filename': config.get('logfile'),
            'maxBytes': (1, 10000, 30000, 100000)[loglevel['file']],
            'backupCount': 1,
            'delay': (True, True, False, False)[loglevel['file']]
        },
        'null': {
            'class': 'logging.NullHandler',
            'formatters': {
                'default': 'simple'
            },
        }
    },
    'loggers': {
        'custom1': {
            'level': 'DEBUG',
            'handlers': [('null', 'console', 'console',
                           'console')[loglevel['console']],
                           ('null', 'file', 'file', 'file')[loglevel['file']]],
            'propagate': False
        }
    },
    'root': {
        'level': 'DEBUG'
    }
}

formconfig = {
    'console': {
        'debug': ('simplecol_default', 'simplecol_cyan',
                               'simplecol_cyan',
                               'verbosecol_cyan')[loglevel['console']],
        'info': ('simplecol_default', 'simplecol_info',
                               'simplecol_info',
                               'verbosecol_info')[loglevel['console']],
        'warning': ('simplecol_default', 'simplecol_yellow',
                             'simplecol_yellow',
                             'verbosecol_yellow')[loglevel['console']],
        'error': ('simplecol_default', 'simplecol_red',
               'simplecol_red', 'verbosecol_red')[loglevel['console']],
        'critical': ('simplecol_default', 'simplecol_red',
                                 'simplecol_red',
                                'verbosecol_red')[loglevel['console']],
    },
    'file': {
        'warning': ('simple', 'verbose', 'verbose',
                                          'verbose')[loglevel['file']],
        'error': ('simple', 'verbose', 'verbose',
                                          'verbose')[loglevel['file']],
        'critical': ('simple', 'verbose', 'verbose',
                                          'verbose')[loglevel['file']],
    },
}

logging.setLoggerClass(loggingext.Logger)
loggingext.dictConfig(logconfig, formconfig)

logger = logging.getLogger('custom1')
