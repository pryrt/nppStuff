Hello, and welcome to the FAQ Desk.

Many people ask questions about how to log in, why we require an account with Google, Facebook, ~~Twitter~~, or GitHub, and why we don't just have email/password login here.

(As of 2023-May-26, the Login With Twitter was disabled, because Twitter disabled free Twitter API access -- which includes login-with-Twitter.)

### How to Log In ###

To log in, go to the https://community.notepad-plus-plus.org/login page, and select one of the **Available Logins**, through one of those [OAuth](https://en.wikipedia.org/wiki/OAuth) / [SSO](https://en.wikipedia.org/wiki/Single_sign-on) providers ("OAuth" is the name of one system whereby you can log into one website using the credentials on another; "SSO" = "single sign on", a generic term for that kind of system).  

When you click on one of those links, you will be asked to log in to the _other_ website (if you aren't logged in already) and to give permission to "share your data" with the Notepad++ Community Forum.  After that, you will have an account here, and be logged in.  Other that the initial connection, you may occasionally have to re-login, but you'll just have to confirm with the provider that you still want to log in here.

### But the Alternative Logins say they will share my data!?!? ###

Only minimal information is shared.  If you have publicly shared a name or email address on your chosen OAuth/SSO provider, the Notepad++ Community Forum will copy that information over to initially populate your profile on this site.  However, you can change _any_ of that data by clicking on your profile icon in the upper right, and selecting **Edit Profile**; your username doesn't even have to match!  

Aside from that initial profile data, the only information we get from the OAuth provider is a response to "is this user still logged in and still allowing you to tell us whether they are logged in"?  The Forum gets back a "yes" or "no" response; on a "yes", you will be logged in here; on a "no", the login will fail.

### But I've never seen anyone else ask me to log in through OAuth! ###

Congratulations; you've avoided playing any Facebook games -- that's quite an accomplishment that you should be proud of. ;-)

Seriously: Many websites use OAuth, and allows cross-logging-in, so I'm surprised you've never seen _any_.  

* As I mentioned, any of the FarmSquirrel, BlowUpMyFriendsWords, or other popular Facebook games use them, as do "what celebrity does my dog look like" apps and "only 1/10 people can score 98.6% on this quiz".

* Many programming tools, like [Travis-CI](http://travis-ci.org/) and [Appveyor](http://appveyor.com/) allow you to use your GitHub credentials to log in, to make it easy to trigger automated code-checks when you commit your code to GitHub.

* imgur.com and similar image/file-sharing sites use OAuth providers.

The list goes on and on.  Maybe you haven't _noticed_ them before, but they are out there, and quite common.  And other than the Facebook games and quizzes, most are harmless.

### But I don't have an account on one of those ##

They are all free, so you could sign up for one.

### Why prefer not using email/password logins ###

The simple answer is that it's more work for us and more dangerous.

OAuth logins are much more secure than a system where your password and login information are stored on the Notepad++ Community server. Those OAuth providers have huge budgets and full-time-employed security teams working around the clock to keep your credentials secure; a mom-and-pop group like us have $0 and 0 employees to stay on top of such things, and _when_ the password-storage was hacked (notice I say _when_, not _if_), you and/or a multitude of other users here would be up-in-arms over the password breach. The safest for everybody is the current method – using OAuth through big-name organizations.

### But you _did_ allow username/password login ###

In the Spring of 2024, we briefly tried the experiment of signing up with just username/password here, bypassing the OAuth/SSO requirement.  Unfortunately, the amount of spam _drastically_ increased when we did.  Aside from the security described above, the OAuth/SSO providers provide an extra layer of technical barrier that prevents spammers from easily creating dummy accounts.  This extra protection turned out to be necessary to keep the Forum usable, so we have again disabled the username/password signup.  

If you signed up during that period and can no longer log in, create a new account using an OAuth/SSO provider; if you had made posts with the old account, send a chat message to @PeterJones, asking that he change the owner of your old posts over to your new account (making sure you confirm your old account name); upon such a request, he will check the metadata of your old and new accounts, and if he confirms that you appear to be the same actual user, he will change the posts over to the new account so that you keep the credit for your posts.

## Multiple login accounts ##

It is preferred that you only actively use a single account in the Forum.

If you _start_ the login process from the wrong OAuth provider (for example, you click the login-with-Google, but your original account was created with login-with-GitHub), it will create a new account here in the forum.  So try to avoid that.

However, if you login with your original/existing OAuth provider _first_ (so that you are logged in with your normal account) and then go to **Edit Profile**, the "Single Sign-On Services", you can associate your single Notepad++ Community Forum with each of the OAuth providers.  This is allowed, and even encouraged.  Doing this means that later, if you accidentally click "Google" instead of "GitHub" and both are associated with your account here, you will log into the same account.  This is useful for when you click on the wrong link (or cannot remember which OAuth provider you originally signed up with).  It's also useful if you've temporarily or permanently forgotten your credentials at one of the OAuth providers or decided to delete your account over there, you can still use one of the others to log in here (for example, if you have associated both GitHub and Google, but forgot your Google login, you could authenticate using the GitHub, then edit your profile here to remove the link to your Google account; if you ever created a replacement Google account, you could re-link it here when done).  

If you accidentally create a second account: once you realize you do, please pick _one_ of the accounts, and stick with that one -- it is recommended that you change the theme on the "wrong" account to some color scheme that you dislike, that makes it obvious when you log in using the wrong account, so that you can log out and then log back in using the correct OAuth provider / account.  A forum Administrator might even be able to help you associate any posts made with the "wrong" account back to your main account.

If you _intentionally_ create multiple accounts, please understand that it can cause confusion during conversations, and is rude to other users.  You are not allowed to use one of your accounts to upvote posts made by another of your accounts, nor may you upvote or downvote any post from multiple of your accounts -- one vote per user per post.  You are not allowed to "hide" behind alternate accounts.

## Anonymous Access ##

"I still don't like it.  Do I have to have an account here to participate?"

You can read any post without an account.  But to make a new topic or post a reply to an existing topic, you have to log in through one of the available providers.

-----

# Notification #

### How To Get Email Notifications ###

The forum has the feature to send email notifications upon replies, mentions, and a variety of other conditions.

To change the notification settings, click on your user icon, and choose **Settings**.  There, you can set whether or not to get the digest, and which notifications should be in-forum only, email only, or both in-form and via email.  

The forum will not email the notifications unless you have confirmed your email address.  To do this, click on your user icon, choose **Edit Profile**, then choose to **Change Email**.  Once you have entered a valid email address and hit **Submit**, the forum will attempt to email you.

Unfortunately, the forum emails do not always make it through; many users have complained that they have never received their confirmation email, whereas many others have no problems receiving the confirmation email.  If you don't receive it, it may have been routed to your spam folder; or your email provider may choose to not pass the email on to you when it receives it from the forum's mail-sending server.  Potential workarounds for those who don't receive it include checking spam folders, trying to change to a different email address (if you have another available -- preferably from a different email provider), or setting to an invalid email address and then changing it back to the correct address again (hitting **Submit** after each change).  You might also ask your email provider if they can be temporarily less-strict about what emails get sent to you (though that's a long shot).  None of those, however, are guaranteed to work.

(If you do change your email, please note that it only affects the sending of the confirmation, notification, and digest emails; it does not change how you log in.  As described above, you still log in with the Google, Facebook, ~~Twitter~~, or GitHub accounts, just like you did before the **Change Email**.)

The administrators of the forum have tried debugging the problem, but they are not email server experts, and as of yet they have not yet been able to improve the reliability beyond where it currently is[.](# "And despite multiple attempts by users, complaining loudly or pestering the administrators about it has not yet been successful in imparting the necessary skills to improve the administrator's results in this regard.")  Every once in a while, I am able to do some more research, and I try to give the administrators more ideas of things to fix, but it's a slow process for non-experts.  Improvements were made in Spring/Summer 2022, and it appears that the confirmation emails are now reaching at least some email providers that used to not receive the emails, but  we cannot guarantee that any given provider or specific address will be able to see the confirmation.

That said, the forum had worked for years without email notification before that feature started working (for some users) in 2021: the only thing that the email confirmation enables is the various email notifications and digest emails; every other feature of the forum works just fine without the confirmation message.  And as users who predated the 2021 email-enabling discovered back then, if you want to see if you have a reply to a post, you can always just log into the forum, and the notification bell icon will indicate if you have any in-forum notifications indicating replies.

If you are unable to get the confirmation email after this, then all I have left to offer is my own sincere apologies, and the apologies I convey on behalf of the other administrators.
