# -*- coding: utf-8 -*-
try:
    tpm
except NameError:
    pass
else:
    tpm.close_all_untitled_regardless_of_modified_state()