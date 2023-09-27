#!perl -l

use 5.014; # strict, //, s//r
use warnings;

sub this_is_my_sub { ... };

sub mypush (\@@) { ... };

sub mypushy :prototype(\@@)  { ... };

print for my $var = 5;
print for my $squot = 'Here: $var not interpolated';
print for my $dquot = "Where: $var yikes\n";
print for my $backtk = `cmd.exe /c echo $var to me`;
print for my $qstr = q(here $var not interpolated);
print for my $qqstr = qq(here $var there);
print for my $qxstr = qx(cmd.exe /c echo $var to me);
print for my @array = qw/one two three/;
print for my @array2 = ('one', 'two', "three");
print for my %hash = ( key => 'value', another => 'string');
print for my $re = qr/regex with $var embedded/i;
print for "hello" =~ m/this $var here/;
print for "hello" =~ s/this $var her/and $var there/r;
print for "hello" =~ y/one $var one/one $var one/;
print my $x = ("5" x int(5)) . "string";
if( -s $0 ) { print "-X are instruction words, even though they aren't in the list\n" }

print for my $hdnoquote = <<EOF;
This is a noquote heredoc with embedded $var
EOF

print for my $hdsingleq = <<'EOF';
This is a singlequote heredoc with embedded $var not interpolated
EOF

print for my $hddoubleq = <<"EOF";
This is a doublequote heredoc with embedded $var
EOF

print for my $hdbacktick = <<`EOF`;
cmd.exe /c echo This is a backtick heredoc with embedded $var for me
EOF

print for my $hdindent = <<~"EOF";
    This is indented
    EOF

=begin

this is pod

    with indentation verbatim text

=cut

#### This is a format

format Something =
    Test: @<<<<<<<< @||||| @>>>>>
          $str,     $%,    '$' . int($num)
.

$str = "widget";
$num = $cost/$quantity;
$~ = 'Something';
write;