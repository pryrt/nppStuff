# encoding=utf-8
"""in response to https://community.notepad-plus-plus.org/topic/21689/

Merge my suggestion with Eko's pointer to https://github.com/notepad-plus-plus/notepad-plus-plus/issues/9296#issuecomment-751706154
"""
from Npp import editor, notepad, NOTIFICATION, EDGEVISUALSTYLE

TAB_CONFIG = {}

pixperchar = 8

def register_lang(func):
    def wrapped():
        for linenum in range(editor.getLineCount()):
            editor.clearTabStops(linenum)
            func(linenum)
    TAB_CONFIG[func.__name__.replace('on_lang_','')] = wrapped
    return wrapped

@register_lang
def on_lang_cobol(linenum):
    for col in [7,8,12,72]:
        editor.addTabStop(linenum, (col-1)*pixperchar)

@register_lang
def on_lang_assembly(linenum):
    for col in [11, 18, 40, 79]:
        editor.addTabStop(linenum, (col-1)*pixperchar)


def on_lang_default():
    pass


def on_set_tab_stops(args):
    #print(str(args))
    lang = notepad.getLanguageName(notepad.getLangType())
    config = lang.lower().replace('udf - ', '')
    func = TAB_CONFIG.get(config, on_lang_default)
    # print(func)
    if 'linesAdded' in args:
        if args['linesAdded'] != 0:
            func()
    else:
        func()

notepad.clearCallbacks(on_set_tab_stops)
notepad.callback(on_set_tab_stops, [NOTIFICATION.BUFFERACTIVATED, NOTIFICATION.LANGCHANGED])
editor.clearCallbacks(on_set_tab_stops)
editor.callback(on_set_tab_stops, [SCINTILLANOTIFICATION.MODIFIED])

"""
123456789x123456789x123456789x123456789x123456789x123456789x123456789x123456789x123456789x123456789x
	7
		8
			12
				72
123456789x123456789x123456789x123456789x123456789x123456789x123456789x123456789x123456789x123456789x
fddsafdsaf	adfdsafdasf
	asdfadsf

sd	asdfdsaf	asdfdsaf







blah	blah
b	b	b	b	b
123456789x123456789x123456789x123456789x123456789x123456789x123456789x123456789x123456789x123456789x\
"""
