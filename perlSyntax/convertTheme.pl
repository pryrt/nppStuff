#!perl

use 5.014; # strict, //, s//r
use warnings;
use autodie;

$| = 1;
my @list = (
    { name => "DEFAULT"                      , styleID => "0" },
    { name => "INSTRUCTION WORD"             , styleID => "5" },
    { name => "NUMBER"                       , styleID => "4" },
    { name => "OPERATOR"                     , styleID => "10" },
    { name => "IDENTIFIER"                   , styleID => "11", fontName => "", fontStyle => "1", fontSize => "" },
    { name => "SCALAR"                       , styleID => "12" },
    { name => "ARRAY"                        , styleID => "13" },
    { name => "HASH"                         , styleID => "14" },
    { name => "SYMBOL TABLE"                 , styleID => "15" },
    { name => "PROTOTYPE"                    , styleID => "40", fontName => "", fontStyle => "1", fontSize => "" },
    { name => "COMMENT LINE"                 , styleID => "2" },
    { name => "STRING SINGLEQUOTE"           , styleID => "7" },
    { name => "STRING DOUBLEQUOTE"           , styleID => "6" },
    { name => "STRING BACKTICKS"             , styleID => "20" },
    { name => "STRING Q"                     , styleID => "26", fontName => "", fontStyle => "2", fontSize => "" },
    { name => "STRING QQ"                    , styleID => "27", fontName => "", fontStyle => "0", fontSize => "" },
    { name => "STRING QX"                    , styleID => "28", fontName => "", fontStyle => "0", fontSize => "" },
    { name => "STRING QR"                    , styleID => "29", fontName => "", fontStyle => "0", fontSize => "" },
    { name => "STRING QW"                    , styleID => "30", fontName => "", fontStyle => "0", fontSize => "" },
    { name => "REGEX MATCH"                  , styleID => "17" },
    { name => "REGEX SUBSTITUTION"           , styleID => "18" },
    { name => "TRANSLATION"                  , styleID => "44", fontName => "", fontStyle => "0", fontSize => "" },
    { name => "HEREDOC DELIMITER"            , styleID => "22", fontName => "", fontStyle => "1", fontSize => "" },
    { name => "HEREDOC SINGLEQUOTE"          , styleID => "23", fontName => "", fontStyle => "2", fontSize => "" },
    { name => "HEREDOC DOUBLEQUOTE"          , styleID => "24", fontName => "", fontStyle => "0", fontSize => "" },
    { name => "HEREDOC BACKTICK"             , styleID => "25", fontName => "", fontStyle => "0", fontSize => "" },
    { name => "VAR IN STRING"                , styleID => "43", fontName => "", fontStyle => "3", fontSize => "" },
    { name => "VAR IN REGEX"                 , styleID => "54", fontName => "", fontStyle => "3", fontSize => "" },
    { name => "VAR IN REGEX SUBSTITUTION"    , styleID => "55", fontName => "", fontStyle => "3", fontSize => "" },
    { name => "VAR IN BACKTICKS"             , styleID => "57", fontName => "", fontStyle => "3", fontSize => "" },
    { name => "VAR IN HEREDOC DOUBLEQUOTE"   , styleID => "61", fontName => "", fontStyle => "3", fontSize => "" },
    { name => "VAR IN HEREDOC BACKTICK"      , styleID => "62", fontName => "", fontStyle => "3", fontSize => "" },
    { name => "VAR IN STRING QQ"             , styleID => "64", fontName => "", fontStyle => "3", fontSize => "" },
    { name => "VAR IN STRING QX"             , styleID => "65", fontName => "", fontStyle => "3", fontSize => "" },
    { name => "VAR IN STRING QR"             , styleID => "66", fontName => "", fontStyle => "3", fontSize => "" },
    { name => "FORMAT IDENTIFIER"            , styleID => "41", fontName => "", fontStyle => "2", fontSize => "" },
    { name => "FORMAT BODY"                  , styleID => "42", fontName => "", fontStyle => "0", fontSize => "" },
    { name => "DATA SECTION"                 , styleID => "21" },
    { name => "POD"                          , styleID => "3" },
    { name => "POD VERBATIM"                 , styleID => "31", fontName => "", fontStyle => "0", fontSize => "" },
    { name => "ERROR"                        , styleID => "1" },
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

my %defaults = ();

sub set_defaults {
    my ($fname) = @_;
    my $rethref = {};
    open my $fh, '<', $fname;
    while(<$fh>) {
        next unless m{(?-s)<WidgetStyle.*?styleID="32".*?/>};
        print STDERR "For $fname, found $_";
        if( m{fgColor\h*=\h*"(\w+)"} ) { $rethref->{fgColor} = $1; };
        if( m{bgColor\h*=\h*"(\w+)"} ) { $rethref->{bgColor} = $1; };
    }
    return $rethref;
}

if(@ARGV) {
    for my $fn (@ARGV) {
        $defaults{$fn} = set_defaults($fn);
    }
}

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
            if(exists $defaults{$ARGV}) {
                for my $key (qw/fgColor bgColor/) {
                    next if $list[$r]{styleID}<=21 and defined($list[$r]{$key});
                    if(exists $defaults{$ARGV}{$key}) { $list[$r]{$key} = $defaults{$ARGV}{$key}; }
                }
            }

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

    #$list[$r]{name}         = $name // $list[$r]{name}; # use the new name no matter what
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
