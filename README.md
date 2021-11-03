# Nute_gunray_bot
Because PrequelMemes does not have enough bots already...

`Current version: v1.0`

## What does it do?
[PrequelMemes](reddit.com/r/prequelmemes) has become infested with bots. They impersonate Obi-Wan Kenobi, Gonk droids, the Senate, etc. Sometimes, they even reply to each other. Thing seem to be getting out of hand.

That is why nute_gunray_bot exists: because things are getting out of hand. Each time a bot replies to another bot, nute_gunray_bot can reply with:

> This is getting out of hand, now there's two of them!

## How does it do this?
The bot is written using Python and [praw](https://praw.readthedocs.io/en/stable/). It gets the top 50 posts from hot, and one by one gets all their comments. It scans all comments to see if they were written by a bot (based on a list of known bots included with the bot). It also looks at the author of the parent comment. If both are bots, it replies with its characteristic phrase. 

I also tried to make the bot not **too** annoying: if there is for example an endless stream of gonks, it will only reply to the second comment in the thread, and not to every third, fourth, etc. 

## When does it do this?
The script in this repository runs once every hour. Since the bot tracks which comments have already been replied to, it can safely scan posts it has already scanned, without replying to double bots that already have their own Nute-comment. 

## Why publish the source?
In case you were wondering: it is **ABSOLUTELY NOT** so that more people can run the same bot. Please don't.
It is so that if something goes wrong, if it starts uncontrollably spamming threads, people can possibly see what's wrong even before I have time to look at it. It's also just nice for the people that are curious what's producing their spam exactly.

If you see something wrong with the bot, or just have a question or suggestion, you can reach me on Reddit on my main account: [svenkw](http://www.reddit.com/u/svenkw).

## Options for v1.1
Features and optimisations I could implement
- *Rolling reply buffer*: now, all comments that have been replied to are saved in one big file. Well, eventually, this might become a big file. And since the code must see if a certain comment ID is somewhere in the list, the longer the list is, the longer this will take. This might significantly slow down the bot performance over time. A solution could be to save the replied list for several days, and after a certain time just kick out the olders IDs to keep the list at a semi-fixed length.
- *Better logging*: This does not change anything for my fellow Redditors, but it might make it easier for me to troubleshoot the bot, and see if it is running appropriately. 
- *Proper config files*: Again, nothing for the end user, but it would be better than the current solution, which is a bunch of static variables at the start of the main python file.