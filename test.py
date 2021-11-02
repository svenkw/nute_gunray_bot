import praw

reddit = praw.Reddit('nute_gunray_bot', user_agent="script:This is getting out of hand v0.2")

with open("bot_data/post_blacklist", 'a+') as f:
    for post in reddit.subreddit("prequelmemes").hot(limit=5):
        f.write(post.id + "\n")