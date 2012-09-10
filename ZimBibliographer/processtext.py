#!/usr/bin/env python
# -*- coding: utf-8 -*-

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


import re
import os.path

from libzimsciunto.utils import get_unexpanded_path

from ZimBibliographer.bibtexutils import get_filedirectory
from ZimBibliographer.bibtexutils import get_entries



def process_text(original_text, bibtex):
    """
    Core function: process the whole text
    * Track cite{} keys
    * Replace them
    * write the modified text

    original_text : 
    bibtex : bibtex

    return
    ------
    modified text
    """

    #In case of a relative path
    bibtex = os.path.expanduser(bibtex)
    basepath = os.path.dirname(bibtex)

    ###########
    # Bibtex
    ###########
    filedirectory = get_filedirectory(bibtex)
    entries_hash = get_entries(bibtex) 
    
    citecommand = re.compile('cite{([0-9a-zA-Z]+)}')

    copy_text = original_text

    keys = citecommand.findall(copy_text)

    ###########
    # Edit text
    ###########
    for key in keys:
        print(key)
        try:
            path = entries_hash[key]['file']
            if entries_hash[key]['type'] == 'article':
                pubtype = entries_hash[key]['journal']['name']
            else:
                pubtype = entries_hash[key]['type']
        except KeyError:
            print('Keyerror !')
            continue #next key

        #Jabref codes path like ":/tmp/file.pdf:PDF"
        # or ":file.pdf:PDF" or ":file.pdf:label:PDF"
        #For the second case, jabref write comments with metadata (filepath)
        #path = re.sub('^:(.*):[A-Z]+', "\\1", path)
        path = re.sub('^(?:.*):(.*):[A-Z]+', "\\1", path)

        if path.startswith('/'):
            path = get_unexpanded_path(path)
        elif path.startswith('~/'):
            pass
        else:
            if filedirectory is None:
                #TODO...
                print('filedirectory is none')
                continue #next key
            path = os.path.join(filedirectory, path) 
            path = get_unexpanded_path(path)


        #Modify the text. Use foo for bibtex data
        cite = 'cite{' + key + '}'
        internal_link = '[[' + str(path) + '|' + key + ', ' + pubtype + ']]'
        copy_text = re.sub(cite, internal_link, copy_text)

    return copy_text
