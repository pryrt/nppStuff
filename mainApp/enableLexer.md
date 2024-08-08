# Go / Golang

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
	- .../src/MISC/PluginsManager/Notepad_plus_msgs.h: add L_GOLANG to the end of the `enum LangType`
	- .../src/menuCmdID.h: add IDM_LANG_GOLANG before IDM_LANG_EXTERNAL
	- .../src/ScintillaComponent/ScintillaEditView.cpp:
		- add to LanguageNameInfo ScintillaEditView::_langNameInfoArray[]
  			- this is the list of language/shortName/longName/L_XXXX/lexer that maps everything together
		- add to ScintillaEditView::defineDocType switch:
			- for GOLANG, add it to the group going to setLexerCpp(typeDoc)
			- for "simple" languages, call a new function (eg L_HOLLYWOOD)
		- for "mediumComplexity" languages, define the new function
	- .../src/ScintillaComponent/ScintillaEditView.h:
		- declare the mediumComplexity
		- declare/define the simpleComplexity (eg setHollywoodLexer)
	- .../src/Notepad_plus.cpp: add case IDM_LANG_.../return L_...
	- .../src/Notepad_plus.rc: add to long "&Language" and "&Language"/"&<LETTER>" lists
	- .../src/NppCommands.cpp: add to long IDM_LANG group in switch()
	- .../src/Parameters.cpp: add case L_.../return IDM_LANG_...
And config files:
	- .../src/langs.model.xml: <Language>...</>
	- .../src/stylers.model.xml & .../installer/themes/*.xml: <LexerType name="... </>

possible autoComplete & functionList: https://github.com/MAPJe71/Languages/tree/master/Go/Config
	- I would have to compare autoComplet-Go vs autoComple-Go2 vs go.API, and compare them all to the default list
	- can test functionList-Go against his https://github.com/MAPJe71/Languages/blob/master/Go/main.go
	- to add a new functionList, I would need to add Unit Tests per https://npp-user-manual.org/docs/function-list/#unit-tests


-----
From C:\Users\Peter\AppData\Roaming\Notepad++\plugins\Config\PythonScript\scripts\nppCommunity\24xxx\24228_cppEnableGlobalclassKeywords.py

```
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
```

So what are the full mapping for instre1 and similar? Search !*.xml for instre1, and find src\Parameters.cpp
```
                                                                            |   src\Parameters.h
	if (!lstrcmp(TEXT("instre1"), str)) return LANG_INDEX_INSTR;            |   const int LANG_INDEX_INSTR = 0;
	if (!lstrcmp(TEXT("instre2"), str)) return LANG_INDEX_INSTR2;           |   const int LANG_INDEX_INSTR2 = 1;
	if (!lstrcmp(TEXT("type1"), str)) return LANG_INDEX_TYPE;               |   const int LANG_INDEX_TYPE = 2;
	if (!lstrcmp(TEXT("type2"), str)) return LANG_INDEX_TYPE2;              |   const int LANG_INDEX_TYPE2 = 3;
	if (!lstrcmp(TEXT("type3"), str)) return LANG_INDEX_TYPE3;              |   const int LANG_INDEX_TYPE3 = 4;
	if (!lstrcmp(TEXT("type4"), str)) return LANG_INDEX_TYPE4;              |   const int LANG_INDEX_TYPE4 = 5;
	if (!lstrcmp(TEXT("type5"), str)) return LANG_INDEX_TYPE5;              |   const int LANG_INDEX_TYPE5 = 6;
	if (!lstrcmp(TEXT("type6"), str)) return LANG_INDEX_TYPE6;              |   const int LANG_INDEX_TYPE6 = 7;
	if (!lstrcmp(TEXT("type7"), str)) return LANG_INDEX_TYPE7;              |   const int LANG_INDEX_TYPE7 = 8;

	if ((str[1] == '\0') && (str[0] >= '0') && (str[0] <= '8')) // up to KEYWORDSET_MAX
		return str[0] - '0';
```

And mapping that:
|  type     |    index-of-8               | LexCPP.h order                                     | List#                        | Style definitions               |   and names                   | SciTE:cpp.properties desc
|-----------|-----------------------------|----------------------------------------------------|------------------------------|---------------------------------|-------------------------------|------------------------
|           |                             | const char *const cppWordLists[] = {               |                              |                                 |                               |
|~~instre1~~|  ~~LANG_INDEX_INSTR = 0;~~  |        "Primary keywords and identifiers",         |	WordList keywords;          | => 05:SCE_C_WORD                | "INSTRUCTION WORD" inistre1   |   puts both syntax and types here
|~~instre2~~|  ~~LANG_INDEX_INSTR2 = 1;~~ |        "Secondary keywords and identifiers",       |	WordList keywords2;         | => 16:SCE_C_WORD2               | "TYPE WORD"                   |   for highlighting user defined keywords or function calls or similar
|~~type1~~  |  ~~LANG_INDEX_TYPE = 2;~~   |        "Documentation comment keywords",           |	WordList keywords3;         | => 17:SCE_C_COMMENTDOCKEYWORD   | "COMMENT DOC KEYWORD"         |   for doxygen
|~~type2~~  |  ~~LANG_INDEX_TYPE2 = 3;~~  |        "Global classes and typedefs",              |	WordList keywords4;         | => 19:SCE_C_GLOBALCLASS         | TBD                           |   <n.a>
|~~type3~~  |  ~~LANG_INDEX_TYPE3 = 4;~~  |        "Preprocessor definitions",                 |	WordList ppDefinitions;     |                                 |                               |   for preprocessor definitions, grays things out
|~~type4~~  |  ~~LANG_INDEX_TYPE4 = 5;~~  |        "Task marker and error marker keywords",    |	WordList markerList;        | => 26:SCE_C_TASKMARKER          |                               |   only works in comments, for things like TODO
|           |                             |         nullptr,                                   |                              |                                 |                               |
|           |                             | };                                                 |                              |                                 |                               |


So even though Go has four lists that I'd _like_ to use, it might only accept instre1, instre2, and type2; with type1 being reserved for doxygen
Weird, I've got mismatch: my notes from 24228 claim that type1 is going to keywords2, but the 0..8 mapping implies that type1 really goes to keywords3.
I did verify that COMMENT_DOCK_KEYWORD really does use type2-list and the \param and similar comment-doc keywords from langs.model.xml.
So apparently, Notepad++ isn't doing the mapping I thought.

```
ScintillaEditView::setCppLexer():
    SCI_SETKEYWORDS, 2, doxygenKeyWords_char        # populates that string from the getWordList(LANG_INDEX_TYPE2)
    SCI_SETKEYWORDS, 0, cppInstrs                   # populates that string from getCompleteKeywordList(LANG_INDEX_INSTR)
    SCI_SETKEYWORDS, 1, cppTypes                    # populates that string from getCompleteKeywordList(LANG_INDEX_TYPE)
```

So if I wanted keywords4 to be populated, I would have to add
```
    SCI_SETKEYWORDS, 3, _____                       # where ____ needs to be populated from getCompleteKeywordList(LANG_INDEX_INSTR2)
```
Since it was wrong above, cross those out.

So if I want to experiment with that, I'd need to add instre2 => SCE_C_GLOBALCLASS(19) => "SOMENAME" to the XML files, and add the overhead for `SCI_SETKEYWORDS,3`  

Since the Go reference calls them "predeclared identifiers", it would make sense to put all the constants/zero-values/functions together (I'd prefer separate, but LexCPP doesn't give that option), and call "SOMENAME" as "PREDECLARED IDENTIFIERS".

I'll give that a try sometime when my mind is more fresh.  

For now, I'll just fix APIs/go.xml to use `&lt;-` instead of `<-` in the attribute, and add the XML for the re-categorization

---

Added the instre2 to `ScintillaEditView::setCppLexer()`.  Added "go" to all the themes, not just `stylers.model.xml`
per https://stackoverflow.com/questions/10298291/cannot-push-to-github-keeps-saying-need-merge :
```
git reset --soft 1f4cbdb
git commit -m "Add syntax highlighting for Go/Golang" -m "(as done in SciTE, Go/Golang can use cpp lexer)"
git push -f origin
```


2024-Apr-11: my "Go" PR was merged into main codebase!

---

# Raku

- https://github.com/notepad-plus-plus/notepad-plus-plus/issues/4465
- https://github.com/perl6/user-experience/issues/19

MAPJe71 doesn't have functionList for Raku, even as a starting point.  Tried a websearch for "raku" and "notepad++" and "functionlist", but found nothing; and without "functionlist", there is more, but not anything helpful.  Since I didn't include functionList for Go, either, that's not a big deal.

- https://fossies.org/linux/gscite/raku.properties

extensions: `*.p6;*.pm6;*.pod6;*.t6;*.raku;*.rakumod;*.rakudoc;*.rakutest`

Lexer options (might need to set one or more of these): https://github.com/notepad-plus-plus/notepad-plus-plus/blob/master/lexilla/lexers/LexRaku.cxx#L134-L148

| N++     | Description              | list        | LexRaku Var          | SCE               | Keywords
|---------|--------------------------|-------------|----------------------|-------------------|----------
| instre1 | base                     | 0 keywords  | keywords             | SCE_RAKU_WORD     | BEGIN CATCH CHECK CONTROL END ENTER EVAL FIRST INIT KEEP LAST LEAVE NEXT POST PRE START TEMP UNDO after also andthen as async augment bag before but category circumfix class cmp complex constant contend default defer div does dynamic else elsif enum eq eqv extra fail fatal ff fff for gather gcd ge given grammar gt handles has if infix is lcm le leave leg let lift loop lt macro make maybe method mix mod module multi ne not o only oo or orelse orwith postcircumfix postfix prefix proto regex repeat require return-rw returns role rule size_t slang start str submethod subset supersede take temp term token trusts try unit unless until when where while with without x xor xx
| instre2 | functions                | 1 keywords2 | functions            | SCE_RAKU_FUNCTION | ACCEPTS AT-KEY EVALFILE EXISTS-KEY Filetests IO STORE abs accept acos acosec acosech acosh acotan acotanh alarm and antipairs asec asech asin asinh atan atan2 atanh base bind binmode bless break caller ceiling chars chdir chmod chomp chop chr chroot chrs cis close closedir codes comb conj connect contains continue cos cosec cosech cosh cotan cotanh crypt dbm defined die do dump each elems eof exec exists exit exp expmod fc fcntl fileno flat flip flock floor fmt fork formats functions get getc getpeername getpgrp getppid getpriority getsock gist glob gmtime goto grep hyper import index int invert ioctl is-prime iterator join keyof keys kill kv last lazy lc lcfirst lines link list listen local localtime lock log log10 lsb lstat map match mkdir msb msg my narrow new next no of open ord ords our pack package pairs path pick pipe polymod pop pos pred print printf prototype push quoting race rand read readdir readline readlink readpipe recv redo ref rename requires reset return reverse rewinddir rindex rmdir roots round samecase say scalar sec sech seek seekdir select semctl semget semop send set setpgrp setpriority setsockopt shift shm shutdown sign sin sinh sleep sockets sort splice split sprintf sqrt srand stat state study sub subst substr substr-rw succ symlink sys syscall system syswrite tan tanh tc tclc tell telldir tie time times trans trim trim-leading trim-trailing truncate uc ucfirst unimatch uniname uninames uniprop uniprops unival unlink unpack unpolar unshift untie use utime values wait waitpid wantarray warn wordcase words write
| type1   | types                    | 2 keywords3 | typesBasic           | SCE_RAKU_TYPEDEF  | AST Any Block Bool CallFrame Callable Code Collation Compiler Complex ComplexStr Cool CurrentThreadScheduler Date DateTime Dateish Distribution Distribution::Hash Distribution::Locally Distribution::Path Duration Encoding Encoding::Registry Endian FatRat ForeignCode HyperSeq HyperWhatever Instant Int IntStr Junction Label Lock::Async Macro Method Mu Nil Num NumStr Numeric ObjAt Parameter Perl PredictiveIterator Proxy RaceSeq Rat RatStr Rational Real Routine Routine::WrapHandle Scalar Sequence Signature Str StrDistance Stringy Sub Submethod Telemetry Telemetry::Instrument::Thread Telemetry::Instrument::ThreadPool Telemetry::Instrument::Usage Telemetry::Period Telemetry::Sampler UInt ValueObjAt Variable Version Whatever WhateverCode atomicint bit bool buf buf1 buf16 buf2 buf32 buf4 buf64 buf8 int int1 int16 int2 int32 int4 int64 int8 long longlong num num32 num64 rat rat1 rat16 rat2 rat32 rat4 rat64 rat8 uint uint1 uint16 uint2 uint32 uint4 uint64 uint8 utf16 utf32 utf8
| type2   | types composite          | 3 keywords4 | typesComposite       | SCE_RAKU_TYPEDEF  | Array Associative Bag BagHash Baggy Blob Buf Capture Enumeration Hash Iterable Iterator List Map Mix MixHash Mixy NFC NFD NFKC NFKD Pair Positional PositionalBindFailover PseudoStash QuantHash Range Seq Set SetHash Setty Slip Stash Uni utf8
| type3   | types domain specific    | 4 keywords5 | typesDomainSpecific  | SCE_RAKU_TYPEDEF  | Attribute Cancellation Channel CompUnit CompUnit::Repository CompUnit::Repository::FileSystem CompUnit::Repository::Installation Distro Grammar IO IO::ArgFiles IO::CatHandle IO::Handle IO::Notification IO::Path IO::Path::Cygwin IO::Path::QNX IO::Path::Unix IO::Path::Win32 IO::Pipe IO::Socket IO::Socket::Async IO::Socket::INET IO::Spec IO::Spec::Cygwin IO::Spec::QNX IO::Spec::Unix IO::Spec::Win32 IO::Special Kernel Lock Match Order Pod::Block Pod::Block::Code Pod::Block::Comment Pod::Block::Declarator Pod::Block::Named Pod::Block::Para Pod::Block::Table Pod::Defn Pod::FormattingCode Pod::Heading Pod::Item Proc Proc::Async Promise Regex Scheduler Semaphore Supplier Supplier::Preserving Supply Systemic Tap Thread ThreadPoolScheduler VM
| type4   | types domain exceptions  | 5 keywords6 | typesExceptions      | SCE_RAKU_TYPEDEF  | Backtrace Backtrace::Frame CX::Done CX::Emit CX::Last CX::Next CX::Proceed CX::Redo CX::Return CX::Succeed CX::Take CX::Warn Exception Failure X::AdHoc X::Anon::Augment X::Anon::Multi X::Assignment::RO X::Attribute::NoPackage X::Attribute::Package X::Attribute::Required X::Attribute::Undeclared X::Augment::NoSuchType X::Bind X::Bind::NativeType X::Bind::Slice X::Caller::NotDynamic X::Channel::ReceiveOnClosed X::Channel::SendOnClosed X::Comp X::Composition::NotComposable X::Constructor::Positional X::Control X::ControlFlow X::ControlFlow::Return X::DateTime::TimezoneClash X::Declaration::Scope X::Declaration::Scope::Multi X::Does::TypeObject X::Dynamic::NotFound X::Eval::NoSuchLang X::Export::NameClash X::IO X::IO::Chdir X::IO::Chmod X::IO::Copy X::IO::Cwd X::IO::Dir X::IO::DoesNotExist X::IO::Link X::IO::Mkdir X::IO::Move X::IO::Rename X::IO::Rmdir X::IO::Symlink X::IO::Unlink X::Inheritance::NotComposed X::Inheritance::Unsupported X::Method::InvalidQualifier X::Method::NotFound X::Method::Private::Permission X::Method::Private::Unqualified X::Mixin::NotComposable X::NYI X::NoDispatcher X::Numeric::Real X::OS X::Obsolete X::OutOfRange X::Package::Stubbed X::Parameter::Default X::Parameter::MultipleTypeConstraints X::Parameter::Placeholder X::Parameter::Twigil X::Parameter::WrongOrder X::Phaser::Multiple X::Phaser::PrePost X::Placeholder::Block X::Placeholder::Mainline X::Pod X::Proc::Async X::Proc::Async::AlreadyStarted X::Proc::Async::BindOrUse X::Proc::Async::CharsOrBytes X::Proc::Async::MustBeStarted X::Proc::Async::OpenForWriting X::Proc::Async::TapBeforeSpawn X::Proc::Unsuccessful X::Promise::CauseOnlyValidOnBroken X::Promise::Vowed X::Redeclaration X::Role::Initialization X::Scheduler::CueInNaNSeconds X::Seq::Consumed X::Sequence::Deduction X::Signature::NameClash X::Signature::Placeholder X::Str::Numeric X::StubCode X::Syntax X::Syntax::Augment::WithoutMonkeyTyping X::Syntax::Comment::Embedded X::Syntax::Confused X::Syntax::InfixInTermPosition X::Syntax::Malformed X::Syntax::Missing X::Syntax::NegatedPair X::Syntax::NoSelf X::Syntax::Number::RadixOutOfRange X::Syntax::P5 X::Syntax::Perl5Var X::Syntax::Regex::Adverb X::Syntax::Regex::SolitaryQuantifier X::Syntax::Reserved X::Syntax::Self::WithoutObject X::Syntax::Signature::InvocantMarker X::Syntax::Term::MissingInitializer X::Syntax::UnlessElse X::Syntax::Variable::Match X::Syntax::Variable::Numeric X::Syntax::Variable::Twigil X::Temporal X::Temporal::InvalidFormat X::TypeCheck X::TypeCheck::Assignment X::TypeCheck::Binding X::TypeCheck::Return X::TypeCheck::Splice X::Undeclared
| type5   | adverbs                  | 6 keywords7 | adverbs              | SCE_RAKU_ADVERB   | D a array b backslash c closure delete double exec exists f function h hash heredoc k kv p q qq quotewords s scalar single sym to v val w words ww x

Oddly, while they have four different keyword lists for types, they only have one SCE_RAKU_TYPEDEF=22 style number for it; since Notepad++ cannot map multiple lists to the same Style in StyleConfigurator, I guess I'll have to merge those.


|  # | SCE                    | Styling                                               |
|----|------------------------|-------------------------------------------------------|
|  0 | SCE_RAKU_DEFAULT       | fore:#808080                                          |
|  1 | SCE_RAKU_ERROR         | \$(colour.error)                                       |
|  2 | SCE_RAKU_COMMENTLINE   | \$(colour.code.comment.line),$(font.code.comment.line) |
|  3 | SCE_RAKU_COMMENTEMBED  | \$(colour.code.comment.doc),$(font.code.comment.doc)   |
|  4 | SCE_RAKU_POD           | \$(colour.code.comment.box),$(font.code.comment.box)   |
|  5 | SCE_RAKU_CHARACTER     | \$(colour.char),$(font.monospace)                      |
|  6 | SCE_RAKU_HEREDOC_Q     | fore:#7F007F,back:#DDD0DD,notbold                     |
|  7 | SCE_RAKU_HEREDOC_QQ    | fore:#7F007F,back:#DDD0DD,bold                        |
|  8 | SCE_RAKU_STRING        | \$(colour.char),$(font.monospace)                      |
|  9 | SCE_RAKU_STRING_Q      | $(style.raku.8)                                       |
| 10 | SCE_RAKU_STRING_QQ     | \$(colour.string),$(font.monospace)                    |
| 11 | SCE_RAKU_STRING_Q_LANG | $(style.raku.10)                                      |
| 12 | SCE_RAKU_STRING_VAR    | fore:#D600B5,bold                                     |
| 13 | SCE_RAKU_REGEX         | fore:#000000,back:#A0FFA0                             |
| 14 | SCE_RAKU_REGEX_VAR     | $(style.raku.12),back:#A0FFA0                         |
| 15 | SCE_RAKU_ADVERB        | $(colour.preproc),bold                                |
| 16 | SCE_RAKU_NUMBER        | $(colour.number)                                      |
| 17 | SCE_RAKU_PREPROCESSOR  | \$(colour.notused), $(font.notused)                     |
| 18 | SCE_RAKU_OPERATOR      | $(colour.operator),bold                               |
| 19 | SCE_RAKU_WORD          | $(colour.keyword),bold                                |
| 20 | SCE_RAKU_FUNCTION      | $(style.raku.19)                                      |
| 21 | SCE_RAKU_IDENTIFIER    | $(colour.operator)                                    |
| 22 | SCE_RAKU_TYPEDEF       | $(style.raku.19)                                      |
| 23 | SCE_RAKU_MU            | $(style.raku.0)                                       |
| 24 | SCE_RAKU_POSITIONAL    | fore:#6E05BE                                          |
| 25 | SCE_RAKU_ASSOCIATIVE   | fore:#F4D50A                                          |
| 26 | SCE_RAKU_CALLABLE      | $(style.raku.21)                                      |
| 27 | SCE_RAKU_GRAMMAR       | $(style.raku.15)                                      |
| 28 | SCE_RAKU_CLASS         | $(style.raku.15)                                      |

### 2024-Apr-13

While preparing my environment, making sure I could build today's main branch, etc, I noticed a comment in `langs.model.xml` for `name="asm"` that says the `type5` and `type6` keywords must "also be in ....".  That got me curiuos, so I looked at `stylers.model.xml`, and saw that it only has style entries for `type1-4` .  So I wonder if the right thing is to have the `<Keywords>` entries separate for Raku's `type1-4`, but only have the single `type1` entry for the SCE_RAKU_TYPEDEF style.  I think that's my plan.

Start with the `langs.model` with the 7 lists; then do `stylers.model` by copying perl's big list, and replicating over the ones that seem similar, assigning the keywordClass for ADVERB, WORD, FUNCTION, and TYPEDEF.  For the styles that don't have an equivalent, use `raku.properties` suggestions.  With that, I can see `raku` in the **Preferences > Language** and **Style Configurator** language list, but the Style Configurator complains about not being able to look up the keyword lists for the four styles, since I haven't done the code fixes yet.  Still, good starting point

- /PowerEditor/src/MISC/PluginsManager/Notepad_plus_msgs.h: add L_RAKU to the end of the `enum LangType`
- /PowerEditor/src/menuCmdID.h: add IDM_LANG_RAKU as +90, before IDM_LANG_EXTERNAL
- /PowerEditor/src/ScintillaEditView.cpp and .h:
	- add to LanguageNameInfo ScintillaEditView::_langNameInfoArray[]
	- add to ScintillaEditView::defineDocType switch:
		- simple vs complex:
			- for "simple" language, call a new function (eg L_HOLLYWOOD) and define it just in .h, calling setLexer
				- looking at the setLexer() that it calls, it defines 0 as instre1, 1 as instre2, and 2-8 as type1-7, for whichever you pass in
				- it also does SCI_SETPROPERTY for fold, fold.compact, fold.comment
			- for "mediumComplexity" languages, define the new function where it manually does the lists, where it does a separate SCI_SETKEYWORDS call for eac
		- Based on the numbering, I can just use "simple", because LexRaku.cpp uses the same order as NPP does... but it depends if I need to change the other properties or not.  Oddly, even the ones like setSqlLexer(), which set a property, are defined in the .h, So calling this "simple".
		- Create setRakuLexer() in .h, with the setLexer() call for lists 0-6
		- setLexer() already does the fold/fold.compact/fold.comment to 1.    Set the raku-specific folding to 1 as well.
		- in .cpp, add `L_RAKU:setRakuLexer();` to the switch
- /PowerEditor/src/Notepad_plus.cpp: add case IDM_LANG_.../return L_...
- /PowerEditor/src/Notepad_plus.rc: add to long "&Language" and "&Language"/"&<LETTER>" lists
- /PowerEditor/src/NppCommands.cpp: add to long IDM_LANG group in switch()
- /PowerEditor/src/Parameters.cpp: add case L_.../return IDM_LANG_...
- /PowerEditor/installer/APIs/raku.xml: autoComplete file (simply alphabetize the keyword lists)
- NO - /PowerEditor/installer/functionList/raku: not implemented, since I'm not confident in my ability to handle exceptions

### 2024-Apr-14

Finished the themes.

Squash / force-push:
```
git reset --soft 906f6e4
git commit -m "Add syntax highlighting for Raku" -m "Based on SciTE, Go/Golang can use cpp lexer." -m "use the Perl color scheme from each theme as the basis for the Raku color scheme"
git push -f origin
```

=> https://github.com/notepad-plus-plus/notepad-plus-plus/pull/15000

# Enabling SubStyles in Main App

After working with SubStyles in the handful of lexers using PythonScript ([main script](https://github.com/pryrt/nppStuff/blob/main/pythonScripts/useful/SubStylesForLexer.py) and [experiments](https://github.com/pryrt/nppStuff/blob/main/pythonScripts/nppCommunity/25xxx/25980-SubStyle-Experiments.py)), I have some ideas for how I'd do it if I were implementing SubStyles in the base app:
- I would limit it to probably 8 substyles per language
- I might want something like `ScintillaEditView::SetLexer(langType, LIST|OF|LISTS)` and `ScintillaEditView::SetKeywords(langType, *keywords, index)` to help wrap them and make them consistent
	- bash uses simple
 	- cpp family of course uses complex

### 2024-Aug-08

- PR `https://github.com/notepad-plus-plus/notepad-plus-plus/issues/15520`
- Trying to get the screenshot for Don with the extra keyword lists, I learned that Notepad++ will only show the builtin+user boxes in the GUI for known keywordClass, so I will need to figure out how to get that enabled for my new keywords -- that's probably the first thing to do.
    - src\Parameters.cpp::StyleArray::addStyler() calls the getKwClassFromName() and populates the _keywordClass element of the Style structure instance
        - I will probably want to expand this variable to handle the keyword class integer for substyle# as well as the already-defined ones
    - src\Parameters.cpp::getKwClassFromName() returns the appropriate LANG_INDEX_xxx
    - src\Parameters.h defines the LANG_INDEX_xxx as constants -- so this is where I'd add the LANG_INDEX_SUBSTYLEn definitions as well
    - src\Parameters.cpp::NppParameters::feedKeyWordsParameters() is where those are populated, and that compares against KEYWORDSET_MAX
    - scintilla\include\Scinitlla.h defines KEYWORDSET_MAX to be 30.  (But a derived constant is limited to SCE_USER_KWLIST_TOTAL=28, so I wouldn't want to go above that; wait, no, I think those SCE_USER_xxx constants ar for UDL, based on the folder-in-code, etc)
    - src\ScintillaComponent\ScintillaEditView.cpp::ScintillaEditView::SetExternalLexer also uses KEYWORDSET_MAX ... but I believe it's only used for lexer plugins, not normal lexers
    - src\WinControls\ColourPicker\WordStyleDlg.cpp::WordStyleDlg::setVisualFromStyle()'s `shouldBeDisplayed` Boolean appears to be what determines whether the boxes get displayed or not
    - Originally, I had been thinking I'd do mine alongside the existing keywords, but the more I read here (as may be obvious from the tone of my notes), the more my mind has shifted to just adding mine into the same feature
        - Based on what I've read so far, LANG_INDEX_SUBSTYLE1-8 could be set to 11-18, which would leave room for Don to expand the normal keywords from 0-8 to 0-10 and 19-29
    - src\ScintillaComponent\ScintillaEditView.cpp::SctinillaEditView::makeStyle() -- this is used by some of the lexers (like HTML) for easily setting lists 0-9 based on which language
        - so I think I would want a parallel `makeSubStyle()` which used its own *pSsKwArray for those lexers that need it
- At this point, I need to start making code changes, to see if I've understood things correctly.
    - I've already added substyles1-8 to the CPP lexer, so now I want to see if I can get it to show the lists.
    - src\Parameters.h = add the LANG_INDEX_SUBSTYLE# values
    - src\Parameters.cpp::getKwClassFromName() = add the returns for those.
    - since the _keywordClass integer is set from that function, I _think_ that's all I need to do to make it visible
    - build and try: at first, I thought it was working -- I was able to add it, and I saw them in the Style Configurator.  But then something happened, and it's started crashing.
    - revert and build: it doesn't crash
    - put it back, but using 9-16 instead of 11-18 and build: it still crashes
    - I wonder whether it's the user keywords -- yes, as soon as I don't have any user keywords in stylers.xml, it stops crashing.  So there's obviously some array out-of-bounds, but I have no idea where.
    - Bring them back one at a time: they are all working now.  What?! I guess I'll have to watch carefully; my guess is that somehwhere, there's an array out-of-bounds, but it doesn't always trigger, depending on active memory map.  Still, untill I've got more framework in place (and maybe I'll figure out the list as I start dealing with the actual keywords lists), I should probably restrict it to having user keywords for just substyle1
    - src\Parameters.cpp::NppParameters::feedKeyWordsParameters() = debugPrint the default-keyword-list, and see that it's reading the default lists okay (also saw that there's a limit of `NB_LIST = 20` for the actual number of keyword lists can be added to the data structure)
    - trying to find where the user-added keywords go, because they must be grabbed when stylers.xml is loaded -- okay, it's in the Parameters.cpp::StyleArray::addStyler() (though it's hard to get the context, because that's restricted to the caller)
