# encoding=utf-8
"""in response to https://github.com/notepad-plus-plus/notepad-plus-plus/issues/18198

Proof of concept of how I might solve such a problem

Store all the user configuration globals at the very top, so they are easy for user to edit:
===== GLOBALS ====================================================================================
"""
gsSnapshotDirectory = "c:/temp/nppCustomSnapshot"        # set this to your desired location; either use / or \\ as path separator
"""
===== END GLOBALS ================================================================================

===== TODO =======================================================================================
[ ] figure out and clean out which existing snapshots aren't needed anymore
    - my idea would be to recurse through all the files in gsSnapshotDirectory,
        and any that aren't still in the dFilesToArchive should be cleaned out
        (probably better to go in a seperate function call on the same modifiedFiles)
[ ] setup time snapshot,
    - threading.Timer() example: p27550_TimedDualSave.py
    - every S seconds, it will call runCustomSessionSnapshot(), then schedule the next instance
[ ] setup callback on NPPM_BEFORESHUTDOWN (NOTIFICATIONS.SHUTDOWN)
    - call runCustomSessionSnapshot()
    - cancel remaining threading.Timer instance
"""

from Npp import notepad, editor, console, BUFFERENCODING
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
            sFileName = pPath.name
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
                    'pathName':     tFileInfo[0],
                    'fileName':     sFileName,
                    'index':        tFileInfo[2],
                    'view':         tFileInfo[3],
                    'archiveTail':  sArchiveTail
                }

        return dTrackModifiedFiles

    def archiveFiles(dFilesToArchive):
        encMap = {
                # https://docs.python.org/3/library/codecs.html#text-encodings
                int(BUFFERENCODING.COOKIE)       : 'utf-8',     # noBOM
                int(BUFFERENCODING.ENC8BIT)      : 'mcbs',      # ANSI, CP_ACP
                int(BUFFERENCODING.ANSI)         : 'ascii',     # badly named
                int(BUFFERENCODING.UCS2BE)       : 'utf_16_be', # need manual BOM
                int(BUFFERENCODING.UCS2BE_NOBOM) : 'utf_16_be',
                int(BUFFERENCODING.UCS2LE)       : 'utf_16_le', # need manual BOM
                int(BUFFERENCODING.UCS2LE_NOBOM) : 'utf_16_le',
                int(BUFFERENCODING.UTF8)         : 'utf-8-sig'  # auto BOM
        }
        #console.write(f"{str(dFilesToArchive):<120.120}\n")
        for kBufID in dFilesToArchive.keys():
            d = dFilesToArchive[kBufID]
            notepad.activateIndex(d['view'], d['index'])
            e = notepad.getEncoding()
            t = editor.getText()
            bytestring = t.encode(encMap[int(e)], errors='replace')
            if e == BUFFERENCODING.UCS2BE:
                bytestring = codec.BOM_UTF16_BE + bytestring
            elif e == BUFFERENCODING.UCS2LE:
                bytestring = codec.BOM_UTF16_LE + bytestring

            pArchivePath = pathlib.PureWindowsPath(gsSnapshotDirectory).joinpath(d['archiveTail'], d['fileName'])

            #console.write(f"{str(True):<5.5} | {d['pathName']:<90.90} | {str(pArchivePath):<90.90} | v{d['view']}.i{d['index']} | e:{encMap[int(e)]:<12.12} | l:{len(bytestring)}\n")

            pathlib.WindowsPath(pArchivePath.parent).mkdir(parents=True, exist_ok=True)

            with open(str(pArchivePath), 'wb') as f:
                f.write(bytestring)

        # TODO: I should also figure out which existing snapshots aren't needed anymore...
        #   but that's more logic than I'm interested in for now.


    ############################################################################
    # Now that helper functions are defined, do the algorithm:
    ############################################################################
    #console.show()
    #console.clear()

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
