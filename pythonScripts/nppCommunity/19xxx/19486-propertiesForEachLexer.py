# encoding=utf-8
"""in response to https://notepad-plus-plus.org/community/topic/19486/

this is tangential to that.  If you want to find all the properties for a given lexer,
this code will print it for you.
"""
from Npp import *

console.show()
console.clear()

notepad.new()
keep = notepad.getLangType()

#for t in [LANGTYPE.ADA, LANGTYPE.ASM, LANGTYPE.ASN1, LANGTYPE.ASP, LANGTYPE.AU3, LANGTYPE.AVS, LANGTYPE.BAANC, LANGTYPE.BASH, LANGTYPE.BATCH, LANGTYPE.BLITZBASIC, LANGTYPE.C, LANGTYPE.CAML, LANGTYPE.CMAKE, LANGTYPE.COBOL, LANGTYPE.COFFEESCRIPT, LANGTYPE.CPP, LANGTYPE.CS, LANGTYPE.CSOUND, LANGTYPE.CSS, LANGTYPE.D, LANGTYPE.DIFF, LANGTYPE.ERLANG, LANGTYPE.ESCRIPT, LANGTYPE.FLASH, LANGTYPE.FORTH, LANGTYPE.FORTRAN, LANGTYPE.FORTRAN_77, LANGTYPE.FREEBASIC, LANGTYPE.GUI4CLI, LANGTYPE.HASKELL, LANGTYPE.HTML, LANGTYPE.IHEX, LANGTYPE.INI, LANGTYPE.INNO, LANGTYPE.JAVA, LANGTYPE.JAVASCRIPT, LANGTYPE.JS, LANGTYPE.JSON, LANGTYPE.JSP, LANGTYPE.KIX, LANGTYPE.LATEX, LANGTYPE.LISP, LANGTYPE.LUA, LANGTYPE.MAKEFILE, LANGTYPE.MATLAB, LANGTYPE.MMIXAL, LANGTYPE.NIMROD, LANGTYPE.NNCRONTAB, LANGTYPE.NSIS, LANGTYPE.OBJC, LANGTYPE.OSCRIPT, LANGTYPE.PASCAL, LANGTYPE.PERL, LANGTYPE.PHP, LANGTYPE.POWERSHELL, LANGTYPE.PROPS, LANGTYPE.PS, LANGTYPE.PUREBASIC, LANGTYPE.PYTHON, LANGTYPE.R, LANGTYPE.RC, LANGTYPE.REBOL, LANGTYPE.REGISTRY, LANGTYPE.RUBY, LANGTYPE.RUST, LANGTYPE.SCHEME, LANGTYPE.SEARCHRESULT, LANGTYPE.SMALLTALK, LANGTYPE.SPICE, LANGTYPE.SQL, LANGTYPE.SREC, LANGTYPE.SWIFT, LANGTYPE.TCL, LANGTYPE.TEHEX, LANGTYPE.TEX, LANGTYPE.TXT, LANGTYPE.TXT2TAGS, LANGTYPE.USER, LANGTYPE.VB, LANGTYPE.VERILOG, LANGTYPE.VHDL, LANGTYPE.VISUALPROLOG, LANGTYPE.XML, LANGTYPE.YAML]:
for t in LANGTYPE.values.values():
    n = notepad.getLanguageName(t)
    d = notepad.getLanguageDesc(t)
    console.write("{!s:<35.35s} {!s:<35.35s}  {!s:<35.35s}\n".format(t,n,d))

    notepad.setLangType(t)
    for s in editor.propertyNames().split():
        if editor.getPropertyInt(s,-65537) > -65537:
            v = str(editor.getPropertyInt(s,-65537))
        else:
            v = '"' + editor.getProperty(s) + '"'
        console.write("\t{:<32.32s}:{: <9.9s}: {:<32.32s} \"{}\"\n".format(
            "'"+s+"'",
            "{:01d}={:<s}".format(editor.propertyType(s), str(TYPEPROPERTY.values[editor.propertyType(s)])),
            v,
            editor.describeProperty(s))
        )

notepad.setLangType(keep)
notepad.close()
