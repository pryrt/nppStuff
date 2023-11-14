# encoding=utf-8
"""collectionInterface

This provides an interface to the official UserDefinedLanguage Collection and nppThemes Collection.

The end goal is a GUI which allows selecting one or more UDL, autoCompletion, and/or theme files, which would then
be downloaded and installed in the correct location, and Notepad++ automatically restarted

I am going to have to start learning Eko's [WinDialog](https://github.com/Ekopalypse/NppPythonScripts/tree/master/helper/WinDialog) library

Next Steps:
    - .download_udl():
        - used the basic interface in my experimental code (which is now deleted)
        - return object = {
                'content': slurp+stringify,
                'Content-Type': f.info.getheader('Content-Type'),
                'status': f.getcode(),
                'ERROR': str(e) # if it exists
            }
        - TODO: need to do type checking: either text/xml or text/plain that resolves to valid XML
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

    def download_theme(self, theme_file_name):
        """grab the specified theme

        theme_file_name should include the .xml extension (eg: 'blah.xml')
        the tool will automatically create the URL, including the themes subdirectory ('.../themes/blah.xml')
        """
        pass

    def _dl_from_id_key(self,udl_id, key, chain = None):
        o = self._udl_hoh[udl_id]

        if chain is None:
            chain = {
                'content': None,                # slurp+stringify,
                'Content-Type': None,           # f.info.getheader('Content-Type'),
                'status': None,                 # f.getcode(),
                'ERROR': None,                  # str(e) # if it exists
            }

        console.write(u'trying id={}, key={}\n'.format(udl_id, key))

        if key in o and o[key]:
            try:
                f = urllib2.urlopen(o[key])
                fi = f.info()
                chain['URL'] = o[key]
                chain['content'] = f.read()
                chain['Content-Type'] = fi.getheader('Content-Type')
                chain['status'] = f.getcode()
            except urllib2.HTTPError as e:
                if chain['ERROR']:
                    prefix = str(chain['ERROR'])
                else:
                    prefix = u''
                msg = u'{}{} => {}\n'.format(prefix, o[key], str(e))
                chain['ERROR'] = Exception(msg) # but don't raise it yet...

        return chain


    def download_udl(self, udl_id = None, udl_display_name = None):
        """grab the specified UDL

        can be specified by udl_id (based on o['id-name'])
        or specified by udl_display_name (based on o['display-name'])
        """
        chain = {
            'content': None,                # slurp+stringify,
            'Content-Type': None,           # f.info.getheader('Content-Type'),
            'status': None,                 # f.getcode(),
            'ERROR': None,                  # str(e) # if it exists
        }

        if udl_id and udl_id in self._udl_hoh:

            if chain['content'] is None:
                chain = self._dl_from_id_key(udl_id, '_collection_url')

            if chain['content'] is None:
                chain = self._dl_from_id_key(udl_id, 'repository')

            if chain['content'] is None:
                if isinstance(chain['ERROR'], Exception):
                    raise chain['ERROR']
                elif isinstance(chain['ERROR'], str) or isinstance(chain['ERROR'], unicode):
                    raise Exception(chain['ERROR'])
                else:
                    raise Exception("[ERROR] Cannot determine what went wrong when I tried {}".format(udl_id))

        elif udl_display_name:

            raise Exception("udl_display_name interface not implemented yet")

        else:

            raise Exception("provided with neither a valid udl_id nor a valid udl_display_name; don't know what to do")

        # TODO: need to check the content type, and complain if it's not XML

        return chain

console.clear();
collectionInterface = CollectionInterface()
#console.write(json.dumps({ "UDLs": collectionInterface.list_udls() , "nppThemes": collectionInterface.list_themes()}, sort_keys=True, indent=2, separators=(',',':')))
#console.write("\n")

# AgenaUDL => the Collection doesn't have the file, and the repo link goes to the repo-parent, not the XML itself
ro = collectionInterface.download_udl(udl_id = 'AgenaUDL')
console.write(json.dumps(ro, sort_keys=True, indent=2) + "\n\n")

# 6502Assembly_byCarlMyerholtz => it exists in the collection repo, but comes out as text/plain, not text/xml.
#       It appears that GitHub's "raw" interface sends things as text/plain, to keep it raw.
#       So I will need to be able to accept either, and do additional checking if the text is reasonable XML.
ro = collectionInterface.download_udl(udl_id = '6502Assembly_byCarlMyerholtz')
console.write(json.dumps(ro, sort_keys=True, indent=2) + "\n\n")

# 'RouterOS Script' => gives invalid URL
#       At some point, I should probably add a "reverse checker", to make sure that every UDL filename
#       is also in the JSON's 'id-name'
# ro = collectionInterface.download_udl(udl_id = '6502Assembly_byCarlMyerholtz')
# console.write(json.dumps(ro, sort_keys=True, indent=2) + "\n\n")

del(collectionInterface)
