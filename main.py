import praw
from os import chdir
from praw.models import MoreComments
import json

# Try to change directory to home/pi/nute_gunray_bot on pi
# If it doesn't work, it's not running on the pi
# So we don't have to change the directory anyways
try:
    chdir("/home/pi/nute_gunray_bot")
except:
    print("not running on pi")
    pass

# Get config from config.json file
# Config.json in gitignore to have separate configs for local testing and running on pi
with open("config.json") as f:
    config = json.load(f)
    BOT_FILE = config["bot_list"]
    REPLIED_FILE = config["replied_file"]
    BLACKLIST_FILE = config["blacklist_file"]
    IGNORE_FILE = config["ignore_file"]
    NUM_POSTS = config["num_posts"]
    REPLY = config["reply"]
    VERSION = config["version"]

# Logging setup
replied_counter = 0
skipped_counter = 0
post_counter = 0

# =====================================
# Get stored information from files
# =====================================
def get_replied():
    with open(REPLIED_FILE, 'r') as f:
        replied = f.read().splitlines()
    
    return replied

def get_bot_list():
    with open(BOT_FILE, 'r') as f:
        bot_list = f.read().splitlines()

    return bot_list

def get_blacklist():
    with open(BLACKLIST_FILE, 'r') as f:
        post_blacklist = f.read().splitlines()
    return post_blacklist

def get_ignore_list():
    with open(IGNORE_FILE, 'r') as f:
        ignore_list = f.read().splitlines()
    return ignore_list


# =====================================
# Functions for the main loop
# =====================================
def get_dict(comment_list):
    """
    Creates a dictionary where every comment ID is matched with an author
    """
    ca_dict = dict()
    for comment in comment_list:
        if isinstance(comment, MoreComments):
            pass # do nothing for MoreComments instances
        else:
            # add id-author pair
            ca_dict[comment.id] = comment.author

    return ca_dict

def check_ignore_list(comment, ignore_list):
    if comment.author in ignore_list:
        return True
    
    return False

def check_top_level(comment):
    if comment.parent_id[:3] == "t3_":
        return True

    return False

def check_replied_self(comment, replied):
    if comment.id in replied:
        return True

    return False

def check_replied_parent(comment, replied):
    parent_id = comment.parent_id[3:]
    if parent_id in replied:
        return True

    return False

def add_replied_self(comment):
    with open(REPLIED_FILE, 'a+') as f:
        f.write(comment.id + "\n")

def add_replied_parent(comment):
    with open(REPLIED_FILE, 'a+') as f:
        f.write(comment.parent_id[3:] + "\n")

def check_bot_self(comment, bot_list):
    if comment.author in bot_list:
        return True

    return False

def check_bot_parent(comment, ca_dict, bot_list):
    parent_id = comment.parent_id[3:]
    parent_author = ca_dict[parent_id]
    if parent_author in bot_list:
        return True

    return False

# Create Reddit instance
reddit = praw.Reddit('nute_gunray_bot', user_agent=f"script:This is getting out of hand {VERSION}")

bot_list = get_bot_list()
replied = get_replied()
post_blacklist = get_blacklist()
ignore_list = get_ignore_list()

# Main loop
for post in reddit.subreddit("prequelmemes").hot(limit=NUM_POSTS):

    # Ignore all posts in blacklist
    if post.id in post_blacklist:
        continue

    print(f"Starting examining post with title \"{post.title}\"")
    comment_list = post.comments.list()

    ca_dict = get_dict(comment_list)

    for comment in comment_list:
        # ignore MoreComments instances
        if isinstance(comment, MoreComments):
            pass 
        
        else:
            # Do not reply to users in the ignore list
            if check_ignore_list(comment, ignore_list):
                pass

            elif check_top_level(comment):
                #print("Failed TL check")
                pass
            elif check_replied_self(comment, replied):
                #print("Failed self replied check")
                skipped_counter += 1
                pass
            elif check_replied_parent(comment, replied):
                add_replied_self(comment)
                replied.append(comment.id)
                skipped_counter += 1

                #print("Failed parent replied check, adding self to replied")
            elif check_bot_self(comment, bot_list):
                if check_bot_parent(comment, ca_dict, bot_list):
                    
                    add_replied_self(comment)
                    add_replied_parent(comment)

                    replied.append(comment.id)
                    replied.append(comment.parent_id[3:])
                    

                    if REPLY:
                        new_comment = comment.reply("This is getting out of hand, now there are two of them!")
                        add_replied_self(new_comment)
                        replied.append(new_comment.id)

                    print(f"author: {comment.author}, parent: {ca_dict[comment.parent_id[3:]]}")
                    replied_counter += 1

    post_counter += 1

print(f"Checked {post_counter} posts \r\nReplied to {replied_counter} comments \r\nSkipped {skipped_counter} comments to avoid maximum spam")