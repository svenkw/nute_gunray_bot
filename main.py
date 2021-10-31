from os import scandir
import praw
from praw.models import MoreComments
from time import time

# Parameters
NUM_POSTS = 63
BOT_FILE = "bot_data/bot_list"
SCANNED_FILE = "bot_data/scanned_posts"
SCORE_LIMIT = 0
MIN_POST_AGE = 10

REPLY = True

def check_post_age(post):
    created = post.created_utc
    
    # post_age in hours
    post_age = (time() - created)/3600

    return post_age

def get_scanned_posts():
    with open(SCANNED_FILE, 'r') as f:
        scanned_posts = f.read().splitlines()

    return scanned_posts

def add_post_to_list(post_id):
    with open(SCANNED_FILE, 'a+') as f:
        f.write(post_id + "\n")

def get_bot_list():
    with open(BOT_FILE, 'r') as f:
        bot_list = f.read().splitlines()

    return bot_list

def comment_author_dict(comment_list):
    ca_dict = dict()
    for comment in comment_list:
        if isinstance(comment, MoreComments):
            pass
        else:
            ca_dict[comment.id] = comment.author

    return ca_dict

def get_double_bot_comments(post, ca_dict):
    count = 0
    for comment in comment_list:
        if isinstance(comment, MoreComments):
            pass
        else:
            comment_author = comment.author
            if comment_author in bot_list:
                if comment.parent_id[:3] == "t3_":
                    # Top level comment, so no parent, and therefore no two of them
                    pass
                else:
                    comment_parent_author = ca_dict[comment.parent_id[3:]]
                    if comment_parent_author in bot_list:
                        #print(f"{comment.author} responded to {comment_parent_author} with \"{comment.body}\"")
                        if REPLY:
                            comment.reply("This is getting out of hand, now there are two of them!")
                        
                        count +=1
    return count

# Create Reddit instance
reddit = praw.Reddit('nute_gunray_bot', user_agent="script:This is getting out of hand v0.1")

# Read the names of the active bots on PrequelMemes from file
bot_list = get_bot_list()

# Get a list of all the post IDs that have already been scanned
scanned_posts = get_scanned_posts()

# Start scanning
for post in reddit.subreddit("prequelmemes").new(limit=NUM_POSTS):

    if post.id in scanned_posts:
        print("already scanned")
        pass
    elif check_post_age(post) < MIN_POST_AGE:
        print(f"post too young, it is only {check_post_age(post)} hours old")
        pass
    else:
        print(f"Starting examining post with title \"{post.title}\"")
        comment_list = post.comments.list()

        ca_dict = comment_author_dict(comment_list)

        count =get_double_bot_comments(comment_list, ca_dict)
        print(f"{count} bot-on-bot conversations")

        add_post_to_list(post.id)