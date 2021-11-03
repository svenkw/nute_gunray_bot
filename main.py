import praw
from os import chdir
from praw.models import MoreComments

chdir("/home/pi/nute_gunray_bot")

# Parameters
NUM_POSTS = 50
BOT_FILE = "bot_data/bot_list"
SCANNED_FILE = "bot_data/scanned_posts"
REPLIED_FILE = "bot_data/replied"
BLACKLIST_FILE = "bot_data/post_blacklist"
SCORE_LIMIT = 0
MIN_POST_AGE = 10

REPLY = True

# Logging setup
replied_counter = 0
skipped_counter = 0
post_counter = 0

def add_to_replied(comment_id):
    """
    Add the comment to the list of comments that have already been replied to
    """
    with open(REPLIED_FILE, 'a+') as f:
        f.write(comment_id + "\n")

def check_replied(comment_id, replied):
    """
    Check if the comment is already on the list of comments that have been replied to
    """
    if comment_id in replied:
        #print(f"already replied to {ca_dict[comment_id]}")
        return True

    return False

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

def check_bot(comment, bot_list):
    """
    Check if the comment is made by a registered bot account
    """
    comment_author = comment.author
    if comment_author in bot_list:
        return True

    return False

def check_parent_bot(comment, ca_dict, bot_list):
    """
    Check if the parent of the bot comment is also a bot
    """
    global replied, skipped_counter
    
    parent_comment_id = comment.parent_id

    if parent_comment_id[:3] == "t3_":
        #print("top level comment")
        return False

    parent_author = ca_dict[parent_comment_id[3:]]

    # If the parent comment is in replied, return False (aka do not reply to this comment)
    if check_replied(parent_comment_id[3:], replied):
        replied.append(comment.id)
        skipped_counter += 1
        return False
    
    # If all criteria are met, also add parent id to replied list
    elif parent_author in bot_list:
        replied.append(parent_comment_id[3:])
        add_to_replied(parent_comment_id[3:])
        return True

    return False

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

# Create Reddit instance
reddit = praw.Reddit('nute_gunray_bot', user_agent="script:This is getting out of hand v1.1")

# Read the names of the active bots on PrequelMemes from file
bot_list = get_bot_list()

# Get the list of comment IDs of comments that have already been replied to
replied = get_replied()

post_blacklist = get_blacklist()

# Start scanning
for post in reddit.subreddit("prequelmemes").hot(limit=NUM_POSTS):

    if post.id in post_blacklist:
        #print('blacklisted')
        continue

    print(f"Starting examining post with title \"{post.title}\"")
    comment_list = post.comments.list()

    ca_dict = get_dict(comment_list)

    for comment in comment_list:
        if isinstance(comment, MoreComments):
            pass # ignore MoreComments instances
        else:
            if check_bot(comment, bot_list):
                if check_parent_bot(comment, ca_dict, bot_list):
                    replied.append(comment.id)
                    add_to_replied(comment.id)
                    
                    if REPLY:
                        new_comment = comment.reply("This is getting out of hand, now there are two of them!")
                        add_to_replied(new_comment.id)
                        replied.append(new_comment.id)
                    
                    replied_counter += 1

    post_counter += 1

print(f"Checked {post_counter} posts \r\nReplied to {replied_counter} comments \r\nSkipped {skipped_counter} comments to avoid maximum spam")