# -*- coding: utf-8 -*-
from __future__ import print_function

#########################################
#
#  MacroDisassemblerForNpp (MDFN)
#
#########################################

#-------------------------------------------------------------------------------

from Npp import *
import inspect
import os
import xml.etree.ElementTree as et  # https://docs.python.org/3/library/xml.etree.elementtree.html
from datetime import datetime as dt
import DisassemblerData as dd

#-------------------------------------------------------------------------------

find_msg_cracker_dict = {
    1601 : {
        'name' : 'find_what',
        'where' : 'sParam',
    },
    1602 : {
        'name' : 'replace_with',
        'where' : 'sParam',
    },
    1625 : {
        'name' : 'mode',
        'where' : 'lParam',
        'numeric_value_to_str' : {
            0 : 'normal',
            1 : 'extended',
            2 : 'regex',
        },
    },
    1652 : {
        'name' : 'filters',
        'where' : 'sParam',
    },
    1653 : {
        'name' : 'directory',
        'where' : 'sParam',
    },
    1700 : {
        'name' : 'initialize',
    },
    1701 : {
        'name' : 'execute',
        'where' : 'lParam',
        'numeric_value_to_str' : {
            1    : 'find_next',
            1608 : 'replace',
            1609 : 'replace_all',
            1614 : 'count',
            1615 : 'mark',
            1633 : 'clear_marking',
            1635 : 'replace_in_open_tabs',
            1636 : 'find_in_open_tabs',
            1641 : 'find_in_active_tab',
            1656 : 'find_in_files',
            1660 : 'replace_in_files',
            1665 : 'replace_in_projects',
            1666 : 'find_in_projects',
        },
        'numeric_value_to_relevant_options' : {
            1    : 1 | 2 |                          256 | 512 | 1024,             # find_next
            1608 : 1 | 2 |                          256 | 512 | 1024,             # replace
            1609 : 1 | 2 |                    128 | 256 | 512 | 1024,             # replace_all
            1614 : 1 | 2 |                    128 | 256 | 512 | 1024,             # count
            1615 : 1 | 2 | 4 | 16 |           128 | 256 | 512 | 1024,             # mark
            1633 :             16 |           128 | 256 | 512       ,             # clear_marking
            1635 : 1 | 2 |                                      1024,             # replace_in_open_tabs
            1636 : 1 | 2 |                                      1024,             # find_in_open_tabs
            1641 : 1 | 2 |                                      1024,             # find_in_active_tab
            1656 : 1 | 2 |          32 | 64 |                   1024,             # find_in_files
            1660 : 1 | 2 |          32 | 64 |                   1024,             # replace_in_files
            1665 : 1 | 2 |                    128 | 256 | 512 | 1024,             # replace_in_projects
            1666 : 1 | 2 |                    128 | 256 | 512 | 1024,             # find_in_projects
        },
    },
    1702 : {
        'name' : 'options',
        'where' : 'lParam',
        'bit_weights_numeric_value_to_str' : {
            1 : 'whole_word',
            2 : 'match_case',
            4 : 'purge_before',
            16 : 'bookmark_line',
            32 : 'in_subfolders',
            64 : 'in_hidden',
            128 : 'in_selection__OR__project1',
            256 : 'wrap_around__OR__project2',
            512 : 'backward_dir__OR__project3',
            1024 : 'dot_matches_newline',
        },
    },
}

#-------------------------------------------------------------------------------

class MDFN(object):

    def __init__(self):

        self.debug_on = True if 1 else False  # don't use this variable elsewhere, use "self.dprint()" or "if self.debugging_on():"
        self.this_script_name = inspect.getframeinfo(inspect.currentframe()).filename.split(os.sep)[-1].rsplit('.', 1)[0]
        self.this_script_path_without_ext = inspect.getframeinfo(inspect.currentframe()).filename.rsplit('.', 1)[0]
        self.turn_debug_on_file = self.this_script_path_without_ext + '__DebugON.cfg'
        self.turn_debug_off_file = self.this_script_path_without_ext + '__DebugOFF.cfg'
        #with open(self.turn_debug_on_file, 'w') as f: pass  # easy create file; don't leave this enabled!

        plugin_config_dir = notepad.getPluginConfigDir()
        npp_config_dir = os.path.join(plugin_config_dir, '..' + os.sep + '..')
        #self.dprint('npp_config_dir:', npp_config_dir)

        shortcuts_xml = os.path.abspath(os.path.join(npp_config_dir, r'shortcuts.xml'))
        #self.dprint('shortcuts_xml:', shortcuts_xml)
        assert os.path.isfile(shortcuts_xml)

        notepad.new()
        eol = [ '\r\n', '\n', '\r' ][ editor.getEOLMode() ]

        macro_node_format_template = '<Macro name="{name}" Ctrl="{Ctrl}" Alt="{Alt}" Shift="{Shift}" Key="{Key}">{comment}'
        action_node_format_template = '    <Action type="{type}" message="{message}" wParam="{wParam}" lParam="{lParam}" sParam="{sParam}" />' + eol + '        {comment}'

        root = et.parse(shortcuts_xml)

        line_output_list = []

        for macro_node in root.iter('Macro'):

            #self.dprint('mac node:', macro_node.attrib)

            key_comment = ''
            key = int(macro_node.attrib['Key'])
            if key != 0:
                key_comment = '    '
                if key not in dd.key_id_to_key_str_dict:
                    key_comment += 'unknown-key:{}'.format(key)
                else:
                    virtual_key_str = dd.key_id_to_key_str_dict[key]
                    key_modifiers = ''
                    if macro_node.attrib['Shift'] == 'yes': key_modifiers += '+'
                    if macro_node.attrib['Ctrl'] == 'yes': key_modifiers += '^'
                    if macro_node.attrib['Alt'] == 'yes': key_modifiers += '%'
                    if len(key_modifiers) > 0: key_comment += key_modifiers + '('
                    key_comment += virtual_key_str
                    if len(key_modifiers) > 0: key_comment += ')'
            macro_node.attrib['comment'] = key_comment

            #self.dprint(macro_node_format_template.format(**(macro_node.attrib)))

            line_output_list.append('')  # create a blank line between macros in output
            line_output_list.append(macro_node_format_template.format(**(macro_node.attrib)))

            for action_node in macro_node.iter('Action'):

                #self.dprint('act node:', action_node.attrib)

                if '\r' in action_node.attrib['sParam']: action_node.attrib['sParam'] = action_node.attrib['sParam'].replace('\r', '\\r')
                if '\n' in action_node.attrib['sParam']: action_node.attrib['sParam'] = action_node.attrib['sParam'].replace('\n', '\\n')

                msg = int(action_node.attrib['message'])
                wp = int(action_node.attrib['wParam'])

                action_comment = ''

                if msg in dd.cmd_id_to_cmd_str_dict:

                    action_comment += dd.cmd_id_to_cmd_str_dict[msg]

                elif wp in dd.cmd_id_to_cmd_str_dict:

                    action_comment += dd.cmd_id_to_cmd_str_dict[wp]

                elif msg in find_msg_cracker_dict:

                    value_str = ''

                    if 'where' in find_msg_cracker_dict[msg]:

                        which_attrib_has_this_msgs_data = find_msg_cracker_dict[msg]['where']

                        the_data = action_node.attrib[which_attrib_has_this_msgs_data]

                        if 'numeric_value_to_str' in find_msg_cracker_dict[msg]:
                            numeric_data = int(the_data)
                            if numeric_data in find_msg_cracker_dict[msg]['numeric_value_to_str']:
                                value_str = find_msg_cracker_dict[msg]['numeric_value_to_str'][numeric_data]
                            else:
                                value_str = 'BOGUS-NUMERIC-VALUE'

                        elif 'bit_weights_numeric_value_to_str' in find_msg_cracker_dict[msg]:
                            value_str = ''
                            numeric_data = int(the_data)
                            running_single_bitweight = 1
                            search_options_str_list = []
                            while numeric_data != 0:
                                if (numeric_data & running_single_bitweight) != 0:
                                    search_options_str_list.append(find_msg_cracker_dict[msg]['bit_weights_numeric_value_to_str'][running_single_bitweight])
                                numeric_data &= ~running_single_bitweight
                                running_single_bitweight <<= 1
                            value_str += '/'.join(search_options_str_list)

                    if len(value_str) > 0: value_str = ':' + value_str

                    action_comment += 'SEARCH:' + find_msg_cracker_dict[msg]['name'] + value_str

                else:

                    action_comment += 'unknown-action'

                action_node.attrib['comment'] = action_comment

                action_node.attrib['sParam'] = action_node.attrib['sParam'].encode('utf-8')  # trouble if unicode data in sParam; fix

                #self.dprint(action_node_format_template.format(**(action_node.attrib)))
                line_output_list.append(action_node_format_template.format(**(action_node.attrib)))

        document_text = eol.join(line_output_list) + eol
        editor.setText(document_text)
        editor.setSavePoint()

    def print(self, *args, **kwargs):
        try:
            self.print_first
        except AttributeError:
            self.print_first = True
        if self.print_first:
            console.show()      # this will put input focus in the PS console window, at the >>> prompt
            #console.clear()
            editor.grabFocus()  # put input focus back into the editor window
            self.print_first = False
        d_tag = ''
        if 'debug' in kwargs:
            now = dt.now()
            hr = now.strftime('%I')
            if hr[0] == '0': hr = hr[1:]
            ap = 'p' if now.strftime('%p')[0] == 'P' else 'a'
            ms = now.strftime('%f')[:3]
            d_tag = now.strftime('<%a{hr}:%M:%S{ap}.{ms}>'.format(hr=hr, ap=ap, ms=ms))
            del kwargs['debug']
        print(self.__class__.__name__ + d_tag + ':', *args, **kwargs)

    def debugging_on(self): return (self.debug_on or os.path.isfile(self.turn_debug_on_file)) and not os.path.isfile(self.turn_debug_off_file)

    def dprint(self, *args, **kwargs):  # debug print function
        if self.debugging_on():
            kwargs['debug'] = True
            self.print(*args, **kwargs)

#-------------------------------------------------------------------------------

if __name__ == '__main__': MDFN()
