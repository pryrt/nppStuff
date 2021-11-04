# -*- coding: utf-8 -*-

from Npp import editor

word_matches = []
def match_found(m): word_matches.append(editor.getTextRange(m.span(0)[0], m.span(0)[1]))
editor.research('\w+', match_found)
histogram_dict = {}
for word in word_matches:
    if word not in histogram_dict:
        histogram_dict[word] = 1
    else:
        histogram_dict[word] += 1
output_list = []
for k in histogram_dict: output_list.append('{}={}'.format(k, histogram_dict[k]))
output_list.sort()
editor.copyText('\r\n'.join(output_list))
