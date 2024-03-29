import json
import urllib.request as requests
import urllib.parse

from enum import Enum

from Npp import editor

from WinDialog import Button, ComboBox, DefaultButton, Dialog, Label, TextBox
from WinDialog.win_helper import WindowStyle as WS

TITLE = "Translate"
DEFAULTLANG = "English"

class Languages(Enum):
    """Translated language options."""
    Chinese    = "zh"
    English    = "en"
    French     = "fr"
    German     = "de"
    Italian    = "it"
    Japanese   = "ja"
    Portuguese = "pt"
    Russian    = "ru"
    Spanish    = "es"

class Returns(object):
    """The input / output for the Translator service."""
    def __init__(self, text="", srclang=DEFAULTLANG, dstlang=DEFAULTLANG):
        self.text = text
        self.trans = ""
        self.srclang = srclang
        self.dstlang = dstlang

class Translator(Dialog):
    """A Translator dialog interface."""
    def __init__(self, ret=Returns()):
        super().__init__(               title=TITLE         , center = True      , size=(290, 165) )
        self.translate = DefaultButton( title='&Translate'  , position=(120, 145), size=(50, 11)  )
        self.label1    = Label(         title='Text:'       , position=(10, 12)  , size=(35, 11)  )
        self.text      = TextBox(                             position=(45, 10)  , size=(235, 55) )
        self.swapt     = Button(        title='^&v'         , position=(45, 67)  , size=(20, 14)  )
        self.srclang   = ComboBox(                            position=(75, 68)  , size=(80, 14)  )
        self.swapl     = Button(        title='<&=>'        , position=(165, 67) , size=(20, 14)  )
        self.dstlang   = ComboBox(                            position=(200, 68) , size=(80, 14)  )
        self.label2    = Label(         title='Translated:' , position=(10, 84)  , size=(35, 11)  )
        self.trans     = TextBox(                             position=(45, 82)  , size=(235, 55) )
        self.replace   = Button(        title='&Replace'    , position=(175, 145), size=(50, 11)  )
        self.close     = Button(        title='&Close'      , position=(230, 145), size=(50, 11)  )

        self.ret = ret

        self.onIdOk             = self._on_translate
        self.translate.onClick  = self._on_translate
        self.swapt.onClick      = self._on_swapt
        self.swapl.onClick      = self._on_swapl
        self.srclang.onSelEndOk = self._on_translate
        self.dstlang.onSelEndOk = self._on_translate
        self.replace.onClick    = self._on_replace
        self.close.onClick      = self._on_close

        self.srclang.style = self.srclang.style | WS.TABSTOP
        self.dstlang.style = self.dstlang.style | WS.TABSTOP
        self.text.style    = self.text.style    | WS.VSCROLL # | WS.HSCROLL
        self.trans.style   = self.trans.style   | WS.VSCROLL # | WS.HSCROLL

        self.show()

    def initialize(self):
        """Initialize the dialog."""
        self.text.setText(self.ret.text)
        self._init_langs()
        if self.ret.srclang != self.ret.dstlang and self.ret.text != "":
            self._on_translate()

    def _init_langs(self):
        srclang = list(n.name for n in Languages)
        if self.ret.srclang in srclang:
            srclang.insert(0, self.ret.srclang)
        self.srclang.set(srclang)

        dstlang = list(n.name for n in Languages)
        if self.ret.dstlang in dstlang:
            dstlang.insert(0, self.ret.dstlang)
        self.dstlang.set(dstlang)

    def _on_translate(self):
        """Translate the text."""
        if self.text.getText() == "":
            return

        text_encoded = urllib.parse.quote(self.text.getText())

        srclang = Languages[self.srclang.getSelectedItemText()]
        dstlang = Languages[self.dstlang.getSelectedItemText()]
        if srclang == dstlang:
            return

        # Set return languages
        self.ret.srclang = srclang.name
        self.ret.dstlang = dstlang.name

        srccode = srclang.value
        dstcode = dstlang.value
        # EXAMPLE: LANGPAIR=EN|IT USING 2 LETTER ISO OR RFC3066 LIKE ZH-CN
        langpair = f"{srccode}|{dstcode}"

        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
        r = requests.urlopen(requests.Request(url=f"http://mymemory.translated.net/api/get?q={text_encoded}&langpair={langpair}", headers=headers))
        if r.status != 200:
            return

        ret = r.read()
        response = json.loads(ret.decode('utf8'))['responseData']['translatedText']
        # Set return translation
        if response is not None:
            self.ret.trans = response
        else:
            self.ret.trans = "(no translation found)"
        self.trans.setText(self.ret.trans)

        # Set return text
        self.ret.text = self.text.getText()

    def _on_swapl(self):
        """Swap languages."""
        self.ret.dstlang = self.srclang.getSelectedItemText()
        self.ret.srclang = self.dstlang.getSelectedItemText()
        self._init_langs()
        self._on_translate()

    def _on_swapt(self):
        """Swap texts."""
        self.ret.trans = self.text.getText()
        self.ret.text  = self.trans.getText()
        self.text.setText(self.ret.text)
        self.trans.setText(self.ret.trans)
        self._on_swapl()

    def _on_replace(self):
        """Replace text with translation in document."""
        if self.ret.trans != "":
            editor.replaceSel(self.ret.trans)
            self.terminate()

    def _on_close(self):
        self.terminate()

class Translate():
    """A translator service."""
    def __init__(self):
        self.srclang = DEFAULTLANG
        self.dstlang = DEFAULTLANG

    def _editor_getWordAtCaretOrSelection(self):
        retval = ''
        (sel_start, sel_end) = (editor.getSelectionStart(), editor.getSelectionEnd())
        if editor.getSelections() == 1 and sel_start != sel_end:
            retval = editor.getTextRange(sel_start, sel_end)
        else:
            start_of_word_pos = editor.wordStartPosition(editor.getCurrentPos(), True)
            end_of_word_pos = editor.wordEndPosition(start_of_word_pos, True)
            if start_of_word_pos != end_of_word_pos:
                retval = editor.getTextRange(start_of_word_pos, end_of_word_pos)
                editor.setSelection(end_of_word_pos, start_of_word_pos)
        return retval

    def translate(self):
        text = ""
        if editor.getSelectionEmpty():
            sel = self._editor_getWordAtCaretOrSelection()
            if len(sel) > 0: 
                text = sel
        else:
            text = editor.getSelText()

        ret = Returns(text, self.srclang, self.dstlang)
        Translator(ret)
        self.srclang = ret.srclang
        self.dstlang = ret.dstlang


Translate().translate()
