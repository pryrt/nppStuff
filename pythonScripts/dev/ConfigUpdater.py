# encoding=utf-8
"""Config Files Sometimes Need Updating, Too

When it updates, Notepad++ tends to avoid updating important things like langs.xml, stylers.xml, and your themes;
it does this because it doesn't want to overwrite your customizations, but that has the drawback that you end up
missing new styles, new languages, and updated keyword lists.
"""
from Npp import editor,notepad,console
import xml.etree.ElementTree as ET  # https://docs.python.org/3/library/xml.etree.elementtree.html
import os

class ConfigUpdater(object):
    def __init__(self):
        self.dirNpp          = notepad.getNppDir()
        self.dirPluginConfig = notepad.getPluginConfigDir()
        self.dirNppConfig    = os.path.dirname(os.path.dirname(self.dirPluginConfig))

    def go(self):
        self.update_stylers()
        self.update_langs()

    def update_stylers(self):
        fModel = os.path.join(self.dirNpp, 'stylers.model.xml')
        fStylers = os.path.join(self.dirNppConfig, 'stylers.xml')
        console.write("Stylers: model = '{}'\nStylers: active = '{}'\n".format(fModel, fStylers))

        treeModel = ET.parse(fModel)
        treeStylers = ET.parse(fStylers)

        #https://github.com/pryrt/nppStuff/blob/cdd094148bd54f4b1c8e24cc328cc0afd558cf26/pythonScripts/nppCommunity/sessionChecker.py#L122
        # ... gives example of iterating through specific elements
        # Better example is in officail docs, here:
        #   https://docs.python.org/3/library/xml.etree.elementtree.html#finding-interesting-elements
        #   ROOT.iter('xxx') goes through all xxx nodes inside the ROOT (also works on whole TREE, not just ROOT)
        #       example = treeModel.iter('LexerType')   # iterates through all LexerType nodes
        #   ROOT.findall('xxx') lists all xxx that are direct children
        #   ROOT.find('xxx') lists first xxx that is direct child
        # The find/findall also accept full XPath in the find strings:
        #   https://docs.python.org/3/library/xml.etree.elementtree.html#xpath-support
        #       example: treeStylers.findall("//LexerType[@ext!='']") finds all LexerType nodes that have non-empty ext attributes
        for elLexerType in treeStylers.findall("//LexerType[@ext!='']"):
            console.write("LexerType {}\n".format(elLexerType.attrib))

        # TODO: iterate through all the treeModel, and see if there are any LexerTypes that cannot also be found in treeStylers

    def update_langs(self):
        pass

ConfigUpdater().go()
