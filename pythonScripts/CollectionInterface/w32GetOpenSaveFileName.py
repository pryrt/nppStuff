# encoding=utf-8
# https://gist.githubusercontent.com/nicomgd/1097a0b7ca3715da4e71/raw/80a92ca6f35d355a0dd1c7305ddd7e1c113726e3/getOpenFileName.py
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

OFN_ENABLESIZING        =0x00800000
OFN_PATHMUSTEXIST       =0x00000800
OFN_OVERWRITEPROMPT     =0x00000002
OFN_NOCHANGEDIR         =0x00000008
OFN_NOTESTFILECREATE    =0x00010000       # https://learn.microsoft.com/en-us/windows/win32/api/commdlg/ns-commdlg-openfilenamea
MAX_PATH=1024


def _buildOFN(title, default_extension, filter_string, fileBuffer):

  ofn = OPENFILENAME()
  ofn.lStructSize = ctypes.sizeof(OPENFILENAME)
  ofn.lpstrTitle = title
  ofn.lpstrFile = ctypes.cast(fileBuffer, LPTSTR)
  ofn.nMaxFile = MAX_PATH
  ofn.lpstrDefExt = default_extension
  ofn.lpstrFilter = filter_string
  ofn.Flags = OFN_ENABLESIZING | OFN_PATHMUSTEXIST | OFN_OVERWRITEPROMPT | OFN_NOCHANGEDIR | OFN_NOTESTFILECREATE
  return ofn


def getOpenFileName(title, default_extension, filter_string, initialPath):

  if initialPath is None:
    initialPath = ""
  filter_string = filter_string.replace("|", "\0")
  fileBuffer = ctypes.create_unicode_buffer(initialPath, MAX_PATH)
  ofn = _buildOFN(title, default_extension, filter_string, fileBuffer)

  if GetOpenFileName(ctypes.byref(ofn)):
    clean_name = (fileBuffer[:]).split("\0", 1)[0].rstrip("\0")
    return clean_name
  else:
    return None


def getSaveFileName(title, default_extension, filter_string, initialPath):

  if initialPath is None:
    initialPath = ""
  filter_string = filter_string.replace("|", "\0")
  fileBuffer = ctypes.create_unicode_buffer(initialPath, MAX_PATH)
  ofn = _buildOFN(title, default_extension, filter_string, fileBuffer)

  if GetSaveFileName(ctypes.byref(ofn)):
    clean_name = (fileBuffer[:]).split("\0", 1)[0].rstrip("\0")
    return clean_name
  else:
    return None
