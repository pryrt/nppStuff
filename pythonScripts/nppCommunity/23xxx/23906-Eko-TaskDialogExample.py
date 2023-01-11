# -*- coding: utf-8 -*-
"""
Author: @Ekopalypse
Forum:  https://community.notepad-plus-plus.org/topic/23906/finding-available-shortcut-keys-originally-where-s-the-new-window-command/29
Gist:   https://gist.github.com/Ekopalypse/5771d3677735816a106ab698b8a989a3
"""
import platform
import ctypes
from ctypes import wintypes


LRESULT = LONG_PTR = wintypes.LONG if platform.architecture()[0] == '32bit' else wintypes.LARGE_INTEGER

FindWindow = ctypes.windll.user32.FindWindowW
FindWindow.argtypes = [wintypes.LPCWSTR, wintypes.LPCWSTR]
FindWindow.restype = wintypes.HWND

GetModuleHandle = ctypes.windll.kernel32.GetModuleHandleW
GetModuleHandle.argtypes = [wintypes.LPCWSTR]
GetModuleHandle.restype = wintypes.HMODULE

LoadResource = ctypes.windll.kernel32.LoadResource
LoadResource.argtypes = [wintypes.HMODULE, wintypes.HRSRC]
LoadResource.restype = wintypes.HGLOBAL

# HRSRC FindResourceExA(
  # [in, optional] HMODULE hModule,
  # [in]           LPCSTR  lpType,
  # [in]           LPCSTR  lpName,
  # [in]           WORD    wLanguage
# );

FindResource = ctypes.windll.kernel32.FindResourceExA
FindResource.argtypes = [wintypes.HMODULE,
                         LONG_PTR,  # because we are using the resource from Npp itself, we use an integer instead of a pointer
                         LONG_PTR,  # because we are using the resource from Npp itself, we use an integer instead of a pointer
                         wintypes.WORD]
FindResource.restype = wintypes.HRSRC

FreeResource = ctypes.windll.kernel32.FreeResource
FreeResource.argtypes = [wintypes.HGLOBAL]
FreeResource.restype = wintypes.BOOL

LockResource = ctypes.windll.kernel32.LockResource
LockResource.argtypes = [wintypes.HGLOBAL]
LockResource.restype = wintypes.LPVOID

SizeofResource = ctypes.windll.kernel32.SizeofResource
SizeofResource.argtypes = [wintypes.HMODULE, wintypes.HRSRC]
SizeofResource.restype = wintypes.DWORD

CreateIconFromResource = ctypes.windll.user32.CreateIconFromResourceEx
CreateIconFromResource.argtypes = [ctypes.POINTER(ctypes.c_byte),
                                   wintypes.DWORD,
                                   wintypes.BOOL,
                                   wintypes.DWORD,
                                   wintypes.INT,
                                   wintypes.INT,
                                   wintypes.UINT]
CreateIconFromResource.restype = wintypes.HICON

SendMessage = ctypes.windll.user32.SendMessageW
SendMessage.argtypes = [wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM]
SendMessage.restype = LRESULT

HRESULT = wintypes.LONG
TASKDIALOGCALLBACK = ctypes.WINFUNCTYPE(HRESULT,
                                        wintypes.HWND,
                                        wintypes.UINT,
                                        wintypes.WPARAM,
                                        wintypes.LPARAM,
                                        LONG_PTR)

# defined in commctrl.h

class TDM:
    # task dialog messages
    NAVIGATE_PAGE                       = 1125  # wParam = 0, lParam addressof new config structure
    CLICK_BUTTON                        = 1126  # wParam = Button ID
    SET_MARQUEE_PROGRESS_BAR            = 1127  # wParam = 0 (nonMarque) wParam != 0 (Marquee)
    SET_PROGRESS_BAR_STATE              = 1128  # wParam = new progress state
    SET_PROGRESS_BAR_RANGE              = 1129  # lParam = MAKELPARAM(nMinRange, nMaxRange)
    SET_PROGRESS_BAR_POS                = 1130  # wParam = new position
    SET_PROGRESS_BAR_MARQUEE            = 1131  # wParam = 0 (stop marquee), wParam != 0 (start marquee), lparam = speed (milliseconds between repaints)
    SET_ELEMENT_TEXT                    = 1132  # wParam = element (TASKDIALOG_ELEMENTS), lParam = new element text (LPCWSTR)
    CLICK_RADIO_BUTTON                  = 1134  # wParam = Radio Button ID
    ENABLE_BUTTON                       = 1135  # lParam = 0 (disable), lParam != 0 (enable), wParam = Button ID
    ENABLE_RADIO_BUTTON                 = 1136  # lParam = 0 (disable), lParam != 0 (enable), wParam = Radio Button ID
    CLICK_VERIFICATION                  = 1137  # wParam = 0 (unchecked), 1 (checked), lParam = 1 (set key focus)
    UPDATE_ELEMENT_TEXT                 = 1138  # wParam = element (TASKDIALOG_ELEMENTS), lParam = new element text (LPCWSTR)
    SET_BUTTON_ELEVATION_REQUIRED_STATE = 1139  # wParam = Button ID, lParam = 0 (elevation not required), lParam != 0 (elevation required)
    UPDATE_ICON                         = 1140  # wParam = icon element (TASKDIALOG_ICON_ELEMENTS), lParam = new icon (hIcon if TDF_USE_HICON_* was set, PCWSTR otherwise)


class TDN:
    # task dialog notifications
    CREATED                 = 0
    NAVIGATED               = 1
    BUTTON_CLICKED          = 2   # wParam = Button ID
    HYPERLINK_CLICKED       = 3   # lParam = (LPCWSTR)pszHREF
    TIMER                   = 4   # wParam = Milliseconds since dialog created or timer reset
    DESTROYED               = 5
    RADIO_BUTTON_CLICKED    = 6   # wParam = Radio Button ID
    DIALOG_CONSTRUCTED      = 7
    VERIFICATION_CLICKED    = 8   # wParam = 1 if checkbox checked, 0 if not, lParam is unused and always 0
    HELP                    = 9
    EXPANDO_BUTTON_CLICKED  = 10  # wParam = 0 (dialog is now collapsed), wParam != 0 (dialog is now expanded)


class TDF:
    # task dialog flags
    ENABLE_HYPERLINKS           = 0x1
    USE_HICON_MAIN              = 0x2
    USE_HICON_FOOTER            = 0x4
    ALLOW_DIALOG_CANCELLATION   = 0x8
    USE_COMMAND_LINKS           = 0x10
    USE_COMMAND_LINKS_NO_ICON   = 0x20
    EXPAND_FOOTER_AREA          = 0x40
    EXPANDED_BY_DEFAULT         = 0x80
    VERIFICATION_FLAG_CHECKED   = 0x100
    SHOW_PROGRESS_BAR           = 0x200
    SHOW_MARQUEE_PROGRESS_BAR   = 0x400
    CALLBACK_TIMER              = 0x800
    POSITION_RELATIVE_TO_WINDOW = 0x1000
    RTL_LAYOUT                  = 0x2000
    NO_DEFAULT_RADIO_BUTTON     = 0x4000
    CAN_BE_MINIMIZED            = 0x8000
# if (NTDDI_VERSION >= NTDDI_WIN8)
    NO_SET_FOREGROUND           = 0x10000,  # Don't call SetForegroundWindow() when activating the dialog
# endif # (NTDDI_VERSION >= NTDDI_WIN8)
    SIZE_TO_CONTENT             = 0x1000000   # used by ShellMessageBox to emulate MessageBox sizing behavior


class TASKDIALOG_BUTTON(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('nButtonID',     wintypes.INT),
        ('pszButtonText', wintypes.LPCWSTR)
    ]


class TASKDIALOGCONFIG(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('cbSize',                  wintypes.UINT),
        ('hwndParent',              wintypes.HWND),
        ('hInstance',               wintypes.HINSTANCE),
        ('dwFlags',                 wintypes.UINT),  # TASKDIALOG_FLAGS),
        ('dwCommonButtons',         wintypes.UINT),  # TASKDIALOG_COMMON_BUTTON_FLAGS),
        ('pszWindowTitle',          wintypes.LPCWSTR),
        ('hMainIcon',               wintypes.HICON),
        ('pszMainInstruction',      wintypes.LPCWSTR),
        ('pszContent',              wintypes.LPCWSTR),
        ('cButtons',                wintypes.UINT),
        ('pButtons',                ctypes.POINTER(TASKDIALOG_BUTTON)),
        ('nDefaultButton',          wintypes.INT),
        ('cRadioButtons',           wintypes.UINT),
        ('pRadioButtons',           ctypes.POINTER(TASKDIALOG_BUTTON)),
        ('nDefaultRadioButton',     wintypes.INT),
        ('pszVerificationText',     wintypes.LPCWSTR),
        ('pszExpandedInformation',  wintypes.LPCWSTR),
        ('pszExpandedControlText',  wintypes.LPCWSTR),
        ('pszCollapsedControlText', wintypes.LPCWSTR),
        ('hFooterIcon',             wintypes.HICON),
        ('pszFooter',               wintypes.LPCWSTR),
        ('pfCallback',              TASKDIALOGCALLBACK),  # PFTASKDIALOGCALLBACK),
        ('lpCallbackData',          LONG_PTR),
        ('cxWidth',                 wintypes.UINT),
    ]

    def __init__(self):
        self.cbSize = ctypes.sizeof(self)


TaskDialogIndirect = ctypes.windll.Comctl32.TaskDialogIndirect
TaskDialogIndirect.argtypes = [ctypes.POINTER(TASKDIALOGCONFIG),
                               ctypes.POINTER(wintypes.INT),
                               ctypes.POINTER(wintypes.INT),
                               ctypes.POINTER(wintypes.BOOL)]
TaskDialogIndirect.restype = HRESULT

def return_icon_handle(width=16, height=16, item=2):
    # load icon from npp executable
    resource_handle = FindResource(None, 3, item, 1033) # 3=Icon, 2=second icon in resource table, 1033=Language
    data_handle = LoadResource(None, resource_handle)
    size = SizeofResource(None, resource_handle)
    ptr = LockResource(data_handle)
    __ptr = ctypes.cast(ptr, ctypes.POINTER(ctypes.c_byte))
    icon_handle = CreateIconFromResource(__ptr, size, True, 0x00030000, width, height, 0)
    FreeResource(data_handle)

    return icon_handle


class TASK_DIALOG:

    def __init__(self, flags=None, debug=False):
        self.event_handler = {
            TDN.CREATED: self.on_created,
            TDN.NAVIGATED: self.on_navigated,
            TDN.BUTTON_CLICKED: self.on_button_clicked,
            TDN.HYPERLINK_CLICKED: self.on_hyperlink_clicked,
            TDN.TIMER: self.on_timer,
            TDN.DESTROYED: self.on_destroyed,
            TDN.RADIO_BUTTON_CLICKED: self.on_radio_button_clicked,
            TDN.DIALOG_CONSTRUCTED: self.on_dialog_constructed,
            TDN.VERIFICATION_CLICKED: self.on_verification_clicked,
            TDN.HELP: self.on_help,
            TDN.EXPANDO_BUTTON_CLICKED: self.on_expand_button_clicked,
        }
        self.debug = debug
        self.hwnd = None
        self.aborted = False
        self.checked_verification = None
        self.checked_radio_btn = None
        self.do_check_verification = False

        self.config = TASKDIALOGCONFIG()
        self.config.hwndParent = FindWindow(u'Notepad++', None)
        self.config.hInstance = GetModuleHandle(u"notepad++.exe")
        if self.debug: print(self.config.hInstance)
        if flags is None:
            self.config.dwFlags = TDF.ALLOW_DIALOG_CANCELLATION | TDF.SIZE_TO_CONTENT
        else:
            self.config.dwFlags = (flags
                    | TDF.ALLOW_DIALOG_CANCELLATION  # or is needed as flags might be None
                    | TDF.SIZE_TO_CONTENT
                    # | TDF.USE_COMMAND_LINKS
                    # | TDF.USE_HICON_MAIN
                    # | TDF.USE_HICON_FOOTER
                    # | TDF.SHOW_MARQUEE_PROGRESS_BAR
                    )
        if self.debug: print('self.config.dwFlags: ', hex(self.config.dwFlags))

        self.dwCommonButtons = None
        self.config.pszWindowTitle = 'TASK_DIALOG'
        self.config.pszMainInstruction = ''
        self.config.hMainIcon = return_icon_handle(32, 32)
        if self.debug: print('self.config.hMainIcon: ', self.config.hMainIcon)
        self.config.pfCallback = TASKDIALOGCALLBACK(self.dialog_callback)
        self.button_callbacks = {}
        # self.radio_button_callbacks = {}


    def __create_buttons(self, list_of_buttons):
        buttons_array = (TASKDIALOG_BUTTON * len(list_of_buttons))()
        for i, button in enumerate(list_of_buttons):
            buttons_array[i].nButtonID = button[0]
            buttons_array[i].pszButtonText = button[1]
            self.button_callbacks[button[0]] = None if len(button) < 3 else button[2]
            # self.radio_button_callbacks[button[0]] = lambda x:1 if len(button) < 3 else button[2]
        return buttons_array

    def create_page(self,
                    title=None,
                    push_buttons=None,
                    radio_buttons=None,
                    main_instruction=None,
                    content=None,
                    default_button=None,
                    default_radio_button=None,
                    verification_text=None,
                    expanded_information=None,
                    expanded_control_text=None,
                    collapsed_control_text=None,
                    footer=None,
                    width=None):

        if title:
            self.config.pszWindowTitle = title

        if main_instruction:
            self.config.pszMainInstruction = main_instruction

        if content:
            self.config.pszContent = content

        if push_buttons is None:
            pass
        elif len(push_buttons) == 0:
            self.config.cButtons = 0
        else:
            self.config.cButtons = len(push_buttons)
            self.config.pButtons = self.__create_buttons(push_buttons)

        if default_button:
            self.config.nDefaultButton = default_button

        if radio_buttons is None:
            pass
        elif len(radio_buttons) == 0:
            self.config.cRadioButtons = 0
        else:
            self.config.cRadioButtons = len(radio_buttons)
            self.config.pRadioButtons = self.__create_buttons(radio_buttons)

        if default_radio_button:
            self.config.nDefaultRadioButton = default_radio_button

        if verification_text:
            self.checked_verification = 0
            if self.do_check_verification:
                self.config.dwFlags |= TDF.VERIFICATION_FLAG_CHECKED
                self.checked_verification = 1
            self.config.pszVerificationText = verification_text
        elif verification_text is None:
            self.config.pszVerificationText = None

        if expanded_information:
            self.config.pszExpandedInformation = expanded_information

        if expanded_control_text:
            self.config.pszExpandedControlText = expanded_control_text

        if collapsed_control_text:
            self.config.pszCollapsedControlText = collapsed_control_text

        if footer:
            self.config.pszFooter = footer

        self.config.cxWidth = width if width is not None else self.config.cxWidth

        SendMessage(self.hwnd, TDM.NAVIGATE_PAGE, 0, ctypes.addressof(self.config))


    def dialog_callback(self, hwnd, msg, wparam, lparam, lpRefData):
        if msg in self.event_handler:
            return self.event_handler[msg](hwnd, msg, wparam, lparam, lpRefData)
        return 1

    def on_created(self, hwnd, msg, wparam, lparam, lpRefData):
        if self.debug: print('on_created:', hwnd, msg, wparam, lparam, lpRefData)
        return 1

    def on_navigated(self, hwnd, msg, wparam, lparam, lpRefData):
        if self.debug: print('on_navigated', hwnd, msg, wparam, lparam, lpRefData)
        return 1

    def on_hyperlink_clicked(self, hwnd, msg, wparam, lparam, lpRefData):
        if self.debug: print('on_hyperlink_clicked', hwnd, msg, wparam, lparam, lpRefData)
        return 1

    def on_timer(self, hwnd, msg, wparam, lparam, lpRefData):
        if self.debug: print('on_timer', hwnd, msg, wparam, lparam, lpRefData)
        return 1

    def on_destroyed(self, hwnd, msg, wparam, lparam, lpRefData):
        if self.debug: print('on_destroyed', hwnd, msg, wparam, lparam, lpRefData)
        return 1

    def __on_button_clicked(self, wparam):
        callback = self.button_callbacks[wparam]
        if callback is not None:
            res = callback(wparam)
            if res in [0, 1]:
                return res
        return 1

    def on_button_clicked(self, hwnd, msg, wparam, lparam, lpRefData):
        if wparam == 2:  # ensures that the dialog can be cancelled
            self.aborted = True
            return 0
        callback = self.button_callbacks[wparam]
        if callback is not None:
            res = callback(wparam)
            if res in [0, 1]:
                return res
        return 1
        # return self.__on_button_clicked(wparam)

    def on_radio_button_clicked(self, hwnd, msg, wparam, lparam, lpRefData):
        if self.debug: print('on_radio_button_clicked', hwnd, msg, wparam, lparam, lpRefData)
        callback = self.button_callbacks[wparam]
        if callback is not None:
            res = callback(wparam)
            if res in [0, 1]:
                return res
        return 1
        # return self.__on_button_clicked(wparam)

    def on_dialog_constructed(self, hwnd, msg, wparam, lparam, lpRefData):
        if self.debug: print('on_dialog_constructed', hwnd, msg, wparam, lparam, lpRefData)
        self.hwnd = hwnd
        return 1

    def on_verification_clicked(self, hwnd, msg, wparam, lparam, lpRefData):
        if self.debug: print('on_verification_clicked', hwnd, msg, wparam, lparam, lpRefData)
        self.checked_verification = wparam
        return 1

    def on_help(self, hwnd, msg, wparam, lparam, lpRefData):
        if self.debug: print('on_help', hwnd, msg, wparam, lparam, lpRefData)
        return 1

    def on_expand_button_clicked(self, hwnd, msg, wparam, lparam, lpRefData):
        if self.debug: print('on_expand_button_clicked', hwnd, msg, wparam, lparam, lpRefData)
        return 1


    def show(self):
        res = TaskDialogIndirect(
            ctypes.byref(self.config),
            None,
            None,
            None if self.checked_verification is None else ctypes.byref(wintypes.INT(self.checked_verification))
        )
        if self.debug: print('show returned:', res)


if __name__ == '__main__':

    def on_close(id):
        return 0

    def on_option(id):
        print('on_option:', id)

    def on_option2(id):
        print('on_option2:', id)

    def on_next(id):
        MyDialog.create_page(
            title = 'modified window title',  # Overwrite existing attribute or set new one if it was not set before.
            verification_text = None,  # Remove attribute from dialog
            push_buttons = [(1000, 'Close', on_close)]
        )

    MyDialog = TASK_DIALOG(flags=TDF.USE_COMMAND_LINKS | TDF.USE_HICON_MAIN, debug=False)
    MyDialog.create_page(
        title = 'my window title',
        push_buttons = [(1000, 'Close this task', on_close), (1001, 'Next', on_next)],
        radio_buttons = [
            (2000, 'option &0', on_option),
            (2001, 'option 1', on_option2),
            (2002, 'option 2', on_option2),
            (2003, 'option &3', on_option),
        ],
        main_instruction = 'my main instructions',
        content = 'This is the content used to determine the size of the dialog if no width is specified',
        default_button = 1001,
        default_radio_button = 2000,
        verification_text = 'agree to it?',
        expanded_information = 'kinda suspicios??',  # if used with |TDF.EXPAND_FOOTER_AREA goes into the footer area
        collapsed_control_text = 'show collapsed text',
        expanded_control_text = 'collapse suspicios text',
        footer = 'shoot the foot',
        width = 400
    )

    MyDialog.show()
    print(MyDialog.checked_verification)
