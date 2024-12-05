# encoding=utf-8
"""in response to https://github.com/bruderstein/PythonScript/issues/36#issuecomment-2517921387

"""
from Npp import editor1,editor2,notepad,console,BUFFERENCODING,MENUCOMMAND
import ctypes   # .windll, .addressof, .create_string_buffer
from ctypes.wintypes import HWND, UINT, WPARAM, LPARAM, HMODULE, LPCWSTR, LPCSTR, LPVOID
import sys
import os

SendMessageW = ctypes.windll.user32.SendMessageW
SendMessageW.argtypes = [HWND, UINT, WPARAM, LPARAM]
SendMessageW.restype = LPARAM

SCI_GETTEXT = 2182

console.show()

fnUTF8 = os.environ['TMP']+"\\pryrt.utf8"
with open(fnUTF8, "wt", encoding="utf8") as f:
    print('Ärger', file=f)

fnANSI = os.environ['TMP']+"\\pryrt.ansi"
with open(fnANSI, "wt", encoding="iso8859-1") as f:
    print('Ärger', file=f)

notepad.open(fnUTF8)
idUTF8 = notepad.getCurrentBufferID()

notepad.open(fnANSI)
idANSI = notepad.getCurrentBufferID()
notepad.menuCommand(MENUCOMMAND.VIEW_GOTO_ANOTHER_VIEW)

# first, confirm that PS3 editor.getText() doesn't handle ANSI correctly
notepad.activateBufferID(idUTF8)
try:
    txt = editor.getText()
    console.write(fnUTF8 + ":\t.getText() =>\t" + txt)
except UnicodeDecodeError as e:
    console.writeError(fnUTF8 + ":\t.getText() =>\tERROR = " + str(e) + "\n")

notepad.activateBufferID(idANSI)
try:
    txt = editor.getText()
    console.write(fnANSI + ":\t.getText() =>\t" + txt)
except UnicodeDecodeError as e:
    console.writeError(fnANSI + ":\t.getText() =>\tERROR = " + str(e) + "\n")

# now look at the SendMessageW instead of .getText()
notepad.activateBufferID(idUTF8)
#try:
if True:
    byte_length = SendMessageW(editor.hwnd, SCI_GETTEXT, 0, 0)
    byte_buffer = ctypes.create_string_buffer(byte_length + 1)
    SendMessageW(editor.hwnd, SCI_GETTEXT, byte_length, ctypes.addressof(byte_buffer))
    console.write("{}:\t.SCI_GETTEXT =>\t{}\t|\tCODEPAGE={}\n".format(fnUTF8, byte_buffer[:byte_length], editor.getCodePage()))
#except Exception as e:
#    console.writeError(fnUTF8 + ":\t.getText() =>\tERROR = " + str(e) + "\n")

notepad.activateBufferID(idANSI)
#try:
if True:
    byte_length = SendMessageW(editor.hwnd, SCI_GETTEXT, 0, 0)
    byte_buffer = ctypes.create_string_buffer(byte_length + 1)
    SendMessageW(editor.hwnd, SCI_GETTEXT, byte_length, ctypes.addressof(byte_buffer))
    console.write("{}:\t.SCI_GETTEXT =>\t{}\t|\tCODEPAGE={}\n".format(fnANSI, byte_buffer[:byte_length], editor.getCodePage()))
#except Exception as e:
#    console.writeError(idANSI + ":\t.getText() =>\tERROR = " + str(e) + "\n")

# I see that there is SCI_ENCODEDFROMUTF8/editor.encodedFromUTF8() to convert text
#   from internal UTF8 to the encoding used by the document,
#   but there does not appear to be an equivalent to convert from the document's encoding into UTF8
# Ah, but I did find SCI_GETCODEPAGE/editor.getCodePage()
#   ... it returns 65001 for UTF8, 0 if you choose ANSI, and 65001 for any of the NPP "character set" selections...
#   ... so you cannot figure out which codepage ANSI refers to on your machine, and
#       cannot figure out the character set for those, either. :-(
# At this point, I'm not sure that I can provide enough useful information, so not going to post it in the PS3 GH Issue yet

notepad.activateBufferID(idANSI)
notepad.close()
notepad.activateBufferID(idUTF8)
notepad.close()
