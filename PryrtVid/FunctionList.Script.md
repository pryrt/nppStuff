Hello. Welcome to PryrtVid.

In this video, I am going to walk you through how to develop a Function List for your particular programming language in Notepad++.

Notepad++ comes pre-bundled with many function list definitions (for most of the languages that Notepad++ recognizes)... but, as is common in Notepad++, you may want to create your own custom rules for a Function List, either for an existing language or for your own custom language (a UDL).

To get started, you'll want to bookmark a few pages:

https://npp-user-manual.org/docs/function-list/ 

This is the function list overview in the online Notepad++ User Manual.  It explains what the Function List feature does, gives some details about the various nodes in the XML configuration files (more on these later), and even goes into what's required if you want to submit your function list definition to be distributed with Notepad++.

https://npp-user-manual.org/docs/config-files/#function-list 

This explains the difference in the config files for function list for newer versions of Notepad++ (v7.9.1 and later) and older versions (v7.9 and earlier).  In this video, I will assume you have v7.9.1 or newer.

https://community.notepad-plus-plus.org/topic/19480/faq-desk-function-list-basics 

The Notepad++ Community Forum has a FAQ entry on the basics of function list behavior.  It gives the perspective of the Community's foremost expert on function lists.  It contains everything I am going to cover here, but much more succinctly.

For my example, I am going to be defining the Function List for a User Defined Language (UDL).

Defining a whole UDL is a subject for an entire video, so I won't cover all the details.  But if you don't have yours yet, we'll start with two things: create the UDL and give it a name, and associate an extension with it.

Go to the Language menu, User Defined Language, and Define Your Language.  Click "Save As" and give it a name: I will use `PryrtLanguage`.  Save this string.  Assume that PryrtLanguage files end in .pry, so we'll type `pry` into the Extension box (don't include the dot).  So anytime Notepad++ opens a `.pry` file, it will automatically choose the PryrtLanguage UDL.  That's it: that's as much as we need for our UDL definition to make Function List work right.

Next, we need to tell Notepad++ how to map that UDL to the configuration file for the function list.  We use the `overrideMap.xml`, which can be found in `%AppData%\Notepad++\functionList\overrideMap.xml`, which we can open in Notepad++.  Add the line
```
			<association id= "udl_pryrtlanguage.xml"	        userDefinedLangName="PryrtLanguage"/>
```
... right next to the other User Defined Languages.  Please note: the filename can be whatever you want it to be.  But the userDefinedLangName must match the name of your UDL exactly.  That's why I had you save the string earlier.

While we're here, you can point Notepad++ to a customized version for a built-in language as well.  The comments show examples, and you can just copy/paste the line for the language you want to change, and then change the filename for that language.  For example, if I have a different Function List for Perl called `my_perl.xml`, I can just copy the Perl language #21 row outside of the comments, and edit it to `my_perl.xml`.  The next time I restarted Notepad++, the Perl Function List would be controlled by `my_perl.xml` instead of `perl.xml`.  But we're not doing that now, so let's delete that.

Now, in the same folder as overrideMap, create the XML file to define your Function List -- it's easiest to just copy an existing one to a file that matches the name in the association-id.  Let's strip out all the old regex (unless you happened to pick a language that's very similar to your UDL).  And let's fill out the parser information: the display name can be anything, though it normally matches the name of the UDL, so `PryrtLanguage`.  The ID must be unique; often, just use an all-lowercase version of the displayName, sometimes with extra like `_syntax`.  The comment expression is a regular expression that will recognize comments -- this allows the parser to _not_ show you "functions" or "classes" that are inside a comment.  

For PryrtLanguage, comments happen to be anything after a hashtag to the end of the line, so `(?-s)#.*$` -- I used the modifier `(?-s)` to make sure that .* doesn't gobble up newlines.

Back on the Function List page, you saw me gloss over the differences between Function Parser, Class Parser, and Mixed Parser.  That's because we're going into more details on that now.

First, what's a "function" versus a "class". From the purposes of this parser, a "class" is just a name for a container -- it could be a "class" or an "object" or a "structure", or it might be whatever meaningful container might be in your language.
The function might be a subroutine, function, or method name; or it might be something else.  For example, in a markdown file, maybe you want headers to be "classes", and links to be the "functions".

