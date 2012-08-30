#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

def process_text(original_text, foo):
    """
    Core function: process the whole text
    * 

    original_text : 
    foo : TODO

    return
    ------
    copy_text
    """
    citecommand = re.compile('cite{[0-9a-zA-Z]+}')

    copy_text = original_text

    keys = citecommand.findall(copy_text)

    for key in keys:
        print(key)

    return copy_text
