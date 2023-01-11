# https://notepad-plus-plus.org/community/topic/16420/applying-defined-language-to-all-open-files
#   For each open file
#       * activate the file's tab
#       * select the Language menu's item for the MySuperCool UDL, or whatever it's named

udl_name = 'Markdown'   # change as needed

#console.clear()
#console.show()

files_tups_list = notepad.getFiles()
curr_file = notepad.getCurrentFilename()
console.write("current:"+curr_file+"\n")
for tup in files_tups_list:
    file = tup[0]
    console.write("file:"+tup[0]+"\t")
    console.write("id:"+str(tup[1])+"\t")
    console.write("idx:"+str(tup[2])+"\t")
    console.write("view:"+str(tup[3])+"\n")

    notepad.activateFile(file)
    keep = notepad.getCurrentLang()
    #console.write("lang:" + str(notepad.getCurrentLang()) + "\t" + str(int(notepad.getCurrentLang())) + "\n")
    #   notepad.setLangType(LANGTYPE.USER)          # couldn't find a way to make this select a particular UDL
    #notepad.menuCommand(MENUCOMMAND.LANG_USER)     # ditto
    notepad.runMenuCommand('Language', udl_name)    # here's one that will
    #console.write("lang:" + str(notepad.getCurrentLang()) + "\t" + str(int(notepad.getCurrentLang())) + "\n")
    #notepad.setLangType(keep)
    #console.write("lang:" + str(notepad.getCurrentLang()) + "\t" + str(int(notepad.getCurrentLang())) + "\n")

notepad.activateFile(curr_file)

# Note, the thread https://notepad-plus-plus.org/community/topic/11341/using-a-user-defined-language-as-default/11
#   has similar content, but does it when you switch to a particular file...