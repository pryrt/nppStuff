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

$comm->forAllUsersDo(sub {
    my ($user) = @_;
    state $counter = 0;
    if($user->{banned}) {
        printf "* %-8d %-30.30s: post:%-4d b:%d bexpire:%-16d until:%-16d readable:%s\n",
            $user->{uid},
            $user->{username},
            $user->{postcount},
            $user->{banned},
            $user->{'banned:expire'},
            $user->{banned_until},
            $user->{banned_until_readable},

            if  abs(scalar(time) - $user->{lastonline}/1000) > 86400*365
            ;
    }
    return 0 if $user->{postcount} or $user->{banned};
    # {lastonline} and {joindate} are in millisec-based epoch time; perl and I expect second-based, so div-1000
    my $activity = abs($user->{lastonline} - $user->{joindate})/1000;
    return 0 if $activity > 86400;
    my $age = abs(scalar(time) - $user->{lastonline}/1000);
    return 0 if $age < 86400*365;
    my $min = fmod($age/60, 60);
    my $hrs = fmod($age/60/60, 24);
    my $dys = fmod($age/60/60/24,365);
    my $yrs = ($age/60/60/24/365);
    printf "- %-8d %-30.30s: %-32.32s activeTime:%-15.15s posts:%d banned:%d age:%dyrs %02ddys %02d:%05.2f\n",
        $user->{uid},
        $user->{username},
        $user->{lastonlineISO},
        $activity,
        $user->{postcount},
        $user->{banned},
        #$age,
        $yrs, $dys, $hrs, $min,
        ;
    eval { $comm->deleteUserAndContent($user->{uid}); 1 } or do {
        warn "deleteUserAndContent ERROR: ", $@;
    };
    #return 1 if ++$counter < 100;   # only delete 100 users per run
    return 1;
});
