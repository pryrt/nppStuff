"""functionListTester

author = PeterJones @ community.notepad-plus-plus.org

This script will [hopefully] load a functionList XML file, extract its regexes, and try to indicate what will and won't match (to prevent needing to restart Notepad++ while doing development on a functionList)

1. Open the functionList XML in editor2
2. Open the file with the function names in editor1

derived from my sessionChecker.py

#### TODO:
1. FEATURE: Needs to implement className/nameExpr inside a function-only parser
    ie, class without classRange, example
        sub PERLQUALIFIED::Method { 1; }
2. BUG: if there is no classRange element, it complains
3. BUG: it doesn't handle r'(?x)' free-spacing mode correctly
    - possibly doesn't know free-spacing
    - possibly xml parser got rid of EOL, so free-spacing comments never end

"""

# reference: https://stackoverflow.com/questions/48746478/how-do-i-extract-value-of-xml-attribute-in-python
# reference: https://docs.python.org/2/library/xml.etree.elementtree.html
import xml.etree.ElementTree as ET
import os.path
import re
import traceback # https://stackoverflow.com/a/1156048
do_trace = False


# I originally hoped I could make a modal MessageBox, so that could prompt the user to move files around to the right place
# r = notepad.messageBox("message", "title", MESSAGEBOXFLAGS.OKCANCEL);
# replace that with the assumption of editor2==XML, editor1==FileWithFunctions

xmlEditor = editor2
funcEditor = editor1

console.clear()

try:
    console.write("try xml=editor2\n")
    xmlTree = ET.fromstring(xmlEditor.getText())
except ET.ParseError:
    # swap if not right
    xmlEditor = editor1
    funcEditor = editor2
    try:
        console.write("try xml=editor1\n")
        xmlTree = ET.fromstring(xmlEditor.getText())
    except ET.ParseError:
        raise ValueError('Neither editor is showing an XML file') # TODO: add buffer filenames

console.write("xmlEditor = {} in editor{}\n".format(xmlEditor, "2" if xmlEditor==editor2 else "1"))
console.write("funcEditor = {} in editor{}\n".format(funcEditor, "1" if funcEditor==editor1 else "2"))

if xmlTree.find('./functionList') is None:
    raise ValueError('XML did not have functionList', ET.tostring(xmlTree))

parser = xmlTree.find('./functionList/parser')

#console.write("whole XML:\n==========\n{}\n==========\n".format(ET.tostring(xmlTree)))

# these don't exist by default, so add them to an inheriting enumeration
class MY_MENUCOMMAND(MENUCOMMAND):
    SEARCH_UNMARKALLEXT = 43032
    SEARCH_MARKONEEXT1 = 43062
    SEARCH_MARKONEEXT2 = 43063
    SEARCH_MARKONEEXT3 = 43064
    SEARCH_MARKONEEXT4 = 43065
    SEARCH_MARKONEEXT5 = 43066

    def unused():
        pass

#console.write("inherit.SEARCH_UNMARKALLEXT1={:d}, PCJ={:d}\n".format(MY_MENUCOMMAND.SEARCH_UNMARKALLEXT1, MY_MENUCOMMAND.PCJ_SEARCH_UNMARK_ALL))

def markingFunction(m,ext):
    #console.write("\t\t\t\tmarking match m=<{}> span={}\n".format(m.group(0), m.span(0)))
    console.write("\t\t\t\tmarking match span={}\n".format(m.span(0)))
    if do_trace: traceback.print_stack()
    mstart, mend = m.span(0)
    #mlen = mend - mstart
    #funcEditor.startStyling(mstart,0)
    #funcEditor.setStyling(mlen, 14)
    funcEditor.setSelection(mstart, mend)
    notepad.menuCommand(ext)
    funcEditor.setSelection(0,0)
    return

def containerMarkingFunction(m,re2,ext):
    mstart, mend = m.span(0)
    console.write("\t\t\tcontainer:{}..{}\n".format(mstart, mend))
    if do_trace: traceback.print_stack()
    funcEditor.research(re2, lambda m: markingFunction(m,ext), re.S|re.M, mstart, mend, 1)
    console.write("\t\t\tEND container\n")
    return

#### First, clear all EXT marks (token styles)
notepad.menuCommand(MY_MENUCOMMAND.SEARCH_UNMARKALLEXT)

#### COMMENTS are EXT5

try:
    reComment = parser.attrib['commentExpr']
    console.write("reComment = {}\n".format(reComment))
    funcEditor.research(reComment, lambda m: markingFunction(m,MY_MENUCOMMAND.SEARCH_MARKONEEXT5))
except KeyError:
    notepad.menuCommand(MY_MENUCOMMAND.SEARCH_UNMARKALLEXT5)


#### CLASS RANGE are EXT3 (used to have note: "if it doesn't find CLASS NAME in the CLASS RANGE", but I'm not sure I like that condition)
#### CLASS NAMES are EXT2
#### FUNCTION NAMES in CLASS are EXT1

try:
    # look for all classes (EXT3)
    classRange = parser.find('./classRange')
    reClassMain = classRange.attrib['mainExpr']
    console.write('<classRange MainExpr="{}">\n'.format(reClassMain))
    funcEditor.research(reClassMain, lambda m: markingFunction(m,MY_MENUCOMMAND.SEARCH_MARKONEEXT3), re.S|re.M)

    # look for each class name (EXT2)
    classNameExpressions = classRange.findall('./className/nameExpr')
    if len(classNameExpressions) == 0:
        console.write("\tno class name expressions\n")
        pass
    else:
        console.write("\tfound {:d} class name expressions\n".format(len(classNameExpressions)))
        for classElem in classNameExpressions:
            reClassName = classElem.attrib['expr']
            console.write("\t<nameExpr expr='{}'>\n".format(reClassName))
            funcEditor.research(reClassMain, lambda m: containerMarkingFunction(m,reClassName,MY_MENUCOMMAND.SEARCH_MARKONEEXT2), re.S|re.M)

    # look for each function (EXT1)
    classFunction = classRange.find('./function')
    reClassFunctionMain = classFunction.attrib['mainExpr']
    console.write("\t<classRange><function mainExpr='{}'>\n".format(reClassFunctionMain))
    classFunctionExpressions = classFunction.findall('./functionName/funcNameExpr')
    if len(classFunctionExpressions) == 0:
        console.write("\t\tno class function expressions, so just matching class function main")
        funcEditor.research(reClassMain, lambda m: containerMarkingFunction(m,reClassFunctionMain,MY_MENUCOMMAND.SEARCH_MARKONEEXT1), re.S|re.M)
        console.write("\t\tEND no class function expressions, so just matching class function main")
    else:
        do_trace = False
        for funcNameElem in classFunctionExpressions:
            reClassFuncName = funcNameElem.attrib['expr']
            console.write("\t\tnth class function name expression: {}\n".format(reClassFuncName))
            #funcEditor.research(reClassFunctionMain,lambda m: containerMarkingFunction(m,reClassFuncName,MY_MENUCOMMAND.SEARCH_MARKONEEXT3),re.S|re.M)
            def onlyInThisClass(m):
                console.write("\t\t\tonlyInThisClass.span = {}\n".format(m.span(0)))
                cstart, cstop = m.span(0)
                funcEditor.research(reClassFunctionMain, lambda m: containerMarkingFunction(m,reClassFuncName,MY_MENUCOMMAND.SEARCH_MARKONEEXT1),re.S|re.M,cstart,cstop)
                pass
            funcEditor.research(reClassMain, onlyInThisClass, re.S|re.M)
            console.write("\t\tEND nth class function name expression: {}\n".format(reClassFuncName))
        console.write("\t\tEND FOR\n")
        do_trace = False

except KeyError:
    notepad.menuCommand(MY_MENUCOMMAND.SEARCH_UNMARKALLEXT1)
    notepad.menuCommand(MY_MENUCOMMAND.SEARCH_UNMARKALLEXT2)
    notepad.menuCommand(MY_MENUCOMMAND.SEARCH_UNMARKALLEXT3)

#### NORMAL FUNCTION NAMES are EXT4

try:
    functionRange = parser.find('./function')
    reFunctionMain = functionRange.attrib['mainExpr']
    nameExpressions = functionRange.findall('./functionName/nameExpr')
    console.write('<function MainExpr="{}"> => {:d}\n'.format(reFunctionMain, len(nameExpressions)))
    if len(nameExpressions) == 0:
        funcEditor.research(reFunctionMain, lambda m: markingFunction(m,MY_MENUCOMMAND.SEARCH_MARKONEEXT4), re.S|re.M)
    else:
        for nameElem in nameExpressions:
            reFunctionName = nameElem.attrib['expr']
            console.write("\t<nameExpr expr='{}'>\n".format(reFunctionName))
            funcEditor.research(reFunctionMain, lambda m: containerMarkingFunction(m,reFunctionName,MY_MENUCOMMAND.SEARCH_MARKONEEXT4), re.S|re.M)
    # TODO: implement className/nameExpr inside the normal function as well, using EXT2
except KeyError:
    notepad.menuCommand(MY_MENUCOMMAND.SEARCH_UNMARKALLEXT5)

'''
triple quotes
'''

