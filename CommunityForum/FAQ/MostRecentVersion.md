# FAQ: Why Can't I Just Say "Most Recent Version"

Hello.  You've likely been directed here because you had a request for help where you said "I use the most recent version".  Despite what you might think, that's _not_ actually enough to tell us what version of Notepad++ you are using.

## Quick Version:

The best idea is to always look at the **?**-menu's **Debug Info**, copy that to clipboard, and paste it into your post in the Forum.  This is best practice.

## Details

But _why_ isn't "most recent version" sufficient?

### It's Ambiguous

There are actually multiple versions at a time that can be reasonably considered "the most recent", and we don't know which you are talking about.

1. If you have automatic updates turned on, Notepad++ only polls every couple of weeks, to avoid overloading the server with "do I have the most recent version" request.  So if a version was released and triggered for automatic updates between the time Notepad++ last polled for automatic updates and now, you might not have the most recently released and triggered version, even though you have automatic updates enabled.  Thus, having automatic updates turned on is not a guarantee you have the most recent version, despite what some people think.
2. There is the version available using **?**-menu's **Update Notepad++** action. This _can_ be "most recent", but isn't _necessarily_ the "most recent".  This forces checking the server for a new version, so can be more recent than just having automatic updates turned on.  However, per the User Manual's description of [Upgrading](https://npp-user-manual.org/docs/upgrading/), new versions aren't triggered for update immediately, and not all versions are ever triggered for auto-update.  As described there, if a released version is in the 1-2 week buffer between initial release and triggering auto-update, or if a released version is discovered to have critical regressions or bugs, a given version might have been released, but not triggered for automatic update, so **? > Update Notepad++** won't show it.
3. There is the newest version available on the official [Notepad++ downloads page](https://notepad-plus-plus.org/downloads/).  This is _normally_ the most recent official release, whether or not is has been triggered for automatic update.  However, for some _critical_ bugs found, the Developer may remove a version from that page, even though it used to be there.  So someone who downloaded the version before it was removed would disagree as to what version is "most recent".
4. There are sometimes "Release Candidate" versions, which have been publicly linked [Community Forum "Announcements" section](https://community.notepad-plus-plus.org/category/1/announcements) by the Developer.  These are similar to "beta" versions, and are announced before they are uploaded to the official [Notepad++ downloads page](https://notepad-plus-plus.org/downloads/), so that readers of the Forum can check the Release Candidate for major regressions or new bugs that the Developer didn't notice.

All three of those can be validly considered "most recent".  If you don't tell us an exact version number, we cannot know which of those three meanings is your meaning.  (And to be blunt, some people occasionally haven't actually checked recently, and so they think it's the most

### It's _Still_ Ambiguous


Even if you tell us "I am using vX.Y.Z", that is not sufficient.  Notepad++ has three different executables for a given release version: 32-bit, normal 64-bit, and 64-bit ARM -- referred to as "bitness".  Some bugs show up in only one of those three variants of the same version.  Thus, it's actually necessary for you to specify which executable you are using for a given version.

### It's Not Sufficient

Even if you tell us "I am using vX.Y.Z with bitness B", that is not sufficient.  For many issues, it's actually a plugin's fault, and isn't solely dependent on the version and bitness of Notepad++.  Thus, you need to list all the plugins.  These are listed in the **Debug Info**.

And sometimes, there are other settings or environmental factors which are shared in **Debug Info** that will help us to help you.

Thus, the easiest way to give _all_ this information is to share your **? > Debug Info** instead of just saying "most recent version".

### It's Not Future-Proof

Further, without being explicit about version, your question and our replies are not future proof.  Someone who comes a week or a month or a year later and reads your question cannot easily know which version was "the newest version" at the time you asked your question; they only have a reasonable idea of what they think the "most recent version" is when they are reading your discussion, and thus it means something different to them than it did to you.  Thus, if they see that you had a problem with "the most recent version", they have no idea whether they are using the same version, and whether any fixes or workarounds described in the continued discussion will apply to them.  

## Conclusion

**? > Debug Info** is not ambiguous.  **? > Debug Info** contains bitness information and plugin information and system information.  **? > Debug Info** is future-proof.  Thus, the best idea is to share **? > Debug Info** when you need to supply us with what version you are using.  Anything less, and you are likely to be pointed to this FAQ.
