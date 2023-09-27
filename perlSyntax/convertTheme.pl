#!perl

use 5.014; # strict, //, s//r
use warnings;
$| = 1;
my @list = (
    { name => "DEFAULT"                      , styleID => "0", fgColor => "FF0000", bgColor => "FFFFFF", fontName => "", fontStyle => "0", fontSize => "", colorStyle => '0', },
    { name => "INSTRUCTION WORD"             , styleID => "5", fgColor => "0000FF", bgColor => "FFFFFF", fontName => "", fontStyle => "1", fontSize => "", keywordClass => 'instre1', colorStyle => '0', },
    { name => "NUMBER"                       , styleID => "4", fgColor => "FF0000", bgColor => "FFFFFF", fontName => "", fontStyle => "0", fontSize => "", colorStyle => '0', },
    { name => "OPERATOR"                     , styleID => "10", fgColor => "000080", bgColor => "FFFFFF", fontName => "", fontStyle => "1", fontSize => "", colorStyle => '0', },
    { name => "IDENTIFIER"                   , styleID => "11", fgColor => "004080", bgColor => "FFFFFF", fontName => "", fontStyle => "0", fontSize => "", colorStyle => '0', },
    { name => "SCALAR"                       , styleID => "12", fgColor => "FF8000", bgColor => "FFFFFF", fontName => "", fontStyle => "0", fontSize => "", colorStyle => '0', },
    { name => "ARRAY"                        , styleID => "13", fgColor => "CF34CF", bgColor => "FFFFFF", fontName => "", fontStyle => "0", fontSize => "", colorStyle => '0', },
    { name => "HASH"                         , styleID => "14", fgColor => "8080C0", bgColor => "FFFFFF", fontName => "", fontStyle => "0", fontSize => "", colorStyle => '0', },
    { name => "SYMBOL TABLE"                 , styleID => "15", fgColor => "FF0000", bgColor => "FFFFFF", fontName => "", fontStyle => "1", fontSize => "", colorStyle => '0', },
    { name => "PROTOTYPE"                    , styleID => "40", fgColor => "000080", bgColor => "FFFFFF", fontName => "", fontStyle => "1", fontSize => "", colorStyle => '0', },
    { name => "COMMENT LINE"                 , styleID => "2", fgColor => "008000", bgColor => "FFFFFF", fontName => "", fontStyle => "0", fontSize => "", colorStyle => '0', },
    { name => "STRING SINGLEQUOTE"           , styleID => "7", fgColor => "808080", bgColor => "FFFFFF", fontName => "", fontStyle => "2", fontSize => "", colorStyle => '0', },
    { name => "STRING DOUBLEQUOTE"           , styleID => "6", fgColor => "808080", bgColor => "FFFFFF", fontName => "", fontStyle => "0", fontSize => "", colorStyle => '0', },
    { name => "STRING BACKTICKS"             , styleID => "20", fgColor => "FFFF00", bgColor => "808080", fontName => "", fontStyle => "1", fontSize => "", colorStyle => '0', },
    { name => "STRING Q"                     , styleID => "26", fgColor => "804080", bgColor => "FFFFFF", fontName => "", fontStyle => "2", fontSize => "", colorStyle => '0', },
    { name => "STRING QQ"                    , styleID => "27", fgColor => "804080", bgColor => "FFFFFF", fontName => "", fontStyle => "0", fontSize => "", colorStyle => '0', },
    { name => "STRING QX"                    , styleID => "28", fgColor => "8000FF", bgColor => "FFEEEC", fontName => "", fontStyle => "0", fontSize => "", colorStyle => '0', },
    { name => "STRING QR"                    , styleID => "29", fgColor => "8080FF", bgColor => "F8FEDE", fontName => "", fontStyle => "0", fontSize => "", colorStyle => '0', },
    { name => "STRING QW"                    , styleID => "30", fgColor => "CF34CF", bgColor => "FFFFFF", fontName => "", fontStyle => "0", fontSize => "", colorStyle => '0', },
    { name => "REGEX MATCH"                  , styleID => "17", fgColor => "8080FF", bgColor => "F8FEDE", fontName => "", fontStyle => "0", fontSize => "", colorStyle => '0', },
    { name => "REGEX SUBSTITUTION"           , styleID => "18", fgColor => "8080C0", bgColor => "FFEEEC", fontName => "", fontStyle => "0", fontSize => "", colorStyle => '0', },
    { name => "TRANSLATION"                  , styleID => "44", fgColor => "8080C0", bgColor => "FFEEEC", fontName => "", fontStyle => "0", fontSize => "", colorStyle => '0', },
    { name => "HEREDOC DELIMITER"            , styleID => "22", fgColor => "550055", bgColor => "EEEEFF", fontName => "", fontStyle => "1", fontSize => "", colorStyle => '0', },
    { name => "HEREDOC SINGLEQUOTE"          , styleID => "23", fgColor => "7F007F", bgColor => "EEEEFF", fontName => "", fontStyle => "2", fontSize => "", colorStyle => '0', },
    { name => "HEREDOC DOUBLEQUOTE"          , styleID => "24", fgColor => "7F007F", bgColor => "EEEEFF", fontName => "", fontStyle => "0", fontSize => "", colorStyle => '0', },
    { name => "HEREDOC BACKTICK"             , styleID => "25", fgColor => "8000FF", bgColor => "FFEEEC", fontName => "", fontStyle => "0", fontSize => "", colorStyle => '0', },
    { name => "VAR IN STRING"                , styleID => "43", fgColor => "808080", bgColor => "FFFFFF", fontName => "", fontStyle => "3", fontSize => "", colorStyle => '0', },
    { name => "VAR IN REGEX"                 , styleID => "54", fgColor => "8080FF", bgColor => "F8FEDE", fontName => "", fontStyle => "3", fontSize => "", colorStyle => '0', },
    { name => "VAR IN REGEX SUBSTITUTION"    , styleID => "55", fgColor => "8080C0", bgColor => "FFEEEC", fontName => "", fontStyle => "3", fontSize => "", colorStyle => '0', },
    { name => "VAR IN BACKTICKS"             , styleID => "57", fgColor => "FFFF00", bgColor => "808080", fontName => "", fontStyle => "3", fontSize => "", colorStyle => '0', },
    { name => "VAR IN HEREDOC DOUBLEQUOTE"   , styleID => "61", fgColor => "7F007F", bgColor => "EEEEFF", fontName => "", fontStyle => "3", fontSize => "", colorStyle => '0', },
    { name => "VAR IN HEREDOC BACKTICK"      , styleID => "62", fgColor => "8000FF", bgColor => "FFEEEC", fontName => "", fontStyle => "3", fontSize => "", colorStyle => '0', },
    { name => "VAR IN STRING QQ"             , styleID => "64", fgColor => "804080", bgColor => "FFFFFF", fontName => "", fontStyle => "3", fontSize => "", colorStyle => '0', },
    { name => "VAR IN STRING QX"             , styleID => "65", fgColor => "8000FF", bgColor => "FFEEEC", fontName => "", fontStyle => "3", fontSize => "", colorStyle => '0', },
    { name => "VAR IN STRING QR"             , styleID => "66", fgColor => "8080FF", bgColor => "F8FEDE", fontName => "", fontStyle => "3", fontSize => "", colorStyle => '0', },
    { name => "FORMAT IDENTIFIER"            , styleID => "41", fgColor => "C000C0", bgColor => "FFFFFF", fontName => "", fontStyle => "2", fontSize => "", colorStyle => '0', },
    { name => "FORMAT BODY"                  , styleID => "42", fgColor => "C000C0", bgColor => "FFF0FF", fontName => "", fontStyle => "0", fontSize => "", colorStyle => '0', },
    { name => "DATA SECTION"                 , styleID => "21", fgColor => "808080", bgColor => "FFFFFF", fontName => "", fontStyle => "0", fontSize => "", colorStyle => '0', },
    { name => "POD"                          , styleID => "3", fgColor => "000000", bgColor => "FFFFFF", fontName => "", fontStyle => "0", fontSize => "", colorStyle => '0', },
    { name => "POD VERBATIM"                 , styleID => "31", fgColor => "004000", bgColor => "EEFFEE", fontName => "", fontStyle => "0", fontSize => "", colorStyle => '0', },
    { name => "SYNTAX ERROR"                 , styleID => "1", fgColor => "FF80C0", bgColor => "FFFFFF", fontName => "", fontStyle => "3", fontSize => "", colorStyle => '0', },
);
my %row;
for my $r ( 0 .. $#list ) {
    my $id = $list[$r]{styleID};
    $row{$id} = $r;
}
@row{qw/8 9 19/} = (-1,-1,-1);

# print join(", ", map { sprintf '%02d', $_       } sort { $row{$a} <=> $row{$b} } keys(%row)), "\n";
# print join(", ", map { sprintf '%02d', $row{$_} } sort { $row{$a} <=> $row{$b} } keys(%row)), "\n";
# exit;

while(<>) {
    state $within;
    state $group;
    if( m{<LexerType\b.*?\bname="perl".*?>} ) {
        $within = 1;
        $group = '';
        next;
    }
    if( $within && m{</LexerType>} ) {
        for my $r (0 .. $#list ) {
            printf qq(            %s ), '<WordsStyle';
            for my $key ( qw/name styleID fgColor bgColor fontName fontStyle fontSize colorStyle keywordClass/ ) {
                printf qq(%s="%s" ), $key, $list[$r]{$key} if exists $list[$r]{$key};
            }
            if(defined $list[$r]{content}) {
                printf qq(>%s</WordsStyle>\n), $list[$r]{content};
            } else {
                printf qq(%s\n), '/>';
            }
        }
        undef $within;
        undef $group;
    }
    next unless $within;

    my ($name) = m{<WordsStyle.*\bname\h*=\h*"([^">]*)"}    or die "name is required";
    my ($id)   = m{<WordsStyle.*\bstyleID\h*=\h*"([^">]*)"} or die "styleID is required";
    my ($r)    = exists($row{$id}) ? $row{$id} : die "invalid ID:'$id'";
    my ($fg)   = m{<WordsStyle.*\bfgColor\h*=\h*"([^">]*)"};
    my ($bg)   = m{<WordsStyle.*\bbgColor\h*=\h*"([^">]*)"};
    my ($fn)   = m{<WordsStyle.*\bfontName\h*=\h*"([^">]*)"};
    my ($fs)   = m{<WordsStyle.*\bfontStyle\h*=\h*"([^">]*)"};
    my ($fz)   = m{<WordsStyle.*\bfontSize\h*=\h*"([^">]*)"};
    my ($cs)   = m{<WordsStyle.*\bcolorStyle\h*=\h*"([^">]*)"};
    my ($kc)   = m{<WordsStyle.*\bkeywordClass\h*=\h*"([^">]*)"};
    my ($content) = m{>([^<]+)</WordsStyle>};

    $_ = '';    # don't print (yet) when $within...
    next if $r < 0;  # remove 8=PUNCTUATION 9=PREPROCESSOR 19=LONGQUOTE

    $list[$r]{name}         = $name // $list[$r]{name};
    $list[$r]{fgColor}      = $fg   // $list[$r]{fgColor};
    $list[$r]{bgColor}      = $bg   // $list[$r]{bgColor};
    $list[$r]{fontName}     = $fn   // $list[$r]{fontName};
    $list[$r]{fontStyle}    = $fz   // $list[$r]{fontStyle};
    $list[$r]{fontSize}     = $fz   // $list[$r]{fontSize};
    $list[$r]{colorStyle}   = $cs;                               delete $list[$r]{colorStyle} unless defined $cs;
    $list[$r]{keywordClass} = $kc   // $list[$r]{keywordClass};  delete $list[$r]{keywordClass} unless defined $list[$r]{keywordClass};
    $list[$r]{content}      = $content;

} continue {
    print;
    close ARGV if eof;  # reset $.
}
