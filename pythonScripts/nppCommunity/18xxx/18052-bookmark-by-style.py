# encoding=utf-8
"""by @Alan-Kilborn: in response to https://notepad-plus-plus.org/community/topic/18052/bookmark-by-style"""
from Npp import *
import re

def main():

    MARK_BOOKMARK = 24  # N++ normal bookmark marker number; identifier pulled from N++ source code

    # identifiers pulled from N++ source code:
    SCE_UNIVERSAL_FOUND_STYLE_EXT1 = 25  # N++ style 1 indicator number
    SCE_UNIVERSAL_FOUND_STYLE_EXT2 = 24  # N++ style 2 indicator number
    SCE_UNIVERSAL_FOUND_STYLE_EXT3 = 23  # N++ style 3 indicator number
    SCE_UNIVERSAL_FOUND_STYLE_EXT4 = 22  # N++ style 4 indicator number
    SCE_UNIVERSAL_FOUND_STYLE_EXT5 = 21  # N++ style 5 indicator number
    SCE_UNIVERSAL_FOUND_STYLE = 31  # N++ red-"mark" feature highlighting style indicator number

    def is_line_bookmarked(line_nbr): return (editor.markerGet(line_nbr) & (1 << MARK_BOOKMARK)) != 0

    def highlight_indicator_range_tups_generator(indicator_number):
        if editor.indicatorEnd(indicator_number, 0) == 0: return
        indicator_end_pos = 0  # set special value to key a check the first time thru the while loop
        while True:
            if indicator_end_pos == 0 and editor.indicatorValueAt(indicator_number, 0) == 1:
                indicator_start_pos = 0
            else:
                indicator_start_pos = editor.indicatorEnd(indicator_number, indicator_end_pos)
            indicator_end_pos = editor.indicatorEnd(indicator_number, indicator_start_pos)
            if indicator_start_pos == indicator_end_pos: break  # no more matches
            yield (indicator_start_pos, indicator_end_pos)

    user_input = notepad.prompt('Select style(s) you want to bookmark lines of:',
        '',
        '[   ] Style #1      [   ] Style #2\r\n[   ] Style #3      [   ] Style #4\r\n[   ] Style #5      [   ] Redmark\r\n\r\n[   ] CLEAR bookmarks instead of setting, for items chosen')
    if user_input == None: return
    if len(user_input) == 0: return
    user_input = re.sub(r'\s{4,}', '\r\n', user_input)
    ui_choices_list = user_input.splitlines()
    selected = ''
    for uic in ui_choices_list:
        m = re.search(r'\[([^]]+)\]', uic)
        if m and m.group(1) != ' ' * len(m.group(1)):
            selected += uic
    if len(selected) == 0: return

    indicator_number_list = []
    if '1' in selected: indicator_number_list.append(SCE_UNIVERSAL_FOUND_STYLE_EXT1)
    if '2' in selected: indicator_number_list.append(SCE_UNIVERSAL_FOUND_STYLE_EXT2)
    if '3' in selected: indicator_number_list.append(SCE_UNIVERSAL_FOUND_STYLE_EXT3)
    if '4' in selected: indicator_number_list.append(SCE_UNIVERSAL_FOUND_STYLE_EXT4)
    if '5' in selected: indicator_number_list.append(SCE_UNIVERSAL_FOUND_STYLE_EXT5)
    if 'red' in selected.lower(): indicator_number_list.append(SCE_UNIVERSAL_FOUND_STYLE)
    clearing_not_setting = True if 'clear' in selected.lower() else False

    at_least_1_match_of_style = False
    at_least_1_bookmark_change_made = False

    for indic_number in indicator_number_list:

        for (styled_start_pos, styled_end_pos) in highlight_indicator_range_tups_generator(indic_number):

            at_least_1_match_of_style = True

            bookmark_start_line = editor.lineFromPosition(styled_start_pos)
            bookmark_end_line = editor.lineFromPosition(styled_end_pos)

            for bm_line in range(bookmark_start_line, bookmark_end_line + 1):

                if clearing_not_setting:
                    if is_line_bookmarked(bm_line):
                        editor.markerDelete(bm_line, MARK_BOOKMARK)
                        at_least_1_bookmark_change_made = True
                else:
                    if not is_line_bookmarked(bm_line):
                        editor.markerAdd(bm_line, MARK_BOOKMARK)
                        at_least_1_bookmark_change_made = True

    if at_least_1_match_of_style:
        if at_least_1_bookmark_change_made:
            notepad.messageBox('Lines with selected style(s) have been {}bookmarked.'.format('un' if clearing_not_setting else ''), '')
        else:
            notepad.messageBox('No changes in bookmarks made.', '')
    else:
        notepad.messageBox('No text found matching selected style(s).', '')

main()
