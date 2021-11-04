# encoding=utf-8
"""https://notepad-plus-plus.org/community/topic/18134/style-token-not-saved/7

@Alan-Kilborn did his own, which worked for him...
"""

from Npp import *
import os

def main():

    result = notepad.messageBox("SAVE current doc's styling to disk file?\r\n\r\nYES = Yes, please\r\nNO = LOAD styling info from file and apply to current doc\r\nCANCEL = I'm outta here", '', MESSAGEBOXFLAGS.YESNOCANCEL)
    if result == MESSAGEBOXFLAGS.RESULTCANCEL: return
    saving_not_loading = True if result == MESSAGEBOXFLAGS.RESULTYES else False

    # identifiers pulled from N++ source code:
    SCE_UNIVERSAL_FOUND_STYLE_EXT1 = 25  # N++ style 1 indicator number
    SCE_UNIVERSAL_FOUND_STYLE_EXT2 = 24  # N++ style 2 indicator number
    SCE_UNIVERSAL_FOUND_STYLE_EXT3 = 23  # N++ style 3 indicator number
    SCE_UNIVERSAL_FOUND_STYLE_EXT4 = 22  # N++ style 4 indicator number
    SCE_UNIVERSAL_FOUND_STYLE_EXT5 = 21  # N++ style 5 indicator number
    SCE_UNIVERSAL_FOUND_STYLE = 31  # N++ red-"mark" feature highlighting style indicator number

    indicator_number_list = []
    indicator_number_list.append(SCE_UNIVERSAL_FOUND_STYLE_EXT1)
    indicator_number_list.append(SCE_UNIVERSAL_FOUND_STYLE_EXT2)
    indicator_number_list.append(SCE_UNIVERSAL_FOUND_STYLE_EXT3)
    indicator_number_list.append(SCE_UNIVERSAL_FOUND_STYLE_EXT4)
    indicator_number_list.append(SCE_UNIVERSAL_FOUND_STYLE_EXT5)
    indicator_number_list.append(SCE_UNIVERSAL_FOUND_STYLE)

    if saving_not_loading:

        def highlight_indicator_range_tups_generator(indicator_number):
            '''
            the following logic depends upon behavior that isn't exactly documented;
            it was noticed that calling editor.indicatorEnd() will yield the "edge"
            (either leading or trailing) of the specified indicator greater than the position
            specified by the caller
            this is definitely different than the scintilla documentation:
            "Find the start or end of a range with one value from a position within the range"
            '''
            if editor.indicatorEnd(indicator_number, 0) == 0: return
            indicator_end_pos = 0  # set special value to key a check the first time thru the while loop
            while True:
                if indicator_end_pos == 0 and editor.indicatorValueAt(indicator_number, 0) == 1:
                    # we have an indicator starting at position 0!
                    # when an indicator highlight starts at position 0, editor.indicatorEnd()
                    #  gives us the END of the marking rather than the beginning;
                    #  have to compensate for that:
                    indicator_start_pos = 0
                else:
                    indicator_start_pos = editor.indicatorEnd(indicator_number, indicator_end_pos)
                indicator_end_pos = editor.indicatorEnd(indicator_number, indicator_start_pos)
                if indicator_start_pos == indicator_end_pos: break  # no more matches
                yield (indicator_start_pos, indicator_end_pos)

        with open('styling.txt', 'w') as f:
            for indic_number in indicator_number_list:
                for (styled_start_pos, styled_end_pos) in highlight_indicator_range_tups_generator(indic_number):
                    f.write('{i} {start} {stop}\n'.format(i=indic_number, start=styled_start_pos, stop=styled_end_pos))
            console.clear()
            console.write("save styling.txt => {}/{}".format(os.getcwd(),f.name))
            console.show()

    else:

        with open('styling.txt') as f:
            console.clear()
            console.write("read styling.txt => {}/{}".format(os.getcwd(),f.name))
            console.show()
            for line in f:
                (indic, start, end) = line.rstrip().split()
                editor.setIndicatorCurrent(int(indic))
                editor.indicatorFillRange(int(start), int(end) - int(start))

main()
