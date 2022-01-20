# -*- coding: utf-8 -*-
'''
    This script searches through the entire active document for HTML/CSS colors in the form #ABCDEF (# followed by 6 hex digits), and colors them per their own value.  Running the script multiple times will toggle the colorization on and off.

    Each file has its own state variable, so it will track the colorization state of all your files.  (It will get out of sync if you close a file when it's colorized, then later re-open that file).

    If the colors are getting deleted at other times, one of your lexers or plugins might be changing the INDICATOR number 0, so you can try to set INDICATOR_ID to another integer (0..7 are for lexers, 8..31 are for the Notepad++ application itself, I cannot guarantee which will or won't be used by your setup) on the INDICATOR_ID = ... line, below

    URL: https://gist.github.com/pryrt/3055e137f3cb9b67a5265125507b2eae

    modified from a notification-based script in the gist at https://gist.github.com/pryrt/5ade1a13501c4df47f2fd8c00f1c7b03

    modified from Ekopalypse's EnhanceAnyLexer script at https://github.com/Ekopalypse/NppPythonScripts/blob/master/npp/EnhanceAnyLexer.py

'''
import sys
from Npp import (notepad, editor, editor1, editor2,
                 INDICATORSTYLE, INDICFLAG, INDICVALUE)

excluded_styles = [] #[1, 3, 4, 6, 7, 12, 16, 17, 18, 19]
start_position, end_position = 0,0

INDICATOR_ID = 7
editor1.indicSetStyle(INDICATOR_ID, INDICATORSTYLE.DASH)
editor1.indicSetFlags(INDICATOR_ID, INDICFLAG.VALUEFORE)
editor2.indicSetStyle(INDICATOR_ID, INDICATORSTYLE.DASH)
editor2.indicSetFlags(INDICATOR_ID, INDICFLAG.VALUEFORE)

def rgb(r, g, b):
    '''
        Helper function
        Retrieves rgb color triple and converts it
        into its integer representation

        Args:
            r = integer, red color value in range of 0-255
            g = integer, green color value in range of 0-255
            b = integer, blue color value in range of 0-255
        Returns:
            integer
    '''
    return (b << 16) + (g << 8) + r

def argb(a, r, g, b):
    '''
        Helper function
        Retrieves rgb color triple and converts it
        into its integer representation

        Args:
            a = alpha, use FF for normal (non-transparent)
            r = integer, red color value in range of 0-255
            g = integer, green color value in range of 0-255
            b = integer, blue color value in range of 0-255
        Returns:
            integer
    '''
    return (a << 24) + (b << 16) + (g << 8) + r

def paint_it(color, match_position, length, start_position, end_position):
    '''
        This is where the actual coloring takes place.
        Color, the position of the first character and
        the length of the text to be colored must be provided.
        Coloring occurs only if the character at the current position
        has not a style from the excluded styles list assigned.

        Args:
            color = integer, expected in range of 0-16777215
            match_position = integer,  denotes the start position of a match
            length = integer, denotes how many chars need to be colored.
            start_position = integer,  denotes the start position of the visual area
            end_position = integer,  denotes the end position of the visual area
        Returns:
            None
    '''
    if (match_position + length < start_position or
        match_position > end_position or
        editor.getStyleAt(match_position) in excluded_styles):
        return

    editor.setIndicatorCurrent(INDICATOR_ID)
    editor.setIndicatorValue(color)
    editor.indicatorFillRange(match_position, length)


def grab_color_and_paint_hex6(m):
    #console.write("match({}..{})='{}'\n".format(m.start(0),m.end(0), m.group(0)))
    r = int(m.group(0)[1:3], base=16)
    g = int(m.group(0)[3:5], base=16)
    b = int(m.group(0)[5:7], base=16)
    my_rgb = rgb(r,g,b) | INDICVALUE.BIT
    paint_it(my_rgb,
                    m.span(0)[0],
                    m.span(0)[1] - m.span(0)[0],
                    start_position,
                    end_position)

def grab_color_and_paint_hex8(m):
    #console.write("match({}..{})='{}'\n".format(m.start(0),m.end(0), m.group(0)))
    a = int(m.group(0)[1:3], base=16)
    r = int(m.group(0)[3:5], base=16)
    g = int(m.group(0)[5:7], base=16)
    b = int(m.group(0)[7:9], base=16)
    my_rgb = rgb(r,g,b) | INDICVALUE.BIT
    paint_it(my_rgb,
                    m.span(0)[0],
                    m.span(0)[1] - m.span(0)[0],
                    start_position,
                    end_position)

def grab_color_and_paint_rgbparen(m):
    #console.write("match({}..{})='{}'\n".format(m.start(0),m.end(0), m.group(0)))
    console.write("matches: 0:{}\t1:{}\t2:{}\t3:{}\n".format(m.group(0),m.group(1),m.group(2),m.group(3)))
    r = int(m.group(1))
    g = int(m.group(2))
    b = int(m.group(3))
    my_rgb = rgb(r,g,b) | INDICVALUE.BIT
    paint_it(my_rgb,
                    m.span(0)[0],
                    m.span(0)[1] - m.span(0)[0],
                    start_position,
                    end_position)

my_file = notepad.getCurrentFilename()

try:
    my_state[my_file] = not my_state[my_file]
except NameError:               # if dictionary does not yet exist
    my_state = {}               #   dictionary needs to be instantiated
    my_state[my_file] = True    #   and key needs to be populated
except KeyError:                # if dictionary key does not yet exist
    my_state[my_file] = True    #   key needs to be populated

editor.setIndicatorCurrent(INDICATOR_ID)
editor.indicatorClearRange(0, editor.getTextLength())

if my_state[my_file]:
    start_position = editor.positionFromLine(0)
    end_position = editor.getLineEndPosition(editor.getLineCount()-1)

    #console.write("lines:{}..{}, pos:{}..{}\n".format(start_line,end_line,start_position,end_position))

    editor.research(r'\#[[:xdigit:]]{6}\b',
                grab_color_and_paint_hex6,
                0,
                start_position,
                end_position)

    editor.research(r'\#[[:xdigit:]]{8}\b',
                grab_color_and_paint_hex8,
                0,
                start_position,
                end_position)

    editor.research(r'rgb\(\h*(\d+)\h*,\h*(\d+)\h*,\h*(\d+)\h*\)',
                grab_color_and_paint_rgbparen,
                0,
                start_position,
                end_position)

