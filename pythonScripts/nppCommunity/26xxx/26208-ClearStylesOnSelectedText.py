# encoding=utf-8
"""in response to https://community.notepad-plus-plus.org/topic/26208/

Sometimes, you have multiple tokens all assigned to the same Style*Token, but then
want to clear the style _on just the selected text_, while leaving other tokens
with the same style(s) alone, so they will remain styled. (This is a targeted version of the Clear Styles menu options.)
"""
from Npp import editor
INDICATORS = [21, 22, 23, 24, 25, 31]
for i in range(editor.getSelections()):
    start = editor.getSelectionNStart(i)
    end = editor.getSelectionNEnd(i)
    if end-start == 0:
        start = editor.wordStartPosition(start, True)
        end = editor.wordEndPosition(start, True)
    for indicator in INDICATORS:
        editor.setIndicatorCurrent(indicator)
        editor.indicatorClearRange(start, end-start)
