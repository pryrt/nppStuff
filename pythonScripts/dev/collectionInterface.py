# encoding=utf-8
"""collectionInterface

This provides an interface to the official UserDefinedLanguage Collection and nppThemes Collection.

The end goal is a GUI which allows selecting one or more UDL, autoCompletion, and/or theme files, which would then
be downloaded and installed in the correct location, and Notepad++ automatically restarted

I am going to have to start learning Eko's [WinDialog](https://github.com/Ekopalypse/NppPythonScripts/tree/master/helper/WinDialog) library

"""
from Npp import *
import urllib2  # .urlopen() returns stream
import json     # .load(f) => load from stream; .loads(s) => load from string; .dump(o) => dump to stream; .dumps(o) => dump to string

class CollectionInterface(object):
    """Provides an interface to the UserDefinedlanguage Collection and nppThemes Collection.

    Use this to list or download a specific UDL, autoCompletion, or Theme from the Collections.
    """
    def __init__(self):
        """Instantiation"""

        # grab the udl-list.json -- as of the 2023-Nov-06 update to the repo,
        #   this now contains both UDL and autoCompletion info, to avoid
        f = urllib2.urlopen("https://raw.githubusercontent.com/notepad-plus-plus/userDefinedLanguages/master/udl-list.json")
        o = json.load(f)
        self._udls = o['UDLs']
        #   TODO: maybe restructure the local JSON so that it's key/object pairs rather than a list of anonymous objects

        # grab the nppThemes table-of-contents JSON (new as of 2023-Nov-06)
        f = urllib2.urlopen("https://raw.githubusercontent.com/notepad-plus-plus/nppThemes/master/themes/.toc.json")
        self._themes = json.load(f)

    def list_themes(self):
        """returns a list of theme names"""
        return self._themes

    def list_udls(self):
        """returns a list of strings"""
        retval = []
        for o in sorted(self._udls, key=lambda d: d['display-name'].lower()):
            s = u'[{}]({}) => {}\n'.format(
                o['display-name'],
                o['id-name'] + ".xml",
                o['description']
            )
            # console.write(s)
            retval.append(s)
        return retval

    def download_theme(theme_file_name):
        """grab the specified theme

        theme_file_name should include the .xml extension (eg: 'blah.xml')
        the tool will automatically create the URL, including the themes subdirectory ('.../themes/blah.xml')
        """
        pass

    def download_udl(udl_id = None, udl_display_name = None):
        """grab the specified UDL

        can be specified by udl_id (based on o['id-name'])
        or specified by udl_display_name (based on o['display-name'])
        """
        pass

console.clear();
collectionInterface = CollectionInterface()
console.write(json.dumps({ "UDLs": collectionInterface.list_udls() , "nppThemes": collectionInterface.list_themes()}, sort_keys=True, indent=2, separators=(',',':')))
console.write("\n")
del(collectionInterface)
