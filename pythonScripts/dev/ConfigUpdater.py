# encoding=utf-8
"""Config Files Sometimes Need Updating, Too

When it updates, Notepad++ tends to avoid updating important things like langs.xml, stylers.xml, and your themes;
it does this because it doesn't want to overwrite your customizations, but that has the drawback that you end up
missing new styles, new languages, and updated keyword lists.
"""
from Npp import editor,notepad,console
import xml.etree.ElementTree as ET  # https://docs.python.org/3/library/xml.etree.elementtree.html
import os
import re

class CommentedTreeBuilder(ET.TreeBuilder):
    # https://stackoverflow.com/a/34324359/5508606
    def comment(self, data):
        self.start(ET.Comment, {})
        self.data(data)
        self.end(ET.Comment)

class ConfigUpdater(object):
    def __init__(self):
        self.dirNpp          = notepad.getNppDir()
        self.dirPluginConfig = notepad.getPluginConfigDir()
        self.dirNppConfig    = os.path.dirname(os.path.dirname(self.dirPluginConfig))
        self.saved_comment   = None
        self.has_top_level_comment = False

    def go(self):
        #TMP#self.update_stylers(dirNppConfig, 'stylers.xml')

        # loop over all CFG-directory themes and call .update_stylers()
        dirCfgThemes = os.path.join(self.dirNppConfig, 'themes')
        self.update_stylers(dirCfgThemes, 'ExtraTheme.xml') #TMP#
        return

        if os.path.exists(dirCfgThemes):
            for f in os.listdir(dirCfgThemes):
                if f[-4:]=='.xml' and os.path.isfile(os.path.join(dirCfgThemes,f)):
                    self.update_stylers(dirCfgThemes, f)

        # loop over all NPP-directory themes and call .update_stylers() [skip if this is same directory as CFG]
        dirNppThemes = os.path.join(self.dirNpp, 'themes')
        if os.path.exists(dirNppThemes) and dirCfgThemes != dirNppThemes:
            for f in os.listdir(dirNppThemes):
                if f[-4:]=='.xml' and os.path.isfile(os.path.join(dirNppThemes,f)):
                    self.update_stylers(dirNppThemes, f)

        self.update_langs()

        return


    def update_stylers(self, themeDir, themeName):
        fModel = os.path.join(self.dirNpp, 'stylers.model.xml')
        fTheme = os.path.join(themeDir, themeName)
        console.write("\n\nstylers.model = '{}'\ntheme = '{}'\n".format(fModel, fTheme))

        # preserve comments by using
        #   <https://stackoverflow.com/a/34324359/5508606>

        # can always get the model file's tree
        treeModel = ET.parse(fModel, parser=ET.XMLParser(target=CommentedTreeBuilder()))

        # but the styler/theme file might have a top-level comment, which xml.etree.ElementTree doesn't like,
        #   so if there's a top-level comment, grab the string, remove (and save) the comment, and process the edited text instead
        try:
            treeTheme = ET.parse(fTheme, parser=ET.XMLParser(target=CommentedTreeBuilder()))
        except ET.ParseError as e:
            strXML = self.get_text_without_toplevel_comment(fTheme)
            if strXML is None:
                console.writeError(e)
                raise e # re-raise original exception
            treeTheme = ET.ElementTree(ET.fromstring(strXML, parser=ET.XMLParser(target=CommentedTreeBuilder())))

        #https://github.com/pryrt/nppStuff/blob/cdd094148bd54f4b1c8e24cc328cc0afd558cf26/pythonScripts/nppCommunity/sessionChecker.py#L122
        # ... gives example of iterating through specific elements
        # Better example is in official docs, here:
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
                #console.write("NOT FOUND[{}] => {}\n".format(strToFind, elStylersMatchLT))
                self.add_missing_lexer(elModelLexer, elThemeLexerStyles)
            else:
                pass # console.write("YES FOUND[{}] => {}\n".format(strToFind, elStylersMatchLT.attrib))

        # sort the lexers by name
        #       cf: https://stackoverflow.com/questions/25338817/sorting-xml-in-python-etree
        #       ``` def sortchildrenby(parent, attr):
        #       ```     parent[:] = sorted(parent, key=lambda child: child.get(attr))
        #       ``` sortchildrenby(root, 'NAME')
        #   use trick <https://stackoverflow.com/a/18411610/5508606> to get 'searchResult' sorted last
        elThemeLexerStyles[:] = sorted(elThemeLexerStyles, key=lambda child: (child.get('name') == 'searchResult', child.get('name')))

        # NEXT TODO: need to look for missing GlobalStyles elements as well
        #   most important would be getting the right names and styleID,
        #   but it would be nice to propagate the comments before "Global override" and before "Selected text colour" as well

        # grab the source and destination GlobalStyles
        elModelGlobalStyles = treeModel.find('GlobalStyles')
        elThemeGlobalStyles = treeTheme.find('GlobalStyles')
        elThemeNewGlobals = ET.Element('GlobalStyles')
        # experiment: if I have an element, I can insert a comment with specific text before it:
        #t = ET.Element('First', attrib={})
        #t.text = '1'
        #t.tail = 'after'
        #elThemeNewGlobals.append(t)
        #elThemeNewGlobals.insert(0,ET.Comment(" New Comment Here "))
        #console.write("elThemeNewGlobals = {}\n".format(
        #    ET.tostring(elThemeNewGlobals, encoding="unicode", xml_declaration=False)
        #))
        #return

        # iterate through the model GlobalStyles elements
        for elWidgetStyle in elModelGlobalStyles:
            if "function Comment" in str(elWidgetStyle):
                console.write("MODEL: <!--{}-->\n".format(elWidgetStyle.text))
            else:
                console.write("MODEL: {} => {}\n".format(elWidgetStyle.tag, elWidgetStyle.attrib))


        # fix the indentation for the whole tree
        ET.indent(treeTheme, space = "    ", level=0)

        # write the tree to an XML file (reinserting the comment if needed)
        self.write_xml_with_optional_comment(treeTheme, fTheme)

        return


    def add_missing_lexer(self, elModelLexer, elLexerStyles):
        #console.write("add_missing_lexer({})\n".format(elModelLexer.attrib['name']))
        elNewLexer = ET.SubElement(elLexerStyles, 'LexerType', attrib=elModelLexer.attrib)
        for elWordsStyle in elModelLexer.iter("WordsStyle"):
            #console.write("- need WordsStyle => {}\n".format(elWordsStyle.attrib))
            attr = {
                'name': elWordsStyle.attrib['name'],
                'styleID': elWordsStyle.attrib['styleID'],
                'fgColor': elWordsStyle.attrib['fgColor'],
                'bgColor': elWordsStyle.attrib['bgColor'],
                'fontName': "",
                'fontStyle': elWordsStyle.attrib['fontStyle'],
                'fontSize': "",
            }
            if 'keywordClass' in elWordsStyle.attrib:
                attr['keywordClass'] = elWordsStyle.attrib['keywordClass']
            ET.SubElement(elNewLexer, 'WordsStyle', attrib=attr)

        #ET.indent(elNewLexer, space = "    ", level=2)

    def get_text_without_toplevel_comment(self, fTheme):
        with open(fTheme, 'r') as f:
            lines = f.readlines()
        slurp = "".join(lines)
        if lines[1].strip()[0:4] != "<!--":
            return None

        #console.write("slurp[:100] = {}...\n".format(slurp[:100]))

        # need to do it once to get the match's text to be able to store it
        m = re.search(r'<!--.*?-->\r?\n', slurp, flags=re.DOTALL)
        #console.write("matched comment: {} at ({},{})\n".format(m.group(0),m.start(0),m.end(0)))
        self.saved_comment = m.group(0)
        self.has_top_level_comment = True

        # and now do the substitution
        edited = re.sub(r'<!--.*?-->\r?\n', r'', slurp, count=1, flags=re.DOTALL)
        #console.write("edited:\n{}\n".format(edited))

        return edited

    def write_xml_with_optional_comment(self, treeTheme, fTheme):
        #   use xml_declaration=True in order to get <?xml...?>
        #   set encoding="unicode" in .tostring() to get printable string,
        #       or encoding="UTF-8" in .tostring() or .write() to get the encoded bytes for writing UTF-8 to a file
        strOutputXml = ET.tostring(treeTheme.getroot(), encoding="unicode", xml_declaration=True)

        if self.has_top_level_comment:
            m = re.search(r'<\?xml.*?\?>\r?\n', strOutputXml, flags=re.DOTALL)
            e = m.end(0)
            strOutputXml = strOutputXml[:e] + self.saved_comment + strOutputXml[e:]

        # for now, show the result; TODO = write to file fTheme
        #console.write("{}\n".format(strOutputXml))

    def update_langs(self):
        pass

ConfigUpdater().go()
