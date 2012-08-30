#!/usr/bin/env python

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>
#
# Author: Francois Boulogne <fboulogne at sciunto dot org>, 2012

#System...
import sys
import os
import getopt

import logging


#our lib...
from ZimBibliographer import zimnotes
from ZimBibliographer import utils
#from ZimArchivist import timechecker
#from ZimArchivist import archive



#############
# Main
#############

#FIXME
def usage():
    """ Print usage... """
    usage = """
    zimarchivist --cache -d ~/Notes

    Actions:
        --cache: make a cache
        Arg: 
            -d: Zim notes directory
        Option:
            -f: Zim file path (Otherwise, the notebook is processed)


        --clean: clean the cache by removing unnecessary archives
        Arg: 
            -d: Zim notes directory

     Other options:
        --no-timecheck: Do not check if zim file has been modified
                        since the last time.
    """

    print(usage)


if __name__ == '__main__':
    try:
        os.makedirs(os.path.expanduser('~/.zimbibliographer'), exist_ok=True)
    except:
        print('Impossible to create ~/.zimbibliographer/, Exiting...')
        sys.exit(2)

    lock_file = '~/.zimbibliographer/zimbibliographer.lock'

    utils.create_pidfile(lock_file)

    log_filename = os.path.expanduser('~/.zimbibliographer/zimbibliographer.log')
    logging.basicConfig(filename=log_filename, filemode='w', level=logging.DEBUG)

    
    zim_root = None
    zim_archive_path = None
    zim_file_path = None
    
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hb:d:f:", ['help'])
    except getopt.GetoptError:
        logging.critical('Wrong option')
        usage() 
        sys.exit(2)

        
    checktime = True
    
    #FIXME : review args...
    for opt, arg in opts:   
        if opt in ('-h', '--help'):
            logging.debug("Option -h")
            usage()
            sys.exit(0)
        elif opt in '--log':
            pass
            #TODO
            #logging.basicConfig(filename=log_filename, filemode='w', level=logging.DEBUG)
        elif opt in '--no-timecheck':
            logging.debug("Option --no-timecheck")
            checktime = False
        elif opt in '-b':
            logging.debug("Option -b: " + str(arg))
            bibfile = os.path.realpath(arg) 
        elif opt in '-d':
            logging.debug("Option -d: " + str(arg))
            zim_root = os.path.realpath(arg) 
        elif opt in '-f':
            logging.debug("Option -f: " + str(arg))
            zim_file_path = os.path.realpath(arg) 


        
    if zim_file_path == None: 
        zim_files = zimnotes.get_zim_files(zim_root)
    else:
        zim_files = [zim_file_path]
    

    if bibfile == None:
        logging.critical('missing bibtex option')
        #TODO
        sys.exit(1)

    logging.info('Processing zim files')
    from ZimBibliographer.processtext import process_text
    from ZimBibliographer.timechecker import TimeChecker
    
    timechecker = TimeChecker('~/.zimbibliographer/time.db', zim_root)
    #remove zimroot
    zimnotes.process_zim_file(timechecker, zim_root, zim_files, process_text, checktime, 1, bibfile ) #FIXME: last arg


    utils.release_pidfile(lock_file)
