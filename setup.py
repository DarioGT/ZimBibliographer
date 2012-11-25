#!/usr/bin/env python

from distutils.core import setup
from ZimBibliographer import info

setup(
    name         = 'ZimBibliographer',
    version      = info.VERSION,
    url          = info.URL,
    author       = "Francois Boulogne",
    author_email = info.EMAIL,
    license      = info.LICENSE,
    description  = info.SHORT_DESCRIPTION,
    packages     = ['ZimBibliographer'],
    scripts      = ['zimbibliographer'],
    requires     = ['libZimSciunto (>=0.3)'],
)
