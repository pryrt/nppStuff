from Npp import notepad, LANGTYPE

NAME_OF_UDL = 'Markdown (preinstalled)' # <<- needs to be specified to match the UDL you want to select
NAME_OF_UDL2 = 'Markdown (preinstalled dark mode)' # <<- needs to be specified to match the UDL you want to select

language = notepad.getLangType()
desc = notepad.getLanguageDesc(language)    # this needs PythonScript 1.5.4 or newer

if desc == 'User Defined language file - {}'.format(NAME_OF_UDL):
    notepad.runMenuCommand('Language', NAME_OF_UDL2)
else:
    notepad.runMenuCommand('Language', NAME_OF_UDL)

