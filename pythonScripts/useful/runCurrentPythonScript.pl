#!perl

use 5.012; # strict, //
use warnings;

use Win32::Mechanize::NotepadPlusPlus ':main';

for(notepad->getCurrentFilename()) {
    m{PythonScript[\\/]scripts[\\/](.*)[\\/]}i;
    my ($tail) = $1 // '';
    s{.*[\\/]}{}g;
    s{\.py$}{}g;
    my @menuNames = ('Plugins', 'Python Script', 'Scripts', split(m{[\\/]}, $tail), $_);
    my $status = notepad->runMenuCommand(@menuNames) || 0;
    #print "runMenuCommand(", join(' | ', @menuNames), ") => $status\n";
}

# Run entry should be `wperl "C:\Users\PJones2\AppData\Roaming\Notepad++\plugins\config\PythonScript\scripts\runCurrentPythonScript.pl"`
