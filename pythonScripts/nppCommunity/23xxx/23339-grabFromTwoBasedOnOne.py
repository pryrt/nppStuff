# encoding=utf-8
"""in response to https://community.notepad-plus-plus.org/topic/23339/pasting-copied-text-in-a-search-window-in-a-macro

This searches in the "objects" file for every line:
    <ObjectRef ref="..."/>
It grabs the ref ID, and searches for that ID in the "hosts" file
    <Host id="id4843X9273" name="object_name" comment="" ro="False">
It grabs the name field from the matching line in the "hosts" file
It then replaces the whole <ObjectRef.../> with that name field

In the lines below, change the paths to the two files:
- The first path is the "objects" file,
- The second is the "hosts" file.
- Both must be opened in Notepad++, but it doesn't matter which view they are in.
- Full paths are required.

It makes it a single undo action, so if you don't like the results, you can just hit UNDO
"""
from Npp import editor,notepad,console

class Class23339(object):
    def go(self, object_fname, host_fname):
        self.object_fname = object_fname
        self.host_fname = host_fname
        notepad.activateFile(object_fname)
        editor.rereplace(r'<ObjectRef ref="([^"]*)"/>', lambda m: self.repl_in_objects(m))

    def repl_in_objects(self, m):
        notepad.activateFile(self.host_fname)
        editor.research(r'<Host id="{}" name="(.*?)"'.format(m.group(1)), lambda ms: self.find_in_hosts(ms))
        notepad.activateFile(self.object_fname)
        return self.found_in_hosts

    def find_in_hosts(self, m):
        self.found_in_hosts = m.group(1)

editor.beginUndoAction()
Class23339().go(
    r"c:\users\peter.jones\downloads\tempdata\nppCommunity\objects.xml",
    r"c:\users\peter.jones\downloads\tempdata\nppCommunity\hosts.xml"
)
editor.endUndoAction()
