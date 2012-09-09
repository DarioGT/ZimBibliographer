#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Functions using (wrapping) bibtexparser
"""

from ZimBibliographer.bibtexparser import BibTexParser
import re

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
