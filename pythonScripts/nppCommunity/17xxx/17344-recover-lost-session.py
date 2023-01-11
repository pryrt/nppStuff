# encoding=utf-8
"""in response to https://community.notepad-plus-plus.org/topic/17344/
specifically, translate the ideas behind https://community.notepad-plus-plus.org/post/79695 to PythonScript

0. Install Python Script plugin, if not yet installed
1. Use Plugins > PythonScript > New Script, give this a name (like `RecoverLostSession.py`)
2. Plugins > PythonScript > Scripts > `RecoverLostSession` to recover it
    1. click YES to load the recovered session immediately
    2. click NO to save the recovered session into an XML file that you can later load with File > Load Session...
    3. click CANCEL to ignore the recovered session
"""
from Npp import editor,notepad,console
import os
import tempfile

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
        s = notepad.messageBox("YES to load recovered session now\nNO to save as a new session file\nCANCEL to ignore recovered session", "Recovered Session", MESSAGEBOXFLAGS.YESNOCANCEL)
        if s == MESSAGEBOXFLAGS.RESULTYES:
            self.load_session()
        elif s == MESSAGEBOXFLAGS.RESULTNO:
            self.saveas_session()
        return

    def determine_directories(self):
        cfg_plg_cfg = notepad.getPluginConfigDir()
        (cfg_plg, x) = os.path.split(cfg_plg_cfg)
        (self.cfg_dir, x) = os.path.split(cfg_plg)
        self.bkup_dir = os.path.join(self.cfg_dir, 'backup')
        self.xml_full = self.xml_prefix
        self.session_xml_path = os.path.join(self.cfg_dir, 'session.xml')
        return

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
        return

    def saveas_session(self):
        notepad.new()
        editor.setText(self.xml_full)
        notepad.save()
        notepad.close()
        return

    def load_session(self):
        _, fn = tempfile.mkstemp('.xml')
        f = open(fn, 'w')
        f.write(self.xml_full)
        f.close()
        notepad.loadSession(f.name)
        try:
            os.remove(f.name)
        except WindowsError as e:
            if e.winerror == 32: # cannot delete is fine, just ignore it
                pass
            else:
                raise e
        return

SessionRecovery().go()
