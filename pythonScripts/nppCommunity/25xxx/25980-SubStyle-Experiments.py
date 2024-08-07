# encoding=utf-8
"""in response to https://community.notepad-plus-plus.org/topic/25980/

Starting to experiment with SubStyles

https://github.com/ScintillaOrg/lexilla/issues/260
  - encouraged me to get the SciTE 5.5.1 source and prebuilt,
    and after some prodding, able to get enough to see `decrypt` added as substyled keyword
  - however, despite their assertion, I couldn't find examples in their code
    of how they _use_ any of those commands -- not as SCI_xxx messages, nor as the
    Scintilla::Message enumeration.
  - but when I searched the source, was able to find their python-based testing framework

<SciTE Source Directory>/scintilla/test/simpleTests.py :: TestSubStyles()
  - shows how they _test_ SubStyles, which gives a pretty good example of how to use
    at least some of the commands.  I will try it out, both on the CPP which they show in their
    example, then try to replicate with

<SciTE Source>/lexilla/test/examples/hypertext/x.php.styled
  - shows the styleID -- confirming `decrypt` gets styleID=198,
    which is either PHP_WORD(121) + 77, or PHP_DEFAULT(118) + 80

Ah, finally found it: <source>/scite/src/SciTEProps.cxx::ReadProperties()
  - finds all the `substyles.` in the SciTE.properties file,
    and does the SetIdentifiers from there.

"""
from Npp import *
import os
import textwrap

def tryCPP():
    console.write("\ncpp lexer: \n")
    tmpfile = os.path.join(os.environ["TEMP"], '25980_SubStyle.cpp')
    if os.path.exists(tmpfile):
        notepad.open(tmpfile)
    else:
        notepad.new()
        notepad.saveAs(tmpfile)

    editor.clearAll()
    src = textwrap.dedent(r'''    #include <stdio.h>

    int main()
    {
        printf("hello world\n");
    }
    ''')
    editor.addText(src)
    notepad.save()

    bases = editor.getSubStyleBases()
    bases_hex = ":".join("0x{0:02x}({0:>3d})".format(c) for c in bases.encode())
    console.write(f"bases = \"{bases}\" = >>{bases_hex}<<\n")
    # bases = "" = >>0x0b( 11):0x11( 17)<<
    # ⇒ matches what the test say it should get: 11=C++ IDENTIFIER; 17=C++ COMMENT DOC KEYWORD
    console.write("distance = 0x{0:02x}({0:>3d})\n".format(editor.distanceToSecondaryStyles()))

    # LexCPP: SubStyles subStyles{ styleSubable, SubStylesFirst, SubStylesAvailable, inactiveFlag };
    #   uses the global SubStyles.h `constexpr int SubStylesFirst = 0x80;` as its start-of-substyles region,
    #   which is `firstSubStyle` in simpleTests::TestSubStyles::TestAllocate()
    firstSubStyle = 0x80    # SubStyles.h::SubStylesFirst
    console.write("GetStyleFromSubStyle = 0x{0:02x}({0:>3d})\n".format(editor.getStyleFromSubStyle(firstSubStyle)))
    SCE_C_IDENTIFIER = 11   # 0x0b
    console.write("getSubStylesStart =  0x{0:02x}({0:>3d})\n".format(editor.getSubStylesStart(SCE_C_IDENTIFIER)))
    console.write("getSubStylesLength =  0x{0:02x}({0:>3d})\n".format(editor.getSubStylesLength(SCE_C_IDENTIFIER)))

    numSubStyles = 5
    subs = editor.allocateSubStyles(SCE_C_IDENTIFIER, numSubStyles)
    console.write("allocateSubStyles(n={1}) =  0x{0:02x}({0:>3d})\n".format(subs, numSubStyles))

    console.write("after allocation: getSubStylesStart =  0x{0:02x}({0:>3d})\n".format(editor.getSubStylesStart(SCE_C_IDENTIFIER)))
    console.write("after allocation: getSubStylesLength =  0x{0:02x}({0:>3d})\n".format(editor.getSubStylesLength(SCE_C_IDENTIFIER)))

    # the getStyleFromSubStyle is the reverse mapping, which will give the parent for anything from the list of substyles (and a main style will just return itself)
    console.write("getStyleFromSubStyle(n={1}) =  0x{0:02x}({0:>3d})\n".format(editor.getStyleFromSubStyle(SCE_C_IDENTIFIER), subs))
    console.write("getStyleFromSubStyle(n={1}) =  0x{0:02x}({0:>3d})\n".format(editor.getStyleFromSubStyle(SCE_C_IDENTIFIER), subs+numSubStyles-1))
    console.write("getStyleFromSubStyle(n={1}) =  0x{0:02x}({0:>3d})\n".format(editor.getStyleFromSubStyle(SCE_C_IDENTIFIER), SCE_C_IDENTIFIER))

    # now try freeing them
    editor.freeSubStyles()
    console.write("after free: getSubStylesStart =  0x{0:02x}({0:>3d})\n".format(editor.getSubStylesStart(SCE_C_IDENTIFIER)))
    console.write("after free: getSubStylesLength =  0x{0:02x}({0:>3d})\n".format(editor.getSubStylesLength(SCE_C_IDENTIFIER)))
    console.write("after free: getStyleFromSubStyle(n={1}) =  0x{0:02x}({0:>3d})\n".format(editor.getStyleFromSubStyle(SCE_C_IDENTIFIER), subs))
    console.write("after free: getStyleFromSubStyle(n={1}) =  0x{0:02x}({0:>3d})\n".format(editor.getStyleFromSubStyle(SCE_C_IDENTIFIER), subs+numSubStyles-1))
    console.write("after free: getStyleFromSubStyle(n={1}) =  0x{0:02x}({0:>3d})\n".format(editor.getStyleFromSubStyle(SCE_C_IDENTIFIER), SCE_C_IDENTIFIER))

    # allocate 3 after freedom: verify it goes back to the start of the substyle region
    numSubStyles = 3
    subs = editor.allocateSubStyles(SCE_C_IDENTIFIER, numSubStyles)
    console.write("allocate 3 after freedom: allocateSubStyles(n={1}) =  0x{0:02x}({0:>3d})\n".format(subs, numSubStyles))
    console.write("allocate 3 after freedom: getSubStylesStart =  0x{0:02x}({0:>3d})\n".format(editor.getSubStylesStart(SCE_C_IDENTIFIER)))
    console.write("allocate 3 after freedom: getSubStylesLength =  0x{0:02x}({0:>3d})\n".format(editor.getSubStylesLength(SCE_C_IDENTIFIER)))

    notepad.close()

def tryPHP():
    console.write("\nphp lexer: \n")
    tmpfile = os.path.join(os.environ["TEMP"], '25980_SubStyle.php')
    if os.path.exists(tmpfile):
        notepad.open(tmpfile)
    else:
        notepad.new()
        notepad.saveAs(tmpfile)

    editor.clearAll()
    src = textwrap.dedent(r'''    <head> <!-- About to script -->
    <?php
    decrypt "xyzzy";
    echo __FILE__.__LINE__;
    echo "<!-- -->\n";
    /* ?> */
    ?>
    <strong>for</strong><b>if</b>
    <?= 'short echo tag' ?>
    <? echo 'short tag' ?>
    <script>
        alert("<?php echo "PHP" . ' Code'; ?>");
        alert('<?= 'PHP' . "Code"; ?>');
        var xml =
        '<?xml version="1.0" encoding="iso-8859-1"?><SO_GL>' +
        '<GLOBAL_LIST mode="complete"><NAME>SO_SINGLE_MULTIPLE_COMMAND_BUILDER</NAME>' +
        '<LIST_ELEMENT><CODE>1</CODE><LIST_VALUE><![CDATA[RM QI WEB BOOKING]]></LIST_VALUE></LIST_ELEMENT>' +
        '<LIST_ELEMENT><CODE>1</CODE><LIST_VALUE><![CDATA[RM *PCC]]></LIST_VALUE></LIST_ELEMENT>' +
        '</GLOBAL_LIST></SO_GL>';
    </script>
    ''')
    editor.addText(src)
    notepad.save()

    bases = editor.getSubStyleBases()
    bases_hex = ":".join("0x{0:02x}({0:>3d})".format(c) for c in bases.encode())
    console.write(f"bases = \"{bases}\" = >>{bases_hex}<<\n")
    # bases = ".=J`y" = >>0x01(  1):0x03(  3):0x2e( 46):0x3d( 61):0x4a( 74):0x60( 96):0x79(121)<<
    # ⇒ confirmed that styleID=121 (PHP KEYWORD) does allow substyles
    console.write("distance = 0x{0:02x}({0:>3d})\n".format(editor.distanceToSecondaryStyles()))

    # LexHTML: SubStyles subStyles{styleSubable,SubStylesHTML,SubStylesAvailable,0};
    #   uses the local `constexpr int SubStylesHTML = 0xC0;` as its start-of-substyles region,
    #   so I would want to use that here
    firstSubStyle = 0xC0    # LexHTML.cxx::SubStylesHTML
    console.write("GetStyleFromSubStyle = 0x{0:02x}({0:>3d})\n".format(editor.getStyleFromSubStyle(firstSubStyle)))
    SCE_HPHP_WORD = 121 # 0x79
    console.write("getSubStylesStart =  0x{0:02x}({0:>3d})\n".format(editor.getSubStylesStart(SCE_HPHP_WORD)))
    console.write("getSubStylesLength =  0x{0:02x}({0:>3d})\n".format(editor.getSubStylesLength(SCE_HPHP_WORD)))

    # split the allocation into two groups
    numSubStyles = 1
    subs = editor.allocateSubStyles(SCE_HPHP_WORD, numSubStyles)
    console.write("allocateSubStyles(n={1}) =  0x{0:02x}({0:>3d})\n".format(subs, numSubStyles))

    numSubStyles = 4
    subs = editor.allocateSubStyles(SCE_HPHP_WORD, numSubStyles)
    console.write("allocateSubStyles(n={1}) =  0x{0:02x}({0:>3d})\n".format(subs, numSubStyles))

    console.write("after allocation: getSubStylesStart =  0x{0:02x}({0:>3d})\n".format(editor.getSubStylesStart(SCE_HPHP_WORD)))
    console.write("after allocation: getSubStylesLength =  0x{0:02x}({0:>3d})\n".format(editor.getSubStylesLength(SCE_HPHP_WORD)))
    # so with the multi-alloc, able to see that the second allocation updates the START location for the particular parent style

    # let's free them all, then allocate one substyle for each of the bases
    editor.freeSubStyles()
    subHash = dict()
    for parent in bases.encode():
        key = str(parent)
        subHash[key] = dict()
        subHash[key]['parent'] = parent
        subHash[key]['count'] = editor.allocateSubStyles(parent, 1)
        subHash[key]['start'] = editor.getSubStylesStart(parent)
        subHash[key]['length'] = editor.getSubStylesLength(parent)
        console.write("allocation base=#{:03}: ret={:03}, start={:03}, length={:03}\n".format(
            subHash[key]['parent'],
            subHash[key]['count'],
            subHash[key]['start'],
            subHash[key]['length']
        ))

    # let's try to define some coloration and keywords
    subStyle = editor.getSubStylesStart(SCE_HPHP_WORD)
    editor.styleSetFore(subStyle, (0x00,0xA0,0x00)) # same as scite example
    editor.styleSetBack(subStyle, (255,255,0))      # yellow background
    editor.setIdentifiers(subStyle, "decrypt")

    # confirm (without closing) closing that if I check just after it's allocated,
    #   it properly colors with green on yellow,
    #   but if I change tabs and back, the getSubStylesStart resets to -1 and the color goes away
    #   so like the enhance-any-lexer, it needs to be reset every time you open or activate a buffer

    notepad.close()

def listAllSubstylable():
    notepad.new()
    LANGUAGES = [eval('MENUCOMMAND.{}'.format(x)) for x in dir(MENUCOMMAND) if x.startswith('LANG_') and not x.startswith('LANG_USER')]
    for L in LANGUAGES:
        #console.write("{0:03d}) {0}\n".format(L))
        notepad.menuCommand(L);
        bases = editor.getSubStyleBases()
        if len(bases):
            bases_hex = ":".join("0x{0:02x}({0:>3d})".format(c) for c in bases.encode())
            console.write("{0:03d} {0}:\t{1}\n".format(L, bases_hex))
    editor.clearAll()
    notepad.close()

console.clear()
console.show()
tryCPP()
del(tryCPP)
tryPHP()
del(tryPHP)
#listAllSubstylable()
