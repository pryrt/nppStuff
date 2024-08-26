# encoding=utf-8
"""Config Files Sometimes Need Updating, Too

When it updates, Notepad++ tends to avoid updating important things like langs.xml, stylers.xml, and your themes;
it does this because it doesn't want to overwrite your customizations, but that has the drawback that you end up
missing new styles, new languages, and updated keyword lists.

Author: PeterJones @ community.notepad-plus-plus.org
Version: 1.0 (2024-Aug-26)

INSTRUCTIONS:
1. Install this script per FAQ https://community.notepad-plus-plus.org/topic/23039/faq-how-to-install-and-run-a-script-in-pythonscript
2. If you are installed in "C:\Program Files\Notepad++", run Notepad++ as Administrator, otherwise run it normally
3. Run this script from PythonScript 3
"""
from Npp import editor,notepad,console,MESSAGEBOXFLAGS
import xml.etree.ElementTree as ET  # https://docs.python.org/3/library/xml.etree.elementtree.html
import os
import re
import textwrap

if notepad.getPluginVersion() < '3.0':
    ET.indent = lambda x, space="", level=0: None   # avoid `AttributeError: 'module' object has no attribute 'indent'` in PS2

class CommentedTreeBuilder(ET.TreeBuilder):
    # https://stackoverflow.com/a/34324359/5508606
    def comment(self, data):
        self.start(ET.Comment, {})
        self.data(data)
        self.end(ET.Comment)

class ConfigUpdater(object):
    def __init__(self):
        self.dirNpp                 = notepad.getNppDir()
        self.dirPluginConfig        = notepad.getPluginConfigDir()
        self.dirNppConfig           = os.path.dirname(os.path.dirname(self.dirPluginConfig))
        self.saved_comment          = None
        self.has_top_level_comment  = False
        self.tree_model             = None
        self.model_default_colors   = { 'fgColor': None, 'bgColor': None }

    def go(self):
        self.get_model_styler()

        dirCfgThemes = os.path.join(self.dirNppConfig, 'themes')
        if False:
            # debug path -- just do ExtraTheme
            self.update_stylers(dirCfgThemes, 'ExtraTheme.xml') #TMP#
        else:
            # update main stylers.xml
            self.update_stylers(self.dirNppConfig, 'stylers.xml')

            # then loop over all CFG-directory themes and call .update_stylers()
            if os.path.exists(dirCfgThemes):
                for f in os.listdir(dirCfgThemes):
                    if f[-4:]=='.xml' and os.path.isfile(os.path.join(dirCfgThemes,f)):
                        self.update_stylers(dirCfgThemes, f)

            # finally, loop over all NPP-directory themes and call .update_stylers() [skip if this is same directory as CFG]
            dirNppThemes = os.path.join(self.dirNpp, 'themes')
            if os.path.exists(dirNppThemes) and dirCfgThemes != dirNppThemes:
                for f in os.listdir(dirNppThemes):
                    if f[-4:]=='.xml' and os.path.isfile(os.path.join(dirNppThemes,f)):
                        self.update_stylers(dirNppThemes, f)

        self.update_langs()

        console.write("DONE with ConfigUpdater\n\n")

        ans = notepad.messageBox(
            # message
            """Exit Notepad++ Now?
            The updated themes and langs files will not take effect until you restart Notepad++.
            Answer YES to have the script SaveAll and exit for you.
            Answer NO if you will exit and restart Notepad++ yourself.
            """,
            "Exit Notepad++ Now?",  # title
            MESSAGEBOXFLAGS.YESNO   # options
        )
        if ans == MESSAGEBOXFLAGS.RESULTYES:
            notepad.saveAllFiles()
            notepad.menuCommand(MENUCOMMAND.FILE_EXIT)

        return

    def get_model_styler(self):
        fModel = os.path.join(self.dirNpp, 'stylers.model.xml')
        self.tree_model = ET.parse(fModel, parser=ET.XMLParser(target=CommentedTreeBuilder()))
        elDefaultWidget = self.tree_model.find(".//GlobalStyles/WidgetStyle[@styleID='32']")
        self.model_default_colors['fgColor'] = elDefaultWidget.attrib['fgColor']
        self.model_default_colors['bgColor'] = elDefaultWidget.attrib['bgColor']
        #console.write("get_model_styler({}) => default:{}\n".format(fModel, self.model_default_colors))
        return

    def update_stylers(self, themeDir, themeName):
        fTheme = os.path.join(themeDir, themeName)
        console.write("update_stylers('{}')\n".format(fTheme))

        # preserve comments by using
        #   <https://stackoverflow.com/a/34324359/5508606>

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

        # and get the active theme's default colors, too
        self.get_theme_globals(treeTheme)

        # Need to grab the Theme's <LexerStyles> node for future insertions
        elThemeLexerStyles = treeTheme.find('LexerStyles')
        #console.write("Theme's LexerStyles: {} with {} sub-nodes\n".format(elThemeLexerStyles, len(elThemeLexerStyles)))

        # iterate through all the treeModel, and see if there are any LexerTypes that cannot also be found in treeTheme
        for elModelLexer in self.tree_model.iter("LexerType"):
            #console.write("LexerType {}\n".format(elModelLexer.attrib))
            strToFind = ".//LexerType[@name='{}']".format(elModelLexer.attrib['name'])
            elStylersMatchLT = treeTheme.find(strToFind)
            if elStylersMatchLT is None:
                #console.write("NOT FOUND[{}] => {}\n".format(strToFind, elStylersMatchLT))
                self.add_missing_lexer(elModelLexer, elThemeLexerStyles)
            else:
                # iterate through each WordsStyle in the elModelLexer and see if it can
                #   be found in the elStylersMatchLT (similar to GlobalStyles's add_missing_globals(), below)
                self.add_missing_lexer_styles(elModelLexer, elStylersMatchLT)

        # sort the lexers by name
        #       cf: https://stackoverflow.com/questions/25338817/sorting-xml-in-python-etree
        #       ``` def sortchildrenby(parent, attr):
        #       ```     parent[:] = sorted(parent, key=lambda child: child.get(attr))
        #       ``` sortchildrenby(root, 'NAME')
        #   use trick <https://stackoverflow.com/a/18411610/5508606> to get 'searchResult' sorted last
        elThemeLexerStyles[:] = sorted(elThemeLexerStyles, key=lambda child: (child.get('name') == 'searchResult', child.get('name')))

        # look for missing GlobalStyles elements as well
        self.add_missing_globals(treeTheme)

        # fix the indentation for the whole tree
        if notepad.getPluginVersion() > '2.0':
            ET.indent(treeTheme, space = "    ", level=0)

        # write the tree to an XML file (reinserting the comment if needed)
        self.write_xml_with_optional_comment(treeTheme, fTheme)

        return

    def get_theme_globals(self, treeTheme):
        elThemeGlobalStyles = treeTheme.find('GlobalStyles')

        # See if the "Default Style" already exists
        #   if so, use the colors from there for new GlobalStyles elements,
        #   otherwise use the model default colors
        self.active_theme_default_colors = {
            'fgColor': self.model_default_colors['fgColor'],
            'bgColor': self.model_default_colors['bgColor'],
        }
        elThemeGlobalDefaults = elThemeGlobalStyles.find("WidgetStyle[@styleID='32']")
        if elThemeGlobalDefaults is not None:
            self.active_theme_default_colors['fgColor'] = elThemeGlobalDefaults.attrib['fgColor']
            self.active_theme_default_colors['bgColor'] = elThemeGlobalDefaults.attrib['bgColor']
            #console.write("Found Theme Globals: {}\n".format(self.active_theme_default_colors))
        #else:
        #    console.write("Missing Theme Globals: using {} by default\n".format(self.active_theme_default_colors))

    def add_missing_lexer(self, elModelLexer, elLexerStyles):
        #console.write("add_missing_lexer({})\n".format(elModelLexer.attrib['name']))
        elNewLexer = ET.SubElement(elLexerStyles, 'LexerType', attrib=elModelLexer.attrib)
        for elWordsStyle in elModelLexer.iter("WordsStyle"):
            #console.write("- need WordsStyle => {}\n".format(elWordsStyle.attrib))
            attr = {
                'name': elWordsStyle.attrib['name'],
                'styleID': elWordsStyle.attrib['styleID'],
                'fgColor': self.model_default_colors['fgColor'],
                'bgColor': self.model_default_colors['bgColor'],
                'fontName': "",
                'fontStyle': "",
                'fontSize': "",
            }
            if 'keywordClass' in elWordsStyle.attrib:
                attr['keywordClass'] = elWordsStyle.attrib['keywordClass']
            ET.SubElement(elNewLexer, 'WordsStyle', attrib=attr)

        #if notepad.getPluginVersion() > '2.0':
        #    ET.indent(elNewLexer, space = "    ", level=2)

    def add_missing_globals(self, treeTheme):
        # grab the source and destination GlobalStyles
        elModelGlobalStyles = self.tree_model.find('GlobalStyles')
        elThemeGlobalStyles = treeTheme.find('GlobalStyles')
        elThemeNewGlobals = ET.Element('GlobalStyles')

        # iterate through the model GlobalStyles elements
        elPreviousThemeWidget = None
        for elWidgetStyle in elModelGlobalStyles:
            if "function Comment" in str(elWidgetStyle):
                #console.write("MODEL <!--{}-->\n".format(elWidgetStyle.text))
                elThemeNewGlobals.append(ET.Comment(elWidgetStyle.text))
            else:   # normal element
                #console.write("MODEL: {} => {}\n".format(elWidgetStyle.tag, elWidgetStyle.attrib))
                strSearch = "WidgetStyle[@name='{}']".format(elWidgetStyle.attrib['name'])
                elFoundThemeWidget = elThemeGlobalStyles.find(strSearch)
                msg = None
                if elFoundThemeWidget is None:
                    # need to add the new widget with the correct default colors
                    elNewWidget = ET.SubElement(elThemeNewGlobals, 'WidgetStyle', {
                        'name': elWidgetStyle.attrib['name'],
                        'styleID': elWidgetStyle.attrib['styleID'],
                        'fgColor': self.active_theme_default_colors['fgColor'],
                        'bgColor': self.active_theme_default_colors['bgColor'],
                        'fontName': '',
                        'fontStyle': '0',
                        'fontSize': '',
                    })
                    msg = 'ADDED'
                else:
                    # copy this from the theme to the new
                    #console.write("Widget attrib = {}\n".format(elFoundThemeWidget.attrib))
                    elNewWidget = ET.SubElement(elThemeNewGlobals, 'WidgetStyle', {
                        'name': elWidgetStyle.attrib['name'],
                        'styleID': elWidgetStyle.attrib['styleID'],
                        'fgColor': elFoundThemeWidget.attrib['fgColor'] if 'fgColor' in elFoundThemeWidget.attrib else self.active_theme_default_colors['fgColor'],
                        'bgColor': elFoundThemeWidget.attrib['bgColor'] if 'bgColor' in elFoundThemeWidget.attrib else self.active_theme_default_colors['bgColor'],
                        'fontName': elFoundThemeWidget.attrib['fontName'] if 'fontName' in elFoundThemeWidget.attrib else '',
                        'fontStyle': elFoundThemeWidget.attrib['fontStyle'] if 'fontStyle' in elFoundThemeWidget.attrib else '0',
                        'fontSize': elFoundThemeWidget.attrib['fontSize'] if 'fontSize' in elFoundThemeWidget.attrib else '',
                    })
                    msg = 'FOUND'

                elPreviousThemeWidget = elNewWidget
                #console.write("{} {}\n".format(msg, elPreviousThemeWidget.attrib))

        # populate the actual with the new
        elThemeGlobalStyles[:] = elThemeNewGlobals[:]

    def add_missing_lexer_styles(self, elModelLexer, elThemeLexerType):
        #console.write("add_missing_lexer_styles({})\n".format(elModelLexer.attrib['name']))

        # use values from get_theme_globals() in self.active_theme_default_colors[]
        #   as the colors for use when looping through the MODEL's list for this lexer
        #   add any that are missing need to be added, using the theme's GlobalColors
        for elModelStyle in elModelLexer.iter("WordsStyle"):
            #console.write("- check if WordsStyle {} is already in this theme\n".format(elModelStyle.attrib))
            strSearch = "WordsStyle[@styleID='{}']".format(elModelStyle.attrib['styleID'])
            elFoundThemeStyle = elThemeLexerType.find(strSearch)
            if elFoundThemeStyle is None:
                elNewStyle = ET.SubElement(elThemeLexerType, 'WordsStyle', {
                    'name':         elModelStyle.attrib['name'],
                    'styleID':      elModelStyle.attrib['styleID'],
                    'fgColor':      self.active_theme_default_colors['fgColor'],
                    'bgColor':      self.active_theme_default_colors['bgColor'],
                    'fontName':     '',
                    'fontStyle':    '0',
                    'fontSize':     '',
                })
                #console.writeError("- ADDED to {}: style {}\n".format(elThemeLexerType.attrib['name'], elNewStyle.attrib))
            else:
                # for names that have changed n the model, update the theme to match the model's name
                #   (keeps up-to-date with the most recent model)
                if elFoundThemeStyle.attrib['name'] != elModelStyle.attrib['name']:
                    #console.write("- RENAME {}'s styleID={}: theme's {} to model's {}\n".format(elModelLexer.attrib['name'], elModelStyle.attrib['styleID'], elFoundThemeStyle.attrib['name'], elModelStyle.attrib['name']))
                    elFoundThemeStyle.attrib['name'] = elModelStyle.attrib['name']
                    #console.writeError("- RENAME in {}: style {}\n".format(elThemeLexerType.attrib['name'], elFoundThemeStyle.attrib))

        return


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
        if notepad.getPluginVersion() < '3.0':
            # Python 2.7 has different options on the xml.etree.ElementTree module
            strOutputXml = '<?xml version="1.0" encoding="UTF-8" ?>\n' + ET.tostring(treeTheme.getroot(), encoding="utf-8")
            # also, the .indent method didn't work, so needs some fixing of indentation
            import re
            strOutputXml = re.sub(r'><Widget', r'>\n        <Widget', strOutputXml)
            strOutputXml = re.sub(r'></',      r'>\n    </',          strOutputXml)
            strOutputXml = re.sub(r'></',      r'>\n    </',          strOutputXml)
            strOutputXml = re.sub(r'/><!--',   r'/>\n        <!--',   strOutputXml)
        else:
            strOutputXml = ET.tostring(treeTheme.getroot(), encoding="unicode", xml_declaration=True)

        if self.has_top_level_comment:
            m = re.search(r'<\?xml.*?\?>\r?\n', strOutputXml, flags=re.DOTALL)
            e = m.end(0)
            strOutputXml = strOutputXml[:e] + self.saved_comment + strOutputXml[e:]

        #console.write("{}\n".format(strOutputXml))
        with open(fTheme, 'w') as f:
            f.write(strOutputXml)

    def update_langs(self):
        fLangActive = os.path.join(self.dirNppConfig, 'langs.xml')
        fLangModel = os.path.join(self.dirNpp, 'langs.model.xml')
        console.write("update_langs('{}', '{}')\n".format(fLangActive, fLangModel))

        # get the trees
        self.tree_langmodel = ET.parse(fLangModel, parser=ET.XMLParser(target=CommentedTreeBuilder()))
        self.tree_langs = ET.parse(fLangActive, parser=ET.XMLParser(target=CommentedTreeBuilder()))

        # Need to grab the active and model <Languages> nodes
        elActiveLanguages = self.tree_langs.find('Languages')
        elModelLanguages = self.tree_langmodel.find('Languages')
        #console.write("Theme's LexerStyles: {} with {} sub-nodes\n".format(elThemeLexerStyles, len(elThemeLexerStyles)))

        # Loop through model languages, inserting missing data:
        for elModelLang in elModelLanguages.iter("Language"):
            strToFind = ".//Language[@name='{}']".format(elModelLang.attrib['name'])
            elLangMatch = elActiveLanguages.find(strToFind)

            # 1. add any missing languages to Active
            if elLangMatch is None:
                elActiveLanguages.append(elModelLang)
                #console.write("- ADDED {}<{}>\n".format(elModelLang.tag, elModelLang.attrib))
                continue

            # Loop through keyword elements in the model, inserting missing data
            for elModelLangKeyword in elModelLang.iter("Keywords"):
                #console.write("DEBUG: {}'s MODEL {}<{}>\n".format(elModelLang.attrib['name'], elModelLangKeyword.tag, elModelLangKeyword.attrib))
                strToFind = ".//Keywords[@name='{}']".format(elModelLangKeyword.attrib['name'])
                elLangKWMatch = elLangMatch.find(strToFind)

                # 2. add any missing Keyword elements to existing Active
                if elLangKWMatch is None:
                    elLangMatch.append(elModelLangKeyword)
                    #console.write("- ADDED {}<{}> to {}<{}>\n".format(elModelLangKeyword.tag, elModelLangKeyword.attrib, elModelLang.tag, elModelLang.attrib['name']))
                    continue

                # 3. add any missing keywords to existing Active element
                if elModelLangKeyword.text is not None:
                    kw_list_model = elModelLangKeyword.text.split()
                    kw_list_active = elLangKWMatch.text.split() if elLangKWMatch.text else []

                    # if the active list doesn't have any words, add all of the words from the model
                    if len(kw_list_active)==0:
                        elLangKWMatch.text = elModelLangKeyword.text
                        #console.write("- ADDED ({}) to empty {}<{}> list in  {}<{}>\n".format(elLangKWMatch.text, elLangKWMatch.tag, elLangKWMatch.attrib['name'], elModelLang.tag, elModelLang.attrib['name']))
                        continue

                    # loop through the model words and add any missing ones
                    was_added = []
                    for str_kw in kw_list_model:
                        if str_kw not in kw_list_active:
                            kw_list_active.append(str_kw)
                            was_added.append(str_kw)

                    if len(was_added):
                        #console.write("- ADDED {} to partial {}<{}> list in  {}<{}>\n".format(was_added, elLangKWMatch.tag, elLangKWMatch.attrib['name'], elModelLang.tag, elModelLang.attrib['name']))
                        pass

                    if len(kw_list_active)>1:
                        kw_list_active[:] = sorted(kw_list_active)

                    # update the actual list into the sorted text (with no more than ~8000 char per line)
                    elLangKWMatch.text = textwrap.fill(" ".join(kw_list_active), width=8000, break_long_words=False, break_on_hyphens=False, subsequent_indent=" "*16)

            # bringing in missing comments from before specific keywords

            # Look for comments in the model for this language
            kw_comment_map = { 'model': {}, 'active': {} }
            keep_comment = None
            for elModelLangKWComment in elModelLang:
                if "function Comment" in str(elModelLangKWComment):
                    keep_comment = elModelLangKWComment
                elif keep_comment is not None:
                    kw_comment_map['model'][elModelLangKWComment.attrib['name']] = keep_comment
                    keep_comment = None
            #console.write("DEBUG: {} MODEL keyword comments = {}\n".format(elModelLang.attrib['name'], kw_comment_map['model']))

            # now look for comments in the active for this language
            keep_comment = None
            for elActiveLangKWComment in elLangMatch:
                if "function Comment" in str(elActiveLangKWComment):
                    if keep_comment is not None:
                        raise Exception("NOT IMPLEMENTED: cannot have multiple lines of pre-<Keywords> comments in a row\nInform the author that Notepad++ v{} langs.model.xml requires this feature...".format(".".join(str(x) for x in notepad.getVersion())))
                    keep_comment = elActiveLangKWComment
                elif keep_comment is not None:
                    kw_comment_map['active'][elActiveLangKWComment.attrib['name']] = keep_comment
                    keep_comment = None
            #console.write("DEBUG: {} ACTIVE keyword comments = {}\n".format(elModelLang.attrib['name'], kw_comment_map['active']))

            # now determine if active is missing any from model, and add it
            for key,cmt in kw_comment_map['model'].items():
                if key not in kw_comment_map['active']:
                    strSearch = "Keywords[@name='{}']".format(key)
                    elFoundLanguage = elLangMatch.find(strSearch)
                    if elFoundLanguage is None: continue    # this should never happen, but fail gracefully if it does

                    idx = list(elLangMatch).index(elFoundLanguage)
                    elLangMatch.insert(idx, cmt)

                    #console.write("DEBUG: {} didn't have comment before {}, so added <!--{}-->\n".format(elModelLang.attrib['name'], key, cmt.text))


        # Sort langs with comments
        self.sort_langs_with_comments(elActiveLanguages)

        # fix the indentation for the whole tree
        if notepad.getPluginVersion() > '2.0':
            ET.indent(self.tree_langs, space = "    ", level=0)

        # output the final file

        #   use xml_declaration=True in order to get <?xml...?>
        #   set encoding="unicode" in .tostring() to get printable string,
        #       or encoding="UTF-8" in .tostring() or .write() to get the encoded bytes for writing UTF-8 to a file
        if notepad.getPluginVersion() < '3.0':
            strOutputXml = '<?xml version="1.0" encoding="UTF-8" ?>\n' + ET.tostring(self.tree_langs.getroot(), encoding="utf-8")
        else:
            strOutputXml = ET.tostring(self.tree_langs.getroot(), encoding="unicode", xml_declaration=True)

        #console.write("{}\n".format(strOutputXml))
        with open(fLangActive, 'w') as f:
            f.write(strOutputXml)

    def sort_langs_with_comments(self, elActiveLanguages):
        # Temporarily store/remove comments
        comment_map = {}
        unnamed_comment_key = None
        for elThisLanguageRow in elActiveLanguages:
            #console.write("ActiveLangauges: child {} => {}\n".format(elThisLanguageRow.tag, elThisLanguageRow.attrib))
            if "function Comment" in str(elThisLanguageRow):
                unnamed_comment_key = list(elActiveLanguages).index(elThisLanguageRow)
                #console.write("ActiveLanguages: comment '{}' at index {}\n".format(elThisLanguageRow.text, unnamed_comment_key))
                comment_map[unnamed_comment_key] = { 'element': elThisLanguageRow, 'before': None }
            elif unnamed_comment_key is not None:
                comment_map[unnamed_comment_key]['before'] = elThisLanguageRow.attrib['name']
                unnamed_comment_key = None
        #console.write("Intermediate comment map = {}\n".format(comment_map))
        for key,cmt in comment_map.items():
            elActiveLanguages.remove(cmt['element'])
        #console.write("Final comment map = {}\n".format(comment_map))

        # sort the languages: normal, alphabetical, searchResult
        #   use a variant of the one earlier, except map 'normal' to 0, 'searchResult' to 2, and everything else to 1 so it will be sorted in between
        elActiveLanguages[:] = sorted(elActiveLanguages, reverse=False, key=lambda child: (2 if (child.get('name') == 'searchResult') else 0 if (child.get('name') == 'normal') else 1, child.get('name')))

        # reinsert comments
        for key,cmt in comment_map.items():
            strSearch = "Language[@name='{}']".format(cmt['before'])
            elFoundLanguage = elActiveLanguages.find(strSearch)
            if elFoundLanguage is not None:
                idx = list(elActiveLanguages).index(elFoundLanguage)
                elActiveLanguages.insert(idx, cmt['element'])

ConfigUpdater().go()