from Npp import notepad, NOTIFICATION
from datetime import datetime
import shutil
import os
import threading

class clsTimedDualSave:
    """class to encapsulate functions for TimedDualSave"""

    ### START CUSTOMIZABLE SECTION ########################################################################
    ### The user should customize SAVEINTERVAL and TRACKPATHS
    #######################################################################################################
    # SAVEINTERVAL gives the number of seconds between automatic saves.  Use 60 for one minute
    SAVEINTERVAL = 3;
    # CHECKINTERVAL gives the number of seconds between automatic checks for .  Use 60 for one minute
    CHECKINTERVAL = 5;
    # TRACKPATHS is a dictionary of paths to track, in the format REMOTEPATH: LOCALPATH, for example:
    #       Note that you need \\ for each path separator
    #   TRACKPATHS = {
    #           'X:\\': 'C:\\localPath\\X\\',
    #           '\\\\machinename\\shareDirectory\\': 'c:\\localpath\\shareDirectory\\'
    #   }
    TRACKPATHS = {
        'C:\\usr\\local\\apps\\npp\\npp.8.9.6.1.ps3.x64\\plugins\\Config\\PythonScript\\': 'c:\\temp\\'
    }
    ### END CUSTOMIZABLE SECTION ##########################################################################

    # Debugging flags
    _DEBUG_CALLBACKS = False
    _DEBUG_SCHEDULE = False
    _DEBUG_CHECK = True

    def __init__(self):
        console.write(f"Initializing clsTimedDualSave ...\n");
        self.track = {};
        self.launchTimerCheckDrives();
        self.registerCallbacks();
        self.trackAlreadyOpenFiles();
        console.write(f"... done initializing clsTimedDualSave ...\n");

    def __del__(self):
        self.endTimerCheckDrives()

    def launchTimerCheckDrives(self):
        self.timerCheckDrives = threading.Timer(self.CHECKINTERVAL, self.checkDrives)
        self.timerCheckDrives.start()
        if self._DEBUG_CHECK:
            console.write(f"... RESTART timerCheckDrives for {self.CHECKINTERVAL} from {datetime.now()}...\n")

    def endTimerCheckDrives(self):
        if self.timerCheckDrives:
            self.timerCheckDrives.cancel()
            self.timerCheckDrives = None
            if self._DEBUG_CHECK:
                console.write(f"... END timerCheckDrives ...\n")

    def translateFileNameFromTrackPaths(self, fileName):
        """decide whether to watch a given path or not
        For the simple version, just checks if the fileName in question starts with any of the paths listed in self.TRACKPATHS
        You could customize this to your own needs, if you need something different from
        """
        for p in self.TRACKPATHS.keys():
            if self._DEBUG_SCHEDULE:
                console.write(f"...   !! t='{fileName}'\n      vs p='{p}'\n")
            if fileName.startswith(p):
                f = os.path.basename(fileName)
                n = self.TRACKPATHS[p]
                s = '' if n[-1]=="\\" else "\\"
                return n + s + f
            if self._DEBUG_SCHEDULE:
                console.write(f"...   !! DIDNT START WITH p={p}\n")
        return None

    def checkDrives(self):
        drives = []
        for p in self.TRACKPATHS.keys():
            if p[1] == ':':
                console.write(f"... NEWDEBUG timerCheckDrives: {p} => drive {p[0:2]}...\n")
                if p[0:2] not in drives:
                    drives.append(p[0:2])
            # POSSIBLE FUTURE FEATURE: look for '\\\\machinename\\' as well
            if self._DEBUG_CHECK:
                console.write(f"... timerCheckDrives: check {p} ...\n")

        console.write(f"... NEWDEBUG drives={drives}...\n")
        for d in drives:
            if not os.path.isdir(d):
                # not sure how to do this, and not sure I have enough "I care" to continue working on it, because
                # I think, fundamentally, this is a silly thing to do, and I've finished the parts that I was most interested in
                console.writeError(f"TODO: Need to copy the current buffer for each of the files on {d} to the destination drive")

        # update and start new instance of the timer
        self.launchTimerCheckDrives()

    def cbAfterSaveOrOpen(self, kwargs):
        """Callback for FILESAVED and FILEOPENED notifications"""
        bufferID = kwargs['bufferID']
        fileName = notepad.getBufferFilename(bufferID)
        if self.scheduleFilename(fileName):
            if self._DEBUG_CALLBACKS:
                console.write(f'cbAfterSaveOrOpen:  {bufferID} => "{fileName}" =>\n\t ... {self.track[fileName]} ...\n');

    def cbBeforeClose(self, kwargs):
        """Callback for FILESAVED and FILEOPENED notifications"""
        bufferID = kwargs['bufferID']
        fileName = notepad.getBufferFilename(bufferID)
        if fileName in self.track:
            if self._DEBUG_CALLBACKS:
                console.write(f'cbBeforeClose:  {bufferID} => "{fileName}" =>\n\t ... {self.track[fileName]} ...\n');
            if 'timer' in self.track[fileName]:
                self.track[fileName]['timer'].cancel()
                del self.track[fileName]['timer']
                if self._DEBUG_CALLBACKS:
                    console.write(f'cbBeforeClose: cancelled timer ...\n');
            del self.track[fileName]

    def registerCallbacks(self):
        notepad.callback(self.cbAfterSaveOrOpen, [NOTIFICATION.FILESAVED, NOTIFICATION.FILEOPENED])
        notepad.callback(self.cbBeforeClose, [NOTIFICATION.FILEBEFORECLOSE])
        console.write(f"... registering clsTimedDualSave callbacks ...\n");

    def trackAlreadyOpenFiles(self):
        if self._DEBUG_SCHEDULE:
            console.write(f"... initiate tracking on existing files ...\n");
        for fileName, bufferID, index, view in notepad.getFiles():
            if self.scheduleFilename(fileName):
                if self._DEBUG_SCHEDULE:
                    console.write(f"... - scheduled '{fileName}' ...\n");
        if self._DEBUG_SCHEDULE:
            console.write(f"... finished initiating tracking on existing files.\n");

    def scheduleFilename(self, fileName):
        """Makes sure the file is tracked
        - if it's already tracked, cancel any existing timer
        - set a new timer to run self.remoteSave at SAVEINTERVAL seconds from now
        """

        if self._DEBUG_SCHEDULE:
            console.write(f"...   !! DEBUG: start scheduleFilename('{fileName}')\n");

        if not self.translateFileNameFromTrackPaths(fileName):
            return False

        if fileName in self.track:
            if 'timer' in self.track[fileName]:
                self.track[fileName]['timer'].cancel();
                if self._DEBUG_SCHEDULE:
                    console.write(f"DEBUG: cancel old timer for '{fileName}'\n");

        self.track[fileName] = {
            'lastSave': datetime.now(),
            'timer':    threading.Timer(self.SAVEINTERVAL, self.remoteSave, args=None, kwargs={'fileName': fileName})
        }

        if fileName in self.track:
            if 'timer' in self.track[fileName]:
                self.track[fileName]['timer'].start();

        if self._DEBUG_SCHEDULE:
            console.write(f"DEBUG: should call self.remoteSave in {self.SAVEINTERVAL}sec from {self.track[fileName]['lastSave']}\n");

        return True

    def remoteSave(self, fileName):
        newName = self.translateFileNameFromTrackPaths(fileName)
        if self._DEBUG_SCHEDULE or self._DEBUG_CALLBACKS:
            console.write(f"{datetime.now()}: remoteSave\n\tfrom '{fileName}'\n\tto '{newName}'\n")
        shutil.copy(fileName, newName)

global myTimedDualSave; # singleton
try:
    myTimedDualSave
    notepad.clearCallbacks()
    myTimedDualSave.endTimerCheckDrives()
    del myTimedDualSave
    del clsTimedDualSave
    console.write(f"!!!!! Cleared TimedDualSave: must run again to be in effect !!!!\n");
except:
    console.clear()
    myTimedDualSave = clsTimedDualSave()
