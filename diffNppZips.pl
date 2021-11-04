#!/usr/bin/env perl

use 5.012; # //, strict
use warnings;

use Archive::Zip;
use Text::Diff;
use File::Spec::Functions qw/canonpath catfile/;

my $folder = canonpath($ARGV[0]||guessbase());
my $fileold = catfile($folder, $ARGV[1] || 'npp.8.1.2.portable.x64.zip');
my $filenew = catfile($folder, $ARGV[2] || 'npp.8.1.3.portable.x64.zip');

die "old version '$fileold' does not exist" unless -f $fileold;
die "new version '$filenew' does not exist" unless -f $filenew;

print STDERR "old: $fileold\n";
print STDERR "new: $filenew\n";

my $zold = Archive::Zip->new(); $zold->read($fileold);
my $znew = Archive::Zip->new(); $znew->read($filenew);

#print "old => ", $zold->memberNames(), "\n\t", $zold->members(), "\n";
#print "new => ", $znew->memberNames(), "\n\t", $znew->members(), "\n";

my %old; @old{ $zold->memberNames() } = ($zold->members());
my %new; @new{ $znew->memberNames() } = ($znew->members());
my %union = (%old, %new);
my %seen = (localization => 0, functionList => 0);

for my $entry ( undef, sort keys %union ) {
    next unless defined $entry;
    print("'$entry' only found in old\n"), next   unless exists $new{$entry};
    print("'$entry' only found in new\n"), next   unless exists $old{$entry};
    print("comparing '$entry'\n");
    my $folder = undef;
    if( $entry =~ m{/$} ) {
        next; # entries that end in / are folders, and do not need diff run
    }
    elsif( $entry =~ m{\.(zip|exe|dll)$} ) {
        my ($oc,$nc) = map $_->{$entry}->crc32String(), \%old, \%new;
        printf "binary mismatch: crc %s vs %s\n", $oc, $nc unless $oc eq $nc;
        next;
    } elsif ( $entry =~ m{(localization|functionList)/} ) {
        ++$seen{$folder = $1};
    }

    my $cold = $zold->contents( $entry );
    my $cnew = $znew->contents( $entry );

    if( !defined($cold) || !defined($cnew) ) {
        printf "\tWARN(%s)\n\tcold:%-15.15s\n\tcnew:%-15.15s\n", $entry, $cold//'<undef>', $cnew//'<undef>';
    } else {
        my $diff = diff \$cold, \$cnew;
        if(length($diff) && defined($folder) && ($seen{$folder}>1)) {
            print "comparing $folder ($seen{$folder})\n";
        } else {
            print $diff;
        }
    }

} continue {
    print "-"x40, "\n";
}

exit;

sub guessbase {
    for my $base (
        'c:/usr/local/apps/npp/',
        'c:/usr/local/apps/other-npp/',
        'c:/usr/local/apps/npp-other/',
        '.',
    ) {
        return $base if -d $base;
    }
}

1;
