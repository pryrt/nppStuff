# -*- coding: utf-8 -*-
'''
Makes lexilla's "hidden" lexers available for NPP.

If you run it multiple times, it will toggle enabled/disabled.
Note: when it disables, you have to switch out of that tab _on that view/editor#_ for it to stop highlighting

A more generic version of 23275-enable-stata-lexer.py, which can be extended
as the framework for handling all of the hidden lexers, not just SAS and Stata

The post https://community.notepad-plus-plus.org/post/78579 helped update it for Notepad++ v8.4.3
'''

from Npp import notepad, editor, NOTIFICATION
from ctypes import windll, WINFUNCTYPE, addressof, create_unicode_buffer
from ctypes.wintypes import HWND, UINT, WPARAM, LPARAM, HMODULE, LPCWSTR, LPCSTR, LPVOID

class GenericLexer:
    _lexer_name = b"Generic"

    def __init__(self):
        self.lexer_name = create_unicode_buffer(self._lexer_name)

    def announce(self, lexintf):
        # console.write("I will colorize {} from {}\n".format(self._lexer_name, str(lexintf)))
        pass

    def colorize(self, lexintf):
        raise NotImplementedError("You should be calling colorize() on a specific lexer, not on the {} parent class".format(__class__))

# specific lexer subclasses
class RakuLexer(GenericLexer):
    """
        Raku was Perl6

    """

    _lexer_name = b"raku"
    SCE_RAKU_DEFAULT            = 0
    SCE_RAKU_ERROR              = 1
    SCE_RAKU_COMMENTLINE        = 2
    SCE_RAKU_COMMENTEMBED       = 3
    SCE_RAKU_POD                = 4
    SCE_RAKU_CHARACTER          = 5
    SCE_RAKU_HEREDOC_Q          = 6
    SCE_RAKU_HEREDOC_QQ         = 7
    SCE_RAKU_STRING             = 8
    SCE_RAKU_STRING_Q           = 9
    SCE_RAKU_STRING_QQ          = 10
    SCE_RAKU_STRING_Q_LANG      = 11
    SCE_RAKU_STRING_VAR         = 12
    SCE_RAKU_REGEX              = 13
    SCE_RAKU_REGEX_VAR          = 14
    SCE_RAKU_ADVERB             = 15
    SCE_RAKU_NUMBER             = 16
    SCE_RAKU_PREPROCESSOR       = 17
    SCE_RAKU_OPERATOR           = 18
    SCE_RAKU_WORD               = 19
    SCE_RAKU_FUNCTION           = 20
    SCE_RAKU_IDENTIFIER         = 21
    SCE_RAKU_TYPEDEF            = 22
    SCE_RAKU_MU                 = 23
    SCE_RAKU_POSITIONAL         = 24
    SCE_RAKU_ASSOCIATIVE        = 25
    SCE_RAKU_CALLABLE           = 26
    SCE_RAKU_GRAMMAR            = 27
    SCE_RAKU_CLASS              = 28


    def colorize(self, lexintf):
        self.announce(lexintf)

        editor.styleSetFore(self.SCE_RAKU_DEFAULT               , notepad.getEditorDefaultForegroundColor())
        editor.styleSetFore(self.SCE_RAKU_ERROR                 , (255,0,0))
        editor.styleSetFore(self.SCE_RAKU_COMMENTLINE           , (0,255,0))
        editor.styleSetFore(self.SCE_RAKU_COMMENTEMBED          , (0,255,0))
        editor.styleSetFore(self.SCE_RAKU_POD                   , (32,32,32))
        editor.styleSetFore(self.SCE_RAKU_CHARACTER             , (128,128,128))
        editor.styleSetFore(self.SCE_RAKU_HEREDOC_Q             , (0,255,0))
        editor.styleSetFore(self.SCE_RAKU_HEREDOC_QQ            , (0,255,0))
        editor.styleSetFore(self.SCE_RAKU_STRING                , (128,128,128))
        editor.styleSetFore(self.SCE_RAKU_STRING_Q              , (128,128,128))
        editor.styleSetFore(self.SCE_RAKU_STRING_QQ             , (128,128,128))
        editor.styleSetFore(self.SCE_RAKU_STRING_Q_LANG         , (128,128,128))
        editor.styleSetFore(self.SCE_RAKU_STRING_VAR            , (128,128,128))
        editor.styleSetFore(self.SCE_RAKU_REGEX                 , (128,128,255))
        editor.styleSetFore(self.SCE_RAKU_REGEX_VAR             , (128,128,255))
        editor.styleSetFore(self.SCE_RAKU_ADVERB                , (255,0,0))    # keywords7
        editor.styleSetFore(self.SCE_RAKU_NUMBER                , (255,0,0))
        editor.styleSetFore(self.SCE_RAKU_PREPROCESSOR          , (0,32,0))
        editor.styleSetFore(self.SCE_RAKU_OPERATOR              , (0,0,128))
        editor.styleSetFore(self.SCE_RAKU_WORD                  , (0,128,0))    # keywords1
        editor.styleSetFore(self.SCE_RAKU_FUNCTION              , (0,0,255))    # keywords2
        editor.styleSetFore(self.SCE_RAKU_IDENTIFIER            , (255,0,255))  # bareword (user functions, etc)
        editor.styleSetFore(self.SCE_RAKU_TYPEDEF               , (255,255,0))  # keywords4
        editor.styleSetFore(self.SCE_RAKU_MU                    , (0,0,128))    # $variable
        editor.styleSetFore(self.SCE_RAKU_POSITIONAL            , (0,0,160))    # @variable
        editor.styleSetFore(self.SCE_RAKU_ASSOCIATIVE           , (0,0,96))     # %variable
        editor.styleSetFore(self.SCE_RAKU_CALLABLE              , (255,0,0))    # ?
        editor.styleSetFore(self.SCE_RAKU_GRAMMAR               , (255,0,0))    # ?
        editor.styleSetFore(self.SCE_RAKU_CLASS                 , (255,0,0))    # ?

        # ordering is important
        if lexintf.nppver() < 8.410:
            self.ilexer_ptr = self.create_lexer_func(self.lexer_name.value)
            #console.write("old: called create_lexer_func({})\n".format(self.lexer_name.value))
        else:
            self.ilexer_ptr = windll.user32.SendMessageW(lexintf.notepad_hwnd, lexintf.NPPM_CREATELEXER, 0, addressof(self.lexer_name))
            #console.write("new: sendmessage NPPM_CREATELEXER({:s})\n".format(self.lexer_name.value))

        editor_hwnd = lexintf.editor1_hwnd if notepad.getCurrentView() == 0 else lexintf.editor2_hwnd
        windll.user32.SendMessageW(editor_hwnd, lexintf.SCI_SETILEXER, 0, self.ilexer_ptr)

        editor.setKeyWords(0, "BEGIN CATCH CHECK CONTROL END ENTER EVAL FIRST INIT KEEP LAST LEAVE NEXT POST PRE START TEMP UNDO after also andthen as async augment bag before but category circumfix class cmp complex constant contend default defer div does dynamic else elsif enum eq eqv extra fail fatal ff fff for gather gcd ge given grammar gt handles has if infix is lcm le leave leg let lift loop lt macro make maybe method mix mod module multi ne not o only oo or orelse orwith postcircumfix postfix prefix proto regex repeat require return-rw returns role rule size_t slang start str submethod subset supersede take temp term token trusts try unit unless until when where while with without x xor xx")
        editor.setKeyWords(1, "ACCEPTS AT-KEY EVALFILE EXISTS-KEY Filetests IO STORE abs accept acos acosec acosech acosh acotan acotanh alarm and antipairs asec asech asin asinh atan atan2 atanh base bind binmode bless break caller ceiling chars chdir chmod chomp chop chr chroot chrs cis close closedir codes comb conj connect contains continue cos cosec cosech cosh cotan cotanh crypt dbm defined die do dump each elems eof exec exists exit exp expmod fc fcntl fileno flat flip flock floor fmt fork formats functions get getc getpeername getpgrp getppid getpriority getsock gist glob gmtime goto grep hyper import index int invert ioctl is-prime iterator join keyof keys kill kv last lazy lc lcfirst lines link list listen local localtime lock log log10 lsb lstat map match mkdir msb msg my narrow new next no of open ord ords our pack package pairs path pick pipe polymod pop pos pred print printf prototype push quoting race rand read readdir readline readlink readpipe recv redo ref rename requires reset return reverse rewinddir rindex rmdir roots round samecase say scalar sec sech seek seekdir select semctl semget semop send set setpgrp setpriority setsockopt shift shm shutdown sign sin sinh sleep sockets sort splice split sprintf sqrt srand stat state study sub subst substr substr-rw succ symlink sys syscall system syswrite tan tanh tc tclc tell telldir tie time times trans trim trim-leading trim-trailing truncate uc ucfirst unimatch uniname uninames uniprop uniprops unival unlink unpack unpolar unshift untie use utime values wait waitpid wantarray warn wordcase words write")
        editor.setKeyWords(2, "AST Any Block Bool CallFrame Callable Code Collation Compiler Complex ComplexStr Cool CurrentThreadScheduler Date DateTime Dateish Distribution Distribution::Hash Distribution::Locally Distribution::Path Duration Encoding Encoding::Registry Endian FatRat ForeignCode HyperSeq HyperWhatever Instant Int IntStr Junction Label Lock::Async Macro Method Mu Nil Num NumStr Numeric ObjAt Parameter Perl PredictiveIterator Proxy RaceSeq Rat RatStr Rational Real Routine Routine::WrapHandle Scalar Sequence Signature Str StrDistance Stringy Sub Submethod Telemetry Telemetry::Instrument::Thread Telemetry::Instrument::ThreadPool Telemetry::Instrument::Usage Telemetry::Period Telemetry::Sampler UInt ValueObjAt Variable Version Whatever WhateverCode atomicint bit bool buf buf1 buf16 buf2 buf32 buf4 buf64 buf8 int int1 int16 int2 int32 int4 int64 int8 long longlong num num32 num64 rat rat1 rat16 rat2 rat32 rat4 rat64 rat8 uint uint1 uint16 uint2 uint32 uint4 uint64 uint8 utf16 utf32 utf8")
        editor.setKeyWords(3, "Array Associative Bag BagHash Baggy Blob Buf Capture Enumeration Hash Iterable Iterator List Map Mix MixHash Mixy NFC NFD NFKC NFKD Pair Positional PositionalBindFailover PseudoStash QuantHash Range Seq Set SetHash Setty Slip Stash Uni utf8")
        editor.setKeyWords(4, "Attribute Cancellation Channel CompUnit CompUnit::Repository CompUnit::Repository::FileSystem CompUnit::Repository::Installation Distro Grammar IO IO::ArgFiles IO::CatHandle IO::Handle IO::Notification IO::Path IO::Path::Cygwin IO::Path::QNX IO::Path::Unix IO::Path::Win32 IO::Pipe IO::Socket IO::Socket::Async IO::Socket::INET IO::Spec IO::Spec::Cygwin IO::Spec::QNX IO::Spec::Unix IO::Spec::Win32 IO::Special Kernel Lock Match Order Pod::Block Pod::Block::Code Pod::Block::Comment Pod::Block::Declarator Pod::Block::Named Pod::Block::Para Pod::Block::Table Pod::Defn Pod::FormattingCode Pod::Heading Pod::Item Proc Proc::Async Promise Regex Scheduler Semaphore Supplier Supplier::Preserving Supply Systemic Tap Thread ThreadPoolScheduler VM")
        editor.setKeyWords(5, "Backtrace Backtrace::Frame CX::Done CX::Emit CX::Last CX::Next CX::Proceed CX::Redo CX::Return CX::Succeed CX::Take CX::Warn Exception Failure X::AdHoc X::Anon::Augment X::Anon::Multi X::Assignment::RO X::Attribute::NoPackage X::Attribute::Package X::Attribute::Required X::Attribute::Undeclared X::Augment::NoSuchType X::Bind X::Bind::NativeType X::Bind::Slice X::Caller::NotDynamic X::Channel::ReceiveOnClosed X::Channel::SendOnClosed X::Comp X::Composition::NotComposable X::Constructor::Positional X::Control X::ControlFlow X::ControlFlow::Return X::DateTime::TimezoneClash X::Declaration::Scope X::Declaration::Scope::Multi X::Does::TypeObject X::Dynamic::NotFound X::Eval::NoSuchLang X::Export::NameClash X::IO X::IO::Chdir X::IO::Chmod X::IO::Copy X::IO::Cwd X::IO::Dir X::IO::DoesNotExist X::IO::Link X::IO::Mkdir X::IO::Move X::IO::Rename X::IO::Rmdir X::IO::Symlink X::IO::Unlink X::Inheritance::NotComposed X::Inheritance::Unsupported X::Method::InvalidQualifier X::Method::NotFound X::Method::Private::Permission X::Method::Private::Unqualified X::Mixin::NotComposable X::NYI X::NoDispatcher X::Numeric::Real X::OS X::Obsolete X::OutOfRange X::Package::Stubbed X::Parameter::Default X::Parameter::MultipleTypeConstraints X::Parameter::Placeholder X::Parameter::Twigil X::Parameter::WrongOrder X::Phaser::Multiple X::Phaser::PrePost X::Placeholder::Block X::Placeholder::Mainline X::Pod X::Proc::Async X::Proc::Async::AlreadyStarted X::Proc::Async::BindOrUse X::Proc::Async::CharsOrBytes X::Proc::Async::MustBeStarted X::Proc::Async::OpenForWriting X::Proc::Async::TapBeforeSpawn X::Proc::Unsuccessful X::Promise::CauseOnlyValidOnBroken X::Promise::Vowed X::Redeclaration X::Role::Initialization X::Scheduler::CueInNaNSeconds X::Seq::Consumed X::Sequence::Deduction X::Signature::NameClash X::Signature::Placeholder X::Str::Numeric X::StubCode X::Syntax X::Syntax::Augment::WithoutMonkeyTyping X::Syntax::Comment::Embedded X::Syntax::Confused X::Syntax::InfixInTermPosition X::Syntax::Malformed X::Syntax::Missing X::Syntax::NegatedPair X::Syntax::NoSelf X::Syntax::Number::RadixOutOfRange X::Syntax::P5 X::Syntax::Perl5Var X::Syntax::Regex::Adverb X::Syntax::Regex::SolitaryQuantifier X::Syntax::Reserved X::Syntax::Self::WithoutObject X::Syntax::Signature::InvocantMarker X::Syntax::Term::MissingInitializer X::Syntax::UnlessElse X::Syntax::Variable::Match X::Syntax::Variable::Numeric X::Syntax::Variable::Twigil X::Temporal X::Temporal::InvalidFormat X::TypeCheck X::TypeCheck::Assignment X::TypeCheck::Binding X::TypeCheck::Return X::TypeCheck::Splice X::Undeclared")
        editor.setKeyWords(6, "D a array b backslash c closure delete double exec exists f function h hash heredoc k kv p q qq quotewords s scalar single sym to v val w words ww x")

class SasLexer(GenericLexer):
    """
        SAS is another language

        %let
        %do
        also        cards        class
        data        input        model
        ods        proc        var
        where
        %printz
        %blah
        %peterfake
        where        run
        * ... comment style 1;
        run
        // ... comment style 2;
        run
        /* comment style 3 */
        5 + 7 = 9
        one
    """

    _lexer_name = b"sas"
    SCE_SAS_DEFAULT                                        = 0
    SCE_SAS_COMMENT                                        = 1
    SCE_SAS_COMMENTLINE                                    = 2
    SCE_SAS_COMMENTBLOCK                                   = 3
    SCE_SAS_NUMBER                                         = 4
    SCE_SAS_OPERATOR                                       = 5
    SCE_SAS_IDENTIFIER                                     = 6
    SCE_SAS_STRING                                         = 7
    SCE_SAS_TYPE                                           = 8
    SCE_SAS_WORD                                           = 9
    SCE_SAS_GLOBAL_MACRO                                   = 10
    SCE_SAS_MACRO                                          = 11
    SCE_SAS_MACRO_KEYWORD                                  = 12
    SCE_SAS_BLOCK_KEYWORD                                  = 13
    SCE_SAS_MACRO_FUNCTION                                 = 14
    SCE_SAS_STATEMENT                                      = 15


    def colorize(self, lexintf):
        self.announce(lexintf)

        editor.styleSetFore(self.SCE_SAS_DEFAULT               , notepad.getEditorDefaultForegroundColor())
        editor.styleSetFore(self.SCE_SAS_COMMENT               , (0,255,0))
        editor.styleSetFore(self.SCE_SAS_COMMENTLINE           , (0,255,0))
        editor.styleSetFore(self.SCE_SAS_COMMENTBLOCK          , (0,255,0))
        editor.styleSetFore(self.SCE_SAS_NUMBER                , (255,0,0))
        editor.styleSetFore(self.SCE_SAS_OPERATOR              , (128,64,0))
        editor.styleSetFore(self.SCE_SAS_IDENTIFIER            , (64,64,64))
        editor.styleSetFore(self.SCE_SAS_STRING                , (128,128,128))
        editor.styleSetFore(self.SCE_SAS_TYPE                  , (128,0,255))       # not implemented
        editor.styleSetFore(self.SCE_SAS_WORD                  , (255,128,0))       # not implemented
        editor.styleSetFore(self.SCE_SAS_GLOBAL_MACRO          , (255,255,0))       # not implemented
        editor.styleSetFore(self.SCE_SAS_MACRO                 , (0,0,255))         # start with %
        editor.styleSetFore(self.SCE_SAS_MACRO_KEYWORD         , (0,255,255))       # keywords/keywords1
        editor.styleSetFore(self.SCE_SAS_BLOCK_KEYWORD         , (0,0,127))         # keywords2
        editor.styleSetFore(self.SCE_SAS_MACRO_FUNCTION        , (0,127,127))       # keywords3
        editor.styleSetFore(self.SCE_SAS_STATEMENT             , (0xAA,0,0))        # keywords4

        # ordering is important
        if lexintf.nppver() < 8.410:
            self.ilexer_ptr = self.create_lexer_func(self.lexer_name.value)
            #console.write("old: called create_lexer_func({})\n".format(self.lexer_name.value))
        else:
            self.ilexer_ptr = windll.user32.SendMessageW(lexintf.notepad_hwnd, lexintf.NPPM_CREATELEXER, 0, addressof(self.lexer_name))
            #console.write("new: sendmessage NPPM_CREATELEXER({:s})\n".format(self.lexer_name.value))

        editor_hwnd = lexintf.editor1_hwnd if notepad.getCurrentView() == 0 else lexintf.editor2_hwnd
        windll.user32.SendMessageW(editor_hwnd, lexintf.SCI_SETILEXER, 0, self.ilexer_ptr)

        editor.setKeyWords(0, "%let %do")
        editor.setKeyWords(1, "also cards class data input model ods proc var where")
        editor.setKeyWords(2, "%printz")
        editor.setKeyWords(3, "run")

class StataLexer(GenericLexer):
    """
        Stata is a statistics language

        * http://galton.uchicago.edu/~eichler/stat22000/Handouts/stata-commands.html

        anova by ci clear correlate ...
        ttest use

        byte int long float double strL

        local life_questions 42
        display `life_questions'
        foreach var in varlist yearmade-kwh {
          summarize `var'
        }

        -(x+y^(x-y))/(x*y)

        "string" + "string"

        "string" * 5

        < > <= >= == != ~=

        generate incgt10k=income>10000 if income<.

        a & b | c & !d
    """

    _lexer_name = b"stata"
    SCE_STATA_DEFAULT                                  = 0
    SCE_STATA_COMMENT                                  = 1
    SCE_STATA_COMMENTLINE                              = 2
    SCE_STATA_COMMENTBLOCK                             = 3
    SCE_STATA_NUMBER                                   = 4
    SCE_STATA_OPERATOR                                 = 5
    SCE_STATA_IDENTIFIER                               = 6
    SCE_STATA_STRING                                   = 7
    SCE_STATA_TYPE                                     = 8
    SCE_STATA_WORD                                     = 9
    SCE_STATA_GLOBAL_MACRO                             = 10
    SCE_STATA_MACRO                                    = 11

    def colorize(self, lexintf):
        self.announce(lexintf)

        editor.styleSetFore(self.SCE_STATA_DEFAULT               , notepad.getEditorDefaultForegroundColor())
        editor.styleSetFore(self.SCE_STATA_COMMENT               , (0,128,0))
        editor.styleSetFore(self.SCE_STATA_COMMENTLINE           , (0,128,0))
        editor.styleSetFore(self.SCE_STATA_COMMENTBLOCK          , (0,128,0))
        editor.styleSetFore(self.SCE_STATA_NUMBER                , (255,128,0))
        editor.styleSetFore(self.SCE_STATA_OPERATOR              , (0,0,128))
        editor.styleSetFore(self.SCE_STATA_IDENTIFIER            , (64,64,64))
        editor.styleSetFore(self.SCE_STATA_STRING                , (128,128,128))
        editor.styleSetFore(self.SCE_STATA_TYPE                  , (128,0,255))     # KeyWords(1)
        editor.styleSetFore(self.SCE_STATA_WORD                  , (0,128,255))     # KeyWords(0)
        editor.styleSetFore(self.SCE_STATA_GLOBAL_MACRO          , (255,255,0))     # not implemented that I can see in LexStata.cxx
        editor.styleSetFore(self.SCE_STATA_MACRO                 , (0,0,255))       # not implemented that I can see in LexStata.cxx

        #### TODO: this block needs to move inside .colorize(), so needs to be reworked to be relative
        # ordering is important
        if lexintf.nppver() < 8.410:
            self.ilexer_ptr = self.create_lexer_func(self.lexer_name.value)
            #console.write("old: called create_lexer_func({})\n".format(self.lexer_name.value))
        else:
            self.ilexer_ptr = windll.user32.SendMessageW(lexintf.notepad_hwnd, lexintf.NPPM_CREATELEXER, 0, addressof(self.lexer_name))
            #console.write("new: sendmessage NPPM_CREATELEXER({:s})\n".format(self.lexer_name.value))

        editor_hwnd = lexintf.editor1_hwnd if notepad.getCurrentView() == 0 else lexintf.editor2_hwnd
        windll.user32.SendMessageW(editor_hwnd, lexintf.SCI_SETILEXER, 0, self.ilexer_ptr)

        editor.setKeyWords(0, "anova by ci clear correlate describe diagplot drop edit exit gen generate graph help if infile input list log lookup oneway pcorr plot predict qnorm regress replace save sebarr set sort stem summ summarize tab tabulate test ttest use")   # keywords SAS: %let %do
        editor.setKeyWords(1, "byte int long float double strL str") # types # SAS: also cards

class HiddenLexerInterface:
    NPPM_CREATELEXER                                   = (1024 + 1000 + 110)
    SCI_SETILEXER                                      = 4033

    def __str__(self):
        return "<" + self.__class__.__name__ + ">"

    def __init__(self):
        '''
            Initialize the class, should be called only once.
        '''

        # **************** configuration area ****************
        """
        files with these extensions and a null lexer (that is, normal text), will be processed by the listed extension

        Examples:
            self.map_extensions['oneext'] = OneFileLexer()                              # *.oneext will be processed by a OneFileLexer instance
            self.map_extensions['notc'] = self.map_extensions['noth'] = NotCLexer()     # *.notc and *.noth will be processed by the same NotCLexer instance
        """
        self.map_extensions = {}
        self.map_extensions['do'] = self.map_extensions['stata'] = StataLexer()
        self.map_extensions['sas'] = SasLexer()
        self.map_extensions['raku'] = RakuLexer()

        # initialize win32 interface info
        self.notepad_hwnd = windll.user32.FindWindowW(u'Notepad++', None)
        self.editor1_hwnd = windll.user32.FindWindowExW(self.notepad_hwnd, None, u"Scintilla", None)
        self.editor2_hwnd = windll.user32.FindWindowExW(self.notepad_hwnd, self.editor1_hwnd, u"Scintilla", None)
        windll.user32.SendMessageW.argtypes = [HWND, UINT, WPARAM, LPARAM]
        windll.user32.SendMessageW.restype  = LPARAM

        # if it's older then v8.4.1, need to make an old CreateLexer; if it's v8.4.2-or-newer, don't need to go searching for the function
        if self.nppver() < 8.410:
            windll.kernel32.GetModuleHandleW.argtypes = [LPCWSTR]
            windll.kernel32.GetModuleHandleW.restype = HMODULE
            windll.kernel32.GetProcAddress.argtypes = [HMODULE, LPCSTR]
            windll.kernel32.GetProcAddress.restype = LPVOID
            handle = windll.kernel32.GetModuleHandleW(None)
            create_lexer_ptr = windll.kernel32.GetProcAddress(handle, b'CreateLexer')

            CL_FUNCTYPE = WINFUNCTYPE(LPVOID, LPCSTR)
            self.create_lexer_func = CL_FUNCTYPE(create_lexer_ptr)
        else:
            pass


        # create the callbacks
        notepad.callback(self.on_langchanged, [NOTIFICATION.LANGCHANGED])
        notepad.callback(self.on_bufferactivated, [NOTIFICATION.BUFFERACTIVATED])

        self.enabled = False

        console.write("Initialized {}\n".format(self.__class__.__name__))

    def init_lexer(self, ext):
        '''
            Initializes the lexer and its properties
            Args:
                None
            Returns:
                None
        '''
        if ext in self.map_extensions:
            self.map_extensions[ext].colorize(self)
            self.lexer_name = self.map_extensions[ext].lexer_name

        #console.write("Stata lexer: set styles\n")

    def check_lexers(self):
        '''
            Checks if the current document is of interest.

            Args:
                None
            Returns:
                None
        '''

        old_lexer = editor.getLexerLanguage()
        old_langtype = "{}".format(notepad.getCurrentLang())
        has_no_lexer_assigned = editor.getLexerLanguage() == 'null'
        _, _, file_extension = notepad.getCurrentFilename().rpartition('.')
        if has_no_lexer_assigned and file_extension in self.map_extensions:
            if self.enabled:
                self.init_lexer(file_extension)
        #console.write("check_lexers: old:{} lex:{} hasnt:{} oldlang:{} newlang:{} << \"{}\" \n".format(
        #    old_lexer, editor.getLexerLanguage(), has_no_lexer_assigned,
        #    old_langtype, notepad.getCurrentLang(), notepad.getCurrentFilename()
        #))


    def on_bufferactivated(self, args):
        '''
            Callback which gets called every time one switches a document.
            Triggers the check if the document is of interest.

            Args:
                provided by notepad object but none are of interest
            Returns:
                None
        '''
        self.check_lexers()
        #console.write("on_bufferactivated\n")


    def on_langchanged(self, args):
        '''
            Callback gets called every time one uses the Language menu to set a lexer
            Triggers the check if the document is of interest

            Args:
                provided by notepad object but none are of interest
            Returns:
                None
        '''
        self.check_lexers()
        #console.write("on_langchanged\n")

    def nppver(self):
        self.NPPM_GETNPPVERSION = 1024 + 1000 + 50
        nppv = windll.user32.SendMessageW(self.notepad_hwnd, self.NPPM_GETNPPVERSION, 1, 0 )
        # for v8.4.1 and newer, this will pad it as 8<<16 + 410 for easy comparison
        # v8.4 will be under old scheme of 8<<16 + 4, v8.3.3 is 8<<16 + 33
        ver = nppv >> 16    # major version
        mnr = nppv & 0xFFFF # minor version
        if (ver <= 8) and (mnr < 10):
            ver += mnr/10.
        elif (ver <= 8) and (mnr < 100):
            ver += mnr/100.
        elif (ver>8) or (mnr>99):
            ver += mnr/1000.

        return ver

    def toggle(self):
        ''' Toggles between enabled and disabled '''
        self.enabled = not self.enabled
        if self.enabled:
            console.write("Enabled Hidden Lexers\n")
        else:
            console.write("Disabled Hidden Lexers\n")
        self.on_bufferactivated(None)

    def main(self):
        '''
            Main function entry point.
            Simulates the buffer_activated event to enforce
            detection of current document and potential styling.

            Args:
                None
            Returns:
                None
        '''
        self.enabled = True
        self.on_bufferactivated(None)


try:
    lexer_interface.toggle()
    if True:
        notepad.clearCallbacks()
        del lexer_interface
        console.write("deleted callbacks and lexer_interface")
except NameError:
    lexer_interface = HiddenLexerInterface()
    lexer_interface.main()
