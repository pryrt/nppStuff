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
        self.update_stylers('stylers.xml')
        # TODO: loop over all themes and call .update_stylers()
        self.update_langs()

    def update_stylers(self, themeName):
        fModel = os.path.join(self.dirNpp, 'stylers.model.xml')
        if themeName=='stylers.xml':
            fTheme = os.path.join(self.dirNppConfig, themeName)
        else:
            fTheme = os.path.join(self.dirNppConfig, 'themes', themeName)
        console.write("stylers.model = '{}'\ntheme = '{}'\n".format(fModel, fTheme))

        treeModel = ET.parse(fModel)
        treeTheme = ET.parse(fTheme)

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
        #       example: finds all LexerType nodes that have non-empty ext attributes
        #           ```
        #           for elLexerType in treeTheme.findall("//LexerType[@ext!='']"):
        #               console.write("LexerType {}\n".format(elLexerType.attrib))
        #           ```

        # Grab the default attributes from the <GlobalStyles><WidgetStyle name="Global override" styleID="0"...>
        self.globalStyle = treeTheme.find('.//GlobalStyles/WidgetStyle[@styleID="0"]')
        #console.write("Global Attributes Saved: {}\n".format(self.globalStyle.attrib))

        # Need to grab the Theme's <LexerStyles> node for future insertions
        elThemeLexerStyles = treeTheme.find('LexerStyles')
        #console.write("Theme's LexerStyles: {} with {} sub-nodes\n".format(elThemeLexerStyles, len(elThemeLexerStyles)))

        # iterate through all the treeModel, and see if there are any LexerTypes that cannot also be found in treeTheme
        for elModelLexer in treeModel.iter("LexerType"):
            #console.write("LexerType {}\n".format(elModelLexer.attrib))
            strToFind = ".//LexerType[@name='{}']".format(elModelLexer.attrib['name'])
            elStylersMatchLT = treeTheme.find(strToFind)
            if elStylersMatchLT is None:
                #console.write("NOT FOUND[{}] => {}; TODO = update XML\n".format(strToFind, elStylersMatchLT))
                self.addMissingLexer(elModelLexer, elThemeLexerStyles)
            else:
                pass # console.write("YES FOUND[{}] => {}\n".format(strToFind, elStylersMatchLT.attrib))


        # maybe: sort the lexers by name
        #       cf: https://stackoverflow.com/questions/25338817/sorting-xml-in-python-etree
        #       ``` def sortchildrenby(parent, attr):
        #       ```     parent[:] = sorted(parent, key=lambda child: child.get(attr))
        #       ``` sortchildrenby(root, 'NAME')
        #   use trick <https://stackoverflow.com/a/18411610/5508606> to get 'searchResult' sorted last
        #elThemeLexerStyles[:] = sorted(elThemeLexerStyles, key=lambda child: (child.get('name') == 'searchResult', child.get('name')))

        # TODO: why is it changing order of GlobalStyles section, and how do I prevent that?

        # fix the indentation for the whole tree
        ET.indent(treeTheme, space = "    ", level=0)

        # for now, show the result; TODO = write to file
        console.write("Show full treeTheme:\n{}\n=====\n".format(ET.tostring(treeTheme.getroot(), encoding="unicode")))
        console.write("\n\n")

    def addMissingLexer(self, elModelLexer, elLexerStyles):
        console.write("addMissingLexer({})\n".format(elModelLexer.attrib['name']))
        elNewLexer = ET.SubElement(elLexerStyles, 'LexerType', attrib=elModelLexer.attrib)
        attr = {} # TODO: inherit from self.globalStyle.attrib; but if I set it EQUAL, then attr[]=... will corrupt globalStyle
        attr['fontName'] = ""
        for elWordsStyle in elModelLexer.iter("WordsStyle"):
            console.write("- need WordsStyle => {}\n".format(elWordsStyle.attrib))
            attr['name'] = elWordsStyle.attrib['name']
            attr['styleID'] = elWordsStyle.attrib['styleID']
            ET.SubElement(elNewLexer, 'WordsStyle', attrib=attr)

        #ET.indent(elNewLexer, space = "    ", level=2)

    def update_langs(self):
        pass

ConfigUpdater().go()
