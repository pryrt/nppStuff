# updateStylers

Notes and ideas for trying to bring my stylers/themes/langs updater into the N++ core.

## 2024-Oct-18

My idea would be for either a specific menu command, or maybe wherever Notepad++ saves styler and similar, would then read .model. and try to bring in any missing nodes into the structure...

So the XML is read or written by TinyXML, and the `_pXmlUserStylerDoc` and `_pXmlDoc` are the pointers to those two objects (the name of the langs.xml object instance pointer isn't overly informative).
- `Parameters.cpp NppParameters::writeStyles()` is what saves the styler (or theme)
  - loaded by `Parameters.cpp load()`, or on-demand using `reloadStylers()`
- `Parameters.cpp NppParameters::insertTabInfo()` is what saves the langs.xml
  - loaded by `Parameters.cpp load()`
- So if I wanted to hook into there, I could either
  - Do the audit when it first loads, so that it's ready from the beginning, and the write will just "be right".  This would also mean that StyleConfigurator would be correct from load
  - Or do the audit when it's going to save it anyway
  - Or only do the audit on demand (menu option) then manually call the save-it functions to force the write
    - if it's on demand, maybe I could use the `reloadStylers()` as an example of how to force it to update Style Configurator.  Or, maybe even better, if I update the XML, write it to disk, then call `reloadStylers()`, it would automatically do it.
    - I really think on-demand would have the best chance of Don approving it

- TinyXML Docs
  - main: https://www.cs.cmu.edu/~preethi/src/tinyxml/docs/
  - node (parent class): https://www.cs.cmu.edu/~preethi/src/tinyxml/docs/classTiXmlNode.html
    - `->Value()` returns different things for different subclasses (filename for document, element name, comment text, tag contents, node text)
  - document (subclass): https://www.cs.cmu.edu/~preethi/src/tinyxml/docs/classTiXmlDocument.html
