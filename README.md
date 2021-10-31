# Nute_gunray_bot
Because PrequelMemes does not have enough bots already...

## What does it do?
[PrequelMemes](reddit.com/r/prequelmemes) has become infested with bots. They impersonate Obi-Wan Kenobi, Gonk droids, the Senate, etc. Sometimes, they even reply to each other. Thing seem to be getting out of hand.

That is why nute_gunray_bot exists: because things are getting out of hand. Each time a bot replies to another bot, nute_gunray_bot can reply with:

> This is getting out of hand, now there's two of them!

## How does it do this?
I used Python and the Python Reddit API Wrapper (praw) to make a quick reddit bot. It just gets the top posts, retreives all comments, and looks if there are comments made by bots whose parent comment is also made by a bot. The bots are simply stored in a separate file, so there is no special functionality involved to see which users are bots and which aren't. 

## When does it do this?
I made this bot based on a comment I say somewhere on the sub, and I thought the idea was funny. However, it is meant to be funny, not annoying. So I decided to have the bot only check a post **once**. The IDs of the posts that have been checked are saved in a text file. I hope it simply takes a while before the file gets too large. 

For now, the bot takes the last 50 posts from new, and looks if the post has been up for a certain time. If it has, the comments are checked for some hot bot-on-bot action, and replies are made. Finally, the ID of the post is added to the list, and the bot moves on. If all posts are checked, it goes to sleep again. 

I plan to run the script every hour or so. More often would not really be helpful. 