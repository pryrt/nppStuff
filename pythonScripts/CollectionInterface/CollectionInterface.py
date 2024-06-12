# encoding=utf-8
"""collectionInterface

This provides an interface to the official UserDefinedLanguage Collection and nppThemes Collection.

Requires PythonScript 3.0.18 or newer (might work on 3.0.17, but won't work before that)

Requires [WinDialog](https://github.com/Ekopalypse/NppPythonScripts/tree/master/helper/WinDialog) library

A GUI which allows selecting one or more UDL, autoCompletion, functionList, and/or theme files, which would then
be downloaded and installed in the correct location, and Notepad++ automatically restarted
"""

from Npp import *
import os
import urllib.request   # urllib2.urlopen() returns stream; py3 urllib.request.urlopen hopefully does same
import urllib.error     # urllib2.HTTPError => urllib.error.HTTPError
import urllib.response  #
import json             # .load(f) => load from stream; .loads(s) => load from string; .dump(o) => dump to stream; .dumps(o) => dump to string
import html             # html.unescape()
from WinDialog import Dialog, Button, Label, ComboBox
from WinDialog.controls.combobox import CBS
from WinDialog.win_helper import WindowStyle as WS
import ctypes
if os.path.dirname(os.path.abspath(__file__)) not in sys.path:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from w32GetOpenSaveFileName import getSaveFileName, getOpenFileName

import subprocess
from ctypes import wintypes
GetCommandLine = ctypes.windll.kernel32.GetCommandLineW
GetCommandLine.restype = wintypes.LPWSTR
GetCommandLine.argtypes = []


class CollectionInterfaceDialog(Dialog):
    _nppConfigDirectory = os.path.dirname(os.path.dirname(notepad.getPluginConfigDir()))
    _nppCfgUdlDirectory = os.path.join(_nppConfigDirectory, 'userDefineLangs')
    _nppCfgFunctionListDirectory = os.path.join(_nppConfigDirectory, 'functionList')
    _nppCfgThemesDirectory = os.path.join(_nppConfigDirectory, 'themes')
    _nppAppAutoCompletionDirectory = os.path.join(notepad.getNppDir(), 'autoCompletion')

    def __init__(self, dataSource, title='Collection Interface'):
        super().__init__(title)
        self.size = (300, 85)
        self.center = True
        self.dataSource = dataSource

        self.desc_lbl       = Label('Download from UDL Collection or Themes Collection', size=(280, 9), position=(10,5))

        self.dl_btn         = Button(title='&Download',     size=( 60, 14), position=(10, 65))
        self.dl_btn.onClick = self.on_download

        self.done_btn       = Button(title='&Done',         size=( 60, 14), position=(80, 65))
        self.done_btn.onClick = self.on_close

        self.restart_btn    = Button(title='&Restart',      size=( 60, 14), position=(300 - 10 - 60, 65))
        self.restart_btn.onClick = self.on_restart

        self.category_lbl   = Label('Category:',            size=( 30,  9), position=(10, 23))
        self.category_cb    = ComboBox('' ,                 size=(240, 52), position=(50, 20))
        self.category_cb.onSelChange = self.on_category_change
        self.category_cb.style |= WS.TABSTOP

        self.file_lbl       = Label('File:',                size=( 30,  9), position=(10, 41))
        self.file_cb        = ComboBox('' ,                 size=(240, 11), position=(50, 40))
        self.file_cb.style |= WS.TABSTOP |  CBS.DISABLENOSCROLL | WS.VSCROLL

        self.end_lbl        = Label('Need RESTART for Notepad++ to see new UDL/AutoCompletion/FunctionList/Themes', size=(280,9), position=(10,55))

        self.initialize = self.on_init
        self.show()

    def on_download(self):
        category = self.category_cb.getSelectedItemText()
        display_name = self.file_cb.getSelectedItemText()
        id_name = self.dataSource._udllist_to_id[display_name] if category != "Theme" else display_name
        dl_dir = None
        unWriteable = False

        # need to switch to actual downloads
        match category:
            case "UDL":
                dl_dir = self._nppCfgUdlDirectory
                ro = self.dataSource.download_udl(udl_id = id_name)

            case "AutoCompletion":
                dl_dir = self._nppAppAutoCompletionDirectory
                ro = self.dataSource.download_autoCompletion(udl_id = id_name)

                # determine whether user can already write to AutoCompletion directory
                try:
                    tf = os.path.join(dl_dir, '~$TMPFILE.PRYRT')
                    fo = open(tf, 'w')
                    fo.close()
                    os.remove(tf)
                    unWriteable = False
                except:
                    unWriteable = True

            case "FunctionList":
                dl_dir = self._nppCfgFunctionListDirectory
                ro = self.dataSource.download_functionList(udl_id = id_name)

            case "Theme":
                dl_dir = self._nppCfgThemesDirectory
                ro = self.dataSource.download_theme(display_name)

            case _:
                raise Exception(f'unknown category {category}!')

        if not(ro):
            raise Exception('Nothing returned from attempted download')
        elif ro['ERROR']:
            if isinstance(ro['ERROR'], Exception):
                raise ro['ERROR']
            elif isinstance(ro['ERROR'], str) or isinstance(ro['ERROR'], unicode):
                raise Exception(ro['ERROR'])
            else:
                raise Exception("[ERROR] Cannot determine what went wrong when I tried to download")

        f = id_name + ".xml" if category != 'Theme' else display_name
        default_fname = os.path.join(dl_dir, f)
        savename = ""
        if not unWriteable:
            savename = getSaveFileName('Save As', 'xml', 'XML (*.xml)|*.xml|All (*.*)|*.*|', default_fname)
        else:
            tmpdir = os.environ['TEMP']
            if not os.path.exists(tmpdir):
                tmpdir = os.environ['TMP']
            if not os.path.exists(tmpdir):
                tmpdir = 'c:\\temp'
            if not os.path.exists(tmpdir):
                tmpdir = 'c:\\tmp'
            if not os.path.exists(tmpdir):
                tmpdir = os.environ['USERPROFILE']
            savename = os.path.join(tmpdir, f)

        if savename:
            try:
                with open(savename, 'w', newline='') as fo:
                    fo.write(ro['content'])
            except PermissionError as e:
                notepad.messageBox(str(e), "ERROR: Permission Error")

        if unWriteable:
            # copy from savename to default_fname with UAC prompt
            #       https://stackoverflow.com/a/41930586
            cmd = 'cmd.exe'
            args = f'/C COPY /Y "{savename}" "{default_fname}"'
            ctypes.windll.shell32.ShellExecuteW(None, "runas", cmd, args, None, 1)

        del(savename)


    def on_close(self):
        self.terminate()

    def on_restart(self):
        #console.write(f"argv => {sys.argv}\n") # this would be useful for the ['cmd','o1',...'oN'] version of Popen => subprocess.Popen(sys.argv)
        #   but since I want the TIMEOUT to give previous instance a chance to close, I need to use the string from GetCommandLine() anyway,
        #   so don't need sys.argv

        cmd = f"cmd /C TIMEOUT /T 2 && {GetCommandLine()}"
        subprocess.Popen(cmd)
        self.terminate()
        notepad.menuCommand(MENUCOMMAND.FILE_EXIT)

    def on_category_change(self):
        choices = {
            'UDL': self.dataSource.list_udls(),
            'AutoCompletion': self.dataSource.list_autocompletes(),
            'FunctionList': self.dataSource.list_functionlists(),
            'Theme': self.dataSource.list_themes()
        }
        selected_text = self.category_cb.getSelectedItemText()
        if selected_text in choices:
            self.file_cb.set(choices[selected_text])
        else:
            self.file_cb.set([])

    def on_init(self):
        self.category_cb.append(['UDL', 'AutoCompletion', 'FunctionList', 'Theme'])
        self.on_category_change()


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

        CollectionInterfaceDialog(self)

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

            o['display-name'] = html.unescape(o['display-name'])

            if 'autoCompletion' in o:
                #console.write("processing({}): found autoCompletion({})\n".format(o['description'], o['autoCompletion']))
                self._ac_hoh[ o['id-name'] ] = {
                    'id-name': o['id-name'],
                    'display-name': o['display-name'],
                    'description': o['description'],
                    'autoCompletion': o['autoCompletion'],
                    'autoCompletionAuthor': o['autoCompletionAuthor'] if 'autoCompletionAuthor' in o else o['author']
                }

            if 'functionList' in o:
                #console.write("processing({}): found functionList({})\n".format(o['description'], o['functionList']))
                self._fl_hoh[ o['id-name'] ] = {
                    'id-name': o['id-name'],
                    'display-name': o['display-name'],
                    'description': o['description'],
                    'functionList': o['functionList'],
                    'functionListAuthor': o['functionListAuthor'] if 'functionListAuthor' in o else o['author']
                }

    def list_themes(self):
        """returns a list of theme names"""
        return self._themes

    def list_udls(self):
        """returns a list of strings"""
        retval = []
        self._udllist_to_id = {}
        for o in sorted(self._udls, key=lambda d: d['display-name'].lower()):
            self._udllist_to_id[o['display-name']] = o['id-name']
            retval.append(o['display-name'])

        return retval

    def list_autocompletes(self):
        return [self._udl_hoh[x]['display-name'] for x in self._ac_hoh.keys()]

    def list_functionlists(self):
        return [self._udl_hoh[x]['display-name'] for x in self._fl_hoh.keys()]

    def _dl_udl_from_id_key(self,udl_id, key, chain = None):
        o = self._udl_hoh[udl_id]
        #console.write(u'trying UDL id={}, key={}\n'.format(udl_id, key))
        return self._dl_generic_from_id_key(udl_id, key, o, chain)

    def _dl_ac_from_id_key(self,udl_id, key, chain = None):
        o = self._ac_hoh[udl_id]
        #console.write(u'trying AutoCompletion id={}, key={}\n'.format(udl_id, key))
        return self._dl_generic_from_id_key(udl_id, key, o, chain)

    def _dl_fl_from_id_key(self,udl_id, key, chain = None):
        o = self._fl_hoh[udl_id]
        #console.write(u'trying FunctionList id={}, key={}\n'.format(udl_id, key))
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
            #console.write("It's text/xml, so it's definitely okay\n")
            return chain

        if chain['Content-Type'][0:10] == 'text/plain' or chain['Content-Type'][0:24] == 'application/octet-stream':
            # deeper checking: look for prolog or element or comment at non-whitespace start of file
            chk = chain['content'].strip()
            if chk[0:5] == '<?xml' or chk[0:12] == '<NotepadPlus' or chk[0:4] == '<!--':
                #console.write("Got {} from url {}, but it actually contains reasonable XML content\n".format(chain['Content-Type'], chain['URL']))
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

    def download_udl(self, udl_id):
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

    def download_autoCompletion(self, udl_id):
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

    def download_theme(self, theme_file_name):
        """grab the specified theme

        theme_file_name should include the .xml extension (eg: 'blah.xml')
        the tool will automatically create the URL, including the themes subdirectory ('.../themes/blah.xml')
        """
        chain = {
            'content': None,                # slurp+stringify,
            'Content-Type': None,           # f.info.getheader('Content-Type'),
            'status': None,                 # f.getcode(),
            'ERROR': None,                  # str(e) # if it exists
        }
        if theme_file_name in self._themes:
            o = {
                'name': theme_file_name,
                'url': u"{}/{}".format('https://raw.githubusercontent.com/notepad-plus-plus/nppThemes/main/themes', theme_file_name)
            }
            return self._dl_generic_from_id_key(theme_file_name, 'url', o, chain)
        else:
            raise Exception("theme '{}' not in list of themes".format(theme_file_name))


console.show();
#console.clear();
collectionInterface = CollectionInterface()
doTest = False

if doTest:
    #console.write(json.dumps({ "UDLs": collectionInterface.list_udls() , "nppThemes": collectionInterface.list_themes()}, sort_keys=True, indent=2, separators=(',',':')))
    #console.write("\n")
    console.write(json.dumps({
        #'UDLs': collectionInterface.list_udls(),
        #'nppThemes': collectionInterface.list_themes(),
        'udlAutoComplete': collectionInterface.list_autocompletes(),
        'udlFunctionList': collectionInterface.list_functionlists(),
    }, sort_keys=True, indent=2)+"\n\n")

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
    if False:
        # disabled once I knew it worked, because it's pretty slow
        ro = collectionInterface.download_autoCompletion(udl_id = 'SciLab_bySamuelGougeon')
        if ro['ERROR']:
            if isinstance(ro['ERROR'], Exception):
                raise ro['ERROR']
            elif isinstance(ro['ERROR'], str) or isinstance(ro['ERROR'], unicode):
                raise Exception(ro['ERROR'])
        console.write(json.dumps(ro, sort_keys=True, indent=2) + "\n\n")

    ##### Testing .download_theme()
    console.write(json.dumps({
        #'UDLs': collectionInterface.list_udls(),
        'nppThemes': collectionInterface.list_themes()
    }, sort_keys=True, indent=2) + "\n\n")
    ro = collectionInterface.download_theme('99er.xml')
    if ro['ERROR']:
        if isinstance(ro['ERROR'], Exception):
            raise ro['ERROR']
        elif isinstance(ro['ERROR'], str) or isinstance(ro['ERROR'], unicode):
            raise Exception(ro['ERROR'])
    console.write(json.dumps(ro, sort_keys=True, indent=2) + "\n\n")
    ##### END `if doTest:`

##### END #####
del(collectionInterface)
