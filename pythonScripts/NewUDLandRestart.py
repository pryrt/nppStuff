# encoding=utf-8
"""NewUDLandRestart.py

Create a new (empty) UDL which is fully transparent, and restart Notepad++ so that it will exist in the right file with reasonable colors, rather than assuming black-on-white and bold+italic+underline and putting it in the old global UDL XML file.
"""
from Npp import notepad, NOTIFICATION, console, editor, MENUCOMMAND
import os, re, subprocess, ctypes
from ctypes import wintypes

nppexe = os.path.join( notepad.getNppDir(), 'notepad++.exe' );

udlName = notepad.prompt( "UDL Name", "Create New UDL and Restart", "DummyName (paren)")
if udlName is None:
    raise Exception("")

udlFile = re.sub(r'[^\w]', '_', udlName) + ".xml"
udlFolder = os.path.join( os.path.dirname(os.path.dirname(notepad.getPluginConfigDir())), 'userDefineLangs')
udlPath = os.path.join( udlFolder, udlFile )

udlFG = editor.styleGetFore(0)
udlBG = editor.styleGetBack(0)
hexFG = "#{:02X}{:02X}{:02X}".format(udlFG[0],udlFG[1],udlFG[2])
hexBG = "#{:02X}{:02X}{:02X}".format(udlBG[0],udlBG[1],udlBG[2])

console.write( str({'folder':udlFolder, 'name':udlName, 'file':udlFile, 'path':udlPath, 'FG':str(udlFG), 'BG':str(udlBG), 'hexFG':hexFG, 'hexBG':hexBG}) + "\n" )

template = """<!-- autogenerated dummy '{udl_file}' for '{udl_name}' using fg='{udl_fg}' bg='{udl_bg}' from active theme -->
<NotepadPlus>
    <UserLang name="{udl_name}" ext="" udlVersion="2.1">
        <Settings>
            <Global caseIgnored="no" allowFoldOfComments="no" foldCompact="no" forcePureLC="0" decimalSeparator="0" />
            <Prefix Keywords1="no" Keywords2="no" Keywords3="no" Keywords4="no" Keywords5="no" Keywords6="no" Keywords7="no" Keywords8="no" />
        </Settings>
        <KeywordLists>
            <Keywords name="Comments"></Keywords>
            <Keywords name="Numbers, prefix1"></Keywords>
            <Keywords name="Numbers, prefix2"></Keywords>
            <Keywords name="Numbers, extras1"></Keywords>
            <Keywords name="Numbers, extras2"></Keywords>
            <Keywords name="Numbers, suffix1"></Keywords>
            <Keywords name="Numbers, suffix2"></Keywords>
            <Keywords name="Numbers, range"></Keywords>
            <Keywords name="Operators1"></Keywords>
            <Keywords name="Operators2"></Keywords>
            <Keywords name="Folders in code1, open"></Keywords>
            <Keywords name="Folders in code1, middle"></Keywords>
            <Keywords name="Folders in code1, close"></Keywords>
            <Keywords name="Folders in code2, open"></Keywords>
            <Keywords name="Folders in code2, middle"></Keywords>
            <Keywords name="Folders in code2, close"></Keywords>
            <Keywords name="Folders in comment, open"></Keywords>
            <Keywords name="Folders in comment, middle"></Keywords>
            <Keywords name="Folders in comment, close"></Keywords>
            <Keywords name="Keywords1"></Keywords>
            <Keywords name="Keywords2"></Keywords>
            <Keywords name="Keywords3"></Keywords>
            <Keywords name="Keywords4"></Keywords>
            <Keywords name="Keywords5"></Keywords>
            <Keywords name="Keywords6"></Keywords>
            <Keywords name="Keywords7"></Keywords>
            <Keywords name="Keywords8"></Keywords>
            <Keywords name="Delimiters"></Keywords>
        </KeywordLists>
        <Styles>
            <WordsStyle name="DEFAULT"              fgColor="{udl_fg}" bgColor="{udl_bg}" colorStyle="0" fontStyle="0" nesting="0" />
            <WordsStyle name="COMMENTS"             fgColor="{udl_fg}" bgColor="{udl_bg}" colorStyle="0" fontStyle="0" nesting="0" />
            <WordsStyle name="LINE COMMENTS"        fgColor="{udl_fg}" bgColor="{udl_bg}" colorStyle="0" fontStyle="0" nesting="0" />
            <WordsStyle name="NUMBERS"              fgColor="{udl_fg}" bgColor="{udl_bg}" colorStyle="0" fontStyle="0" nesting="0" />
            <WordsStyle name="KEYWORDS1"            fgColor="{udl_fg}" bgColor="{udl_bg}" colorStyle="0" fontStyle="0" nesting="0" />
            <WordsStyle name="KEYWORDS2"            fgColor="{udl_fg}" bgColor="{udl_bg}" colorStyle="0" fontStyle="0" nesting="0" />
            <WordsStyle name="KEYWORDS3"            fgColor="{udl_fg}" bgColor="{udl_bg}" colorStyle="0" fontStyle="0" nesting="0" />
            <WordsStyle name="KEYWORDS4"            fgColor="{udl_fg}" bgColor="{udl_bg}" colorStyle="0" fontStyle="0" nesting="0" />
            <WordsStyle name="KEYWORDS5"            fgColor="{udl_fg}" bgColor="{udl_bg}" colorStyle="0" fontStyle="0" nesting="0" />
            <WordsStyle name="KEYWORDS6"            fgColor="{udl_fg}" bgColor="{udl_bg}" colorStyle="0" fontStyle="0" nesting="0" />
            <WordsStyle name="KEYWORDS7"            fgColor="{udl_fg}" bgColor="{udl_bg}" colorStyle="0" fontStyle="0" nesting="0" />
            <WordsStyle name="KEYWORDS8"            fgColor="{udl_fg}" bgColor="{udl_bg}" colorStyle="0" fontStyle="0" nesting="0" />
            <WordsStyle name="OPERATORS"            fgColor="{udl_fg}" bgColor="{udl_bg}" colorStyle="0" fontStyle="0" nesting="0" />
            <WordsStyle name="FOLDER IN CODE1"      fgColor="{udl_fg}" bgColor="{udl_bg}" colorStyle="0" fontStyle="0" nesting="0" />
            <WordsStyle name="FOLDER IN CODE2"      fgColor="{udl_fg}" bgColor="{udl_bg}" colorStyle="0" fontStyle="0" nesting="0" />
            <WordsStyle name="FOLDER IN COMMENT"    fgColor="{udl_fg}" bgColor="{udl_bg}" colorStyle="0" fontStyle="0" nesting="0" />
            <WordsStyle name="DELIMITERS1"          fgColor="{udl_fg}" bgColor="{udl_bg}" colorStyle="0" fontStyle="0" nesting="0" />
            <WordsStyle name="DELIMITERS2"          fgColor="{udl_fg}" bgColor="{udl_bg}" colorStyle="0" fontStyle="0" nesting="0" />
            <WordsStyle name="DELIMITERS3"          fgColor="{udl_fg}" bgColor="{udl_bg}" colorStyle="0" fontStyle="0" nesting="0" />
            <WordsStyle name="DELIMITERS4"          fgColor="{udl_fg}" bgColor="{udl_bg}" colorStyle="0" fontStyle="0" nesting="0" />
            <WordsStyle name="DELIMITERS5"          fgColor="{udl_fg}" bgColor="{udl_bg}" colorStyle="0" fontStyle="0" nesting="0" />
            <WordsStyle name="DELIMITERS6"          fgColor="{udl_fg}" bgColor="{udl_bg}" colorStyle="0" fontStyle="0" nesting="0" />
            <WordsStyle name="DELIMITERS7"          fgColor="{udl_fg}" bgColor="{udl_bg}" colorStyle="0" fontStyle="0" nesting="0" />
            <WordsStyle name="DELIMITERS8"          fgColor="{udl_fg}" bgColor="{udl_bg}" colorStyle="0" fontStyle="0" nesting="0" />
        </Styles>
    </UserLang>
</NotepadPlus>
"""

filled_out = template.format( udl_file=udlFile, udl_name=udlName, udl_fg=hexFG, udl_bg=hexBG)

with open(udlPath, 'w') as f:
    f.write(filled_out)

#notepad.open(udlPath)
notepad.saveAllFiles()

tmpfile = os.path.join(os.environ['TEMP'], 'delself.bat')
with open(tmpfile, 'w') as f:
    f.write("@ECHO Creating UDL '{}':'{}' and restarting Notepad++\n".format(udlName, udlPath))
    f.write("@TIMEOUT /T 2\n")
    f.write('@START "" "{}"\n'.format(nppexe))
    f.write('@del "%~f0"\n')    # delete self; must be last line of batch file

#subprocess.Popen(['cmd', '/C', 'TIMEOUT /t 2 && START {}'.format(nppexe)])
#subprocess.Popen([nppexe])
subprocess.Popen(['cmd', '/C', tmpfile])
#exit()  # this will exit Notepad++ as well, which (in this case) is what I want
notepad.menuCommand(MENUCOMMAND.FILE_EXIT)