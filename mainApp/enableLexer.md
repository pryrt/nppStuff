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

- ISSUE `https://github.com/notepad-plus-plus/notepad-plus-plus/issues/15520`
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

### 2024-Aug-09

- Since I have confirmed I have the langs.xml keyword lists and the user-defined stylers.xml keywords list for the C++ substyles, next step is to make sure i know how to access them from the ScintillaEditView
	- ScintillaEditView::setCppLexer
	- With some OutputDebugString, able to confirm that the pKwArray[i] contains the list of user keywords for a given style, and the getCompleteKeywordList() combines the user keywords with the default keywords, with the user keywords coming first.
	- confirm that the simple .h-only and the .cpp-defined both use the ::makeStyle() to generate the array of keywords
		- it grabs the LexerStyler object
		- then iterate through the styles in the LexerStyler object, and if there's a keyword list to populate, then it tries to populate that string
			- that's probably where my memory issue was: there were only slots 0..10, but I was populating 11..18 or 9..16, both of which overrun the **keywordArray
			- I need to do some debug printing here, to make sure I understand how it's being populated
			- So yes, it would definitely try to set keywordArray[SLOT] = style._keywords.c_str(), which would overflow for SLOT>9.  
	- So I'm thinking that the *pKwArray[10] that's hardcoded throughout really needs to be *pKwArray[NB_LIST] instead, assuming NB_LIST from Parameters.h propagates to ScintillaEditView.  But before I implement that, need to check some logic:
		- NB_LIST is currently only used for the struct "Lang"'s _langKeyWordList[NB_LIST], a specific entry of which is returned from Lang::getWords(), which is called by NppParameters::getWordList(), which is called by setCppLexer() and a few other custom and generically thru ScintillaEditView::getCompleteKeywordList().
		- so yes, it definitely affects all the lexers
		- for now, change just the CPP's *pKwArray[NB_LIST] -- without any changes, it does seem to work.
		- add `pryrt8` to substyle8's user list, and rerun
		- took me a while to get it properly printing the lists -- but now I can see the lists whether there was one in stylers (shows list) or not (shows null)
		- so yes, propagate the [NB_LIST] to all those instances, it still works
	- Curious: since the makeStyle() only needed an output array big enough in order to work, and since I think makeStyle() also calls the SCI_STYLESETFORE/BACK/etc, I _think_ that the colors should already be set for the new styles, so try SCI_STYLEGETFORE/..., and print them: yes, it's printing the unique colors I gave it.
		- Does that mean if I go over to code that has the `pryrt` or `substyle` keywords, I will see highlighting?  Yes!  It works!

SAFETY COMMIT!
```
   SubStyles are working for LexCPP
   - updated to `*pKwArray[NB_LIST]` for all arguments to makeStyle()
   - the makeStyle() already sets the colors
   - doing a loop in the setCppLexer() to call the SubStyle allocate
       and setIdentifiers()
   - my example code will show the new colors on the defined keywords!

   TODO = need to clean it up into a function, and start applying it to the other lexers!
```

- Create a new ScintillaEditView::populateSubStyleKeywords() as a wrapper over my allocate-and-loop
	- try calling that instead of my local copy from setCppLexer ⇒ that works
- Now it's time to start adding them to the other languages
	- C/C#/CPP all work, as does Go and Java.  Javascript and Typescript aren't working... but I think those don't use setCppLexer... I'll have to double-check that.  RC works; ActionScript (Flash) ok; Swift ok.
	- JS/Javascript use setJsLexer(), so let's go populate that one -- that makes Languages>JavaScript work, but not embedded JS (because that uses the HTML lexer, which isn't enabled yet)
	- setXmlLexer is called by L_PHP, L_ASP, L_JSP, L_HTML, L_XML
		- if it's L_XML, it then does the makeStyle directly
		- for the other ones, it then calls _all_ of setHTMLLexer, setEmbedded(JS|Php|Asp)Lexer()
			- setHTMLLexer,JS,Php,Asp each calls their own makeStyle
		- I think that means that for XML, I just call my SubStyles wrapper once, but for the other four, I will call them 4x, so they'll each get their own 8 
		- where do each of the SCE_H* map?
			- HTML uses H_TAG=1 and H_ATTRIBUTE=3 
				- needs to be set in setHTMLLexer()
			- HJ_WORD=46 appears to be the JavaScript Embedded WORD
				- needs to be set in setEmbeddedJSLexer()
			- HJA_WORD=61 is server-side javascript, which Notepad++ isn't using
			- HB_WORD=74 is embedded vbscript, which Notepad++ isn't using
			- HP_WORD=96 is embedded python, which Notepad++ isn't using
			- HPHP_WORD=121 is the PHP, which _is_ being used
				- needs to be set in setEmbeddedPhpLexer()
			- where is ASP?  
				- Digging in, it's 81-86, which LexHTML claims as "server basic", and that range doesn't have any substyles defined.
		- based on what I see here, I think each are going to get their own set of 8 substyles -- so HTML gets 8, embedded JS gets 8, and PHP get 8 -- which is going to be nice.  But I'll have to watch my debug prints to see what StyleID each gets assigned to.
		- TODO: next steps will be starting those allocations, and looking at the StyleID allocated for each

### 2024-Aug-10

- Start by setting up my development here... Since I hadn't edited the src\*.model.xml, but only the local bin directory stylers/langs.xml, I needed to recreate that.
	- hmm, C/C#/CPP all work; Go and Java work; Javascript.js works, but Typescript is not (it doesn't even do the debug print).  I thought I had tested that earlier, but maybe not.
	- no, the L_TYPESCRIPT is elsewhere, so I'll have to do that.  But first:
	- I forgot today to setup and verify RC, FLASH(ACTIONSCRIPT) and SWIFT.  At this point, modify the src\*.model, because I don't want to forget this again ⇒ those work, too
	- Now implement typescript ⇒ good
- Time to move on to the LexHTML family
	- First update the langs*.xml.  
	- Since I don't know which substyle numbers will be assigned, let's call the wrappers next, so I can see the debug prints as I choose each language.
		- XML, split into two, originally did 192 and 200 -- but why 8, rather than 4?  Because i forgot to propagate the parameter to the message, which hardcoded 8.  Fix that.  Now 192 and 196. 
		- Add styles for the XML and HTML, both in those ranges.  Right now, I can see the XML attributes, but not XML tags: it appears in XML mode that all tags are "recognized" and none "unrecognized", and thus it never checks for specific words.  
		- Change XML to allocate all 8 to attributes, instead.
		- Enable the four+four in HTML, and verify it works as expected, with 192 and 196 as the starting points; update the styles to match
		- Enable the embedded JS ⇒ starts at 200.  update the styles to match
		- Enable the embedded PHP ⇒ 208.  update the styles to match
		- Enable the embedded ASP (I think based on HB_WORD=74) ⇒ it does allocate them, starting at 216, and it styles with the empty style; so add styles starting at 216 with user keywords for the asp.  That works.  So even though NPP is using the 81-86, it's allowing me to base its keyword list off of 74 from the 71-76 range, so that's good
- Bash has two groups -- identifier and scalar -- so I should probably split between them.
	- identifier is like a function name.  scalar is `$namehere`
	- however, it's currently defined as a "simple" lexer, so everything's inside setLexer()
		- I think I'll have to grab the relevant parts of setLexer() 
		- yep, that worked, and it identified my four identifiers and four scalars
- I was reminded when bash compiled that it requires changing the .h, which recompiles much more.  
	- I don't want to have to do that too many more times, so let's do some planning
	- I want to update setLexer() to have an optional argument, and I'll want to use it once in GDScript.  Once I get that working, I should be able to propagate to the other simple-languages
		- I will need an optional argument that triggers SubStyles, and gives it the base substyle.  
		- hmm, which was the constant for keyword-list-not-used?  Right, makeClass() checks if _keywordClass isnt STYLE_NOT_USED (-1), so that's the one I was thinking of as my default value.  That's different from all the 
		- Yes, it worked.  
		- Oh, realized I might need a second argument, for the firstSubStyle, in case the lexer uses something other than 128.  No, wait, the populateSubStyleKeywords doesn't need to know where it goes... just my debug print does, and it gets that information.  So I don't need another parameter.
	- Lua and Python are the only ones left to do, since Verilog doesn't really have it. Do those together for one build.
		- Oh, Lua already had 4 keyword categories from normal keywords.  Does it really need 8 more?  I think I'll just enable 4... which means I _do_ need a second optional parameter.
		- Yep, Lua works with the additional 4.  Python with the additional 8.
	- Time to commmit
- Get rid of my debug printing
- Clean up the .model.xml to not have my dummy keywords

### 2024-Aug-11

- Work on updating all the themes.  
	- Yesterday, I did one language, but it was tedious.
	- Record a macro for doing actionscript.  Run it on all the remaining themes.  Save and reload.
	- The other LexCPP languages should all have the same sequence, just changing the intitial search.
	- Change the macro to look for `name="c"` and reload.  It worked.
	- continue through the other lexCPP: cpp, cs, go, java, javascript.js (only three themes have this; add it to TODO), rc, swift (only two have it)
	- The LexHTML are all similar, but not identical.  Do the HTML and XML separately.  PHP.  ASP.  JSP wasn't in there -- oh, right, JSP just uses embedded JS, so update that one
	- Now do the rest, one at a time (custom macro each time): bash, gdscript (only in one), lua, and python.
	- Try each theme (ie, just pick it, don't look too deeply): bespin has error, as does HotFudgeSundae.  Use my main N++ instance with XML Tools to syntax check the HTML, and found a missing `</LexerType>` and a problem on a couple of the `keywordClass="substyle#" />`
- Haven't heard anything from Forum user about PHP.  I think maybe I'll just use the classifications found in the [PHP Reserved Words](https://www.php.net/manual/en/reserved.php) docs:
	- [keywords](https://www.php.net/manual/en/reserved.keywords.php)
	- [constants](https://www.php.net/manual/en/string.constants.php) (include the constants from the keywords page)
	- ["other" reserved](https://www.php.net/manual/en/reserved.other-reserved-words.php)
	- [predefined classes](https://www.php.net/manual/en/reserved.other-reserved-words.php)
	- [functions and methods](https://www.php.net/manual/en/indexes.functions.php) -- this is the huge list
	- Surprised to see that when I take out the any of the ones listed in those 5 pages from the N++ list, there are still about 6000 in the N++ list, along with 6000 from the big list.  
	- I think it makes sense to combine keywords+other into the official list, constants and classes into substyle1, functions and methods into substyle2, and the N++ leftovers into substyle3.  That still leaves 5 substyles that are completely separate, and people who want the official big-list and the N++ leftovers to look the same can just apply the same coloring to both styles.

Before doing my rebase and PR, check against the ScintillaEditView _langNameInfoArray:
- Good thing I did: I forgot typescript in the themes (it was only in two themes, so not a big deal to fix -- oh, and I only forgot it in one of them, even easier)

Now it's ready for the rebase and re-commit.  new message will be:
```
Add new user-accessible keyword lists to specific languages (using Substyles)
- Enable up to 8 Scintilla's SubStyles (each), which allow for new keyword lists and styles for the languages with substyles available: ActionScript, ASP, Bash, C, C++, C#, GDScript, Go, HTML, Java, JavaScript (standalone and embedded), JSP, Lua, PHP, Python, Resource (RC), Swift, TypeScript, and XML.
- The new SubStyles have been added to `langs.model.xml`, `stylers.model.xml`, and the themes.
- PHP, which had thousands of keywords, has had the keywords split into a few groups, using three of the new SubStyles (still leaving five SubStyles completely up to the user to populate)

Fixes #15520
```

Rebased and force-push.  Wait for Actions to run and pass.  Submit PR `https://github.com/notepad-plus-plus/notepad-plus-plus/pull/15537`


#### MISC NOTES:

I thought about:

- _ Propagate javascript.js to all themes
- _ Propagate swift to all themes

Those don't really belong in this PR, however, so don't include it.

## Documentation

In 2019, it was [suggested](https://github.com/notepad-plus-plus/notepad-plus-plus/issues/3292#issuecomment-531320436) that the User Manual could document the add-a-language process; back then, I didn't know anything about the process, but since I've done it twice now, I suppose I can try to document it.  I'll start with a rough draft here, which may eventually become part of the UM.

### Enable Existing Lexilla Lexer in Notepad++

The [Lexilla library](https://github.com/ScintillaOrg/lexilla/) which Notepad++ uses for syntax highlighting has many languages available to it that Notepad++ doesn't yet provide in the **Language** menu and Style Configurator.  In general, just creating an [issue](https://github.com/notepad-plus-plus/notepad-plus-plus/issues) to request a language be enabled is not 
sufficient to get it added, because the developers don't have sufficient knowledge of all Lexilla-enabled languages to know if the addition was successful or not; you should put in the request if there's a langauge in Lexilla that you would like added to Notepad++, but, if possible, you could also put in the Pull Request.

The following are all pieces of the codebase that need to be updated in order to activate a currently-inactive lexer. For this description, "Xyz Pdq" will be the placeholder name of your language; you, of course, need to use your own language's name instead of the placeholder.

- `PowerEditor/src/MISC/PluginsManager/Notepad_plus_msgs.h`: 
	- Need to add an `L_XYZPDQ` constant for your language to the end of the `enum LangType` 
	- Insert it between the last real language in the list and `L_EXTERNAL`; **never** insert it before an already-existing language, as the position in the list gives it an integer that is used throughout the codebase and config files.
- `PowerEditor/src/menuCmdID.h`: 
	- Add `#define IDM_LANG_XYZPDQ` between the last existing language and `IDM_LANG_EXTERNAL`, using the next integer for the value (the `L_...` from the enum should be in that same integer slot in the enum)
- `PowerEditor/src/ScintillaComponent/ScintillaEditView.h`
	- declare `setXyzPdqLexer()`
	- if it's a simple lexer, which just needs to define one or more keyword lists, you can define it here instead of in the `.cpp` below, just calling `setLexer(L_XYZPDQ, LIST_0 | LIST_1 | ...);`, similar to what was done for `setHollywoodLexer()`
	- An aside on the keyword lists: The `lexilla/Lexers/LexXyzPdq.cxx` will contain one or more `WordList` variables; usually in `LexerXyzPdq::WordListSet()`, you will see a mapping between the word list index and th `WordList` variable.  That index corresponds to the `LIST_#` constant used when calling `setLexer()`.  
- `PowerEditor/src/ScintillaComponent/ScintillaEditView.cpp`
	- add the language to `LanguageNameInfo ScintillaEditView::_langNameInfoArray[]`, just before the `L_EXTERNAL` entry.  The table below describes that value that needs to go in each column of that data structure.
	    | Column       | Example        | Description |
		|--------------|----------------|-------------|
		| `_langName`  | `xyzpdq`       | Unique string to identify the language.  Will be used as the `<Language name="xyzpdq" ... />` attribute in `langs.xml` |
		| `_shortName` | `Xyz Pdq`      | This is the text that appears in the **Languages** menu |
		| `_longName`  | `Xyz Pdq file` | This is the text that appears in the **Status Bar**'s file type field |
		| `_langID`    | `L_XYZPDQ`		| This is the `L_XYZPDQ` entry you added to the enum |
		| `_lexerID`   | `xyzpdq` 		| This is the name of the lexer, as defined in the `lexilla/Lexers/LexXyzPdq.cxx`, in the `LexerModule` instantiation |
	- add your language to the big `switch` block in `ScintillaEditView::defineDocType()`; it should call `setXyzPdqLexer(); break`
	- add in the definition for your `setXyzPdqLexer()`
		- If it's just calling `setLexer()`, you can actually define it in the `.h`, as described above.
		- If it requires complicated logic, define it here, instead.
		- If the lexer includes SubStyle keyword capability, you can either initialize them in the optional end arguments of the `setLexer()` call (see `setLuaLexer()` and `setPythonLexer()` in the `.h` for examples of how to use those optional arguments), or your more-complicated definitions may call `populateSubStyleKeywords()` themselves, like `ScintillaEditView::setTypeScriptLexer()` does)
			- if you are unsure whether your language has substyles, just search the `lexilla/Lexers/LexXyzPdq.cxx` for the word `SubStyle`; with some digging in the code, you should be able to determine which Style the SubStyles get attached to, as well.
- `PowerEditor/src/Notepad_plus.cpp`:
    - in the switch in `Notepad_plus::menuID2LangType()`, add 
	   	```
	   	case IDM_LANG_XYZPDQ:
			return L_XYZPDQ;
	   	```
- `PowerEditor/src/Parameters.cpp`:
	- in the switch in `NppParameters::langTypeToCommandID()`, add 
		```
		case L_XYZPDQ:
			id = IDM_LANG_XYZPDQ; break;
		```
- `PowerEditor/src/Notepad_plus.rc`:
	- add a `MENUITEM` in the alphabetically correct place in both the `&Language` big-list, and the `&Language`/`POPUP "X"` per-letter version.
- `PowerEditor/src/NppCommands.cpp`:
	- `Notepad_plus::command()` has a huge switch; add `case IDM_LANG_XYZPDQ:` to the big list of similar `case IDM_LANG_...` entries

And add in config files:
- `PowerEditor/src/langs.model.xml`: add in your `<Language name="xyzpdq"...>` entry with its `<Keywords ...>` entries
    - the `name="instre1"` is the keyword list for `LIST_0`, `instre2` for `LIST_1`, and `type1`-`type7` are `LIST_2`-`LIST_8`; `substyle1`-`substyle8` are for the eight substyles that Notepad++ allows (if the lexer has enabled substyles, of course).
- `PowerEditor/src/stylers.model.xml` and all of the `PowerEditor/installer/themes/*.xml`: add in your `<LexerType name="xyzpdq"...>` with its `<WordsStyles>` entries
    - `lexilla/include/SciLexer.h` has `#define` for `#define SCI_XYZPDQ_* N` values; you will need to make sure you have a `<WordsStyle ... styleID="N" ...>` for each of those styles.

You should also include [autoCompletion](../auto-completion/) definition and [functionList](../function-list/) definition if you have them (they are optional, but highly recommended).

# SAS

`https://github.com/notepad-plus-plus/notepad-plus-plus/issues/16148` is an official request for SAS.  Finally gives me an excuse to add it.

## Keywords

### SciTE
The SciTE-distributed sas.properties file has a tiny list of keywords, so I tried googling for some more.  

```
# Keywords
keywords.$(file.patterns.sas)=%let %do

# Block Keywords
keywords2.$(file.patterns.sas)=also cards class data input model ods proc var where

# Function Keywords
keywords3.$(file.patterns.sas)=%printz

# Statement Keywords
keywords4.$(file.patterns.sas)=run
```

### Notepad4
Found notepad4 incorporated LexSAS `https://github.com/zufuliu/notepad4/commit/4f20795099b37acdf01515f276702de81af5dc13` , and `https://github.com/zufuliu/notepad4/blob/d61230063d13ba68518021fb7011349dd4cc8ac8/src/EditLexers/stlSAS.cpp` shows their keywords[0],[1], and [2] lists (they have no [3]) list.

LexSAS variable    | keywordlists[#] | style | list
-------------------|-----|--------------------------|---
`keywords`         | [0] | SCE_SAS_MACRO_KEYWORD    | abort bquote( cmpres( compstor( copy datatyp( do ds2csv( else end eval( global goto if include index( kverify( left( length( let list local lowcase( macro mend nrbquote( nrquote( nrstr( put qcmpres( qleft( qlowcase( qscan( qsubstr( qsysfunc( qtrim( quote( qupcase( return run scan( str( substr( superq( symdel symexist( symglobl( symlocal( syscall sysevalf( sysexec sysfunc( sysget( syslput sysmacdelete sysmacexec( sysmacexist( sysmexecdepth sysmexecname( sysmstoreclear sysprod( sysrc( sysrput then to trim( tslit( unquote( until upcase( verify( while 
`blockKeywords`    | [1] | SCE_SAS_BLOCK_KEYWORD    |
`functionKeywords` | [2] | SCE_SAS_MACRO_FUNCTIONS  | abs( addrlong( airy( allcomb( allcombi( allperm( anyalnum( anyalpha( anycntrl( anydigit( anyfirst( anygraph( anylower( anyname( anyprint( anypunct( anyspace( anyupper( anyxdigit( arcos( arcosh( arsin( arsinh( artanh( atan( atan2( attrc( attrn( band( beta( betainv( bhamming_32( bhamming_hex( blackclprc( blackptprc( blkshclprc( blkshptprc( blshift( bnot( bor( brshift( bxor( byte( call cat( catq( cats( catt( catx( cdf( ceil( ceilz( cexist( char( choosec( choosen( cinv( clibexist( close( cmiss( cnonct( coalesce( coalescec( collate( comb( compare( compbl( compcost( compfuzz( compfuzz_miss( compged( complev( compound( compress( compsrv_oval( compsrv_unquote2( constant( convx( convxp( cos( cosh( cot( count( countc( countw( csc( css( cumipmt( cumprinc( curobs( cv( daccdb( daccdbsl( daccsl( daccsyd( dacctab( dairy( datdif( date( datejul( datepart( datetime( day( dclose( dcreate( depdb( depdbsl( depsl( depsyd( deptab( dequote( deviance( dhms( dif( digamma( dim( dinfo( divide( dlgcdir( dnum( dopen( doptname( doptnum( dosubl( dread( dropnote( dsname( dur( durp( effrate( envlen( erf( erfc( euclid( execute( exist( exp( expm1( fact( fappend( fclose( fcol( fcopy( fdelete( fetch( fetchobs( fexist( fget( fileexist( filename( fileref( finance( find( findc( findw( finfo( finv( fipname( fipnamel( fipstate( first( floor( floorz( fmtinfo( fnonct( fnote( fopen( foptname( foptnum( fpoint( fpos( fput( fread( frewind( frlen( fsep( fuzz( fwrite( gaminv( gamma( garkhclprc( garkhptprc( gcd( geodist( geomean( geomeanz( getcasurl( getlcaslib( getlsessref( getltag( getoption( getsessopt( getvarc( getvarn( graycode( harmean( harmeanz( hash_fast_hex( hash_xx_hex( hashing( hashing_file( hashing_hmac( hashing_hmac_file( hashing_hmac_init( hashing_init( hashing_part( hashing_term( hbound( hms( holiday( holidayck( holidaycount( holidayname( holidaynx( holidayny( holidaytest( hour( htmldecode( htmlencode( ibessel( ifc( ifn( index( indexc( indexw( input( inputc( inputn( int( intcindex( intck( intcycle( intfit( intfmt( intget( intindex( intnx( intrr( intseas( intshift( inttest( intz( iorcmsg( ipmt( iqr( irr( is8601_convert( jbessel( jsonpp( juldate( juldate7( kurtosis( label( lag( largest( lbound( lcm( lcomb( left( length( lengthc( lengthm( lengthn( lexcomb( lexcombi( lexperk( lexperm( lfact( lgamma( libname( libref( log( log10( log1px( log2( logbeta( logcdf( logistic( logpdf( logsdf( lowcase( lperm( lpnorm( mad( margrclprc( margrptprc( max( md5( mdy( mean( median( min( minute( missing( mod( modexist( module( modulec( modulen( modz( month( mopen( mort( msplint( mvalid( n( netpv( nliteral( nmiss( nomrate( normal( notalnum( notalpha( notcntrl( notdigit( note( notfirst( notgraph( notlower( notname( notprint( notpunct( notspace( notupper( notxdigit( npv( nvalid( nwkdom( open( ordinal( pathname( pctl( pdf( peekclong( peeklong( perm( pmt( point( poisson( pokelong( ppmt( probbeta( probbnml( probbnrm( probchi( probf( probgam( probhypr( probit( probmc( probmed( probnegb( probnorm( probt( propcase( prxchange( prxdebug( prxfree( prxmatch( prxnext( prxparen( prxparse( prxposn( prxsubstr( ptrlongadd( put( putc( putn( pvp( qtr( quantile( quote( ranbin( rancau( rancomb( rand( ranexp( rangam( range( rank( rannor( ranperk( ranperm( ranpoi( rantbl( rantri( ranuni( rename( repeat( resolve( reverse( rewind( right( rms( round( rounde( roundz( saving( savings( scan( sdf( sec( second( sessbusy( sessfound( set( sha256( sha256hex( sha256hmachex( sign( sin( sinh( skewness( sleep( smallest( softmax( sort( sortc( sortn( soundex( spedis( sqrt( squantile( std( stderr( stdize( stfips( stname( stnamel( stream( streaminit( streamrewind( strip( subpad( substr( substrn( sum( sumabs( symexist( symget( symgetn( symglobl( symlocal( symput( symputx( sysexist( sysget( sysmsg( sysparm( sysprocessid( sysprocessname( sysprod( sysrc( system( tan( tanh( time( timepart( timevalue( tinv( tnonct( today( translate( transtrn( tranwrd( trigamma( trim( trimn( trunc( tslvl( typeof( tzoneid( tzonename( tzoneoff( tzones2u( tzoneu2s( uniform( upcase( urldecode( urlencode( uss( uuidgen( var( varfmt( varinfmt( varlabel( varlen( varname( varnum( varray( varrayx( vartype( verify( vformat( vformatd( vformatdx( vformatn( vformatnx( vformatw( vformatwx( vformatx( vinarray( vinarrayx( vinformat( vinformatd( vinformatdx( vinformatn( vinformatnx( vinformatw( vinformatwx( vinformatx( vlabel( vlabelx( vlength( vlengthx( vname( vnamex( vnext( vtype( vtypex( vvalue( vvaluex( week( weekday( whichc( whichn( year( yieldp( yrdif( yyq( zipcity( zipcitydistance( zipfips( zipname( zipnamel( zipstate( 
`statements`       | [3] | SCE_SAS_STATEMENT        | abort alter and array asc attrib by call cards cards4 catname checkpoint connect constraints continue create data datalines datalines4 delete desc describe disconnect distinct do drop else end endsas eq error execute execute_always file filename footnote format from ge goto group gt having if in index infile informat input insert into keep label le leave length libname link list lock lockdown lostcard lt max merge min missing modify ne not options or order otherwise output page proc put putlog quit redirect remove rename replace reset resetline retain return run sasfile select set skip stop sysecho table then title unique until update validate values view when where while 

I reordered those compared to notepad4, so that bquote would be a macro, abs would be a macro function (the closest to "function" I can find), and catname and checkpoint show up as statements

### VIM
The vim file for SAS has a lot more groups: https://www.vim.org/scripts/script.php?script_id=3522

### documentation.sas.com
Global Statements by Category (presumably SCE_SAS_STATEMENT):
https://documentation.sas.com/doc/en/pgmbasecdc/9.4/lestmtsglobal/n07m1xz4g895ttn1bzqksyuncjsd.htm

Dictionary of Functions: ABS, ADDRLONG, etc
https://documentation.sas.com/doc/en/pgmsascdc/v_059/lefunctionsref/p1q8bq2v0o11n6n1gpij335fqpph.htm

Macro Functions: %BQUOTE, etc
https://documentation.sas.com/doc/en/pgmsascdc/9.4_3.5/mcrolref/n1qqdn7r170c30n197p4jfufv1yy.htm
Macro Statements: %COPY, %DISPLAY, etc, on the pager above "Macro Functions" in TOC

### Summary

Hard to figure out how to group things.  I might just take notepad4's list and be done with it...

## Implementation

This afternoon, mostly got it working.  To test the lexing aspect, ignoring N++, use the lexilla build and test:
```
cd lexilla\src
mingw32-make
cd ..\test
mingw32-make test
```
This will create `lexilla\test\examples\sas\*.new` to indicate the new styler outputs, and this helps me find syntax which will exercise each style from the lexer.

## Keywords

Looking more closely at the way that SciTE lexes:

- SCE_SAS_MACRO_KEYWORD => these appear to be pre-populated with ones from https://documentation.sas.com/doc/en/pgmsascdc/9.4_3.5/mcrolref/p08ksb4ivhj2l5n1blya220dr98z.htm => `%abort %by %copy %display %do %do %else %end %global %goto %if %if %input %let %local %macro %mend %put %return %symdel %syscall %sysexec %syslput %sysmacdelete %sysmstoreclear %sysrput %then %to %until %while %window`
- SCE_SAS_MACRO_FUNCTIONS => <https://documentation.sas.com/doc/en/pgmsascdc/9.4_3.5/mcrolref/n1qqdn7r170c30n197p4jfufv1yy.htm> => `%bquote %eval %index %kcmpres %kindex %kleft %klength %kscan %ksubstr %kupcase %length %nrbquote %nrquote %nrstr %qkleft %qkscan %qksubstr %qkupcase %qscan %qsubstr %qsysfunc %quote %qupcase %scan %str %substr %superq %symexist %symglobl %symlocal %sysevalf %sysfunc %sysget %sysmacexec %sysmacexist %sysmexecdepth %sysmexecname %sysprod %unquote %upcase`
- SCE_SAS_STATEMENT =>
    - <https://documentation.sas.com/doc/en/pgmbasecdc/9.4/lestmtsglobal/n07m1xz4g895ttn1bzqksyuncjsd.htm> => `%include %list %run catname checkpoint execute_always comment dm endsas filename footnote libname lock missing options page resetline run sasfile skip sysecho title`
    - <https://documentation.sas.com/doc/en/lestmtsref/3.2/n1g155m65k5pwpn1u9wy7rd1du91.htm> => `%include %list %run abort array attrib by call cards cards4 catname checkpoint continue comment data datalines datalines4 delete describe do do until do while drop else end endsas error execute execute_always file filename footnote format go to if infile informat input keep label leave length libname link list lock lockdown lostcard merge missing modify null options output page put putlog redirect remove rename replace resetline retain return run sasfile select set skip stop sysecho systask sum then title update waitfor where x`
- SCE_SAS_BLOCK_KEYWORD => Block Keywords (SCE_SAS_BLOCK_KEYWORD) Functions & CALL Routines <https://documentation.sas.com/doc/en/pgmsascdc/v_059/lefunctionsref/p1q8bq2v0o11n6n1gpij335fqpph.htm> => `abs addrlong airy allcomb allcombi allperm anyalnum anyalpha anycntrl anydigit anyfirst anygraph anylower anyname anyprint anypunct anyspace anyupper anyxdigit arcos arcosh arsin arsinh artanh atan atan2 attrc attrn band beta betainv bhamming_32 bhamming_hex blackclprc blackptprc blkshclprc blkshptprc blshift bnot bor brshift bxor byte call cat catq cats catt catx cdf ceil ceilz cexist char choosec choosen cinv clibexist close cmiss cnonct coalesce coalescec collate comb compare compbl compcost compfuzz compfuzz_miss compged complev compound compress compsrv_oval compsrv_unquote2 constant convx convxp cos cosh cot count countc countw csc css cumipmt cumprinc curobs cv daccdb daccdbsl daccsl daccsyd dacctab dairy datdif date datejul datepart datetime day dclose dcreate depdb depdbsl depsl depsyd deptab dequote deviance dhms dif digamma dim dinfo divide dlgcdir dnum dopen doptname doptnum dosubl dread dropnote dsname dur durp effrate envlen erf erfc euclid execute exist exp expm1 fact fappend fclose fcol fcopy fdelete fetch fetchobs fexist fget fileexist filename fileref finance find findc findw finfo finv fipname fipnamel fipstate first floor floorz fmtinfo fnonct fnote fopen foptname foptnum fpoint fpos fput fread frewind frlen fsep fuzz fwrite gaminv gamma garkhclprc garkhptprc gcd geodist geomean geomeanz getcasurl getlcaslib getlsessref getltag getoption getsessopt getvarc getvarn gitfn_clone gitfn_commit gitfn_commitfree gitfn_commit_get gitfn_commit_log gitfn_co_branch gitfn_del_branch gitfn_del_repo gitfn_diff gitfn_diff_free gitfn_diff_get gitfn_diff_idx_f gitfn_idx_add gitfn_idx_remove gitfn_mrg_branch gitfn_new_branch gitfn_pull gitfn_push gitfn_reset gitfn_reset_file gitfn_status gitfn_statusfree gitfn_status_get gitfn_version git_branch_chkout git_branch_delete git_branch_merge git_branch_new git_clone git_commit git_commit_free git_commit_get git_commit_log git_delete_repo git_diff git_diff_file_idx git_diff_free git_diff_get git_diff_to_file git_fetch git_index_add git_index_remove git_init_repo git_pull git_push git_rebase git_rebase_op git_ref_free git_ref_get git_ref_list git_reset git_reset_file git_set_url git_stash git_stash_apply git_stash_drop git_stash_pop git_status git_status_free git_status_get git_version graycode harmean harmeanz hashing hashing_file hashing_hmac hashing_hmac_file hashing_hmac_init hashing_init hashing_part hashing_term hash_fast_hex hash_xx_hex hbound hms holiday holidayck holidaycount holidayname holidaynx holidayny holidaytest hour htmldecode htmlencode ibessel ifc ifn index indexc indexw input inputc inputn int intcindex intck intcycle intfit intfmt intget intindex intnx intrr intseas intshift inttest intz iorcmsg ipmt iqr irr is8601_convert jbessel jsonpp juldate juldate7 kurtosis label lag largest lbound lcm lcomb left length lengthc lengthm lengthn lexcomb lexcombi lexperk lexperm lfact lgamma libname libref log log10 log1px log2 logbeta logcdf logistic logpdf logsdf lowcase lperm lpnorm mad margrclprc margrptprc max md5 mdy mean median min minute missing mod modexist module modulec modulen modz month mopen mort msplint mvalid n netpv nliteral nmiss nomrate normal notalnum notalpha notcntrl notdigit note notfirst notgraph notlower notname notprint notpunct notspace notupper notxdigit npv nvalid nwkdom open ordinal pathname pctl pdf peekclong peeklong perm pmt point poisson pokelong ppmt probbeta probbnml probbnrm probchi probf probgam probhypr probit probmc probmed probnegb probnorm probt propcase prxchange prxdebug prxfree prxmatch prxnext prxparen prxparse prxposn prxsubstr ptrlongadd put putc putn pvp qtr quantile quote ranbin rancau rancomb rand randperm ranexp rangam range rank rannor ranperk ranperm ranpoi rantbl rantri ranuni rename repeat resolve reverse rewind right rms round rounde roundz saving savings scan sdf sec second sessbusy sessfound set sha256 sha256hex sha256hmachex sign sin sinh skewness sleep smallest softmax sort sortc sortn soundex spedis sqrt squantile std stderr stdize stfips stname stnamel stream streaminit streamrewind strip subpad substr substrn sum sumabs symexist symget symglobl symlocal symput symputx sysexist sysget sysmsg sysparm sysprocessid sysprocessname sysprod sysrc system tan tanh time timepart timevalue tinv tnonct today translate transtrn tranwrd trigamma trim trimn trunc tslvl typeof tzoneid tzonename tzoneoff tzones2u tzoneu2s uniform upcase urldecode urlencode uss uuidgen var varfmt varinfmt varlabel varlen varname varnum varray varrayx vartype verify vformat vformatd vformatdx vformatn vformatnx vformatw vformatwx vformatx vinarray vinarrayx vinformat vinformatd vinformatdx vinformatn vinformatnx vinformatw vinformatwx vinformatx vlabel vlabelx vlength vlengthx vname vnamex vnext vtype vtypex vvalue vvaluex week weekday whichc whichn year yieldp yrdif yyq zipcity zipcitydistance zipfips zipname zipnamel zipstate`

That list seems reasonable in SciTE, so I'll use those.

## Styling

ID  | CONSTANT               | Style Label    | keyword   | copy color from...
----|------------------------|----------------|-----------|--------------------
0   | SCE_SAS_DEFAULT        | DEFAULT        |           | DEFAULT
1   | SCE_SAS_COMMENT        | COMMENT        |           | COMMENT LINE
2   | SCE_SAS_COMMENTLINE    | COMMENT LINE   |           | COMMENT LINE
3   | SCE_SAS_COMMENTBLOCK   | COMMENT BLOCK  |           | COMMENT LINE
4   | SCE_SAS_NUMBER         | NUMBER         |           | NUMBER
5   | SCE_SAS_OPERATOR       | OPERATOR       |           | OPERATOR
6   | SCE_SAS_IDENTIFIER     | IDENTIFIER     |           | IDENTIFIER
7   | SCE_SAS_STRING         | STRING         |           | STRING QQ
11  | SCE_SAS_MACRO          | MACRO          |           | HASH
12  | SCE_SAS_MACRO_KEYWORD  | MACRO KEYWORD  | instre1   | ARRAY
14  | SCE_SAS_MACRO_FUNCTION | MACRO FUNCTION | type1     | FORMAT IDENTIFIER
13  | SCE_SAS_BLOCK_KEYWORD  | FUNCTION       | instre2   | PROTOTYPE
15  | SCE_SAS_STATEMENT      | STATEMENT      | type2     | INSTRUCTION WORD
