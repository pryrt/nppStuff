# encoding=utf-8
"""collectionInterface

This provides an interface to the official UserDefinedLanguage Collection and nppThemes Collection.

The end goal is a GUI which allows selecting one or more UDL, autoCompletion, and/or theme files, which would then
be downloaded and installed in the correct location, and Notepad++ automatically restarted

I am going to have to start learning Eko's [WinDialog](https://github.com/Ekopalypse/NppPythonScripts/tree/master/helper/WinDialog) library

Next Steps:
    - .download_udl():
        - use the basic interface in my experimental code
        - return object = {
                'content': slurp+stringify,
                'Content-Type': f.info.getheader('Content-Type'),
                'status': f.getcode(),
                'ERROR': str(e) # if it exists
            }
    - .download_theme(): similar to .download_udl()
    - Switch to PS3
    - Learn WinDialog
    - Create Dialog(s) that
        - list all the UDLs or AutoCompletions or Themes,
        - allow selecting one (or more?)
        - downloads and installs the selected file(s)
        - silent on success, msgBox on error, ContinueOnFail

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

        # restructure the local JSON so that it's key/object pairs rather than a list of anonymous objects
        self._udls_aoh_to_hoh()

        # grab the nppThemes table-of-contents JSON (new as of 2023-Nov-06)
        f = urllib2.urlopen("https://raw.githubusercontent.com/notepad-plus-plus/nppThemes/master/themes/.toc.json")
        self._themes = json.load(f)

    def _udls_aoh_to_hoh(self):
        self._udl_hoh = {}
        for o in sorted(self._udls, key=lambda d: d['display-name'].lower()):
            # console.write( json.dumps(o, sort_keys=True, separators=(',',':')) + "\n" )
            self._udl_hoh[ o['id-name'] ] = o
            self._udl_hoh[ o['id-name'] ]['_collection_url'] = u'{}{}.xml'.format(
                "https://raw.githubusercontent.com/notepad-plus-plus/userDefinedLanguages/master/UDLs/",
                o['id-name']
            )
        #console.write(json.dumps(self._udl_hoh, sort_keys=True, indent=2) + "\n-----\n")

    def list_themes(self):
        """returns a list of theme names"""
        return self._themes

    def list_udls(self):
        """returns a list of strings"""
        retval = []
        for o in sorted(self._udls, key=lambda d: d['display-name'].lower()):
            # console.write( json.dumps(o, sort_keys=True, indent=2, separators=(',',':')) + "\n" )
            u = u'https://raw.githubusercontent.com/notepad-plus-plus/userDefinedLanguages/master/UDLs/{}.xml'.format(o['id-name'])
            s = u'[{}]({}) => {}\n'.format(
                o['display-name'],
                u, # o['id-name'] + ".xml",
                o['description']
            )
            # console.write(s)
            retval.append(s)

            if o['repository']:
                s = u'\talternate: [{}]({})\n'.format(
                    o['display-name'],
                    o['repository']
                )
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
#console.write(json.dumps({ "UDLs": collectionInterface.list_udls() , "nppThemes": collectionInterface.list_themes()}, sort_keys=True, indent=2, separators=(',',':')))
#console.write("\n")

"""
Current: 'id-name':'AgenaUDL' => the Collection doesn't have the file, and the repo link goes to the repo-parent, not the XML itself
I want to play with urllib2 and seeing if I can get the meta-info
    https://stackoverflow.com/questions/843392/python-get-http-headers-from-urllib2-urlopen-call?noredirect=1&lq=1
"""
if True:
    o = collectionInterface._udl_hoh['AgenaUDL']
    s = None
    se = u''

    if s is None and '_collection_url' in o and o['_collection_url']:
        try:
            f = urllib2.urlopen(o['_collection_url'])
            fi = f.info()   # do this separate in case I want to grab other metadata from the .info() struct
            s = u'{} => {}'.format(
                o['_collection_url'],
                fi.getheader('Content-Type')
            )
            console.write(str(fi)+"\n")
        except urllib2.HTTPError as e:
            msg = u'[ERROR] {} => {}\n'.format(o['_collection_url'], e)
            console.writeError(msg)
            se += msg

    if s is None and 'repository' in o and o['repository']:
        try:
            f = urllib2.urlopen(o['repository'])
            fi = f.info()   # do this separate in case I want to grab other metadata from the .info() struct
            s = u'{} => {}'.format(
                o['repository'],
                fi.getheader('Content-Type')
            )
            console.write(str(fi)+"\n")
        except urllib2.HTTPError as e:
            msg = u'[ERROR] {} => {}\n'.format(o['_collection_url'], e)
            console.writeError(msg)
            se += msg

    if s is None:
        s = se

    console.write(json.dumps( {'AgenaUDL':o, 'result':s}, sort_keys=True, indent=2 ))
"""
Conclusion: I can check the Content-Type for the URL
"""

del(collectionInterface)
