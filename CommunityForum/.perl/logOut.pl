#!perl
# this is a copy of the original example, but it's going to use the library, instead
#
# https://github.com/pryrt/nppStuff/blob/main/CommunityForum/API%20Access.md
# https://docs.nodebb.org/api/write
# https://docs.nodebb.org/api/read

use 5.014; # strict, //, s//r
use warnings;
use HTTP::Tiny;
use Data::Dump;
use JSON;
use POSIX qw/fmod/;
use open ':std', ':encoding(UTF-8)';
use lib './lib';
use Win32::Mechanize::NppCommunity;
$| = 1;

my $comm = Win32::Mechanize::NppCommunity::->new(
    exists $ENV{NPPCOMM_TOKEN} ? (env => 'NPPCOMM_TOKEN') :
           -f '~$token' ? (file => '~$token') :
           (unknown => 'token')
);
my $client = $comm->client();

dd $comm->logoutUser('PeterJones');
dd $comm->logoutUser('not-peter-jones');
