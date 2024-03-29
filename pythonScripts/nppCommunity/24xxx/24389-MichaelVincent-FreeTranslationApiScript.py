# Note: requires PythonScript 3
#import requests    #### per @rdipardo's updates on Michael's other script
import json
import urllib.request as requests
import urllib.parse

from enum import Enum

from Npp import editor, console

from WinDialog import Button, ComboBox, DefaultButton, Dialog, Label, TextBox
from WinDialog.win_helper import WindowStyle as WS

TITLE = "Translate"

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
    def __init__(self, text="", srclang="English", dstlang="English"):
        self.text = text
        self.trans = ""
        self.srclang = srclang
        self.dstlang = dstlang

class Translator(Dialog):
    """A Translator dialog interface."""
    def __init__(self, ret=Returns()):
        super().__init__(               title=TITLE         , center = True      , size=(250, 140) )
        self.translate = DefaultButton( title='&Translate'  , position=(80, 120), size=(50, 11)  )
        self.label1    = Label(         title='Text:'       , position=(10, 12)  , size=(35, 11)  )
        self.text      = TextBox(                             position=(45, 10)  , size=(195, 44) )
        self.swapt     = Button(        title='^&v'         , position=(20, 55)  , size=(20, 14)  )
        self.srclang   = ComboBox(                            position=(45, 56)  , size=(80, 14)  )
        self.swapl     = Button(        title='<&=>'        , position=(132, 55) , size=(20, 14)  )
        self.dstlang   = ComboBox(                            position=(160, 56) , size=(80, 14)  )
        self.label2    = Label(         title='Translated:' , position=(10, 72)  , size=(35, 11)  )
        self.trans     = TextBox(                             position=(45, 70)  , size=(195, 44) )
        self.replace   = Button(        title='&Replace'    , position=(135, 120) , size=(50, 11)  )
        self.close     = Button(        title='&Close'      , position=(190, 120), size=(50, 11)  )

        self.ret = ret

        self.onIdOk             = self.on_translate
        self.translate.onClick  = self.on_translate
        self.swapt.onClick      = self.on_swapt
        self.swapl.onClick      = self.on_swapl
        self.dstlang.onSelEndOk = self.on_translate
        self.replace.onClick    = self.on_replace
        self.close.onClick      = self.on_close

        self.srclang.style = self.dstlang.style | WS.TABSTOP
        self.dstlang.style = self.dstlang.style | WS.TABSTOP

        self.show()

    def initialize(self):
        """Initialize the dialog."""
        self.text.setText(self.ret.text)
        self._init_langs()

    def _init_langs(self):
        srclang = list(n.name for n in Languages)
        if self.ret.srclang in srclang:
            srclang.insert(0, self.ret.srclang)
        self.srclang.set(srclang)

        dstlang = list(n.name for n in Languages)
        if self.ret.dstlang in dstlang:
            dstlang.insert(0, self.ret.dstlang)
        self.dstlang.set(dstlang)

    def on_translate(self):
        """Translate the text."""
        ###text_encoded = requests.utils.quote(self.text.getText())
        text_encoded = urllib.parse.quote(self.text.getText())

        srclang = Languages[self.srclang.getSelectedItemText()]
        dstlang = Languages[self.dstlang.getSelectedItemText()]

        # Set return languages
        self.ret.srclang = srclang.name
        self.ret.dstlang = dstlang.name

        srccode = srclang.value
        dstcode = dstlang.value
        # EXAMPLE: LANGPAIR=EN|IT USING 2 LETTER ISO OR RFC3066 LIKE ZH-CN
        langpair = f"{srccode}|{dstcode}"

        ###r = requests.get(f"http://mymemory.translated.net/api/get?q={text_encoded}&langpair={langpair}")
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
        r = requests.urlopen(requests.Request(f"http://mymemory.translated.net/api/get?q={text_encoded}&langpair={langpair}", headers=headers))
        ###response = r.json()['responseData']['translatedText']
        console.writeError(f"r.status: {r.status}\nr.read: {r.read().decode('utf8')}");
        return;
        response = json.loads(r.read().decode('utf8'))['responseData']['translatedText']

        # Set return translation
        if response is not None:
            self.ret.trans = response
        else:
            self.ret.trans = "(no translation found)"
        self.trans.setText(self.ret.trans)

        # Set return text
        self.ret.text = self.text.getText()

    def on_swapl(self):
        """Swap languages."""
        self.ret.dstlang = self.srclang.getSelectedItemText()
        self.ret.srclang = self.dstlang.getSelectedItemText()
        self._init_langs()

    def on_swapt(self):
        """Swap texts."""
        self.ret.trans = self.text.getText()
        self.ret.text  = self.trans.getText()
        self.text.setText(self.ret.text)
        self.trans.setText(self.ret.trans)

    def on_replace(self):
        """Replace text with translation in document."""
        if self.ret.trans != "":
            editor.replaceSel(self.ret.trans)
            self.terminate()

    def on_close(self):
        """Close dialog."""
        self.terminate()


class Translate():
    """
    A translator service.
    """
    def __init__(self):
        self.text    = ""
        self.trans   = ""
        self.srclang = "English"
        self.dstlang = "English"

    def translate(self):
        text = editor.getSelText()
        if text is not None:
            self.text = text

        ret = Returns(self.text, self.srclang, self.dstlang)
        Translator(ret)
        self.text    = ret.text
        self.trans   = ret.trans
        self.srclang = ret.srclang
        self.dstlang = ret.dstlang

if __name__ == '__main__':
    try:
        isinstance(translate, Translate)
        # print("Translator `translate' already enabled")
    except NameError:
        translate = Translate()

    translate.translate()
