# encoding=utf-8
"""collectionInterface

This provides an interface to the official UserDefinedLanguage Collection and nppThemes Collection.

Requires PythonScript 3

The end goal is a GUI which allows selecting one or more UDL, autoCompletion, functionList, and/or theme files, which would then
be downloaded and installed in the correct location, and Notepad++ automatically restarted

I am going to have to start learning Eko's [WinDialog](https://github.com/Ekopalypse/NppPythonScripts/tree/master/helper/WinDialog) library

Implementation Steps:

    ✓ init object from the UDL and JSON top-level table-of-contents:
        ✓ populate aoh for UDL (_udls)
        ✓ populate array for themes (_themes)
        ✓ from _udls, populate hoh for UDL (_udl_hoh)
        ✓ from _udls, populate hoh for UDL-autoCompletion (_ac_hoh)
        ✓ from _udls, populate hoh for UDL-functionList (_fl_hoh)
        - the hoh structures and _themes array will be passed into the GUI interface for selecting what to download
    ✓ .download_udl():
        ✓ used the basic interface in my experimental code (which is now deleted)
        ✓ return object = {
                'content': slurp+stringify,
                'Content-Type': f.info.getheader('Content-Type'),
                'status': f.getcode(),
                'ERROR': str(e) # if it exists
            }
        ✓ type checking:
            ✓ text/xml allowed
            ✓ text/plain allowed
                ✓ if it resolves to valid XML, it's okay
                ✓ else, "406 Not Acceptable"
            ✓ anything else not allowed => "406 Not Acceptable"
    - .download_autoCompletion(): similar to .download_udl()
    - .download_functionList(): similar to .download_udl()
    - .download_theme(): similar to .download_udl()
    - ✓ Switch to PS3
    - Learn WinDialog
    - Create Dialog(s) that
        - list all the UDLs or AutoCompletions or FunctionLists or Themes,
        - allow selecting one (or more?)
        - downloads and installs the selected file(s)
        - silent on success, msgBox on error, ContinueOnFail

"""
from Npp import *
import urllib.request   # urllib2.urlopen() returns stream; py3 urllib.request.urlopen hopefully does same
import urllib.error     # urllib2.HTTPError => urllib.error.HTTPError
import urllib.response  #
import json             # .load(f) => load from stream; .loads(s) => load from string; .dump(o) => dump to stream; .dumps(o) => dump to string

class CollectionInterface(object):
    """Provides an interface to the UserDefinedlanguage Collection and nppThemes Collection.

    Use this to list or download a specific UDL, autoCompletion, or Theme from the Collections.
    """
    def __init__(self):
        """Instantiation"""

        # grab the udl-list.json -- as of the 2023-Nov-06 update to the repo,
        #   this now contains both UDL and autoCompletion info, to avoid
        f = urllib.request.urlopen("https://raw.githubusercontent.com/notepad-plus-plus/userDefinedLanguages/master/udl-list.json")
        o = json.load(f)
        self._udls = o['UDLs']

        # restructure the local JSON so that it's key/object pairs rather than a list of anonymous objects
        self._udls_aoh_to_hoh()

        # grab the nppThemes table-of-contents JSON (new as of 2023-Nov-06)
        f = urllib.request.urlopen("https://raw.githubusercontent.com/notepad-plus-plus/nppThemes/master/themes/.toc.json")
        self._themes = json.load(f)

    def _udls_aoh_to_hoh(self):
        """
        converts the array-of-hashes (aoh; or to use python terminology, "list of dictionaries") to a hash-of-hashes (hoh; "dictionary of dictionaries")
        - also populates aoh for the autoCompletion and/or functionList definitions that are referenced by a given UDL
        """
        self._udl_hoh = {}
        self._ac_hoh = {}
        self._fl_hoh = {}
        for o in sorted(self._udls, key=lambda d: d['display-name'].lower()):
            # console.write( json.dumps(o, sort_keys=True, separators=(',',':')) + "\n" )
            self._udl_hoh[ o['id-name'] ] = o
            self._udl_hoh[ o['id-name'] ]['_collection_url'] = u'{}{}.xml'.format(
                "https://raw.githubusercontent.com/notepad-plus-plus/userDefinedLanguages/master/UDLs/",
                o['id-name']
            )

            if 'autoCompletion' in o:
                console.write("processing({}): found autoCompletion({})\n".format(o['description'], o['autoCompletion']))
                self._ac_hoh[ o['id-name'] ] = {
                    'id-name': o['id-name'],
                    'display-name': o['display-name'],
                    'description': o['description'],
                    'autoCompletion': o['autoCompletion'],
                    'autoCompletionAuthor': o['autoCompletionAuthor'] if 'autoCompletionAuthor' in o else o['author']
                }
                # TODO: define a '_collection_url' similar to the above, but maybe with more logic so it can handle
                #   if true     => autoCompletions/{id-name}.xml
                #   if value    => autoCompletions/{value}.xml
                #   if url      => {url}
                # ... though I think .download_udl handled that for UDL, so maybe .download_autoCompletion will handle that for ac

            if 'functionList' in o:
                console.write("processing({}): found functionList({})\n".format(o['description'], o['functionList']))
                self._fl_hoh[ o['id-name'] ] = {
                    'id-name': o['id-name'],
                    'display-name': o['display-name'],
                    'description': o['description'],
                    'functionList': o['functionList'],
                    'functionListAuthor': o['functionListAuthor'] if 'functionListAuthor' in o else o['author']
                }
                # TODO: define a '_collection_url' similar to the above, but maybe with more logic so it can handle
                #   if true     => functionList/{id-name}.xml
                #   if value    => functionList/{value}.xml
                #   if url      => {url}
                # ... though I think .download_udl handled that for UDL, so maybe .download_functionList will handle that for fl

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

    def list_autocompletes(self):
        return list(self._ac_hoh.keys())

    def list_functionlists(self):
        return list(self._fl_hoh.keys())

    def download_theme(self, theme_file_name):
        """grab the specified theme

        theme_file_name should include the .xml extension (eg: 'blah.xml')
        the tool will automatically create the URL, including the themes subdirectory ('.../themes/blah.xml')
        """
        pass

    def _dl_udl_from_id_key(self,udl_id, key, chain = None):
        o = self._udl_hoh[udl_id]
        console.write(u'trying UDL id={}, key={}\n'.format(udl_id, key))
        return self._dl_generic_from_id_key(udl_id, key, o, chain)

    def _dl_ac_from_id_key(self,udl_id, key, chain = None):
        o = self._ac_hoh[udl_id]
        console.write(u'trying AutoCompletion id={}, key={}\n'.format(udl_id, key))
        return self._dl_generic_from_id_key(udl_id, key, o, chain)

    def _dl_fl_from_id_key(self,udl_id, key, chain = None):
        o = self._fl_hoh[udl_id]
        console.write(u'trying FunctionList id={}, key={}\n'.format(udl_id, key))
        return self._dl_generic_from_id_key(udl_id, key, o, chain)

    def _dl_generic_from_id_key(self,udl_id, key, o, chain = None):
        if chain is None:
            chain = {
                'content': None,                # slurp+stringify,
                'Content-Type': None,           # f.info.getheader('Content-Type'),
                'status': None,                 # f.getcode(),
                'ERROR': None,                  # str(e) # if it exists
            }

        if key in o and o[key]:
            try:
                f = urllib.request.urlopen(o[key])
                fi = f.headers # was f.info() in Py2
                chain['URL'] = o[key]
                chain['content'] = f.read().decode('utf-8');    # py3 requires the .decode() otherwise it's interpreted as raw bytes
                chain['Content-Type'] = fi.get('Content-Type'); # was fi.getheader('Content-Type')
                chain['status'] = f.getcode()
            except urllib.error.HTTPError as e:
                if chain['ERROR']:
                    prefix = str(chain['ERROR'])
                else:
                    prefix = u''
                msg = u'{}{} => {}\n'.format(prefix, o[key], str(e))
                chain['ERROR'] = Exception(msg) # but don't raise it yet...

        return chain

    def _check_for_xml(self, chain):
        if chain['Content-Type'][0:8] == 'text/xml':
            console.write("It's text/xml, so it's definitely okay\n")
            return chain

        if chain['Content-Type'][0:10] == 'text/plain' or chain['Content-Type'][0:24] == 'application/octet-stream':
            # deeper checking: look for prolog or element or comment at non-whitespace start of file
            chk = chain['content'].strip()
            if chk[0:5] == '<?xml' or chk[0:12] == '<NotepadPlus' or chk[0:4] == '<!--':
                console.write("Got {} from url {}, but it actually contains reasonable XML content\n".format(chain['Content-Type'], chain['URL']))
                return chain

            msg = u'Not Acceptable => got {} from url {} that doesnt seem like XML'.format(chain['Content-Type'], chain['URL'])
            raise urllib.error.HTTPError(chain['URL'], 406, msg, None, None)

        msg = u'Not Acceptable => Content-Type should be text/xml or text/plain, but got {} from url {}'.format(chain['Content-Type'], chain['URL'])
        raise urllib.error.HTTPError(chain['URL'], 406, msg, None, None)

        """
            urllib.error.HTTPError(self, url, code, msg, hdrs, fp)
                https://www.rfc-editor.org/rfc/rfc7231.html#section-6.5.6       406 Not Acceptable
                    "indicates that the target resource does not have a current representation that would be acceptable to the user agent"
                - that sounds like the right thing for
            urllib.URLError(self, reason)
        """



    def download_udl(self, udl_id = None, udl_display_name = None):
        """grab the specified UDL

        can be specified by udl_id (based on o['id-name'])
        [MAYBE TODO] or specified by udl_display_name (based on o['display-name'])
        """
        chain = {
            'content': None,                # slurp+stringify,
            'Content-Type': None,           # f.info.getheader('Content-Type'),
            'status': None,                 # f.getcode(),
            'ERROR': None,                  # str(e) # if it exists
        }

        if udl_id and udl_id in self._udl_hoh:

            if chain['content'] is None:
                chain = self._dl_udl_from_id_key(udl_id, '_collection_url')

            if chain['content'] is None:
                chain = self._dl_udl_from_id_key(udl_id, 'repository')

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

        # need to check the content type, and complain if it's not XML
        chain = self._check_for_xml(chain)

        return chain



    def download_autoCompletion(self, udl_id = None, udl_display_name = None):
        """grab the specified UDL

        can be specified by udl_id (based on o['id-name'])
        [MAYBE TODO] or specified by udl_display_name (based on o['display-name'])
        """
        chain = {
            'content': None,                # slurp+stringify,
            'Content-Type': None,           # f.info.getheader('Content-Type'),
            'status': None,                 # f.getcode(),
            'ERROR': None,                  # str(e) # if it exists
        }

        if udl_id and udl_id in self._ac_hoh:
            o = self._ac_hoh[udl_id]

            #   TestBeds:
            #       Smartsheet_byKevinDickinson         autoCompletion:true
            #       RenderMan-RSL_byStefanGustavson     autoCompletion:local_basename
            #       SciLab_bySamuelGougeon              autoCompletion:URL

            # TODO: start uncommenting these as I enable each mode

            if chain['content'] is None:
                if o['autoCompletion']:
                    key = '_collection_url'
                    if str(True) == str(o['autoCompletion']):
                        o['_collection_url'] = u'{}{}.xml'.format(
                            "https://raw.githubusercontent.com/notepad-plus-plus/userDefinedLanguages/master/autoCompletions/",
                            o['id-name']
                        )
                    elif o['autoCompletion'][0:4] != 'http':
                        o['_collection_url'] = u'{}{}.xml'.format(
                            "https://raw.githubusercontent.com/notepad-plus-plus/userDefinedLanguages/master/autoCompletions/",
                            o['autoCompletion']
                        )
                    else:
                        key = 'autoCompletion'

                    if o[key]:
                        chain = self._dl_ac_from_id_key(udl_id, key)

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

        # need to check the content type, and complain if it's not XML
        if not chain['ERROR']:
            chain = self._check_for_xml(chain)

        return chain

console.show();
console.clear();
collectionInterface = CollectionInterface()
#console.write(json.dumps({ "UDLs": collectionInterface.list_udls() , "nppThemes": collectionInterface.list_themes()}, sort_keys=True, indent=2, separators=(',',':')))
#console.write("\n")
console.write(json.dumps({
    #'UDLs': collectionInterface.list_themes(),
    #'nppThemes': collectionInterface.list_themes(),
    'udlAutoComplete': collectionInterface.list_autocompletes(),
    'udlFunctionList': collectionInterface.list_functionlists(),
}, sort_keys=True, indent=2))

# AgenaUDL => the Collection doesn't have the file, and the repo link goes to the repo-parent, not the XML itself (text/html)
try:
    ro = collectionInterface.download_udl(udl_id = 'AgenaUDL')
    console.write(json.dumps(ro, sort_keys=True, indent=2) + "\n\n")
except urllib.error.HTTPError as e:
    console.writeError('Inserting intentional error for HTML instead of XML or PLAIN:\n')
    console.writeError(u"{} => {}\n\n".format(str(e), json.dumps({
        'e_info': e.info(),
        'e_code': e.getcode(),
        'e_url': e.filename
    }, sort_keys=True, indent=2)))

# 6502Assembly_byCarlMyerholtz => it exists in the collection repo, but comes out as text/plain, not text/xml.
#       It appears that GitHub's "raw" interface sends things as text/plain, to keep it raw.
#       So I will need to be able to accept either, and do additional checking if the text is reasonable XML.
ro = collectionInterface.download_udl(udl_id = '6502Assembly_byCarlMyerholtz')
console.write(json.dumps(ro, sort_keys=True, indent=2) + "\n\n")

# 'RouterOS Script' => gives invalid URL
#   >> httplib.InvalidURL: URL can't contain control characters. u'/notepad-plus-plus/userDefinedLanguages/master/UDLs/RouterOS Script.xml' (found at least u' ')
#       At some point, I should probably add a "reverse checker", to make sure that every UDL filename
#       is also in the JSON's 'id-name'
#ro = collectionInterface.download_udl(udl_id = 'RouterOS Script')
#console.write(json.dumps(ro, sort_keys=True, indent=2) + "\n\n")

## console.write(json.dumps({
##         '_udls': collectionInterface._udls,
##         '_udl_hoh': collectionInterface._udl_hoh,
##         '_themes': collectionInterface._themes,
##     }, sort_keys=True, indent=2) + "\n\n")

console.write(json.dumps({
    '_ac_hoh': collectionInterface._ac_hoh
}, sort_keys=True, indent=2) + "\n\n")

##### Testing .download_autoCompletion()
#       Smartsheet_byKevinDickinson         autoCompletion:true
ro = collectionInterface.download_autoCompletion(udl_id = 'Smartsheet_byKevinDickinson')
if ro['ERROR']:
    if isinstance(ro['ERROR'], Exception):
        raise ro['ERROR']
    elif isinstance(ro['ERROR'], str) or isinstance(ro['ERROR'], unicode):
        raise Exception(ro['ERROR'])
console.write(json.dumps(ro, sort_keys=True, indent=2) + "\n\n")

##### Testing .download_autoCompletion()
#       RenderMan-RSL_byStefanGustavson     autoCompletion:local_basename
ro = collectionInterface.download_autoCompletion(udl_id = 'RenderMan-RSL_byStefanGustavson')
if ro['ERROR']:
    if isinstance(ro['ERROR'], Exception):
        raise ro['ERROR']
    elif isinstance(ro['ERROR'], str) or isinstance(ro['ERROR'], unicode):
        raise Exception(ro['ERROR'])
console.write(json.dumps(ro, sort_keys=True, indent=2) + "\n\n")

##### Testing .download_autoCompletion()
#       SciLab_bySamuelGougeon              autoCompletion:URL
ro = collectionInterface.download_autoCompletion(udl_id = 'SciLab_bySamuelGougeon')
if ro['ERROR']:
    if isinstance(ro['ERROR'], Exception):
        raise ro['ERROR']
    elif isinstance(ro['ERROR'], str) or isinstance(ro['ERROR'], unicode):
        raise Exception(ro['ERROR'])
console.write(json.dumps(ro, sort_keys=True, indent=2) + "\n\n")

##### END #####
del(collectionInterface)
