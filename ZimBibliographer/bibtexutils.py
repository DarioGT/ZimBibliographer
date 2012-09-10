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
    if filedirectory == []:
        return None
    filedirectory = re.sub('\n', '', filedirectory[0])

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
