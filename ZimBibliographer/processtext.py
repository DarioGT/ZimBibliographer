#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os.path
from ZimBibliographer.bibtexparser import BibTexParser
from ZimBibliographer.utils import get_unexpanded_path


def get_filedirectory(bibtex):
    """
    Get filedirectory from the bibfile
    (jabref)
    """
    with open(bibtex, 'r') as bibfile:
        bibtex_content = bibfile.read()
    filedirectory = re.findall('@comment{jabref-meta: fileDirectory:(.+?);}', bibtex_content, re.DOTALL)
    filedirectory = re.sub('\n', '', filedirectory[0])
    if filedirectory == []:
        return None

    return filedirectory


def get_entries(bibtex):
    """
    Return entries from the bibfile
    """
    with open(bibtex, 'r') as bibfile:
        bibliography = BibTexParser(bibfile)

    entries = bibliography.parse()[0] 
    entries_hash = {}
    for entry in entries:
        entries_hash[entry['id']] = entry
    return entries_hash


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
        internal_link = '[[' + str(path) + '|' + key + ', ' + pubtype + ']]' #FIXME
        copy_text = re.sub(cite, internal_link, copy_text)

    return copy_text
