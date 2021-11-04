"""sessionChecker

author = PeterJones @ community.notepad-plus-plus.org

This script will
* prompt to the session XML file in active editor
* grab the filenames from the <File> elements and test if they exist
* for any filenames that do not exist, it will prompt to either
    * YES = replace the session entry with a file selected from a standard Windows GetOpenFilename dialog
    * NO = remote the entry from the session
* when done, session file will be automatically saved
* if you want to revert the changes, hit UNDO (^Z) and then SAVE (^S)

inspired by forum post: https://community.notepad-plus-plus.org/topic/19902/change-how-notepad-handles-non-existing-files-from-a-session/2

Since @Hans-v-Buitenen already calls a script to audit session files "insane",
I decided not to publish to that topic.  I did this mostly to see if I could, anyway.

"""

# reference: https://stackoverflow.com/questions/48746478/how-do-i-extract-value-of-xml-attribute-in-python
# reference: https://docs.python.org/2/library/xml.etree.elementtree.html
import xml.etree.ElementTree as ET
import os.path

###############
# using https://gist.github.com/nicomgd/1097a0b7ca3715da4e71 as a wrapper for getOpenFileName
###############
import ctypes
import ctypes.wintypes as wintypes

LPOFNHOOKPROC = ctypes.c_voidp # TODO
LPCTSTR = LPTSTR = ctypes.c_wchar_p

class OPENFILENAME(ctypes.Structure):
    _fields_ = [("lStructSize", wintypes.DWORD),
                ("hwndOwner", wintypes.HWND),
                ("hInstance", wintypes.HINSTANCE),
                ("lpstrFilter", LPCTSTR),
                ("lpstrCustomFilter", LPTSTR),
                ("nMaxCustFilter", wintypes.DWORD),
                ("nFilterIndex", wintypes.DWORD),
                ("lpstrFile", LPTSTR),
                ("nMaxFile", wintypes.DWORD),
                ("lpstrFileTitle", LPTSTR),
                ("nMaxFileTitle", wintypes.DWORD),
                ("lpstrInitialDir", LPCTSTR),
                ("lpstrTitle", LPCTSTR),
                ("flags", wintypes.DWORD),
                ("nFileOffset", wintypes.WORD),
                ("nFileExtension", wintypes.WORD),
                ("lpstrDefExt", LPCTSTR),
                ("lCustData", wintypes.LPARAM),
                ("lpfnHook", LPOFNHOOKPROC),
                ("lpTemplateName", LPCTSTR),
                ("pvReserved", wintypes.LPVOID),
                ("dwReserved", wintypes.DWORD),
                ("flagsEx", wintypes.DWORD)]

GetOpenFileName = ctypes.windll.comdlg32.GetOpenFileNameW
GetSaveFileName = ctypes.windll.comdlg32.GetSaveFileNameW

OFN_ENABLESIZING      =0x00800000
OFN_PATHMUSTEXIST     =0x00000800
OFN_OVERWRITEPROMPT   =0x00000002
OFN_NOCHANGEDIR       =0x00000008
MAX_PATH=1024


def _buildOFN(title, default_extension, filter_string, fileBuffer):

  ofn = OPENFILENAME()
  ofn.lStructSize = ctypes.sizeof(OPENFILENAME)
  ofn.lpstrTitle = title
  ofn.lpstrFile = ctypes.cast(fileBuffer, LPTSTR)
  ofn.nMaxFile = MAX_PATH
  ofn.lpstrDefExt = default_extension
  ofn.lpstrFilter = filter_string
  ofn.Flags = OFN_ENABLESIZING | OFN_PATHMUSTEXIST | OFN_OVERWRITEPROMPT | OFN_NOCHANGEDIR
  return ofn


def getOpenFileName(title, default_extension, filter_string, initialPath):

  if initialPath is None:
    initialPath = ""
  filter_string = filter_string.replace("|", "\0")
  fileBuffer = ctypes.create_unicode_buffer(initialPath, MAX_PATH)
  ofn = _buildOFN(title, default_extension, filter_string, fileBuffer)

  if GetOpenFileName(ctypes.byref(ofn)):
    return fileBuffer[:]
  else:
    return None


def getSaveFileName(title, default_extension, filter_string, initialPath):

  if initialPath is None:
    initialPath = ""
  filter_string = filter_string.replace("|", "\0")
  fileBuffer = ctypes.create_unicode_buffer(initialPath, MAX_PATH)
  ofn = _buildOFN(title, default_extension, filter_string, fileBuffer)

  if GetSaveFileName(ctypes.byref(ofn)):
    return fileBuffer[:]
  else:
    return None

###############
# end borrowed code
###############

console.clear()

notepad.menuCommand(MENUCOMMAND.FILE_OPEN)

xmlTree = ET.fromstring(editor.getText())

filesNotFound = []

for view in xmlTree.find('./Session'):
    for fileElement in view.findall('File'):
        fn = fileElement.attrib['filename']
        ex = 'exists' if os.path.isfile(fn) else 'does not exist'
        if not os.path.isfile(fn):
            filesNotFound.append((view,fileElement))

for view, fileElement in filesNotFound:
    name = fileElement.attrib['filename']
    t = 'File not found!'
    s = 'Could not find filename="{}"\n'.format(name) + \
        'YES to find new location, NO to remove entry from session'
    r = notepad.messageBox(s, t, MESSAGEBOXFLAGS.YESNO)
    if r == MESSAGEBOXFLAGS.RESULTYES:
        # looking for new location
        print("need to select new file location for \"{}\"".format(name))

        # ask
        repl = getOpenFileName(
            'Pick replacement file for "{}"'.format(name), # title
            "xml", # default extension, if no extension selected
            "Session Files (*.xml)|*.xml|All Files (*.*)|*.*", # file type search filters
            None  #initial path
        )
        if not repl is None:
            # cleanup the reply
            repl = repl.replace("\0", "")
            print('Replace "{}" with "{}"'.format(name, repl))

            # create the file if it doesn't exist
            if not os.path.exists(repl):
                with open(repl, 'a'):
                    pass

            # replace the filename in the XML data structure
            fileElement.attrib['filename'] = repl

    else:
        # remove the non-existent file from the XML data structure
        view.remove(fileElement)

# update the session file, save
txt = ET.tostring(xmlTree)
editor.beginUndoAction()
editor.setText(txt + "\r\n")
editor.convertEOLs(0)
editor.endUndoAction()
notepad.save()

# hitting UNDO now will return to the previous state of the session xml,
# so user could UNDO and SAVE to keep the original session xml file
