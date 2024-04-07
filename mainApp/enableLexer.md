Notes for adding GOLANG or another language
- Feature Request: https://github.com/notepad-plus-plus/notepad-plus-plus/issues/8090
- My Blog Post: https://community.notepad-plus-plus.org/topic/25660/additional-languages-dipping-my-toes-into-code-contribution/2
- SciTE: cpp.properties: https://fossies.org/linux/gscite/cpp.properties
- GoLang:
	- Keywords: https://go101.org/article/keywords-and-identifiers.html     => note that `_` is a "special identifier", and could probably
	- Types/Literals: https://go101.org/article/basic-types-and-value-literals.html
    - https://go101.org/article/constants-and-variables.html    => defines `false` and `true`, `iota`, `nil` as constants, so they should be highlighted
	- cpp.properties puts all of the keywords and types in the same category,
		but I think they should go in the two categories, like C++ does in Notepad++
    - https://go.dev/ref/spec#Predeclared_identifiers => groups them into types, constants (and "zero value" which I'd group with that), and functions
        so there are actually keywords (`instre1`), types (`type1`), constants/zeros, and functions as categories that I'd want separate word lists for
        - Studying the LexCPP, I see keywords (SCE_C_WORD=5), keywords2 (SCE_C_WORD2=16), keywords4 (SCE_C_GLOBALCLASS=19)
- Use L_HOLLYWOOD addition as the template for the changes that I need:
	- https://github.com/notepad-plus-plus/notepad-plus-plus/pull/13417/files
	- Notepad_plus_msgs.h: add L_GOLANG to the end of the `enum LangType`
	- menuCmdID.h: add IDM_LANG_GOLANG before IDM_LANG_EXTERNAL
	- ScintillaEditView.cpp:
		- add to LanguageNameInfo ScintillaEditView::_langNameInfoArray[]
		- add to ScintillaEditView::defineDocType switch:
			- for GOLANG, add it to the group going to setLexerCpp(typeDoc)
			- for "simple" languages, call a new function (eg L_HOLLYWOOD)
		- for "mediumComplexity" languages, define the new function
	- ScintillaEditView.h:
		- declare the mediumComplexity
		- declare/define the simpleComplexity (eg setHollywoodLexer)
	- Notepad_plus.cpp: add case IDM_LANG_.../return L_...
	- Notepad_plus.rc: add to long "&Language" and "&Language"/"&<LETTER>" lists
	- NppCommands.cpp: add to long IDM_LANG group in switch()
	- Parameters.cpp: add case L_.../return IDM_LANG_...
And config files:
	- langs.model.xml: <Language>...</>
	- stylers.model.xml & themes: <LexerType name="... </>

possible autoComplete & functionList: https://github.com/MAPJe71/Languages/tree/master/Go/Config
	- I would have to compare autoComplet-Go vs autoComple-Go2 vs go.API, and compare them all to the default list
	- can test functionList-Go against his https://github.com/MAPJe71/Languages/blob/master/Go/main.go
	- to add a new functionList, I would need to add Unit Tests per https://npp-user-manual.org/docs/function-list/#unit-tests


~~~~
From C:\Users\Peter\AppData\Roaming\Notepad++\plugins\Config\PythonScript\scripts\nppCommunity\24xxx\24228_cppEnableGlobalclassKeywords.py
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

So what are the full mapping for instre1 and similar? Search !*.xml for instre1, and find src\Parameters.cpp            |   src\Parameters.h
	if (!lstrcmp(TEXT("instre1"), str)) return LANG_INDEX_INSTR;                                                        |   const int LANG_INDEX_INSTR = 0;
	if (!lstrcmp(TEXT("instre2"), str)) return LANG_INDEX_INSTR2;                                                       |   const int LANG_INDEX_INSTR2 = 1;
	if (!lstrcmp(TEXT("type1"), str)) return LANG_INDEX_TYPE;                                                           |   const int LANG_INDEX_TYPE = 2;
	if (!lstrcmp(TEXT("type2"), str)) return LANG_INDEX_TYPE2;                                                          |   const int LANG_INDEX_TYPE2 = 3;
	if (!lstrcmp(TEXT("type3"), str)) return LANG_INDEX_TYPE3;                                                          |   const int LANG_INDEX_TYPE3 = 4;
	if (!lstrcmp(TEXT("type4"), str)) return LANG_INDEX_TYPE4;                                                          |   const int LANG_INDEX_TYPE4 = 5;
	if (!lstrcmp(TEXT("type5"), str)) return LANG_INDEX_TYPE5;                                                          |   const int LANG_INDEX_TYPE5 = 6;
	if (!lstrcmp(TEXT("type6"), str)) return LANG_INDEX_TYPE6;                                                          |   const int LANG_INDEX_TYPE6 = 7;
	if (!lstrcmp(TEXT("type7"), str)) return LANG_INDEX_TYPE7;                                                          |   const int LANG_INDEX_TYPE7 = 8;

	if ((str[1] == '\0') && (str[0] >= '0') && (str[0] <= '8')) // up to KEYWORDSET_MAX
		return str[0] - '0';


And mapping that:                   | LexCPP.h                                           | List#                        | Style definitions                     and names                   | SciTE:cpp.properties desc
                                    | const char *const cppWordLists[] = {               |                                                                                                  |
instre1     LANG_INDEX_INSTR = 0;   |        "Primary keywords and identifiers",         |	WordList keywords;          | => 05:SCE_C_WORD                 <= "INSTRUCTION WORD" inistre1   |   puts both syntax and types here
instre2     LANG_INDEX_INSTR2 = 1;  |        "Secondary keywords and identifiers",       |	WordList keywords2;         | => 16:SCE_C_WORD2                <= "TYPE WORD"                   |   for highlighting user defined keywords or function calls or similar
type1       LANG_INDEX_TYPE = 2;    |        "Documentation comment keywords",           |	WordList keywords3;         | => 17:SCE_C_COMMENTDOCKEYWORD    <= "COMMENT DOC KEYWORD"         |   for doxygen
type2       LANG_INDEX_TYPE2 = 3;   |        "Global classes and typedefs",              |	WordList keywords4;         | => 19:SCE_C_GLOBALCLASS          <= TBD                           |   <n.a>
type3       LANG_INDEX_TYPE3 = 4;   |        "Preprocessor definitions",                 |	WordList ppDefinitions;     |                                                                   |   for preprocessor definitions, grays things out
type4       LANG_INDEX_TYPE4 = 5;   |        "Task marker and error marker keywords",    |	WordList markerList;        | => 26:SCE_C_TASKMARKER                                            |   only works in comments, for things like TODO
                                    |         nullptr,                                   |
                                    | };                                                 |

So even though Go has four lists that I'd _like_ to use, it might only accept instre1, instre2, and type2; with type1 being reserved for doxygen
Weird, I've got mismatch: my notes from 24228 claim that type1 is going to keywords2, but the 0..8 mapping implies that type1 really goes to keywords3.
I did verify that COMMENT_DOCK_KEYWORD really does use type2-list and the \param and similar comment-doc keywords from langs.model.xml.
So apparently, Notepad++ isn't doing the mapping I thought.

ScintillaEditView::setCppLexer():
    SCI_SETKEYWORDS, 2, doxygenKeyWords_char        # populates that string from the getWordList(LANG_INDEX_TYPE2)
    SCI_SETKEYWORDS, 0, cppInstrs                   # populates that string from getCompleteKeywordList(LANG_INDEX_INSTR)
    SCI_SETKEYWORDS, 1, cppTypes                    # populates that string from getCompleteKeywordList(LANG_INDEX_TYPE)

So if I wanted keywords4 to be populated, I would have to add
    SCI_SETKEYWORDS, 3, _____                       # where ____ needs to be populated from getCompleteKeywordList(LANG_INDEX_INSTR2)
