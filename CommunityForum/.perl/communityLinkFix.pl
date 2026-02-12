#!perl
# communityLinkFix: I have found ~500 https://notepad-plus-plus/community/... links,
#   which all need to be changed to https://community.notepad-plus-plus/...
#
# References:
# https://github.com/pryrt/nppStuff/blob/main/CommunityForum/API%20Access.md
# https://docs.nodebb.org/api/write
# https://docs.nodebb.org/api/read

use 5.014; # strict, //, s//r
use warnings;
use HTTP::Tiny;
use Data::Dump();
use JSON;
use open ':std', ':encoding(UTF-8)';
use lib './lib';
use Win32::Mechanize::NppCommunity;
$| = 1;

#my $comm = Win32::Mechanize::NppCommunity::->new(file => '~$token');
my $comm = Win32::Mechanize::NppCommunity::->new(
    exists $ENV{NPPCOMM_TOKEN} ? (env => 'NPPCOMM_TOKEN') :
       -f '~$token' ? (file => '~$token') :
       (unknown => 'token')
);
my $client = $comm->client();

our $gDoDryRun = 0;

$comm->forAllCategoriesDo(sub {
    my ($category) = @_;
    printf "Category %2d: \"%s\": topic_count:%d vs totalTopicCount:%d, with post_count:%d\n",
        $category->{cid},
        $category->{name},
        $category->{topic_count},
        $category->{totalTopicCount},
        $category->{post_count},
        ;
    $comm->forAllTopicsInCategoryDo($category->{cid},\&auditThisTopic);
    return 1;
});

## returning undef will stop the loop early; returning 0 or 1 will continue, but I can
##  use that for other checking

sub auditThisTopic {
    my ($topic) = @_;
    return 0 if $topic->{deleted};
    return 0 if $topic->{tid} == 18264; # this topic is talking about the redirect, so I don't want to include those
    state $counter = 0;
    my $str = sprintf "    - %-8d %-30.30s: %-32.32s %-32.32s => posts:%d | topic-deleted:%s\n",
        $topic->{tid},
        $topic->{title},
        $topic->{timestampISO},
        $topic->{lastposttimeISO},
        $topic->{postcount},
        $topic->{deleted},
        ;
    my $posts = $comm->getTopicDetails($topic->{tid})->{posts};
    my $count = 0;
    for my $post (@$posts) {
        if( $post->{content} =~ m{notepad-plus-plus.org/community}) {
            $str .= sprintf "        - %-37.37s | %-8d by %-8d: %-32.32s | tid:%-8d\n",
                "TO FIX MATCHING POST",
                $post->{pid},
                $post->{uid},
                $post->{timestampISO},
                $post->{tid},
                ;

            #$str .= "\n" . Data::Dump::pp({post => $post});
            $count++;
        }
    }
    if($count) {
        print $str;
        return 1;
    }
    return 0;
}
