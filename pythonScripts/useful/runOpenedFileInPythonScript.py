# encoding=utf-8
"""
At one point, @Alan-Kilborn or other Forum regular mentioned they had
a method of running the open file with the PythonScript plugin

I think using getCurrentFilename and runPluginCommand, I can hack together something similar.

Unfortunately, it gives an error that you cannot run multiple PythonScripts at the same time.
"""
from Npp import *
import os

#console.show()
#console.write("\n\n\n")
fullname = notepad.getCurrentFilename()
basename = os.path.basename(fullname)
fileleft = os.path.splitext(basename)[0]
#notepad.runPluginCommand('Python Script', fileleft)

# from https://stackoverflow.com/questions/67631/how-to-import-a-module-given-the-full-path, some answers gave the idea of the runpy library:
import runpy
console.write( "running: \"" + fileleft + "\"\n")
external_globals_dictionary = runpy.run_path(fullname)
console.write( "~~~~~\tdone running: \"" + fileleft + "\"\t~~~~~\n")

# If I want to explore what ends up in that dictionary:
#for key, value in external_globals_dictionary.items():
#    console.write(str(key) + " => " + str(value) + "\n")

# unfortunately, that has the effect that the "if __name__ == '__main__'" code
#   won't trigger.  So it will work for some PySc scripts code but not others
# But it's good enough for debugging purposes.
