"""functionListTester

author = PeterJones @ community.notepad-plus-plus.org

This script will [hopefully] load a functionList XML file, extract its regexes, and try to indicate what will and won't match (to prevent needing to restart Notepad++ while doing development on a functionList)

1. Open the functionList XML in editor2
2. Open the file with the function names in editor1

derived from my sessionChecker.py

"""

# reference: https://stackoverflow.com/questions/48746478/how-do-i-extract-value-of-xml-attribute-in-python
# reference: https://docs.python.org/2/library/xml.etree.elementtree.html
import xml.etree.ElementTree as ET
import os.path

# I originally hoped I could make a modal MessageBox, so that could prompt the user to move files around to the right place
# r = notepad.messageBox("message", "title", MESSAGEBOXFLAGS.OKCANCEL);
# replace that with the assumption of editor2==XML, editor1==FileWithFunctions

xmlEditor = editor2
funcEditor = editor1

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
