## Changelog

### V2.0-pre1
Basically redesigned the entire bot
- Now responds to comments with predefined trigger words with Nute Gunray quotes
- Each trigger has an associated probability. For example, a trigger with a probability of 0.5 means that the bot will reply only in 50% of the cases that it finds the trigger
- Bot only replies once per thread, marking all following comments (and its own) as "replied" comments

The functionality to reply to two bots with the "this is getting out of hand" quote is removed for now. I was focusing on making the bot rules-compliant first. It will be added in again later

### V1.3.1
Preparing for the new character bot rules:
- Bot now includes an ignore list. This has to be updated manually for now
- New "ignore_file" entry in the config file

### V1.3
Complete overhaul of bot logic:
- Only replies once per thread now
- Saves non-bot comments in threads to prevent second reply in thread

Added config file