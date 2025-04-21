#!perl

# https://github.com/pryrt/nppStuff/blob/main/CommunityForum/API%20Access.md
# https://docs.nodebb.org/api/write
# https://docs.nodebb.org/api/read

use 5.014; # strict, //, s//r
use warnings;
use HTTP::Tiny;
use Data::Dump;
use JSON;
use open ':std', ':encoding(UTF-8)';
$| = 1;

my $token = do { local $\; open my $fh, '<', '~$token'; <$fh> };

my $client = HTTP::Tiny->new(
    default_headers => {
        'Content-Type' => 'application/json',
        'Accept' => 'application/json',
        'Authorization' => "Bearer $token",
    },
);

my $response = $client->get('https://community.notepad-plus-plus.org/api/users?section=joindate');
die "$response->{status} $response->{reason}" unless $response->{success};
print "$response->{url}\n\t$response->{status} $response->{reason}\n";
#print $response->{content} if length $response->{content};
my $data = decode_json $response->{content};
#print "KEYS => ", join(" ", sort keys %$data), "\n";
#dd { "pagination" => $data->{pagination} } if exists $data->{pagination};
my $lastpage = $data->{pagination}{last}{page};
print "\n\n";

for my $page (reverse 1 .. $lastpage) {
    my $response = $client->get('https://community.notepad-plus-plus.org/api/users?section=joindate&page='.$page);
    die "$response->{status} $response->{reason}" unless $response->{success};
    #print "$response->{url}\n\t$response->{status} $response->{reason}\n";
    my $data = decode_json $response->{content};
    #print "KEYS => ", join(" ", sort keys %$data), "\n";
    my $users = $data->{users};
    #print "\tnUSERS => ", scalar @$users, "\n";
    #print "\tUSER KEYS => ", join(" ", sort keys %{$users->[0]}), "\n";
    for my $user ( reverse @$users ) {
        next if $user->{postcount};
        my $activity = abs($user->{lastonline} - $user->{joindate});
        next if $activity > 86400;
        printf "- %-8d %-30.30s: %-32.32s %-15.15s => %d\n", $user->{uid}, $user->{username}, $user->{lastonlineISO}, $activity, $user->{postcount};
    }
    #print "nUSERS => ", scalar(keys %$users), "\n";
    #dd { "pagination" => $data->{pagination} } if exists $data->{pagination};
    #print "\n";
}
