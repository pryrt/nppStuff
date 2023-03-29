# encoding=utf-8
"""in response to chat with Alan Kilborn

Alan suggested that I make a script to automatically generate the answer to a \
generic replace-in-region regex question, which basically stuffs the FR/RR/BSR/ESR
into Guy's formula.

I want to make it fancy enough to allow three modes:
    1) Normal -- requires distinct BSR/ESR
    2)

use [MailMerge.py](https://community.notepad-plus-plus.org/post/83683) as an example prompter
"""
from Npp import editor,notepad,console,MESSAGEBOXFLAGS

class cRiRR(object):
    def __init__(self):
        self.this_script_name = inspect.getframeinfo(inspect.currentframe()).filename.split(os.sep)[-1].rsplit('.', 1)[0]
        self.this_script_path_without_ext = inspect.getframeinfo(inspect.currentframe()).filename.rsplit('.', 1)[0]
        options = [
            'Normal = Distinct BSR/ESR',
            'OneLine = Do not extend beyond EOL',
            'Nested = Useful for nested quotes or {{}}'
        ]
        answers = self.ask_options('Enable options by putting an X in each [   ]', options)

    def ask_options(self, prompt_str, option_list):
        text_field = ''
        for opt in option_list:
            if len(text_field)>0: text_field = text_field + '\r\n'
            text_field = text_field + '[  ] ' + opt
        user_input = notepad.prompt(prompt_str, self.this_script_name, text_field)
        console.write('\r\n'*5+str(user_input))

if __name__ == '__main__': cRiRR()
