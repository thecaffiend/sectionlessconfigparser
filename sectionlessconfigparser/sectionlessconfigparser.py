# -*- coding: utf-8 -*-
"""
Config parser that handles key/value config files with no section headers.
"""

from configparser import ConfigParser
from io import StringIO

class SectionlessConfigParser(ConfigParser, object):
    # fake section header for the config file. needed so we can use the config
    # parser class python provides
    DUMMY_SECTION = "DUMMY_SECTION"

    def read_config(self, fname):
        """
        Read/parse the config file.
        """
        with open(fname) as cfg_stream:
            # some trickery.
            # want to use the built in config parser, but it wants the file to
            # be separated in '[sections]'. So, add a fake section to the whole
            # thing when read, but before sending the content stream to the
            # parser...
            # Concept found in many places such as:
            # http://stackoverflow.com/a/10746467
            hdr = "[%s]\n" % (self.DUMMY_SECTION)
            cfg_stream = StringIO(hdr + cfg_stream.read())
            self.readfp(cfg_stream)

    # TODO: rather than make a new method, change this to have same interface as
    #       'get' for configparser objects, but fill in the section
    #       automatically
    def get_val(self, option, default):
        """
        Get the value for a specified option key. Option is case-insensitive.
        There's only one section, so fill that in automatically.
        """
        return self.get(self.DUMMY_SECTION, option, fallback=default)

    def items(self):
        """
        Get a list of all (key, value) tuples in the config file
        """
        return super(SectionlessConfigParser, self).items(self.DUMMY_SECTION)
