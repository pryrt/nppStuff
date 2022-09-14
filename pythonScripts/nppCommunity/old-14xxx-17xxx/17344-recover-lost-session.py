# encoding=utf-8
"""in response to https://community.notepad-plus-plus.org/topic/17344/
specifically, translate https://community.notepad-plus-plus.org/post/79695 to PythonScript
other notes go here
"""
from Npp import editor,notepad,console
#import sys
import os.path

class SessionRecovery(object):
    xml_prefix = "<?xml version=\"1.0\" encoding=\"UTF-8\" ?> \n<NotepadPlus> \n<Session activeView=\"0\"> \n<mainView activeIndex=\"2\">"
    xml_suffix = "</mainView>\n <subView activeIndex=\"0\" />\n</Session>\n</NotepadPlus>\n"
    xml_entry1 = "<File firstVisibleLine=\"0\" xOffset=\"0\" scrollWidth=\"64\" startPos=\"8\" endPos=\"8\" selMode=\"0\" offset=\"0\" wrapCount=\"1\" lang=\"None (Normal Text)\" encoding=\"-1\" userReadOnly=\"no\" filename=\""
    xml_entry2 = "backupFilePath=\""
    xml_endentry = "originalFileLastModifTimestamp=\"0\" originalFileLastModifTimestampHigh=\"0\" mapFirstVisibleDisplayLine=\"-1\" mapFirstVisibleDocLine=\"-1\" mapLastVisibleDocLine=\"-1\" mapNbLine=\"-1\" mapHigherPos=\"-1\" mapWidth=\"-1\" mapHeight=\"-1\" mapKByteInDoc=\"512\" mapWrapIndentMode=\"-1\" mapIsWrap=\"no\" />"
    xml_full = ""

    def go(self):
        self.determine_directories()
        self.build_xml()
        self.output_xml()

    def determine_directories(self):
        cfg_plg_cfg = notepad.getPluginConfigDir()
        (cfg_plg, x) = os.path.split(cfg_plg_cfg)
        (self.cfg_dir, x) = os.path.split(cfg_plg)
        self.bkup_dir = os.path.join(self.cfg_dir, 'backup')
        self.xml_full = self.xml_prefix
        self.session_xml_path = os.path.join(self.cfg_dir, 'session.xml')

    def build_xml(self):
        for (root, dirs, files) in os.walk(self.bkup_dir):
            for f in files:
                filepath = os.path.join(root, f)
                posFile = filepath.find(f)
                posAt = filepath.find("@")
                entry_name = filepath[posFile:posAt]
                this_entry = self.xml_entry1 + entry_name + '" ' + self.xml_entry2 + filepath + '" ' + self.xml_endentry + "\n"
                self.xml_full += "\n    " + this_entry
        self.xml_full += self.xml_suffix

    def output_xml(self):
        #console.write("====BEGIN\n" + self.xml_full + "\n====END\n")
        notepad.new()
        editor.setText(self.xml_full)
        s = notepad.messageBox("YES to save as default session.xml\nNO to bring up SaveAs dialog\nCANCEL to not save at all", "Save session.xml", MESSAGEBOXFLAGS.YESNOCANCEL)
        if s == MESSAGEBOXFLAGS.RESULTYES:
            notepad.saveAs(self.session_xml_path)
        elif s == MESSAGEBOXFLAGS.RESULTNO:
            notepad.save()
            editor.setSavePoint() # allow it to close even if the save dialog is canceled
        else:
            editor.setSavePoint() # allow it to close even if it isn't saved
        notepad.close()
        pass


SessionRecovery().go()

"""
TODO: the YES=>SaveAs will save the session.xml file in the right place,
but then it immediately gets overwritten.

I think I want to change the logic so that
    YES     => saveAs to temporary, load session, and delete temporary
    NO      => use SAVE dialog to save it wherever the user wants
    CANCEL  => stop the SessionRecovery
=> move this logic to the go() function, and call a separate function for each, so that I can keep them completely separate
"""
