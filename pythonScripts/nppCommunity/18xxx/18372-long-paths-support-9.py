# encoding=utf-8
"""https://community.notepad-plus-plus.org/topic/18372/long-paths-support/9 by @Alan-Kilborn"""

import os

def T__main():
    cwd = os.getcwd()
    if not cwd.endswith(os.sep): cwd += os.sep
    temp = 'len_test_XXX_Y.txt'
    accum = 'a'
    for l in range(1, 1000):
        really_temp = temp.replace('Y', accum)
        really_temp = cwd + really_temp
        count_str = '{0:03}'.format(len(really_temp))
        really_temp = really_temp.replace('XXX', count_str)
        with open(really_temp, 'w') as f: f.write(count_str + '\n')
        if len(really_temp) > 265: break
        accum += 'a'

T__main()