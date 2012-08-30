#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

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

    with open(bibtex, 'r') as bibfile:
        bibliography = BibTexParser(bibfile)

    entries = bibliography.parse()[0] 
    entries_hash = {}
    for entry in entries:
        entries_hash[entry['id']] = entry

    citecommand = re.compile('cite{([0-9a-zA-Z]+)}')

    copy_text = original_text

    keys = citecommand.findall(copy_text)

    for key in keys:
        print(key)
        print(entries_hash[key]['file'])
        #TODO
        #Modify the text. Use foo for bibtex data

    return copy_text
