# encoding=utf-8
"""collectionInterface--JustDialog

This is experimenting with Eko's WinDialog interface,
trying to get a form like

    [COMBOBOX]{UDL,AutoCompletion,FunctionList,Theme}
    [COMBOBOX]{pick from list}
    [DOWNLOAD] [CANCEL]

"""
from Npp import console, notepad, editor
from WinDialog import Dialog, Button, Label, ComboBox
from WinDialog.controls.combobox import CBS
from WinDialog.win_helper import WindowStyle as WS
rc = '''
1 DIALOGEX 0, 0, 180, 75
STYLE DS_SETFONT | DS_MODALFRAME | WS_POPUP | WS_CAPTION | WS_SYSMENU
CAPTION "Collection Interface"
LANGUAGE LANG_NEUTRAL, SUBLANG_NEUTRAL
FONT 9, "Segoe UI"
{
    CONTROL "Download"  , IDCDWN, BUTTON,            BS_PUSHBUTTON | WS_CHILD | WS_VISIBLE | WS_TABSTOP      , 10 , 50 , 80 , 14
    CONTROL "Cancel"    , IDCCAN, BUTTON,            BS_PUSHBUTTON | WS_CHILD | WS_VISIBLE | WS_TABSTOP      , 95 , 50 , 75 , 14
    CONTROL "Category:" , IDLCAT, STATIC,            SS_LEFT | WS_CHILD | WS_VISIBLE | WS_GROUP              , 10 , 13 , 30 , 9
    CONTROL ""          , IDCCAT, COMBOBOX,          CBS_DROPDOWNLIST | WS_CHILD | WS_VISIBLE | WS_TABSTOP   , 50 , 10 , 120 , 52
    CONTROL "File:"     , IDLFIL, STATIC,            SS_LEFT | WS_CHILD | WS_VISIBLE | WS_GROUP              , 10 , 31 , 30 , 9
    CONTROL ""          , IDCFIL, COMBOBOX,          CBS_DROPDOWN | CBS_DISABLENOSCROLL | WS_VSCROLL | WS_CHILD | WS_VISIBLE | WS_TABSTOP       , 50 , 30 , 120 , 1
}
'''



def on_selchange():
    choices = {
        'UDL': ([str(x) for x in range(101,110)]),
        'AutoCompletion': ([str(x) for x in range(101,110)]),
        'FunctionList': ([str(x) for x in range(201,210)]),
        'Theme': ([str(x) for x in range(1,100)])
    }
    selected_text = dlg.combobox_IDCCAT.getSelectedItemText()
    if selected_text in choices:
        dlg.combobox_IDCFIL.set(choices[selected_text])
    else:
        dlg.combobox_IDCFIL.set([])

def on_selchange2():
    print(u"{:>7d} {:s}".format(dlg.combobox_IDCFIL.getSelectedItem(),dlg.combobox_IDCFIL.getSelectedItemText()))

def on_init():
    dlg.combobox_IDCCAT.append(['UDL', 'AutoCompletion', 'FunctionList', 'Theme'])
    on_selchange()

dlg = WinDialog.create_dialog_from_rc(rc_code=rc)
dlg.center = True
dlg.combobox_IDCCAT.onSelChange = on_selchange
dlg.combobox_IDCFIL.onSelChange = on_selchange2
dlg.button_IDCCAN.onClick = dlg.terminate
dlg.initialize = on_init
#dlg.show()

class CollectionInterfaceDialog(Dialog):
    def __init__(self, title='Classy Collection Interface'):
        super().__init__(title)
        self.size = (180, 75)
        self.center = True

        self.dl_btn         = Button(title='&Download',     size=( 80, 14), position=(10, 50))
        self.dl_btn.onClick = self.on_download

        self.cancel_btn     = Button(title='&Cancel',       size=( 75, 14), position=(95, 50))
        self.cancel_btn.onClick = self.on_close

        self.category_lbl   = Label('Category:',            size=( 30,  9), position=(10, 13))
        self.category_cb    = ComboBox('' ,                 size=(120, 52), position=(50, 10))
        self.category_cb.onSelChange = self.on_category_change
        self.category_cb.style |= WS.TABSTOP

        self.file_lbl       = Label('File:',                size=( 30,  9), position=(10, 31))
        self.file_cb        = ComboBox('' ,                 size=(120, 11), position=(50, 30))
        self.file_cb.onSelChange = self.on_file_change
        self.file_cb.style |= WS.TABSTOP |  CBS.DISABLENOSCROLL | WS.VSCROLL

        self.initialize = self.on_init
        self.show()

    def on_download(self):
        notepad.messageBox(
            'download {}/{}'.format(self.category_cb.getSelectedItemText(),self.file_cb.getSelectedItemText()),
            "Downloading"
        )

    def on_close(self):
        self.terminate()

    def on_category_change(self):
        choices = {
            'UDL': ([str(x) for x in range(101,110)]),
            'AutoCompletion': ([str(x) for x in range(201,310)]),
            'FunctionList': ([str(x) for x in range(231,310)]),
            'Theme': ([str(x) for x in range(1,100)])
        }
        selected_text = self.category_cb.getSelectedItemText()
        if selected_text in choices:
            self.file_cb.set(choices[selected_text])
        else:
            self.file_cb.set([])

    def on_file_change(self):
        pass

    def on_init(self):
        self.category_cb.append(['UDL', 'AutoCompletion', 'FunctionList', 'Theme'])
        self.on_category_change()


CollectionInterfaceDialog()
