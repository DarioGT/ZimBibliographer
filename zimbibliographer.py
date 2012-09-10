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
import argparse

import logging


#our lib...
from libzimsciunto import zimnotes
from libzimsciunto import utils

from ZimBibliographer import info

#############
# Main
#############

if __name__ == '__main__':


    parser = argparse.ArgumentParser(description=info.SHORT_DESCRIPTION,
                     epilog='')

    parser.add_argument('--version', action='version', version=info.NAME + ' ' + info.VERSION) 
    parser.add_argument('zimroot', help='Zim Notes directory', metavar='DIR')
    parser.add_argument('-b', help='Bibtex', metavar='BIBTEX')
    parser.add_argument('-f', help='Zim Notes file', metavar='FILE')
    parser.add_argument('--notimecheck', help='No timecheck', action='store_true') 
    #TODO LOG
    #parser.add_argument('--log', help='log') #FIXME no option
    #        #logging.basicConfig(filename=log_filename, filemode='w', level=logging.DEBUG)

    args = parser.parse_args()



    try:
        os.makedirs(os.path.expanduser('~/.zimbibliographer'), exist_ok=True)
    except:
        print('Impossible to create ~/.zimbibliographer/, Exiting...')
        sys.exit(2)

    lock_file = '~/.zimbibliographer/zimbibliographer.lock'

    utils.create_pidfile(lock_file)

    log_filename = os.path.expanduser('~/.zimbibliographer/zimbibliographer.log')
    logging.basicConfig(filename=log_filename, filemode='w', level=logging.DEBUG)

    
        
    if args.f == None: 
        zim_files = zimnotes.get_zim_files(args.zimroot)
    else:
        zim_files = [args.f]
    

    logging.info('Processing zim files')
    from ZimBibliographer.processtext import process_text
    from libzimsciunto.timechecker import TimeChecker
    
    timechecker = TimeChecker('~/.zimbibliographer/time.db', args.zimroot)
   
    #FIXME: last arg: accept a list of bibfiles
    zimnotes.process_zim_file(timechecker, args.zimroot, zim_files, process_text, args.notimecheck, 4, args.b ) 


    utils.release_pidfile(lock_file)
