#!/usr/bin/env python
# -*- coding: utf-8 -*-

import configparser
import os


class ConfigBibtex():
    """
    Load bitex files from configuration files
    :param name: name of the configuration
    :param location: path of the config directory
    """
    def __init__(self, name='bibtex.conf', location='~/.zimbibliographer'):
        filename = str(name)
        filepath = os.path.join(os.path.expanduser(location), filename)

        self.config = configparser.ConfigParser()
        self.config.read(filepath)

    def get_bibtex_paths(self):
        """
        Get a list containing paths of bibtex files
        """
        paths = []
        for section in self.config.sections():
            path = os.path.expanduser(self.config[section].get('path'))
            paths.append(path)
        return paths

