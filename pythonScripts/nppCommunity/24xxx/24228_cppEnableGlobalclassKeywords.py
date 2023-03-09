# encoding=utf-8
"""in response to https://community.notepad-plus-plus.org/topic/24228/

The C++ lexer from Scintilla/Lexilla comes with a fourth category for keywords,
which uses the style SCE_C_GLOBALCLASS (StyleID=19), which uses keyword index 3.
But it is not enabled in the Notepad++ application.  This script will enable that.

Installation instructions:
1. Main Instructions =  https://community.notepad-plus-plus.org/topic/23039/faq-desk-how-to-install-and-run-a-script-in-pythonscript
2. Save this as cppEnableGlobalclassKeywords.py (per Main Instructions)
3. set the colorForeground , colorBackground, and keywordList starting on line 27, and save
4. put the lines between the ``` in your startup script -- do not indent, do not include the ```
    (see info in the "startup script" section of the Main Instructions)
```
import cppEnableGlobalclassKeywords
lexer_interface_cpp_globalclass = cppEnableGlobalclassKeywords.cppEnableGlobalclassKeywords()
```

"""
from Npp import editor,notepad,console,NOTIFICATION

class cppEnableGlobalclassKeywords(object):
    '''
    To configure, set the foreground and background RGB triples here, as well as
    the space/newline-separated keyword list
    '''
    colorForeground = (0,128,128)   # example foreground: dark cyan
    colorBackground = (255,255,0)   # example background: yellow
    keywordList = """
        UPROPERTY UFUNCTION UCLASS USTRUCT GENERATED_BODY
        AdvancedDisplay AssetRegistrySearchable BlueprintAssignable
        BlueprintAuthorityOnly BlueprintCallable BlueprintGetter
        BlueprintReadOnly BlueprintReadWrite BlueprintSetter
        Config Const DuplicateTransient EditAnywhere EditDefaultsOnly
        EditFixedSize EditInline EditInstanceOnly Export FieldNotify
        Getter GlobalConfig Instanced Interp Localized NoClear
        NonPIEDuplicateTransient NonPIETransient NonTransactional
        NotReplicated Ref Replicated ReplicatedUsing RepRetry SaveGame
        Setter SimpleDisplay SkipSerialization TextExportTransient
        Transient VisibleAnywhere VisibleDefaultsOnly VisibleInstanceOnly
        BlueprintAuthorityOnly BlueprintCallable BlueprintCosmetic BlueprintGetter
        BlueprintImplementableEvent BlueprintNativeEvent BlueprintPure
        BlueprintSetter Client CustomThunk Exec FieldNotify NetMulticast Reliable
        SealedEvent Server ServiceRequest ServiceResponse Unreliable WithValidation
        """

    def __init__(self):
        self.SCE_C_GLOBALCLASS = 19
        self.keywords3 = 3
        notepad.callback(self.on_event, [NOTIFICATION.BUFFERACTIVATED, NOTIFICATION.LANGCHANGED])
        self.on_event(None)
        console.write("Registered cppEnableGlobalclassKeywords for C/C++ GLOBALCLASS Keywords\n")

    def on_event(self,args):
        lexer = editor.getLexerLanguage()
        if lexer == "cpp":
            self.update_cpp()

    def update_cpp(self):
        editor.styleSetFore(self.SCE_C_GLOBALCLASS, self.colorForeground)
        editor.styleSetBack(self.SCE_C_GLOBALCLASS, self.colorBackground)
        editor.setKeyWords(self.keywords3, self.keywordList)

if __name__ == '__main__':
    lexer_interface_cpp_globalclass = cppEnableGlobalclassKeywords()

"""

The ScintillaEditView::setCppLexer [here](https://github.com/notepad-plus-plus/notepad-plus-plus/blob/c8e4e671dad405d60e95ba483991a4b3b77bf2c2/PowerEditor/src/ScintillaComponent/ScintillaEditView.cpp#L929)
only maps
- instre1=>0    which is keywords.  which goes to SCE_C_WORD  (StyleID=5) in LexCPP.cpp/SciLexer.h
- type1=>1      which is keywords2. which goes to SCE_C_WORD2 (StyleID=16)
- type2=>2      which is keywords3. which goes to SCE_C_COMMENTDOCKEYWORD (StyleID=17)
    and while langs.xml defines the list, stylers.xml does not map COMMENT DOC KEYWORD
    to keywordClass="type2", so Style Configurator doesn't show that keyword list in
    the GUI; this is because setCppLexer() also does not check the user-defined keywords
    for type2, and if it showed up in GUI, users would assume they could add words to
    that list
    - these "COMMENT DOC KEYWORD"s are the doxygen and similar syntax in specially-formulated
      comment blocks, and require a prefix like \ or @ while inside that block in order
      to show up as highlighted
For completeness,
- undefined=>3  which is keywords4. which goes to SCE_C_GLOBALCLASS (StyleID=19)

Author: Peter C. Jones (pryrt)

"""
