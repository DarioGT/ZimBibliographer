#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os.path
from ZimBibliographer.bibtexparser import BibTexParser

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
    with open(bibtex, 'r') as bibfile:
        bibtex_content = bibfile.read()
    filedirectory = re.findall('@comment{jabref-meta: fileDirectory:(.+?);}', bibtex_content, re.DOTALL)
    filedirectory = re.sub('\n', '', filedirectory[0])

    with open(bibtex, 'r') as bibfile:
        bibliography = BibTexParser(bibfile)

    entries = bibliography.parse()[0] 
    entries_hash = {}
    for entry in entries:
        entries_hash[entry['id']] = entry

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
        except KeyError:
            print('Keyerror !')
            continue #next key

        #Jabref codes path like ":/tmp/file.pdf:PDF"
        # or ":file.pdf:PDF"
        #For the second case, jabref write comments with metadata
        path = re.sub(':(.*):[a-zA-Z]+', "\\1", path)
        #TODO deal with this second case... :(

        #TODO non expanded path is suitable
        if path.startswith('/'):
            pass
        elif path.startswith('~/'):
            pass
        else:
            path = os.path.join(filedirectory, path) 



        #TODO
        #Modify the text. Use foo for bibtex data
        cite = 'cite{' + key + '}'
        internal_link = '[[' + str(path) + ']]' #FIXME
        copy_text = re.sub(cite, internal_link, copy_text)

    return copy_text
