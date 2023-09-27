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
print my $x = ("5" x int(5)) . "string";


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


__END__

            <WordsStyle name="DEFAULT"                      styleID="0" fgColor="FF0000" bgColor="FFFFFF" fontName="" fontStyle="0" fontSize="" />
            <WordsStyle name="INSTRUCTION WORD"             styleID="5" fgColor="0000FF" bgColor="FFFFFF" fontName="" fontStyle="1" fontSize="" keywordClass="instre1">carp croak</WordsStyle>
            <WordsStyle name="NUMBER"                       styleID="4" fgColor="FF0000" bgColor="FFFFFF" fontName="" fontStyle="0" fontSize="" />
            <WordsStyle name="OPERATOR"                     styleID="10" fgColor="000080" bgColor="FFFFFF" fontName="" fontStyle="1" fontSize="" />
            <WordsStyle name="IDENTIFIER"                   styleID="11" fgColor="004080" bgColor="FFFFFF" fontName="" fontStyle="0" fontSize="" />
            <WordsStyle name="SCALAR"                       styleID="12" fgColor="FF8000" bgColor="FFFFFF" fontName="" fontStyle="0" fontSize="" />
            <WordsStyle name="ARRAY"                        styleID="13" fgColor="CF34CF" bgColor="FFFFFF" fontName="" fontStyle="0" fontSize="" />
            <WordsStyle name="HASH"                         styleID="14" fgColor="8080C0" bgColor="FFFFFF" fontName="" fontStyle="0" fontSize="" />
            <WordsStyle name="SYMBOL TABLE"                 styleID="15" fgColor="FF0000" bgColor="FFFFFF" fontName="" fontStyle="1" fontSize="" />
            <WordsStyle name="PROTOTYPE"                    styleID="40" fgColor="000080" bgColor="FFFFFF" fontName="" fontStyle="1" fontSize="" />
            <WordsStyle name="COMMENT LINE"                 styleID="2" fgColor="008000" bgColor="FFFFFF" fontName="" fontStyle="0" fontSize="" />
            <WordsStyle name="STRING SINGLEQUOTE"           styleID="7" fgColor="808080" bgColor="FFFFFF" fontName="" fontStyle="2" fontSize="" />
            <WordsStyle name="STRING DOUBLEQUOTE"           styleID="6" fgColor="808080" bgColor="FFFFFF" fontName="" fontStyle="0" fontSize="" />
            <WordsStyle name="STRING BACKTICKS"             styleID="20" fgColor="FFFF00" bgColor="808080" fontName="" fontStyle="1" fontSize="" />
            <WordsStyle name="STRING q()"                   styleID="26" fgColor="804080" bgColor="FFFFFF" fontName="" fontStyle="2" fontSize="" />
            <WordsStyle name="STRING qq()"                  styleID="27" fgColor="804080" bgColor="FFFFFF" fontName="" fontStyle="0" fontSize="" />
            <WordsStyle name="STRING qx()"                  styleID="28" fgColor="8000FF" bgColor="FFEEEC" fontName="" fontStyle="0" fontSize="" />
            <WordsStyle name="STRING qr()"                  styleID="29" fgColor="8080FF" bgColor="F8FEDE" fontName="" fontStyle="0" fontSize="" />
            <WordsStyle name="STRING qw()"                  styleID="30" fgColor="CF34CF" bgColor="FFFFFF" fontName="" fontStyle="0" fontSize="" />
            <WordsStyle name="REGEX MATCH"                  styleID="17" fgColor="8080FF" bgColor="F8FEDE" fontName="" fontStyle="0" fontSize="" />
            <WordsStyle name="REGEX SUBSTITUTION"           styleID="18" fgColor="8080C0" bgColor="FFEEEC" fontName="" fontStyle="0" fontSize="" />
            <WordsStyle name="TRANSLATION"                  styleID="44" fgColor="8080C0" bgColor="FFEEEC" fontName="" fontStyle="4" fontSize="" />
            <WordsStyle name="HEREDOC DELIMITER"            styleID="22" fgColor="550055" bgColor="EEEEFF" fontName="" fontStyle="1" fontSize="" />
            <WordsStyle name="HEREDOC SINGLEQUOTE"          styleID="23" fgColor="7F007F" bgColor="EEEEFF" fontName="" fontStyle="2" fontSize="" />
            <WordsStyle name="HEREDOC DOUBLEQUOTE"          styleID="24" fgColor="7F007F" bgColor="EEEEFF" fontName="" fontStyle="0" fontSize="" />
            <WordsStyle name="HEREDOC BACKTICK"             styleID="25" fgColor="8000FF" bgColor="FFEEEC" fontName="" fontStyle="0" fontSize="" />
            <WordsStyle name="VAR IN STRING"                styleID="43" fgColor="808080" bgColor="FFFFFF" fontName="" fontStyle="3" fontSize="" />
            <WordsStyle name="VAR IN REGEX"                 styleID="54" fgColor="8080FF" bgColor="F8FEDE" fontName="" fontStyle="3" fontSize="" />
            <WordsStyle name="VAR IN REGEX SUBSTITUTION"    styleID="55" fgColor="8080C0" bgColor="FFEEEC" fontName="" fontStyle="3" fontSize="" />
            <WordsStyle name="VAR IN BACKTICKS"             styleID="57" fgColor="FFCC00" bgColor="808080" fontName="" fontStyle="2" fontSize="" />
            <WordsStyle name="VAR IN HEREDOC DOUBLEQUOTE"   styleID="61" fgColor="7F007F" bgColor="EEEEFF" fontName="" fontStyle="3" fontSize="" />
            <WordsStyle name="VAR IN HEREDOC BACKTICK"      styleID="62" fgColor="8000FF" bgColor="FFEEEC" fontName="" fontStyle="3" fontSize="" />
            <WordsStyle name="VAR IN STRING QQ"             styleID="64" fgColor="804080" bgColor="FFFFFF" fontName="" fontStyle="3" fontSize="" />
            <WordsStyle name="VAR IN STRING QX"             styleID="65" fgColor="D00000" bgColor="FFEEEC" fontName="" fontStyle="6" fontSize="" />
            <WordsStyle name="VAR IN STRING QR"             styleID="66" fgColor="8080FF" bgColor="F8FEDE" fontName="" fontStyle="3" fontSize="" />
            <WordsStyle name="FORMAT IDENTIFIER"            styleID="41" fgColor="C000C0" bgColor="FFFFFF" fontName="" fontStyle="6" fontSize="" />
            <WordsStyle name="FORMAT BODY"                  styleID="42" fgColor="C000C0" bgColor="FFF0FF" fontName="" fontStyle="4" fontSize="" />
            <WordsStyle name="DATA SECTION"                 styleID="21" fgColor="808080" bgColor="FFFFFF" fontName="" fontStyle="0" fontSize="" />
            <WordsStyle name="POD"                          styleID="3" fgColor="000000" bgColor="FFFFFF" fontName="" fontStyle="0" fontSize="" />
            <WordsStyle name="POD VERBATIM"                 styleID="31" fgColor="004000" bgColor="EEFFEE" fontName="" fontStyle="0" fontSize="" />
            <WordsStyle name="SYNTAX ERROR"                 styleID="1" fgColor="FF80C0" bgColor="FFFFFF" fontName="" fontStyle="3" fontSize="" />

For me:
    STRING BACKTICKS = 8000FF / FFEEEC      style=1
    VAR IN BACKTICKS = D00000 / FFEEEC      style=3

__END__

<Keywords name="instre1">
ADJUST
ARGV
AUTOLOAD
Accept
BEGIN
Balloon
Button
CHECK
CORE
DATA
DESTROY
END
Entry
Frame
INIT
Label
MainLoop
Radiobutton
STDERR
STDIN
STDOUT
SUPER
Tr
UNITCHECK
UNIVERSAL
__DATA__
__END__
__FILE__
__LINE__
__PACKAGE__
__SUB__
abs
accept
address
alarm
and
atan2
attach
attributes
auth_type
autoEscape
autodie
autouse
base
bigfloat
bigint
bignum
bigrat
bind
binmode
bless
blib
br
break
builtin
button
bytes
caller
caption
catch
charnames
chdir
checkbox
checkbox_group
chmod
chomp
chop
chown
chr
chroot
close
closedir
cmp
compile
configure
connect
constant
continue
cookie
cos
crypt
dbmclose
dbmopen
default
defaults
defer
defined
deiconify
delete
delete_all
deprecate
diagnostics
die
div
do
dump
each
else
elseif
elsif
em
encoding
end
end_h1
end_html
end_table
end_ul
endform
endgrent
endhostent
endif
endnetent
endprotoent
endpwent
endservent
eof
eq
escape
escape_HTML
eval
evalbytes
exec
exists
exit
exp
experimental
fc
fcntl
feature
field
fields
filefield
fileno
filetest
finally
flock
font
for
foreach
fork
format
formline
ge
geometry
getc
getgrent
getgrgid
getgrnam
getgrname
gethostbyaddr
gethostbyname
gethostent
getlogin
getnetbyaddr
getnetbyname
getnetent
getpeername
getpgrp
getppid
getpriority
getprotobyname
getprotobynumber
getprotoent
getpwent
getpwnam
getpwuid
getservbyname
getservbyport
getservent
getsockname
getsockopt
given
glob
gmtime
goto
grep
groove
gt
h1
h2
h3
h4
h5
header
hex
hidden
hr
http
https
if
image_button
img
import
index
insert
int
integer
ioctl
isa
isindex
join
keys
kill
last
lc
lcfirst
le
length
less
li
lib
link
listen
local
locale
localtime
lock
log
lstat
lt
map
maxsize
meta_notation
method
minsize
mkdir
mro
msgctl
msgget
msgrcv
msgsnd
multipart_end
multipart_init
multipart_start
my
ne
next
no
not
oct
ok
ol
open
opendir
ops
or
ord
our
overload
overloading
pack
package
param
param_fetch
parent
password_field
path_info
perlfaq
pipe
pop
popup_menu
pos
pre
precision,
print
printf
prototype
push
qq
query_string
quotemeta
qw
qx
radio_group
raise
rand
raw_cookie
re
read
readdir
readline
readlink
readpipe
recv
redirect
redo
ref
referer
remote_addr
remote_host
remote_indent
remote_user
rename
request_method
require
reset
resizable
return
reverse
rewinddir
rindex
rmdir
say
scalar
script_name
scrolling_list
seek
seekdir
select
self_url
semctl
semget
semop
send
server_name
server_port
server_software
set
setgrent
sethostent
setnetent
setpgrp
setpriority
setprotoent
setpwent
setservent
setsockopt
shift
shmctl
shmget
shmread
shmwrite
shutdown
sigtrap
sin
sleep
socket
socketpair
sort
span
splice
split
sprintf
sqrt
srand
stable
start_form
start_h1
start_html
start_multipart_form
start_table
start_ul
startform
stat
state
strict
strong
study
sub
submit
subs
substr
symlink
syscall
sysopen
sysread
sysseek
system
syswrite
table
tagConfigure
td
tell
telldir
textarea
textfield
th
threads
tie
tied
time
times
title
tmpFileName
top
tr
truncate
try
uc
ucfirst
ul
umask
undef
unescape
unescapeHTML
unless
unlink
unpack
unshift
untie
until
update
upload
uploadInfo
url
url_param
use
use_named_parameters
user_agent
user_name
utf8
utime
values
variable
vars
vec
version
virtual_host
vmsish
wait
waitpid
wantarray
warn
warnings
when
while
width
write
x
xor
</Keywords>
