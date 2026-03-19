# encoding=utf-8
"""
Bulk convert the N++ _source_ stylers/themes, so that C++ has ID+64 set to the INACTIVE variants of the styles
"""
from Npp import console
from pathlib import Path
import xml.etree.ElementTree as ET
import copy

console.show()
console.clear()

def editInPlace(p: str):
    #console.write(p + "\n")
    xmlTree = ET.parse(p)
    cpp = xmlTree.find(".//LexerStyles/LexerType[@name='cpp']")
    #console.write(f"{cpp.tag} {cpp.attrib}\n") # str(cpp.attrib)+"\n")
    new_styles = []
    for ws in cpp.findall('./WordsStyle'):
        if 'styleID' in ws.attrib and int(ws.attrib['styleID']) < 128:
            #console.write(f"- {ws.tag} {ws.attrib}\n")
            #console.write("- {}".format(ET.tostring(ws, encoding='unicode', method='xml', short_empty_elements=True)))

            new_ws = copy.deepcopy(ws)
            current_id = int(new_ws.attrib['styleID'])
            new_ws.set('styleID', str(current_id+64))
            current_name = new_ws.attrib['name']
            new_ws.set('name', f"{current_name} (INACTIVE)")
            #console.write("→ {}".format(ET.tostring(new_ws, encoding='unicode', method='xml', short_empty_elements=True)))

            def _clamp(v):
                if v<0:
                    return 0
                elif v>255:
                    return 255
                else:
                    return int(v)

            #TODO: for new_ws (and raw_ws), change color toward background
            def upd_clr(node):
                fg = int(node.get('fgColor', 'FFFFFF'), 16)
                bg = int(node.get('bgColor', '000000'), 16)
                fgr = (fg >> 16) & 0xFF
                fgg = (fg >> 8) & 0xFF
                fgb = (fg >> 0) & 0xFF
                bgr = (bg >> 16) & 0xFF
                bgg = (bg >> 8) & 0xFF
                bgb = (bg >> 0) & 0xFF
                #console.write(f"DBG FG:{fgr:02X} {fgg:02X} {fgb:02X} BG:{bgr:02X} {bgg:02X} {bgb:02X}")
                fgr = _clamp(fgr + (bgr-fgr)*0.65)
                fgg = _clamp(fgg + (bgg-fgg)*0.65)
                fgb = _clamp(fgb + (bgb-fgb)*0.65)
                fg = (fgr << 16) | (fgg << 8) | (fgb)
                #console.write(f" NEW FG:{fgr:02X} {fgg:02X} {fgb:02X} RGB:{fg:06X}\n")
                node.set('fgColor', f"{fg:06X}")

            upd_clr(new_ws)

            new_styles.append(new_ws)

            if current_name == 'STRING':
                raw_ws = copy.deepcopy(new_ws)
                raw_ws.set('styleID', str(20+64))
                raw_ws.set('name', "STRINGRAW (INACTIVE)")
                upd_clr(raw_ws)
                new_styles.append(raw_ws)

    if len(new_styles)>0:
        b4 = cpp.find("./WordsStyle[@styleID='128']")
        if b4 is not None:
            idx = list(cpp).index(b4)
            cpp[idx:idx] = new_styles # slice the new WordsStyle elements into cpp before the appropriate idx
        else:
            cpp.extend(new_styles)


    #### This almost does what I want, but messes up other LexerType contents (because of comments, etc)
    #ET.indent(xmlTree, space="    ")
    ##console.write(ET.tostring(xmlTree.getroot(), encoding='unicode', method='xml', short_empty_elements=True))
    #xmlTree.write(p, encoding='unicode', xml_declaration=True, short_empty_elements=True)
    #### so instead, just return the string for the cpp LexerType
    ET.indent(cpp, space="    ")
    return "=== {} =====\n{}\n".format(p, ET.tostring(cpp, encoding='unicode', method='xml', short_empty_elements=True))


directory = r'C:\usr\local\share\github\notepad-plus-plus\PowerEditor\installer\themes'
xml_files = [str(p.absolute()) for p in Path(directory).glob('*.xml')]
xml_files.insert(0, r'C:\usr\local\share\github\notepad-plus-plus\PowerEditor\src\stylers.model.xml')
#console.write(editInPlace(xml_files[0]))
for x in xml_files:
    console.write(editInPlace(x))

# editor.setProperty('lexer.cpp.track.preprocessor', 1)
