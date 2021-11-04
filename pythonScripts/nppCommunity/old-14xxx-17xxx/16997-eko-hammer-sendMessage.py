import ctypes
from Npp import notepad, LANGTYPE

LANGUAGES = LANGTYPE.values.values()
SendMessage = ctypes.windll.user32.SendMessageW

# #define NPPM_GETLANGUAGEDESC  (NPPMSG + 84)
NPPM_GETLANGUAGEDESC = 2024+84
# // INT NPPM_GETLANGUAGEDESC(int langType, TCHAR *langDesc)
# // Get programming language short description from the given language type (LangType)
# // Return value is the number of copied character / number of character to copy (\0 is not included)
# // You should call this function 2 times - the first time you pass langDesc as NULL to get the number of characters to copy.
# // You allocate a buffer of the length of (the number of characters + 1) then call NPPM_GETLANGUAGEDESC function the 2nd time
# // by passing allocated buffer as argument langDesc
npp_hwnd = ctypes.windll.user32.FindWindowW(u'Notepad++', None)
for i in range(10+1):
  for language in LANGUAGES:
    length = ctypes.windll.user32.SendMessageW(npp_hwnd, NPPM_GETLANGUAGEDESC, language, None)
    buffer = ctypes.create_unicode_buffer(length+1)
    return_value = ctypes.windll.user32.SendMessageW(npp_hwnd, NPPM_GETLANGUAGEDESC, language, ctypes.byref(buffer))
    print buffer.value

# crash
# for language in LANGUAGES:
    # print notepad.getLanguageDesc(language)
