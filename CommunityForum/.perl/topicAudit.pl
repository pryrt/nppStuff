#!perl
# topicAudit:
#   check topics:
#       if topic is deleted, check to see if any of its posts need to be deleted [TODO: then delete them]
#       if topic undeleted, check if all its posts already deleted [TODO: then delete it]
#
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

# ugh: unfortunately, the /api/recent or /api/top or /api/popular all limit to 10 pages (200 topics),
#   so I am not sure how to actually loop through all.
# Still, this is enough to find a couple deleted topics that have undeleted posts
sub auditThisTopic {
    my ($topic) = @_;
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
    if($topic->{deleted}) {
        my $postsToPurge = [];
        for my $post (@$posts) {
            if(! $post->{deleted}) {
                $str .= sprintf "        - %-37.37s | %-8d by %-8d: %-32.32s | \n",
                    "TO PURGE POST",
                    $post->{pid},
                    $post->{uid},
                    $post->{timestampISO},
                    ;

                push @$postsToPurge, $post->{pid};
            } else {
                $str .= sprintf "        - %-37.37s | %-8d by %-8d: %-32.32s\n",
                    "TO PURGE PREVIOUSLY-DELETED POST",
                    $post->{pid},
                    $post->{uid},
                    $post->{timestampISO},
                    ;

                push @$postsToPurge, $post->{pid};
            }
        }
        if(@$postsToPurge) {
            #++$counter;
            for my $pid ( reverse @$postsToPurge )  {      # cannot purge first post in topic unless all others deleted, so go in reverse order
                # now permanently delete each post
                eval { $comm->purgePost($pid) unless $gDoDryRun; 1 } or do { warn "PURGE DELETED TOPIC'S POSTS:", $@; };
            }
        }
        $str .= "        - TO PURGE TOPIC\n";
        print $str;
        # ... and purge the topic
        eval { $comm->purgeTopic($topic->{tid}) unless $gDoDryRun or @$postsToPurge; 1 } or do { warn "PURGE DELETED TOPIC:", $@; };
    } else {
        my $undeletedCount = 0;
        for my $post (@$posts) {
            $undeletedCount++ if !$post->{deleted};
        }
        $str .= sprintf "        - %-37.37s | postcount: %d, array size: %d, undeleted: %d\t\t\n",
            "TO PURGE ALREADY-EMPTY TOPIC",
            $topic->{postcount},
            scalar @$posts,
            $undeletedCount;
        if(!$undeletedCount) {
            print $str;
            ++$counter;

            # ... and purge the empty topic
            eval { $comm->purgeTopic($topic->{tid}) unless $gDoDryRun; 1 } or do { warn "PURGE ALREADY-EMPTY TOPIC:", $@; };
        }
    }

    return 1;# if $counter < 5;
}

#$comm->forAllTopicsInCategoryDo(3,\&auditThisTopic);

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
