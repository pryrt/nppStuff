# encoding=utf-8
"""in response to https://notepad-plus-plus.org/community/topic/18512/

Convert this MACRO into PythonScript

        <Macro name="ADN Test" Ctrl="no" Alt="no" Shift="no" Key="0">
            <Action type="2" message="0"    wParam="43032" lParam="0" sParam=""  />   <!--  DELETE ALL styles        --> <!-- NPPM_ -->
            <Action type="0" message="2453" wParam="0"     lParam="0" sParam=""  />   <!--  Go to START of line      --> <!-- SCI_ NoString -->
            <Action type="1" message="2170" wParam="0"     lParam="0" sParam="A" />   <!--  Write the letter A       --> <!-- SCI_ YesString -->
            <Action type="1" message="2170" wParam="0"     lParam="0" sParam="T" />   <!--  Write the letter T       --> <!-- SCI_ YesString -->
            <Action type="1" message="2170" wParam="0"     lParam="0" sParam="G" />   <!--  Write the letter G       --> <!-- SCI_ YesString -->
            <Action type="1" message="2170" wParam="0"     lParam="0" sParam="C" />   <!--  Write the letter C       --> <!-- SCI_ YesString -->
            <Action type="0" message="2453" wParam="0"     lParam="0" sParam=""  />   <!--  Go to START of line      --> <!-- SCI_ NoString -->
            <Action type="0" message="2307" wParam="0"     lParam="0" sParam=""  />   <!--  Select the NEXT char     --> <!-- SCI_ NoString -->
            <Action type="2" message="0"    wParam="43022" lParam="0" sParam=""  />   <!--  Apply the 1st STYLE      --> <!-- NPPM_ -->
            <Action type="0" message="2306" wParam="0"     lParam="0" sParam=""  />   <!--  Hit the RIGHT key        --> <!-- SCI_ NoString -->
            <Action type="0" message="2307" wParam="0"     lParam="0" sParam=""  />   <!--  Select the NEXT char     --> <!-- SCI_ NoString -->
            <Action type="2" message="0"    wParam="43024" lParam="0" sParam=""  />   <!--  Apply the 2nd STYLE      --> <!-- NPPM_ -->
            <Action type="0" message="2306" wParam="0"     lParam="0" sParam=""  />   <!--  Hit the RIGHT key        --> <!-- SCI_ NoString -->
            <Action type="0" message="2307" wParam="0"     lParam="0" sParam=""  />   <!--  Select the NEXT char     --> <!-- SCI_ NoString -->
            <Action type="2" message="0"    wParam="43026" lParam="0" sParam=""  />   <!--  Apply the 3rd STYLE      --> <!-- NPPM_ -->
            <Action type="0" message="2306" wParam="0"     lParam="0" sParam=""  />   <!--  Hit the RIGHT key        --> <!-- SCI_ NoString -->
            <Action type="0" message="2307" wParam="0"     lParam="0" sParam=""  />   <!--  Select the NEXT char     --> <!-- SCI_ NoString -->
            <Action type="2" message="0"    wParam="43030" lParam="0" sParam=""  />   <!--  Apply the 5th STYLE      --> <!-- NPPM_ -->
            <Action type="0" message="2306" wParam="0"     lParam="0" sParam=""  />   <!--  Hit the RIGHT key        --> <!-- SCI_ NoString -->
            <Action type="0" message="2454" wParam="0"     lParam="0" sParam=""  />   <!--  Select to START of line  --> <!-- SCI_ NoString -->
            <Action type="0" message="2180" wParam="0"     lParam="0" sParam=""  />   <!--  Hit on the DELETE key    --> <!-- SCI_ NoString -->
        </Macro>

https://www.bioinformatics.org/sms2/random_dna.html

catctaaagggattagttcctgccctcatattcactatccgacccctttaactgtgatgt
cctcgctttttctcgtgagagctgtgaatctttgtgccgtttccaacaaggcctggagcc
ttttcaatgcttgagggtttcaccgcgggtctaacggatgctaagaaaggggtgcggagg
aagggtctttatgctggccgtcggcggttgagagctctgacctataccatggatcccgcg
agcgcggttacgggcaataagggcctcactatgcctcgaacacattgtggacaaagtgta
gtcgaacccacacacgcgcgagactttagggtgtcgaacagtaccatctaattgatggga
agaaatggtttcgtaccacccccgtcgctcagcttagacgggccagagaggggatgggtg
gtcagtggcgtcggttggtgaccgtagaattcgttacagagcgatgttgtatagcttttt
agacgtaggctagcgttttaacttctacaactccagtgattgggttgatggtctgtttgc
ttaccagtcaggtcagctcccgctcatggttctctcgcaaattacttggtcacaccgtga
aagctccacgcaaactaatagtgggattctacactaaagggcgtcactatcacttcttat
acattatagacgtaactacagtagacatactcgcaagcccgctaacgggagcacagatgt
tgagggtatcagcttctgcgactcgggctggatccgatatttttatgcaatgcatctgag
actggcctccctgctacctctacggaagctggtacgaagcgcgctgccttcgactgaaac
ttgcatgcataagttaatgtagtgcagcgcaggtcagccaacataagtagtgagcccagc
cgctggcaggacagttgtcgcggtaaatcacacgtgtggtgaccatctccccatttacag
gtgttagaaaagcaacttcgtattaatccattaatctgag


"""

notepad.menuCommand(43032)      #   <!--  DELETE ALL styles        -->      IDM_SEARCH_CLEARALLMARKS = Search > Unmark All > Clear All Styles
editor.vCHomeWrap()             #   <!--  Go to START of line      -->
editor.replaceSel("A")          #   <!--  Write the letter A       -->
editor.replaceSel("T")          #   <!--  Write the letter T       -->
editor.replaceSel("G")          #   <!--  Write the letter G       -->
editor.replaceSel("C")          #   <!--  Write the letter C       -->
editor.vCHomeWrap()             #   <!--  Go to START of line      -->
editor.charRightExtend()        #   <!--  Select the NEXT char     -->
notepad.menuCommand(43022)      #   <!--  Apply the 1st STYLE      -->      Search > Mark All > Using 1st Style
editor.charRight()              #   <!--  Hit the RIGHT key        -->
editor.charRightExtend()        #   <!--  Select the NEXT char     -->
notepad.menuCommand(43024)      #   <!--  Apply the 2nd STYLE      -->      Search > Mark All > Using 2nd Style
editor.charRight()              #   <!--  Hit the RIGHT key        -->
editor.charRightExtend()        #   <!--  Select the NEXT char     -->
notepad.menuCommand(43026)      #   <!--  Apply the 3rd STYLE      -->      Search > Mark All > Using 3rd Style
editor.charRight()              #   <!--  Hit the RIGHT key        -->
editor.charRightExtend()        #   <!--  Select the NEXT char     -->
notepad.menuCommand(43030)      #   <!--  Apply the 5th STYLE      -->      Search > Mark All > Using 5th Style
editor.charRight()              #   <!--  Hit the RIGHT key        -->
editor.vCHomeWrapExtend()       #   <!--  Select to START of line  -->
editor.clear()                  #   <!--  Hit on the DELETE key    -->

# use notepad.menuCommand(43032) or Search > Unmark All > Clear All Styles to clear the styles when done