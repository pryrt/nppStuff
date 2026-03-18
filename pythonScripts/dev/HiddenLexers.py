# -*- coding: utf-8 -*-
'''
Makes lexilla's "hidden" lexers available for NPP.
- [STOP] SAS - N++ v8.7.8 enabled it internally
- Stata
- X12

The most recent version of this script is available at
https://raw.githubusercontent.com/pryrt/nppStuff/refs/heads/main/pythonScripts/dev/HiddenLexers.py

===========

If you run it multiple times, it will toggle enabled/disabled.
Note: when it disables, you have to switch out of that tab _on that view/editor#_ for it to stop highlighting

A more generic version of 23275-enable-stata-lexer.py, which can be extended
as the framework for handling all of the hidden lexers, not just SAS and Stata

The post https://community.notepad-plus-plus.org/post/78579 helped update it for Notepad++ v8.4.3
'''

from Npp import notepad, editor, console, NOTIFICATION
from ctypes import windll, WINFUNCTYPE, addressof, create_unicode_buffer
from ctypes.wintypes import HWND, UINT, WPARAM, LPARAM, HMODULE, LPCWSTR, LPCSTR, LPVOID
import sys

class GenericLexer:
    _lexer_name = b"Generic"

    def __init__(self):
        tmp_name = self._lexer_name
        if sys.version_info.major==3: tmp_name = self._lexer_name.decode("utf-8")
        self.lexer_name = create_unicode_buffer(tmp_name)

    def announce(self, lexintf):
        return # comment out this line to announce each HiddenLexer enablement
        tmp_name = self._lexer_name
        if sys.version_info.major==3: tmp_name = self._lexer_name.decode("utf-8")
        console.write("I will colorize {} from {}\n".format(tmp_name, str(lexintf)))
        pass

    def colorize(self, lexintf):
        raise NotImplementedError("You should be calling colorize() on a specific lexer, not on the {} parent class".format(__class__))

# specific lexer subclasses
class ConfLexer(GenericLexer):
    """
        Apache .htaccess/*.conf lexer

        https://github.com/notepad-plus-plus/notepad-plus-plus/blob/938b61333260f3fed25fcfd5693b9e16720f2ad1/lexilla/include/SciLexer.h#L611-L620
    """

    _lexer_name = b"conf"

    SCE_CONF_DEFAULT                                    = 0
    SCE_CONF_COMMENT                                    = 1
    SCE_CONF_NUMBER                                     = 2
    SCE_CONF_IDENTIFIER                                 = 3
    SCE_CONF_EXTENSION                                  = 4
    SCE_CONF_PARAMETER                                  = 5
    SCE_CONF_STRING                                     = 6
    SCE_CONF_OPERATOR                                   = 7
    SCE_CONF_IP                                         = 8
    SCE_CONF_DIRECTIVE                                  = 9

    def colorize(self, lexintf):
        self.announce(lexintf)

        editor.styleSetFore(self.SCE_CONF_DEFAULT                 , notepad.getEditorDefaultForegroundColor())
        editor.styleSetFore(self.SCE_CONF_COMMENT                 , (0,127,0))
        editor.styleSetFore(self.SCE_CONF_NUMBER                  , (0,127,127))
        editor.styleSetFore(self.SCE_CONF_IDENTIFIER              , (0,0,127))
        editor.styleSetBack(self.SCE_CONF_IDENTIFIER              , (255,250,160))
        editor.styleSetFore(self.SCE_CONF_EXTENSION               , (0,0,0))
        editor.styleSetBack(self.SCE_CONF_EXTENSION               , (239,239,239))
        editor.styleSetFore(self.SCE_CONF_PARAMETER               , (0,63,192))            # keywords2
        editor.styleSetFore(self.SCE_CONF_STRING                  , (127,0,127))
        editor.styleSetFore(self.SCE_CONF_OPERATOR                , (255,0,0))
        editor.styleSetFore(self.SCE_CONF_IP                      , (0,127,127))
        editor.styleSetFore(self.SCE_CONF_DIRECTIVE               , (0,0,255))           # keywords

        # ordering is important
        if lexintf.nppver() < 8.410:
            self.ilexer_ptr = self.create_lexer_func(self.lexer_name.value)
            #console.write("old: called create_lexer_func({})\n".format(self.lexer_name.value))
        else:
            self.ilexer_ptr = windll.user32.SendMessageW(lexintf.notepad_hwnd, lexintf.NPPM_CREATELEXER, 0, addressof(self.lexer_name))
            #console.write("new: sendmessage NPPM_CREATELEXER({:s})\n".format(self.lexer_name.value))

        editor_hwnd = lexintf.editor1_hwnd if notepad.getCurrentView() == 0 else lexintf.editor2_hwnd
        windll.user32.SendMessageW(editor_hwnd, lexintf.SCI_SETILEXER, 0, self.ilexer_ptr)

        # LexX12.cxx only defines one property; I want to enable folding
        editor.setProperty("fold", "1")
        editor.setMarginWidthN(3,14)    # MARGIN3 = FOLD, WIDTH=14px (standard width in NPP)

        # if I am wrong about keyword lists, each would go here...
        # directives: https://httpd.apache.org/docs/current/mod/directives.html
        editor.setKeyWords(0, """
            acceptfilter acceptmutex acceptpathinfo accessconfig accessfilename action addalt
            addaltbyencoding addaltbytype addcharset adddefaultcharset adddescription addencoding
            addhandler addicon addiconbyencoding addiconbytype addinputfilter addlanguage addmodule
            addmoduleinfo addoutputfilter addoutputfilterbytype addtype agentlog alias aliasmatch
            aliaspreservepath all allow allowconnect allowencodedslashes allowmethods allowoverride
            allowoverridelist anonymous anonymous_authoritative anonymous_logemail anonymous_mustgiveemail
            anonymous_nouserid anonymous_verifyemail assignuserid asyncrequestworkerfactor
            authauthoritative authbasicauthoritative authbasicfake authbasicprovider
            authbasicusedigestalgorithm authdbauthoritative authdbduserpwquery authdbduserrealmquery
            authdbgroupfile authdbmauthoritative authdbmgroupfile authdbmtype authdbmuserfile
            authdbuserfile authdigestalgorithm authdigestdomain authdigestfile authdigestgroupfile
            authdigestnccheck authdigestnonceformat authdigestnoncelifetime authdigestprovider
            authdigestqop authdigestshmemsize authformauthoritative authformbody authformdisablenostore
            authformfakebasicauth authformlocation authformloginrequiredlocation
            authformloginsuccesslocation authformlogoutlocation authformmethod authformmimetype
            authformpassword authformprovider authformsitepassphrase authformsize authformusername
            authgroupfile authldapauthoritative authldapauthorizeprefix authldapbindauthoritative
            authldapbinddn authldapbindpassword authldapcharsetconfig authldapcompareasuser
            authldapcomparednonserver authldapdereferencealiases authldapenabled authldapfrontpagehack
            authldapgroupattribute authldapgroupattributeisdn authldapinitialbindasuser
            authldapinitialbindpattern authldapmaxsubgroupdepth authldapremoteuserattribute
            authldapremoteuserisdn authldapsearchasuser authldapsubgroupattribute authldapsubgroupclass
            authldapurl authmerging authname authncachecontext authncacheenable authncacheprovidefor
            authncachesocache authncachetimeout authnprovideralias authnzfcgicheckauthnprovider
            authnzfcgidefineprovider authtype authuserfile authzdbdlogintoreferer authzdbdquery
            authzdbdredirectquery authzdbmtype authzprovideralias authzsendforbiddenonfailure
            balancergrowth balancerinherit balancermember balancerpersist bindaddress brotlialteretag
            brotlicompressionmaxinputblock brotlicompressionquality brotlicompressionwindow
            brotlifilternote browsermatch browsermatchnocase bs2000account bufferedlogs buffersize
            cachedefaultexpire cachedetailheader cachedirlength cachedirlevels cachedisable cacheenable
            cacheexpirycheck cachefile cacheforcecompletion cachegcclean cachegcdaily cachegcinterval
            cachegcmemusage cachegcunused cacheheader cacheignorecachecontrol cacheignoreheaders
            cacheignorenolastmod cacheignorequerystring cacheignoreurlsessionidentifiers cachekeybaseurl
            cachelastmodifiedfactor cachelock cachelockmaxage cachelockpath cachemaxexpire cachemaxfilesize
            cacheminexpire cacheminfilesize cachenegotiateddocs cachequickhandler cachereadsize
            cachereadtime cacheroot cachesize cachesocache cachesocachemaxsize cachesocachemaxtime
            cachesocachemintime cachesocachereadsize cachesocachereadtime cachestaleonerror
            cachestoreexpired cachestorenostore cachestoreprivate cachetimemargin cgidscripttimeout
            cgimapextension cgipassauth cgiscripttimeout cgivar charsetdefault charsetoptions
            charsetsourceenc checkbasenamematch checkcaseonly checkspelling childperuserid chrootdir
            clearmodulelist contentdigest cookiedomain cookieexpires cookiehttponly cookielog cookiename
            cookiesamesite cookiesecure cookiestyle cookietracking coredumpdirectory customlog dav
            davbasepath davdepthinfinity davgenericlockdb davlockdb davlockdiscovery davmintimeout
            dbdexptime dbdinitsql dbdkeep dbdmax dbdmin dbdparams dbdpersist dbdpreparesql dbdriver
            defaulticon defaultlanguage defaultruntimedir defaulttype define deflatealteretag
            deflatebuffersize deflatecompressionlevel deflatefilternote deflateinflatelimitrequestbody
            deflateinflateratioburst deflateinflateratiolimit deflatememlevel deflatewindowsize deny
            directory directorycheckhandler directoryindex directoryindexredirect directorymatch
            directoryslash documentroot dtraceprivileges dumpioinput dumpiooutput else elseif
            enableexceptionhook enablemmap enablesendfile error errordocument errorlog errorlogformat
            example expiresactive expiresbytype expiresdefault extendedstatus extfilterdefine
            extfilteroptions fallbackresource fancyindexing fileetag files filesmatch filterchain
            filterdeclare filterprotocol filterprovider filtertrace flushmaxpipelined flushmaxthreshold
            forcelanguagepriority forcetype forensiclog from globallog gprofdir gracefulshutdowntimeout
            group h2copyfiles h2direct h2earlyhint h2earlyhints h2maxdataframelen h2maxheaderblocklen
            h2maxsessionstreams h2maxstreamerrors h2maxworkeridleseconds h2maxworkers h2minworkers
            h2moderntlsonly h2outputbuffering h2padding h2proxyrequests h2push h2pushdiarysize
            h2pushpriority h2pushresource h2serializeheaders h2streammaxmemsize h2streamtimeout
            h2tlscooldownsecs h2tlswarmupsize h2upgrade h2websockets h2windowsize header headername
            heartbeataddress heartbeatlisten heartbeatmaxservers heartbeatstorage hostnamelookups
            httpprotocoloptions identitycheck identitychecktimeout if ifdefine ifdirective iffile ifmodule
            ifsection ifversion imapbase imapdefault imapmenu include includeoptional indexheadinsert
            indexignore indexignorereset indexoptions indexorderdefault indexstylesheet inputsed
            isapiappendlogtoerrors isapiappendlogtoquery isapicachefile isapifakeasync isapilognotsupported
            isapireadaheadbuffer keepalive keepalivetimeout keptbodysize languagepriority ldapcacheentries
            ldapcachettl ldapconnectionpoolttl ldapconnectiontimeout ldaplibrarydebug ldapopcacheentries
            ldapopcachettl ldapreferralhoplimit ldapreferrals ldapretries ldapretrydelay
            ldapsharedcachefile ldapsharedcachesize ldaptimeout ldaptrustedca ldaptrustedcatype
            ldaptrustedclientcert ldaptrustedglobalcert ldaptrustedmode ldapverifyservercert limit
            limitexcept limitinternalrecursion limitrequestbody limitrequestfields limitrequestfieldsize
            limitrequestline limitxmlrequestbody listen listenbacklog listencoresbucketsratio
            listentcpdeferaccept loadfile loadmodule location locationmatch lockfile logformat
            logiotrackttfb loglevel logmessage luaauthzprovider luacodecache luahookaccesschecker
            luahookauthchecker luahookcheckuserid luahookfixups luahookinsertfilter luahooklog
            luahookmaptostorage luahookpretranslate luahooktranslatename luahooktypechecker luainherit
            luainputfilter luamaphandler luaoutputfilter luapackagecpath luapackagepath luaquickhandler
            luaroot luascope macro maxclients maxconnectionsperchild maxkeepaliverequests maxmemfree
            maxrangeoverlaps maxrangereversals maxranges maxrequestsperchild maxrequestsperthread
            maxrequestworkers maxspareservers maxsparethreads maxthreads maxthreadsperchild
            mcachemaxobjectcount mcachemaxobjectsize mcachemaxstreamingbuffer mcacheminobjectsize
            mcacheremovalalgorithm mcachesize mdactivationdelay mdbaseserver mdcachallenges
            mdcertificateagreement mdcertificateauthority mdcertificatecheck mdcertificatefile
            mdcertificatekeyfile mdcertificatemonitor mdcertificateprotocol mdcertificatestatus
            mdchallengedns01 mdchallengedns01version mdcheckinterval mdcontactemail mddrivemode
            mdexternalaccountbinding mdhttpproxy mdinitialdelay mdmatchnames mdmember mdmembers
            mdmessagecmd mdmuststaple mdnotifycmd mdomain mdomainset mdportmap mdprivatekeys mdprofile
            mdprofilemandatory mdrenewmode mdrenewviaari mdrenewwindow mdrequirehttps mdretrydelay
            mdretryfailover mdserverstatus mdstapleothers mdstapling mdstaplingkeepresponse
            mdstaplingrenewwindow mdstoredir mdstorelocks mdwarnwindow memcacheconnttl mergeslashes
            mergetrailers metadir metafiles metasuffix mimemagicfile minspareservers minsparethreads
            mmapfile modemstandard modmimeusepathinfo multiviewsmatch mutex namevirtualhost nocache noproxy
            numservers nwssltrustedcerts nwsslupgradeable options order outputsed passenv pidfile port
            privilegesmode protocol protocolecho protocols protocolshonororder proxy proxy100continue
            proxyaddheaders proxybadheader proxyblock proxydomain proxyerroroverride proxyexpressdbmfile
            proxyexpressdbmtype proxyexpressenable proxyfcgibackendtype proxyfcgisetenvif
            proxyftpdircharset proxyftpescapewildcards proxyftplistonwildcard proxyhcexpr proxyhctemplate
            proxyhctpsize proxyhtmlbufsize proxyhtmlcharsetout proxyhtmldoctype proxyhtmlenable
            proxyhtmlevents proxyhtmlextended proxyhtmlfixups proxyhtmlinterp proxyhtmllinks proxyhtmlmeta
            proxyhtmlstripcomments proxyhtmlurlmap proxyiobuffersize proxymatch proxymaxforwards proxypass
            proxypassinherit proxypassinterpolateenv proxypassmatch proxypassreverse
            proxypassreversecookiedomain proxypassreversecookiepath proxypreservehost
            proxyreceivebuffersize proxyremote proxyremotematch proxyrequests proxyscgiinternalredirect
            proxyscgisendfile proxyset proxysourceaddress proxystatus proxytimeout proxyvia
            proxywebsocketfallbacktoproxyhttp qsc qualifyredirecturl readbuffersize readmename
            receivebuffersize redirect redirectmatch redirectpermanent redirectrelative redirecttemp
            redisconnpoolttl redistimeout refererignore refererlog reflectorheader regexdefaultoptions
            registerhttpmethod remoteipheader remoteipinternalproxy remoteipinternalproxylist
            remoteipproxiesheader remoteipproxyprotocol remoteipproxyprotocolexceptions
            remoteiptrustedproxy remoteiptrustedproxylist removecharset removeencoding removehandler
            removeinputfilter removelanguage removeoutputfilter removetype requestheader requestreadtimeout
            require requireall requireany requirenone resourceconfig rewritebase rewritecond rewriteengine
            rewritelock rewritelog rewriteloglevel rewritemap rewriteoptions rewriterule rlimitcpu
            rlimitmem rlimitnproc satisfy scoreboardfile script scriptalias scriptaliasmatch
            scriptinterpretersource scriptlog scriptlogbuffer scriptloglength scriptsock securelisten
            seerequesttail sendbuffersize serveradmin serveralias serverlimit servername serverpath
            serverroot serversignature servertokens servertype session sessioncookiename sessioncookiename2
            sessioncookieremove sessioncryptocipher sessioncryptodriver sessioncryptopassphrase
            sessioncryptopassphrasefile sessiondbdcookiename sessiondbdcookiename2 sessiondbdcookieremove
            sessiondbddeletelabel sessiondbdinsertlabel sessiondbdperuser sessiondbdselectlabel
            sessiondbdupdatelabel sessionenv sessionexclude sessionexpiryupdateinterval sessionheader
            sessioninclude sessionmaxage setenv setenvif setenvifexpr setenvifnocase sethandler
            setinputfilter setoutputfilter singlelisten ssiendtag ssierrormsg ssietag ssilastmodified
            ssilegacyexprparser ssistarttag ssitimeformat ssiundefinedecho sslcacertificatefile
            sslcacertificatepath sslcadnrequestfile sslcadnrequestpath sslcarevocationcheck
            sslcarevocationfile sslcarevocationpath sslcertificatechainfile sslcertificatefile
            sslcertificatekeyfile sslciphersuite sslcompression sslcryptodevice sslengine sslfips
            sslhonorcipherorder sslinsecurerenegotiation sslmutex sslocspdefaultresponder sslocspenable
            sslocspnoverify sslocspoverrideresponder sslocspproxyurl sslocsprespondercertificatefile
            sslocsprespondertimeout sslocspresponsemaxage sslocspresponsetimeskew sslocspuserequestnonce
            sslopensslconfcmd ssloptions sslpassphrasedialog sslprotocol sslproxycacertificatefile
            sslproxycacertificatepath sslproxycarevocationcheck sslproxycarevocationfile
            sslproxycarevocationpath sslproxycheckpeercn sslproxycheckpeerexpire sslproxycheckpeername
            sslproxyciphersuite sslproxyengine sslproxymachinecertificatechainfile
            sslproxymachinecertificatefile sslproxymachinecertificatepath sslproxyprotocol sslproxyverify
            sslproxyverifydepth sslrandomseed sslrenegbuffersize sslrequire sslrequiressl sslsessioncache
            sslsessioncachetimeout sslsessionticketkeyfile sslsessiontickets sslsrpunknownuserseed
            sslsrpverifierfile sslstaplingcache sslstaplingerrorcachetimeout sslstaplingfaketrylater
            sslstaplingforceurl sslstaplingrespondertimeout sslstaplingresponsemaxage
            sslstaplingresponsetimeskew sslstaplingreturnrespondererrors sslstaplingstandardcachetimeout
            sslstrictsnivhostcheck sslusername sslusestapling sslverifyclient sslverifydepth
            sslvhostsnipolicy startservers startthreads stricthostcheck substitute substituteinheritbefore
            substitutemaxlinelength suexec suexecusergroup threadlimit threadsperchild threadstacksize
            timeout traceenable transferlog typesconfig unclist undefine undefmacro unsetenv use
            usecanonicalname usecanonicalphysicalport user userdir vhostcgimode vhostcgiprivs vhostgroup
            vhostprivs vhostsecure vhostuser virtualdocumentroot virtualdocumentrootip virtualhost
            virtualscriptalias virtualscriptaliasip watchdoginterval win32disableacceptex xbithack
            xml2encalias xml2encdefault xml2startparse
        """)   # directives
        # parameters: allo deny on off, etc
        editor.setKeyWords(1, """
            alert any crit debug downgrade-1.0 emerg execcgi false followsymlinks force-response-1.0 includes
            indexes inetd info multiviews no nokeepalive none notice off on standalone true warn x-compress x-gzip yes
        """) # parameters
        # I originally had the CamelCase, but that wouldn't match; I keep forgetting
        #   scintilla does LowerCase matching internally


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

class X12Lexer(GenericLexer):
    """
        X12 EDI is a language for business-to-business transaction software

        * https://x12.org/

        * example: https://iwayinfocenter.informationbuilders.com/TLs/TL_soa_ebiz_edix12/source/sample_docs49.htm
            ISA*00*          *01*          *ZZ*NOTP           *ZZ*NOTP           *050108*0954*U*00501*000000001*0*P*>
            GS*IN*NOTP*NOTP*20050108*0954*1*X*004010
            ST*810*0001
            BIG*20021119*184*20021015*BMB
            REF*IA*040682
            N1*BT*WALGREEN*92*0000
            ITD*02**1.000**30**31*****1% 30 NET 31
            FOB*CC
            PID*S**VI*FL
            IT1*0001*267*CA*53.52**IN*859067
            PID*F*08*VI**BARBIE SING W/ME DISC GRL CD PLYR
            TDS*1421839*1428984
            CAD*T***CFWY*CONSOLIDATED FREIGHTWAYS
            SAC*A*D240***7145**********FREIGHT CHARGE
            ISS*267*CA
            CTT*1
            SE*15*0001
            GE*1*1
            IEA*1*000000001

        Looking at LexX12.cxx, does not appear to have any keyword lists.
    """

    _lexer_name = b"x12"
    SCE_X12_DEFAULT                                    = 0
    SCE_X12_BAD                                        = 1
    SCE_X12_ENVELOPE                                   = 2
    SCE_X12_FUNCTIONGROUP                              = 3
    SCE_X12_TRANSACTIONSET                             = 4
    SCE_X12_SEGMENTHEADER                              = 5
    SCE_X12_SEGMENTEND                                 = 6
    SCE_X12_SEP_ELEMENT                                = 7
    SCE_X12_SEP_SUBELEMENT                             = 8

    def colorize(self, lexintf):
        self.announce(lexintf)

        editor.styleSetFore(self.SCE_X12_DEFAULT                 , notepad.getEditorDefaultForegroundColor())
        editor.styleSetFore(self.SCE_X12_BAD                     , (255,0,0))
        editor.styleSetFore(self.SCE_X12_ENVELOPE                , (255,0,255))
        editor.styleSetFore(self.SCE_X12_FUNCTIONGROUP           , (0,204,0))
        editor.styleSetFore(self.SCE_X12_TRANSACTIONSET          , (0,0,204))
        editor.styleSetFore(self.SCE_X12_SEGMENTHEADER           , (64,64,64))
        editor.styleSetFore(self.SCE_X12_SEGMENTEND              , (128,128,128))
        editor.styleSetFore(self.SCE_X12_SEP_ELEMENT             , (255,0,0))
        editor.styleSetFore(self.SCE_X12_SEP_SUBELEMENT          , (255,127,255))

        editor.styleSetBack(self.SCE_X12_BAD                     , (255,255,0))
        editor.styleSetBack(self.SCE_X12_SEP_ELEMENT             , (237,237,237))
        editor.styleSetBack(self.SCE_X12_SEP_SUBELEMENT          , (237,237,237))

        # ordering is important
        if lexintf.nppver() < 8.410:
            self.ilexer_ptr = self.create_lexer_func(self.lexer_name.value)
            #console.write("old: called create_lexer_func({})\n".format(self.lexer_name.value))
        else:
            self.ilexer_ptr = windll.user32.SendMessageW(lexintf.notepad_hwnd, lexintf.NPPM_CREATELEXER, 0, addressof(self.lexer_name))
            #console.write("new: sendmessage NPPM_CREATELEXER({:s})\n".format(self.lexer_name.value))

        editor_hwnd = lexintf.editor1_hwnd if notepad.getCurrentView() == 0 else lexintf.editor2_hwnd
        windll.user32.SendMessageW(editor_hwnd, lexintf.SCI_SETILEXER, 0, self.ilexer_ptr)

        # LexX12.cxx only defines one property; I want to enable folding
        editor.setProperty("fold", "1")
        editor.setMarginWidthN(3,14)    # MARGIN3 = FOLD, WIDTH=14px (standard width in NPP)

        # if I am wrong about keyword lists, each would go here...
        #editor.setKeyWords(0, "word1 word2")
        #editor.setKeyWords(1, "word11 word12")

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
        #self.map_extensions['sas'] = SasLexer()    # N++ v8.7.8 now enables SAS internally
        self.map_extensions['x12'] = X12Lexer()
        self.map_extensions['htaccess'] = self.map_extensions['conf'] = ConfLexer()

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
        notepad.clearCallbacks(lexer_interface.on_langchanged)
        notepad.clearCallbacks(lexer_interface.on_bufferactivated)
        del lexer_interface
        console.write("deleted callbacks and lexer_interface\n")
except NameError:
    lexer_interface = HiddenLexerInterface()
    lexer_interface.main()
