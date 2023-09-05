Hello, and welcome to the FAQ Desk.

In this FAQ entry, we will be covering how to format your posts in the Notepad++ Community Forum.

## Brief Summary

TL;DR: This forum uses a set of special characters (called "Markdown") in your post to format the text -- and for some formatting, you can use the toolbar on the post window to insert that formatting.  You should look at the **PREVIEW** window to help you make sure your post looks right before hitting **SUBMIT**.  Use the `</>` **Code** button on the toolbar for formatting multi-line example text.  Use backticks \` around the text for formatting text as `typewriter style`, which is useful for asking about regular expressions.

## Preview and Editing

The results of the Markdown syntax can be seen in the **PREVIEW** pane next to the post-editing pane.  If you cannot see the **PREVIEW** pane, click the **SHOW PREVIEW** in the upper-right of the editing input box.  Your post can only be edited for three minutes after you click **SUBMIT**, so make sure you use the **PREVIEW** to get the post looking correct _before_ you submit your post.

## Forum Toolbar

To make post-creation easy, there is an editor toolbar over the post-entry box, so you can just type your text in the entry, highlight a portion of text, and use the toolbar to apply formatting to that text.  If you click the button without selecting text first, it will put in some dummy text that will be formatted in that style, and you can just edit that text with whatever you're trying to say.  The screenshot below shows the buttons available, and tells what each of those buttons do.

![](https://community.notepad-plus-plus.org/assets/uploads/files/1687269718593-ce652379-4ede-4ac5-af76-ab3e2b322a42-image.png)

## Formatting

In a forum discussing the Notepad++ text editor, some of the most useful formatting for our posts are the blocks of multiple lines literal text (or "code") which is useful for sharing example text; or for formatting small strings `in your paragraph` to stand out using typewriter font in red, which is useful when talking about search and replace strings (regular expressions); and the ability to include images in your post to show screenshots of what you need help with; and the ability to make special characters in the forum lose their meaning by putting a backslash \ before the special character.

### Literal Text Blocks

![7584aac5-d690-46c5-8e8e-52f779d0c7de-image.png](https://community.notepad-plus-plus.org/assets/uploads/files/1633357286910-7584aac5-d690-46c5-8e8e-52f779d0c7de-image.png)  When you want to show us data from your editor window ("I have paragraphs X Y Z that I need help with"), you can use the `</>` button on the toolbar, which will insert \`\`\` on a line before and after your selected text.  When your text is between those lines of three backticks each, it will be formatted as a block of typewriter text

~~~txt
```
lines of
**example**
text
1*2*3
```
~~~
will render as
```
lines of
**example**
text
1*2*3
```

Aside from being formatted differently than the other parts of your post, it also has the benefit of telling the forum to display the literal characters, even when they would normally be special characters to the forum.  For example, typing 1\*2\*3 would normally show up in the forum as 1*2*3 with the 2 in italics because a single-asterisk before and after text is the formatting code for "italic" in the forum (see below)... but inside the literal text block shown above, it shows up as the actual characters.  

Also, normally, the forum takes `"quoted text"` and changes the quotes to "smart quotes" or "curly quotes" .  That's fine in a paragraph like this.  But if you are showing us the text you want to search-and-replace on, we cannot be sure whether the "smart quotes" were actually part of your data, or whether they were meant to be `"normal quotes"`.  If you use the literal text block in your post for sharing your example data, we can be sure that the text we see in your post is really the text you have.

**Extras**: For blocks of inline text, you can alternately use \~\~\~ instead of \`\`\`.  Also, on the line of \`\`\` or \~\~\~ before the literal text, you can actually also append a word to tell what kind of text, like `` ```txt ``, `` ```html ``, `` ```xml ``, or `` ```python ``.  This might not seem useful to you at first, but there are times when telling the forum what kind of text will help the forum display it better.  (You can search the internet for "[markdown code block language list](https://www.google.com/search?q=markdown+code+block+language+list)" to find other languages.)

### Red Typewriter Text in your paragraph

To get `red typewriter text` inside your paragraph, use `` `red typewriter text` ``.  Like the literal code blocks above, this will make the forum's special characters not do anything, so `` `1*2*3` `` will show up as `1*2*3`.  It also works so you can show raw HTML entities, so `` `<` `` will render as `<` (though entities in the forum confuse the forum's WYSIWYG editor, so if you edit a post with such text, the forum editor will convert it to the character; sorry, we can't fix that).

In the forum, we often use the `red typewriter text` for search and replace strings (regular expressions), so they stand out, and so that special characters come through.

### Special Characters

As mentioned above, the sequence 1\*2\*3 will show up as 1*2*3 with 2 in italics, because single asterisks \*  around text makes it italic.  To be able to show special characters, you can use a backslash \ before it, like 1\\\*2\\\*3 .  If you _need_ to include the special forum formatting characters in your normal text, that's how.  But really, you should be using literal text blocks and `red typewriter text` when giving us example text and regular expressions.

However, two sequences needs special attention, even inside of `red typewriter text` backslash open bracket or multiline literal text blocks: \\\\[ and \\\\].  The forum treats that more special than others, so backtick backslash open-bracket backtick \`\\\\[\` will render as just `[`, rather than the expected `\\[`; even worse, the forum PREVIEW tab makes it look like you got it right, but really, it still will be wrong in the final post. With the right number of escapes, it is possible to get it right; but if you have the backslash open-bracket in your example text or your regex, you might want to include a screenshot as well, to make sure you communicate it properly.  For a regular expression, where backslash bracket is used to tell the regex to search for a literal open-bracket, it might be best to use an alternate regex for matching the literal open-bracket or closed-bracked, like `\x5B` and `\x5D`, which will format properly in the forum and can be easily copy/pasted, but will still work in your regular expression in Notepad++'s search-and-replace.

Examples of the rendering:
backslash count | raw | in backticks | raw | in backticks
--|--|--|--|--
0 | ] | `]` | [ | `[`
1 | \] | `\]` | \[ | `\[`
2 | \\] | `\\]` | \\[ | `\\[`
3 | \\\] | `\\\]` | \\\[ | `\\\[`
4 | \\\\] | `\\\\]` | \\\\[ | `\\\\[`

The preview of that showed:
![40c67edc-fa38-488a-b1ee-6e6e295e1760-image.png](https://community.notepad-plus-plus.org/assets/uploads/files/1663090113277-40c67edc-fa38-488a-b1ee-6e6e295e1760-image.png) 

But that's not how it rendered, which actually showed up as:
![502969ef-7c34-4ac5-89bd-91a46b22d08f-image.png](https://community.notepad-plus-plus.org/assets/uploads/files/1663090162595-502969ef-7c34-4ac5-89bd-91a46b22d08f-image.png) 

Similar happens in code-text-blocks
```txt
0 | ]        | [
1 | \]        | \[
2 | \\]       | \\[
3 | \\\]      | \\\[
4 | \\\\]     | \\\\[
```

![7c8a96db-3960-4f04-96ea-4fc70102f330-image.png](https://community.notepad-plus-plus.org/assets/uploads/files/1663089851494-7c8a96db-3960-4f04-96ea-4fc70102f330-image.png) 

Further, **if you edit your post**, it will start collapsing backslashes, so they won't all be there when you start your edit, and it will again render incorrectly.

Because of that issue, if you're posting a regex in the forum, it's highly recommended to use `\x5B` and `\x5D` in regexes where you wanted to match a literal [ or ] .

### Entities

You can use HTML entities in your post.  So `&#x263a;` will render as &#x263a; .  

When you edit a post that had entities (correcting a typo or something), the forum software will "kindly" convert all those entities to the underlying characters, which is great... except when you had an entity inside the red-text back-ticks `` `&#x263a;` `` or inside a code/plaintext block (between \`\`\` rows): in that case, it will convert entities that you didn't intend, so the sentence
```
> For example, `☺` would be stored as `&#x263a;` or `π` as `&#x03C0;` .
```

would be rendered as

> For example, `☺` would be stored as `☺` or `π` as `π` .

(which is rather non-sensical) instead of the intended

> For example, `☺` would be stored as `&#x263a;` or `π` as `&#x03C0;` .

So **if you edit a post** that had entities inside red-text \`xxx\` or code/plaintext blocks, you will have to convert them back to entities, or they will render incorrectly.  Sorry.

### Non-breaking spaces

Also, it is known that characters like the non-breaking space (**NBSP**, U+0020) do _not_ make it through: if you paste the **NBSP** character in your example text, the forum will show it as a normal space when it renders, whether it's in the `red-text` or \`\`\` code blocks.  If your code includes non-breaking space characters (or other fancy space or newline characters or control characters or zero-width characters), you will want to use a screenshot of your text in Notepad++, with **View > Show Symbol > Show Non-Printing Characters** and **View > Show Symbol > Show Control Characters & Unicode EOL** options turned on.

### Images in your post

The easiest way to include a screenshot in your post is to use normal Windows methods to take the screenshot (for example, `Alt+PrintScreen` to grab the whole Notepad++ window, or use the Windows Snip & Sketch `Win+Shift+S` to grab smaller section of the screen), and then just use Windows paste `Ctrl+V` to paste it in your post.  

![1c1a19a5-5c66-4a33-98e6-e47a992c3aa7-image.png](https://community.notepad-plus-plus.org/assets/uploads/files/1633357334602-1c1a19a5-5c66-4a33-98e6-e47a992c3aa7-image.png) If you've already saved the screenshot as an image on your computer, you can use the **Upload Image** button on the toolbar to manually upload the image from your computer.  

![a8ca2516-1104-4a75-996d-1456b5d55ff6-image.png](https://community.notepad-plus-plus.org/assets/uploads/files/1633357616638-a8ca2516-1104-4a75-996d-1456b5d55ff6-image.png) If the image is on an external server, you can use the ![]() **Image** button to type `![alt text](image url)` in the forum, and then replace `image url` with the URL of the image; for example, `![](https://some.example.url/KOsSLNe.png)` . (_Please note_: the service `imgur.com` used to be used significantly in this forum, but in mid-2023, something happened between the forum's host and imgur's website, and we can no longer embed pictures from imgur in our posts.  We can link to them, using the link button in the forum, but you cannot see the "live" image from that service.  Sorry for the inconvenience.  If you have a service _like_ imgur, the URL they give you might be the wrapper page, like https://imgur.com/KOsSLNe, which won't properly work as an image in the forum; make sure you grab the URL for the imgage .gif or .png file itself; imgur calls it the "direct link".  But remember: embedding images from imgur itself does not work here anymore, though it might for other hosting services.  But it's easier to just paste the image directly in the forum anyway.)

### Other formatting

`**bold**` or `__bold__` will make your text **bold**

`*italic*` or `_italic_` will make your text _italic_

you can get a list with the **list** button, or putting asterisk-space `* ` or hyphen-space `- ` as the first characters on the line
```
* first bullet
* second bullet
```
* first bullet
* second bullet

Numbered lists with a number, then period or close-parenthesis, then a space
```
1. one
2. two

1) first
2) second
```
1. one
2. two

1) first
2) second

`~~strikethrough~~` will ~~strikethrough~~ your text


Headers: use one or more hashtags followed by a space and the text for the header.  The titles of posts are header one, so I generally stick with header two or lower inside a post:

```
## header two
### header three
#### header four
##### header five
```
## header two
### header three
#### header four
##### header five

\-----
## Other Markdown References

* https://daringfireball.net/projects/markdown/syntax
* https://community.notepad-plus-plus.org/topic/14262/how-to-markdown-code-on-this-forum/4
