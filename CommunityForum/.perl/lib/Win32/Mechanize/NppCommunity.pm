package Win32::Mechanize::NppCommunity;
use 5.014;              # strict, //, s//r
use warnings;
use JSON();
use Exporter 5.57 'import';
our $VERSION = '0.001'; # rrr.mmmsss : rrr is major revision; mmm is minor revision; sss is sub-revision (new feature path or bugfix); optionally use _sss instead, for alpha sub-releases
our @EXPORT = ();


# https://github.com/pryrt/nppStuff/blob/main/CommunityForum/API%20Access.md
# https://docs.nodebb.org/api/write
# https://docs.nodebb.org/api/read
=pod

=encoding utf8

=head1 NAME

Win32::Mechnize::NppCommunity - Automate Admin/Moderator tasks for the Notepad++ Community Forum

=head1 CONSTRUCTORS

=over

=item new

    my $community = Win32::Mechnize::NppCommunity::->new(file => $tokenFile);
    my $community = Win32::Mechnize::NppCommunity::->new(env => $envVarName);

Creates the new NppCommunity object, and initializes the HTTP client for the REST API

=back

=cut

sub new
{
    my ( $class, %args ) = @_;
    my $self = bless {}, $class;

    my $token;
    if( exists($args{file})) {
        $args{file} //= './~$token';    # default
        if ( !-f $args{file} ) {
            die "Could not find token in '$args{file}'";
        } else {
            open my $fh, '<', $args{file};
            chomp($token = <$fh>);
        }
    } elsif (exists $args{env}) {
        die "Could not find ENV{$args{env}}" unless exists $ENV{$args{env}};
        $token = $ENV{$args{env}};
    } else {
        die "Must specify a token through the file or env argument";
    }

    $self->{_client} = HTTP::Tiny->new(
        default_headers => {
            'Content-Type' => 'application/json',
            'Accept' => 'application/json',
            'Authorization' => "Bearer $token",
        },
    );

    $self->login();

    return $self;
}

=head1 METHODS

=over

=item client

    $community->client()->get(...); # sends a GET request using the HTTP client

Gives direct access to the HTTP client.  (Allows extending for when there isn't a method defined for a given action)

=cut

sub client { $_[0]->{_client}; }

=item login

    $community->client()->login();  # verifies you can log in

Verifies you can log in.  Actually run by C<-E<gt>new()> as well.

=cut

sub login
{
    my ($self) = @_;
    my $response = $self->client()->get('https://community.notepad-plus-plus.org/api/login');
    die "$response->{status} $response->{reason}" unless $response->{success};
    my $data = ($response->{headers}{'content-type'} =~ /json/) ?
        JSON::decode_json($response->{content}) :
        $response->{content};
    if(ref $data) {
        die "Does not appear to have logged in correctly.  Check your API token."
    }
    return $data;
}

=item forAllUsersDo

    $community->forAllUsersDo(sub {
        my ($user) = @_;
        return 0 if ...; # return 0 if you want to skip the action on this user
        return 1 if ...; # return 1 if you performed the action on this user
        return undef;    # return undef if you want to stop processing any more users
    });


Runs a subroutine for each user.  The subroutine needs to take in the L<$user> object
as the first argument.  It should return a true value if the action was performed for the user;
it should return 0 or "" if the action was skipped for the user; it should return L<undef>
if the loop needs to stop (don't process the remaining users).

=for HTML <img src="NppCommunity-User.png" class="uml">

=begin comment

    <Command name="PlantUML to PNG" Ctrl="yes" Alt="yes" Shift="yes" Key="80">&quot;c:\usr\local\apps\PlantUML\PngAllActive.bat&quot; &quot;$(FULL_CURRENT_PATH)&quot;</Command>

        @echo off
        echo generate PlantUML from "%1"
        "C:\Cadence\SPB_17.4\tools\pcbdw\java11\bin\java.exe" -D:file.encoding=UTF-8 -jar "%~dp0\plantuml-1.2023.0.jar" -charset UTF-8 %1
        echo created "%~dpn1*.png"
        dir "%~dpn1*.png"
        pause

        https://plantuml.com/download

    <Command name="POD To .pod.html" Ctrl="yes" Alt="yes" Shift="no" Key="80">cmd /c c:\usr\local\scripts\pod2html_clean.bat --css=c:\usr\local\scripts\pod2html.css &quot;$(FULL_CURRENT_PATH)&quot; &gt; &quot;$(CURRENT_DIRECTORY)/~$$(NAME_PART).pod.html&quot;</Command>

=end comment

=begin PlantUML

@startuml NppCommunity-User

skinparam caption {
    FontName monospaced
    FontSize 16
}
Title User Object
Legend left
**Key:**
| <&info> | structures defined elsewhere |
| ... | same structure as the entry above |
| $var | variable value rather than exact text |
| # | comment |

More description down here
endlegend
Caption $data
label EncapsulateYaml [
{{yaml
userCount: ""$n"" 
users:
    -
        banned&#58;expire: 0
        banned: 0
        banned_until: 0
        banned_until_readable: "string"
        displayname: "string"
        email&#58;confirmed: 0
        flags: null
        icon&#58;bgColor: "#f44336"
        icon&#58;text: "string"
        joindate: 0
        joindateISO: "string"
        lastonline: 0
        lastonlineISO: "string"
        picture: "string"
        postcount: 0
        reputation: 0
        status: "string"
        uid: 0
        username: "string"
        userslug: "string"
    - ...
    - $userN
pagination:
    page: 0,
    currentPage: 0,
    pageCount: 0,
    first: ""{...}"" 
    last: ""{...}"" 
...: ...
}}
]

@enduml

=end PlantUML

=cut

sub forAllUsersDo
{
    my ($self, $cref) = @_;
    my $page = 1;
    while(defined $page) {
        my $response = $self->client()->get('https://community.notepad-plus-plus.org/api/users?section=joindate&page='.$page);
        die "$response->{status} $response->{reason}" unless $response->{success};
        my $data = JSON::decode_json($response->{content});
        my $lastpage = $data->{pagination}{last}{page};
        printf "pg %4d/%-4d:\t%d users\n", $page, $lastpage, scalar @{$data->{users}};
        for my $user ( @{$data->{users}} ) {
            return unless defined $cref->($user);
        }
        if(++$page > $lastpage) { undef $page; }
    }
}

=item forRecentTopicsDo

    $community->forRecentTopicsDo(sub {
        my ($topic) = @_;
        return 0 if ...; # return 0 if you want to skip the action on this topic
        return 1 if ...; # return 1 if you performed the action on this topic
        return undef;    # return undef if you want to stop processing any more topics
    });


Runs a subroutine for each topic.  The subroutine needs to take in the L<$topic> object
as the first argument.  It should return a true value if the action was performed for the topic;
it should return 0 or "" if the action was skipped for the topic; it should return L<undef>
if the loop needs to stop (don't process the remaining topics).

=for HTML <img src="NppCommunity-RecentTopics.png" class="uml">

=begin PlantUML

@startuml NppCommunity-RecentTopics

skinparam caption {
    FontName monospaced
    FontSize 16
}
Title Recent Topics Object
Legend left
**Key:**
| <&info> | structures defined elsewhere |
| ... | same structure as the entry above |
| $var | variable value rather than exact text |
| # | comment |

More description down here
endlegend
Caption $data
label EncapsulateYaml [
{{yaml
topicCount: ""$n"" 
topics:
    -
        bookmark: 0
        category: ""{}"" 
        cid: 0
        deleted: 0
        deleterUid: 0
        downvotes: 0
        followed: true
        icons: ""[]"" 
        ignored: true
        index: 0
        isOwner: true
        lastposttime: 0
        lastposttimeISO: "string"
        locked: 0
        mainPid: 0
        numThumbs: 0
        pinExpiry: 0
        pinExpiryISO: "string"
        pinned: 0
        postcount: 0
        postercount: 0
        scheduled: 0
        slug: "string"
        tags: ""[]"" 
        teaser: ""{}"" 
        teaserPid: 0
        thumb: "string"
        thumbs: ""[]"" 
        tid: 0
        timestamp: 0
        timestampISO: "string"
        title: "string"
        titleRaw: "string"
        uid: 0
        unread: true
        unreplied: true
        upvotes: 0
        user: ""{}"" 
        viewcount: 0
        votes: 0
    - ...
    - $topicN
pagination:
    page: 0,
    currentPage: 0,
    pageCount: 0,
    first: ""{...}"" 
    last: ""{...}"" 
...: ...
}}
]

@enduml

=end PlantUML


=cut

sub forRecentTopicsDo
{
    my ($self, $cref) = @_;
    my $page = 1;
    while(defined $page) {
        # originally /api/recent, but that only gives 10 pages (200 topics)
        # /api/top also limited to 10 pages
        my $response = $self->client()->get('https://community.notepad-plus-plus.org/api/recent?page='.$page);
        die "$response->{status} $response->{reason}" unless $response->{success};
        my $data = JSON::decode_json($response->{content});
        my $lastpage = $data->{pagination}{last}{page};
        printf "pg %4d/%-4d:\t%d topics\n", $page, $lastpage, scalar @{$data->{topics}};
        for my $topic ( @{$data->{topics}} ) {
            return unless defined $cref->($topic);
        }
        if(++$page > $lastpage) { undef $page; }
    }
}

=item forAllTopicsInCategoryDo

    $community->forAllTopicsInCategoryDo($categoryID, sub {
        my ($topic) = @_;
        return 0 if ...; # return 0 if you want to skip the action on this topic
        return 1 if ...; # return 1 if you performed the action on this topic
        return undef;    # return undef if you want to stop processing any more topics
    });

Runs a subroutine for each topic in the given category.  The subroutine needs to take in the L<$topic> object
as the first argument.  It should return a true value if the action was performed for the topic;
it should return 0 or "" if the action was skipped for the topic; it should return L<undef>
if the loop needs to stop (don't process the remaining topics).

Categories include BLOGS=3, GENERAL=2, HELPWANTED=4...

=for HTML <img src="NppCommunity-CategoryTopics.png" class="uml">

=begin PlantUML

@startuml NppCommunity-CategoryTopics

skinparam caption {
    FontName monospaced
    FontSize 16
}
Title Topic Object
Legend left
**Key:**
| <&info> | structures defined elsewhere |
| ... | same structure as the entry above |
| $var | variable value rather than exact text |
| # | comment |

More description down here
endlegend
Caption $data
label EncapsulateYaml [
{{yaml
topic_count: ""$n"" 
topics:
    -
        bookmark: 0
        category: ""{}"" 
        cid: 0
        deleted: 0
        deleterUid: 0
        downvotes: 0
        followed: true
        icons: ""[]"" 
        ignored: true
        index: 0
        isOwner: true
        lastposttime: 0
        lastposttimeISO: "string"
        locked: 0
        mainPid: 0
        numThumbs: 0
        pinExpiry: 0
        pinExpiryISO: "string"
        pinned: 0
        postcount: 0
        postercount: 0
        scheduled: 0
        slug: "string"
        tags: ""[]"" 
        teaser: ""{}"" 
        teaserPid: 0
        thumb: "string"
        thumbs: ""[]"" 
        tid: 0
        timestamp: 0
        timestampISO: "string"
        title: "string"
        titleRaw: "string"
        uid: 0
        unread: true
        unreplied: true
        upvotes: 0
        user: ""{}"" 
        viewcount: 0
        votes: 0
    - ...
    - $topicN
pagination:
    page: 0,
    currentPage: 0,
    pageCount: 0,
    first: ""{...}"" 
    last: ""{...}"" 
...: ...
}}
]

@enduml

=end PlantUML



=cut

sub forAllTopicsInCategoryDo
{
    my ($self, $categoryID, $cref) = @_;

    #### # get the topics for the current category:
    #### my $response = $self->client()->get("https://community.notepad-plus-plus.org/api/category/$categoryID");
    #### die "$response->{status} $response->{reason}" unless $response->{success};
    #### my $data = JSON::decode_json($response->{content});
    #### my $topics = $data->{topics};
    #### print "category $categoryID has ", $data->{topic_count}, " topics, with ", scalar(@$topics), " elements in array\n";
    #### print " ... with keys: ", join(", ", sort keys %{ $topics->[0] }), "\n";
    #### print " ... and data->pagination: "; Data::Dump::dd($data->{pagination});
    #### return;

    my $page = 1;
    while(defined $page) {
        my $response = $self->client()->get("https://community.notepad-plus-plus.org/api/category/$categoryID/?page=$page");
        die "$response->{status} $response->{reason}" unless $response->{success};
        my $data = JSON::decode_json($response->{content});
        my $lastpage = $data->{pagination}{last}{page};
        printf "pg %4d/%-4d:\t%6d/%-6d topics on this page\n", $page, $lastpage, scalar @{$data->{topics}}, $data->{topic_count};
        for my $topic ( @{$data->{topics}} ) {
            return unless defined $cref->($topic);
        }
        if(++$page > $lastpage) { undef $page; }
    }
}


=item forAllCategoriesDo

    $community->forAllCategoriesDo($categoryID, sub {
        my ($category) = @_;
        return 0 if ...; # return 0 if you want to skip the action on this topic
        return 1 if ...; # return 1 if you performed the action on this topic
        return undef;    # return undef if you want to stop processing any more topics
    });

Runs a subroutine for each category in the forum.  The subroutine needs to take in the L<$category> object
as the first argument.  It should return a true value if the action was performed for the category;
it should return 0 or "" if the action was skipped for the category; it should return L<undef>
if the loop needs to stop (don't process the remaining categories).

=for HTML <img src="NppCommunity-AllCategories.png" class="uml">

=begin PlantUML

@startuml NppCommunity-AllCategories

skinparam caption {
    FontName monospaced
    FontSize 16
}
Title Category Object
Legend left
**Key:**
| <&info> | structures defined elsewhere |
| ... | same structure as the entry above |
| $var | variable value rather than exact text |
| # | comment |

More description down here
endlegend
Caption $data
label EncapsulateYaml [
{{yaml
categories:
    -
        backgroundImage: "string"
        bgColor: "string"
        children: ""[]"" 
        cid: 0
        class: "string"
        color: "string"
        description: "string"
        descriptionParsed: "string"
        disabled: 0
        icon: "fa-comments-o"
        imageClass: "string"
        isSection: 0
        link: "string"
        maxTags: 0
        minTags: 0
        name: "string"
        numRecentReplies: 0
        order: 0
        parentCid: 0
        postQueue: 0
        post_count: 0
        posts: ""[]"" 
        slug: "string"
        subCategoriesPerPage: 0
        tagWhitelist: ""[]"" 
        teaser: ""{}"" 
        topic_count: 0
        totalPostCount: 0
        totalTopicCount: 0
        unread-class: "string"
        unread: true
    - ...
    - $categoryN
pagination:
    page: 0,
    currentPage: 0,
    pageCount: 0,
    first: ""{...}"" 
    last: ""{...}"" 
...: ...
}}
]

@enduml

=end PlantUML

=cut


sub forAllCategoriesDo
{
    my ($self, $cref) = @_;
    my $page = 1;
    while(defined $page) {
        my $response = $self->client()->get("https://community.notepad-plus-plus.org/api/categories?page=$page");
        die "$response->{status} $response->{reason}" unless $response->{success};
        my $data = JSON::decode_json($response->{content});
        my $lastpage = $data->{pagination}{last}{page};
        printf "pg %4d/%-4d:\t%6d categories on this page\n", $page, $lastpage, scalar @{$data->{categories}};
        for my $category ( @{$data->{categories}} ) {
            return unless defined $cref->($category);
        }
        if(++$page > $lastpage) { undef $page; }
    }
}

=item getTopicDetails

    $community->getTopicDetails($topicID);

C<forRecentTopicsDo>'s loop only gets the simplified topic details from the C</api/recent> endpoint.
This method gets the more detailed results, which includes the information about each post inside the topic.

=cut

sub getTopicDetails
{
    my ($self, $topicID) = @_;
    my $response = $self->client()->get('https://community.notepad-plus-plus.org/api/topic/'.$topicID);
    die "$response->{status} $response->{reason}" unless $response->{success};
    return my $data = JSON::decode_json($response->{content});
}

=item deletePost

    $community->deletePost($postID);

Deletes post using "soft delete", so it does not purge the post from the database.

=cut

sub deletePost
{
    my ($self, $postID) = @_;
    my $response = $self->client()->delete("https://community.notepad-plus-plus.org/api/v3/posts/$postID/state");
    #   the /state argument causes it to be soft-delete rather than purge, if I read API correctly
    die "$response->{url}\n\t=> $response->{status} $response->{reason}" unless $response->{success};
    return my $data = JSON::decode_json($response->{content});
}

=item purgePost

    $community->purgePost($postID);

Deletes post and purges from the database.

=cut

sub purgePost
{
    my ($self, $postID) = @_;
    my $response = $self->client()->delete("https://community.notepad-plus-plus.org/api/v3/posts/$postID");
    die "$response->{url}\n\t=> $response->{status} $response->{reason}" unless $response->{success};
    return my $data = JSON::decode_json($response->{content});
}


=item deleteTopic

    $community->deleteTopic($topicID);

Deletes topic using "soft delete", so it does not purge the topic from the database.

=cut

sub deleteTopic
{
    my ($self, $topicID) = @_;
    my $response = $self->client()->delete("https://community.notepad-plus-plus.org/api/v3/topics/$topicID/state");
    #   the /state argument causes it to be soft-delete rather than purge, if I read API correctly
    die "$response->{url}\n\t=> $response->{status} $response->{reason}" unless $response->{success};
    return my $data = JSON::decode_json($response->{content});
}

=item purgeTopic

    $community->purgeTopic($topicID);

Deletes topic and purges from the database.

=cut

sub purgeTopic
{
    my ($self, $topicID) = @_;
    my $response = $self->client()->delete("https://community.notepad-plus-plus.org/api/v3/topics/$topicID");
    die "$response->{url}\n\t=> $response->{status} $response->{reason}" unless $response->{success};
    return my $data = JSON::decode_json($response->{content});
}


=item deleteUserAndContent

    $community->deleteUserAndContent($userID);

Deletes user and data from the database.

=cut

sub deleteUserAndContent
{
    my ($self, $userID) = @_;
    my $response = $self->client()->delete("https://community.notepad-plus-plus.org/api/v3/users/$userID/content");
    die "$response->{url}\n\t=> $response->{status} $response->{reason}" unless $response->{success};
    $response = $self->client()->delete("https://community.notepad-plus-plus.org/api/v3/users/$userID/account");
    die "$response->{url}\n\t=> $response->{status} $response->{reason}" unless $response->{success};
    #my $response = $self->client()->delete("https://community.notepad-plus-plus.org/api/v3/users/$userID");
    #die "$response->{url}\n\t=> $response->{status} $response->{reason}" unless $response->{success};
    # when I did it with /users/$userID, with no /content and no /account, it would claim to delete, but the next run, they would be back
    #   when I switched to deleting the content first, then just the account, they seem to be really deleted.
    return my $data = JSON::decode_json($response->{content});
}



=back

=head1 AUTHOR

Peter C. Jones C<E<lt>petercj AT cpan DOT orgE<gt>>

=head1 COPYRIGHT

Copyright (C) 2024 Peter C. Jones

=head1 LICENSE

This program is free software; you can redistribute it and/or modify it
under the terms of either: the GNU General Public License as published
by the Free Software Foundation; or the Artistic License.
See L<http://dev.perl.org/licenses/> for more information.

=cut

1;
