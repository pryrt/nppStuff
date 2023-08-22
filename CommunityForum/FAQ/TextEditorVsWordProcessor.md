Hello, and welcome to the FAQ Desk.

You have likely been directed here because you have asked about something that implies you don't fully understand or appreciate the difference between a [Text Editor](https://en.wikipedia.org/wiki/Text_editor) and a [Word Processor](https://en.wikipedia.org/wiki/Word_processor_program).

Notepad++ is a Text Editor, not a Word Processor or Desktop Publishing software.

## Differences between Text Editor and Word Processor

To quote from the Wikipedia [Text Editor](https://en.wikipedia.org/wiki/Text_editor) article,
|---|
|There are important differences between plain text (created and edited by text editors) and rich text (such as that created by word processors or desktop publishing software).|
|Plain text exclusively consists of character representation. Each character is represented by ... _[a sequence of]_ bytes, in accordance to specific character encoding conventions, such as ASCII, ... , UTF-8, or UTF-16. These conventions define many printable characters, but also non-printing characters that control the flow of the text, such as space, line break, and page break. Plain text contains no other information about the text itself, not even the character encoding convention employed. Plain text is stored in text files, although text files do not exclusively store plain text. ...|
|Rich text, on the other hand, may contain metadata, character formatting data (e.g. typeface, size, weight and style), paragraph formatting data (e.g. indentation, alignment, letter and word distribution, and space between lines or other paragraphs), and page specification data (e.g. size, margin and reading direction). Rich text can be very complex. Rich text can be saved in binary format (e.g. DOC), text files adhering to a markup language (e.g. RTF or HTML), or in a hybrid form of both (e.g. Office Open XML).|
|Text editors are intended to open and save text files containing either plain text or anything that can be interpreted as plain text, including the markup for rich text or the markup for something else (e.g. SVG) _[or source code for programming]_.|

(Text was copied 2023-Aug-22.  Text in _[brackets]_ was added or reworded compared to the quoted text.  Elipses `...` indicate text that was removed from the quoted text.)

## A Text Editor Cannot ...

Things you cannot do in a Text Editor (without using a markup/markdown language):
- Set specific text as "bold" or "italic"
- Set specific text as "red" or "green" or "yellow background"
- Set specific text as "headers" or "footnotes"
- Making tables / spreadsheets that don't use text-based `│─┌...` characters for the borders
- Embed images that you can see in Notepad++ inline with the text you are editing

## A Text Editor Can ...

Things you can do in a Text Editor if you are writing in HTML or Markdown or similar markup languages:
- Set specific text to be "bold" or "italic" using markup codes like `<b>text</b>` or `**bolded in markdown**`, and have the Text Editor show you those codes while you are editing, but the codes won't be visible when being rendered by an external tool (such as your web browser)
- Set specific text to be "red" or "yellow background" if the markup language supports it, like `<span style="color: red">...</span>`, and have the Text Editor show you those codes while you are editing, but the codes won't be visible when being rendered by an external tool (such as your web browser)
- Set specific text to be "headers" or similar if the markup language supports it, like `<h1>header</h1>` or `## Level 2 Header`, and have the Text Editor show you those codes while you are editing, but the codes won't be visible when being rendered by an external tool (such as your web browser)
- Making tables using appropriate markup, like `<table>` syntax in HTML or markdown tables, and have the Text Editor show you those codes while you are editing, but the codes won't be visible when being rendered by an external tool (such as your web browser)
- Embedding images that you can see in the browser or other renderer, but not inside Notepad++ in the text editing portion of the application.

With a good Text Editor like Notepad++, you can have syntax highlighting, so that those codes will show up differently than normal text, and for some, it will even apply the natural formatting you'd expect, as well as showing the codes.  And Notepad++ has plenty of plugins which can help with rendering your markup in a window or panel inside Notepad++ (though it won't be rendered in the same panel as you are doing the editing, because it's a Text Editor, not a WYSIWYG editor), and some of those plugins can add buttons to the toolbar to automatically add the formatting codes on selected text.

## But why not make Notepad++ do that?

Or, put another way, "but why can't you put in some hidden codes that would cause Notepad++ to format text in a particular way?"  Because that would change Notepad++ from a Text Editor to a Word Processor, and the not-quite-text files edited by that theoretical Notepad++ would no longer be actual text files.  Notepad++ is and always will be a Text Editor, not a Word Processor.

If you need a Word Processor, use a Word Processor, not a Text Editor.
