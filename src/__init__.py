# UT2004 CacheX - Unreal Tournament 2004 cache extraction utility for Linux.
# Copyright (C) 2011-2014 Dario Giovannetti <dev@dariogiovannetti.net>
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

@author: Dario Giovannetti <dev@dariogiovannetti.net>
@license: GPLv3
@version: 0.9
"""

import sys as _sys
import shutil as _shutil
import os as _os
import re as _re
import time as _time

import consolecolors
import inputtemplate
import plural

from logger import logger
from cliargparse import config

backupsN = config.get_int('backupsN')
cachedir = config.get('cachedir')
targetdir = config.get('targetdir')

inputtemplate.automode = config.get_bool('autoinput')


class CliCode():
    reset = consolecolors.reset
    head1 = consolecolors.code('tBfG')
    arrow = consolecolors.code('tBfP')
    question = consolecolors.code('tBfY')
    error = consolecolors.code('tBfR')

clicode = CliCode()


class CacheFile:
    """A file to be moved from the cache"""
    def __init__(self, reline):
        # Retrieve file name strings
        self.cachename = ''.join((reline.group(1), '.uxx'))
        self.realname = reline.group(2)
        self.realext = reline.group(3)
        self.realpath = ''
    
    def setpath(self):
        # Set the path based on file extension, or don't move the file
        paths = {
                '.ukx': 'Animations/',
                '.ut2': 'Maps/',
                '.ogg': 'Music/',
                '.uax': 'Sounds/',
                '.usx': 'StaticMeshes/',
                '.u': 'System/',
                '.utx': 'Textures/'
                }
        if self.realext in paths:
            self.realpath = paths[self.realext]
        else:
            raise CustomError('{} extension not recognized'.format(self.realext
                                                                   ))


class CustomError(Exception):
    pass


def main():
    try:
        _os.chdir(cachedir)
    except EnvironmentError as e:
        logger.critical('Cannot enter {} ({})'.format(e.filename, e.strerror))
        _sys.exit(1)

    if not _os.path.isdir(targetdir):
        logger.critical('Cannot find {} (check targetdir variable)'.format(
                                                                    targetdir))
        _sys.exit(1)

    try:
        cacheini = open('cache.ini', 'r')
    except EnvironmentError as e:
        logger.critical('Cannot open {} ({})'.format(e.filename, e.strerror))
        _sys.exit(1)
    else:
        with cacheini:
            print('{}=== PREVIEW ==={reset}'.format(clicode.head1,
                                                          reset=clicode.reset))
            
            movelist, dontmovelist = [], []
            
            for line in cacheini:
                dontmove = False
                
                reline = _re.match(
                          '^([0-9A-Z]{32}-[0-9]+)(?:\=)(.+)(\.\w{1,3})(?:\n)$',
                          line)
                if reline:
                    utfile = CacheFile(reline)
                    
                    try:
                        utfile.setpath()
                    except CustomError as e:
                        logger.warning('{} extension has not been '
                                       'recognized, {} will be left in the '
                                       'cache'.format(utfile.realext,
                                                      utfile.cachename))
                        dontmove = True
                    else:
                        if not _os.path.isfile(utfile.cachename):
                            logger.warning('{} does not exist in the cache, '
                                         'its line will be left in cache.ini, '
                                         'but you should probably delete it '
                                         'manually'.format(utfile.cachename))
                            dontmove = True
                        
                        elif _os.path.isfile(_os.path.join(targetdir,
                                                           utfile.realpath,
                                                           utfile.realname +
                                                           utfile.realext)):
                            logger.warning('{} already exists, {} will be '
                                           'left in the cache'.format(
                                                       _os.path.join(targetdir,
                                                              utfile.realpath,
                                                              utfile.realname +
                                                              utfile.realext),
                                                       utfile.cachename))
                            dontmove = True
                
                else:
                    if not _re.match('^(\[Cache\]|\n)', line):
                        line = line.rstrip()
                        logger.warning('"{}" cannot be recognized, it will be '
                                              'left in cache.ini'.format(line))
                    dontmove = True
                
                if dontmove:
                    if not _re.match('^\n', line):
                        dontmovelist.append(line)
                else:
                    movelist.append((utfile.cachename,
                                     _os.path.join(targetdir, utfile.realpath),
                                     _os.path.join(targetdir, utfile.realpath,
                                      utfile.realname + utfile.realext), line))
                    print(utfile.cachename, _os.path.join(targetdir,
                            utfile.realpath, utfile.realname + utfile.realext),
                          sep=' {}-->{reset} '.format(clicode.arrow,
                                                      reset=clicode.reset))

    if len(movelist) == 0:
        logger.info('There are no files to move')
        _sys.exit()  # If writing a message here, the return status would be 1

    question = inputtemplate.InputTemplate(
        prompt='{}Do you want to move the file{P0s}? '
                          '[y|n]{reset} '.format(clicode.question,
                          reset=clicode.reset, **plural.set((len(movelist),))),
        inputs={
            'yes': ('y', 'yes'),
            'no': ('n', 'no')
        },
        auto='yes',
        wrong='Invalid input, please try again'
    )
    logger.debug('Do you want to move the file(s)? {}'.format(question.string))
    if question.group == 'no':
        logger.info('No changes were made')
        _sys.exit()  # If writing a message here, the return status would be 1
    elif question.group == 'yes':
        try:
            if _os.path.isfile('cache.ini.tmp'):
                logger.warning('Overwriting existing cache.ini.tmp')
                open('cache.ini.tmp', 'w').close()
            ftmp = open('cache.ini.tmp', 'a')
        except EnvironmentError as e:
            logger.critical('Cannot open {} ({})'.format(e.filename,
                                                         e.strerror))
            _sys.exit(1)
        else:
            with ftmp:
                moves = 0
                errors = 0
                
                for cache_file in movelist:
                    try:
                        if not _os.path.isdir(cache_file[1]):
                            _os.mkdir(cache_file[1])
                            _os.chmod(cache_file[1], 0o755)
                            logger.debug('{} directory created'.format(
                                                                cache_file[1]))
                    except EnvironmentError as e:
                        logger.error('Cannot create {} directory '
                                     '({})'.format(e.filename, e.strerror))
                        dontmovelist.append(cache_file[3])
                        errors += 1
                    else:
                        try:
                            _shutil.move(cache_file[0], cache_file[2])
                        except EnvironmentError as e:
                            logger.error('Cannot move {} to {} ({})'.format(
                                     cache_file[0], cache_file[2], e.strerror))
                            dontmovelist.append(cache_file[3])
                            errors += 1
                        else:
                            logger.debug('{} moved to {}'.format(cache_file[0],
                                                                cache_file[2]))
                            moves += 1
                
                for line in dontmovelist:
                    ftmp.write(line)
        
        filesmoved = '{} file{P0s} moved'.format(moves, **plural.set((moves,)))
        if errors > 0:
            filesmoved += ' ({} {}ERROR{reset}{P0s} reported)'.format(errors,
                                            clicode.error, reset=clicode.reset,
                                            **plural.set((errors,)))
        logger.info(filesmoved)
        
        if moves > 0:
            bkpext = _time.strftime('%Y%m%d%H%M%S')
            while _os.path.isfile('cache.ini.bak.' + bkpext):
                bkpext = repr(int(bkpext) + 1)
            
            try:
                _shutil.copy('cache.ini', 'cache.ini.bak.' + bkpext)
            except EnvironmentError:
                logger.critical('Couldn\'t create a backup for cache.ini, '
                                'to complete the operations you have to '
                                'overwrite it manually with cache.ini.tmp '
                                '(which is the updated version)')
                raise
            else:
                logger.info('cache.ini backup successfully created')
                
                cachelist = _os.listdir('.')
                datelist = []
                for f in cachelist:
                    redate = _re.match('^(?:cache\.ini\.bak\.)([0-9]{14})$', f)
                    if redate:
                        datelist.append(redate.group(1))
                datelist.sort(reverse=True)
                if backupsN >= 0:
                    for d in datelist[backupsN:]:
                        try:
                            _os.remove('cache.ini.bak.' + d)
                        except EnvironmentError as e:
                            logger.error('Couldn\'t delete obsolete '
                                         'backup: {} ({})'.format(e.filename,
                                                                  e.strerror))

                try:
                    _shutil.move('cache.ini.tmp', 'cache.ini')
                except EnvironmentError:
                    logger.critical('Couldn\' t overwrite cache.ini (the '
                                    'old version) with cache.ini.tmp (the '
                                    'updated version), please do it manually')
                    raise
                else:
                    logger.info('cache.ini correctly updated')
        else:
            try:
                _os.remove('cache.ini.tmp')
            except EnvironmentError as e:
                logger.error('Couldn\'t delete {} ({})'.format(e.filename,
                                                               e.strerror))

if __name__ == '__main__':
    main()
