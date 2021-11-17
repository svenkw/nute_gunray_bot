"""
Main script for the nute_gunray_bot on Reddit
Author: u/svenkw
Created: november 2021
"""


"""
praw: Python Reddit API Wrapper, does all the heavy Reddit lifting
chdir: Used to set the working directory so the script can be run periodically with cron
praw.models.MoreComments: Just a necessary part for using praw
json: Used to import and process the config.json file
"""
import praw
from os import chdir
from praw.models import MoreComments
import json

"""
Change the working directory to /home/pi/nute_gunray_bot
Necessary because cron runs it from another directory, and then it can't find the necessary files
If the chdir() fails, the script is not run on the pi, and this step is simply skipped
"""
try:
    chdir("/home/pi/nute_gunray_bot")
except:
    print("not running on pi")
    pass

"""
Open the config.json file, and extract the parameters into variables
Variables in all-caps are variables that should be treated as constants in the script
"""
with open("config.json") as f:
    config = json.load(f)
    BOT_FILE = config["bot_list"]
    REPLIED_FILE = config["replied_file"]
    BLACKLIST_FILE = config["blacklist_file"]
    IGNORE_FILE = config["ignore_file"]
    NUM_POSTS = config["num_posts"]
    REPLY = config["reply"]
    VERSION = config["version"]

# Initialise variables used for logging
replied_counter = 0
skipped_counter = 0
post_counter = 0

# =====================================
# Get stored information from files
# =====================================
def get_replied():
    """
    Get the list of comments that are already replied to from the correct file
    
    Returns: all IDs from the file in a list
    """
    with open(REPLIED_FILE, 'r') as f:
        replied = f.read().splitlines()
    
    return replied

def get_bot_list():
    """
    Get the list of bot names from the correct file

    Returns: all names of the active bots on prequelmemes in a list
    """
    with open(BOT_FILE, 'r') as f:
        bot_list = f.read().splitlines()

    return bot_list

def get_blacklist():
    """
    Get the list of post IDs stored in the blacklist file. These posts should never be replied to. Mainly used for pinned posts

    Returns: the IDs of the blacklisted posts in a list
    """
    with open(BLACKLIST_FILE, 'r') as f:
        post_blacklist = f.read().splitlines()
    return post_blacklist

def get_ignore_list():
    """
    Get the names of profiles that should be ignored from the correct file

    Returns: the names of the profiles that should be ignored in a list
    """
    with open(IGNORE_FILE, 'r') as f:
        ignore_list = f.read().splitlines()
    return ignore_list


# =====================================
# Functions for the main loop
# =====================================
def get_dict(comment_list):
    """
    Creates a dictionary where every comment ID is matched with an author.

    Key: comment ID
    Result: comment author

    Returns: the comment-author dictionary
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
    """
    Checks if the comment is on the ignore list

    Returns: True if the comment is in the ignore list, False otherwise
    """
    if comment.author in ignore_list:
        return True
    
    return False

def check_top_level(comment):
    """
    Check if the comment is a top-level comment. If it is, it would give problems with the ca_dict, so it needs to be ignored

    Returns: True if the comment is a top-level comment, False otherwise
    """
    if comment.parent_id[:3] == "t3_":
        return True

    return False

def check_replied_self(comment, replied):
    """
    Check if the comment itself is already on the replied-list

    Returns: True if the comment is on the replied list, False otherwise
    """
    if comment.id in replied:
        return True

    return False

def check_replied_parent(comment, replied):
    """
    Check if the comment's parent comment is already on the replied-list

    Returns: True if the comment's parent comment is on the list, False otherwise
    """
    parent_id = comment.parent_id[3:]
    if parent_id in replied:
        return True

    return False

def add_replied_self(comment):
    """
    Append the comment ID of the comment to the replied-file

    Returns: None
    """
    with open(REPLIED_FILE, 'a+') as f:
        f.write(comment.id + "\n")

def add_replied_parent(comment):
    """
    Append the comment ID of the comment's parent comment to the replied-file

    Returns: None
    """
    with open(REPLIED_FILE, 'a+') as f:
        f.write(comment.parent_id[3:] + "\n")

def check_bot_self(comment, bot_list):
    """
    Check if the comment is made by a bot on the bot_list

    Returns: True if the comment is made by a bot, False otherwise
    """
    if comment.author in bot_list:
        return True

    return False

def check_bot_parent(comment, ca_dict, bot_list):
    """
    Check if the comment's parent comment is made by a bot on the bot_list

    Returns: True if the comment's parent comment is made by a bot, False otherwise
    """
    parent_id = comment.parent_id[3:]
    parent_author = ca_dict[parent_id]
    if parent_author in bot_list:
        return True

    return False

# Create Reddit instance
reddit = praw.Reddit('nute_gunray_bot', user_agent=f"script:This is getting out of hand {VERSION}")

# Get all required lists
bot_list = get_bot_list()
replied = get_replied()
post_blacklist = get_blacklist()
ignore_list = get_ignore_list()

# Main bot loop
for post in reddit.subreddit("prequelmemes").hot(limit=NUM_POSTS):

    # Ignore all posts in blacklist
    if post.id in post_blacklist:
        continue # Go to next post, skip all else

    print(f"Starting examining post with title \"{post.title}\"")
    
    # Get all comments from the post and create the ca_dict
    comment_list = post.comments.list()
    ca_dict = get_dict(comment_list)

    # Loop over all comments on the post
    for comment in comment_list:
        # ignore MoreComments instances
        if isinstance(comment, MoreComments):
            pass 
        
        else:
            # Do not reply to users in the ignore list
            if check_ignore_list(comment, ignore_list):
                pass
            # Do not reply to top-level comments (can't be bot-on-bot anyways)
            elif check_top_level(comment):
                pass
            # Do not reply if comment is flagged as 'replied'
            elif check_replied_self(comment, replied):
                skipped_counter += 1 # Just for logging and testing purposes
                pass
            # Dot not reply if the parent comment is flagged as 'replied'
            elif check_replied_parent(comment, replied):
                add_replied_self(comment)
                replied.append(comment.id)
                skipped_counter += 1 # Just for logging and testing purposes
            
            # Do if both comment and parent comment are made by bot
            elif check_bot_self(comment, bot_list):
                if check_bot_parent(comment, ca_dict, bot_list):
                    # Update replied-list
                    add_replied_self(comment)
                    add_replied_parent(comment)
                    # Update replied-file
                    replied.append(comment.id)
                    replied.append(comment.parent_id[3:])
                    
                    # !!VERY IMPORTANT!!
                    # Make sure that any testing platform has the "reply" parameter in config.json set to false
                    # Git does not transfer the replied file, so testing and running on two separate machines without this flag will result in double comments
                    # Config file is also not transferred through git
                    if REPLY:
                        new_comment = comment.reply("This is getting out of hand, now there are two of them!")
                        add_replied_self(new_comment)
                        replied.append(new_comment.id)

                    print(f"author: {comment.author}, parent: {ca_dict[comment.parent_id[3:]]}") # Just for logging and testing purposes
                    replied_counter += 1 # Just for logging and testing purposes

    post_counter += 1 # Just for logging and testing purposes

print(f"Checked {post_counter} posts \r\nReplied to {replied_counter} comments \r\nSkipped {skipped_counter} comments to avoid maximum spam") # Just for logging and testing purposes