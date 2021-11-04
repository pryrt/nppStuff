#### Edit PerlMonks question
from Npp import *

def pmq_CreatePerlMonksQuestion():
    notepad.open('C:\Users\peter.jones\OneDrive - maximintegrated.onmicrosoft.com\OneDriveDocuments\SOPW.html')
    editor.documentStart()
    #console.show()
    #console.write("\n"+__name__ + "\n")

if __name__ == '__main__': pmq_CreatePerlMonksQuestion()

#### OLD: add css to first line
# # goto first line
# editor.gotoLine(0)  # goto first line, first position
# # insert the css;
# #   python multiline (heredoc) quotes start/stop with triple-quote '''
# editor.addText('''<style>
# body {
#     font-family: sans-serif;
# }
# c, code {
#     font-family: monospace;
#     white-space: pre;
#     display: block;
#     border: 1px solid #677;
#     border-radius: 4px;
#     padding: 0 2px;
#     background: #cff;
# }
# p c, p code {
#     display: inline;
# }
# spoiler, readmore {
#     display: block;
#     border: 1px solid #777;
#     border-radius: 4px;
#     background: #ccc;
#     padding: 0 1ex;
# }
# </style>
# ''');