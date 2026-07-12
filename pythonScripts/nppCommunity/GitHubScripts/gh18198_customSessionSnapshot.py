# encoding=utf-8
"""in response to https://github.com/notepad-plus-plus/notepad-plus-plus/issues/18198

Experimenting with how I might solve such a problem

Store all the globals at the very top, so they are easy for user to edit:
===== GLOBALS ====================================================================================
"""
gsSnapshotDirectory = "c:/temp/"        # set this to your desired location; either use / or \\ as path separator
"""
===== END GLOBALS ================================================================================
"""

from Npp import notepad, editor, console
import pathlib
import zlib

def runCustomSessionSnapshot():
    ############################################################################
    # Define internal helper functions
    ############################################################################
    def findModifiedFiles():
        # track modified files
        dTrackModifiedFiles = {}

        for tFileInfo in notepad.getFiles():
            sName = tFileInfo[0]
            pPath = pathlib.PureWindowsPath(sName)
            pDir = pPath.parent
            sDirTail = pDir.name
            iCRC = zlib.crc32(str(pDir).encode('utf-8'))
            sArchiveTail = f"{sDirTail}_{iCRC:08x}"

            # find out if it's modified
            notepad.activateIndex(tFileInfo[3], tFileInfo[2])
            isModified = editor.getModify()
            #console.write(f"{str(isModified):<5.5} | {str(tFileInfo):<90.90} | {sName:<40.40} | {str(pDir):<40.40} | {sDirTail:<20.20} | {iCRC:08x} | {sArchiveTail:<40.40} |\n")

            # track it if modified:
            kBufID = tFileInfo[1]
            if isModified and not kBufID in dTrackModifiedFiles:
                dTrackModifiedFiles[kBufID] = {
                    'name':         tFileInfo[0],
                    'index':        tFileInfo[2],
                    'view':         tFileInfo[3],
                    'archiveTail':  sArchiveTail
                }

        return dTrackModifiedFiles

    def archiveFiles(dFilesToArchive):
        console.write(f"{str(dFilesToArchive):<120.120}\n")
        for kBufID in dFilesToArchive.keys():
            d = dFilesToArchive[kBufID]
            notepad.activateIndex(d['view'], d['index'])
            e = notepad.getEncoding()
            console.write(f"{str(True):<5.5} | {d['name']:<90.90} | {d['archiveTail']:<40.40} | v{d['view']}.i{d['index']} | e:{str(e):<12.12}\n")

    ############################################################################
    # Now that helper functions are defined, do the algorithm:
    ############################################################################
    console.show()
    console.clear()

    # store orignal state
    tOriginalState = (notepad.getCurrentView(), notepad.getCurrentDocIndex(notepad.getCurrentView()), notepad.getCurrentDocIndex(0), notepad.getCurrentDocIndex(1))
    #console.write(f"{gOriginalState}\n")

    # find modified files, and archive them
    modifiedFiles = findModifiedFiles()
    archiveFiles(modifiedFiles)

    # restore original state
    if tOriginalState[2] != -1:
        notepad.activateIndex(0, tOriginalState[2])
    if tOriginalState[3] != -1:
        notepad.activateIndex(1, tOriginalState[3])
    notepad.activateIndex(tOriginalState[0], tOriginalState[1])

runCustomSessionSnapshot()
