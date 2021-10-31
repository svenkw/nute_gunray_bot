import praw
from praw.models import MoreComments

# Parameters
NUM_POSTS = 100
BOT_FILE = "bot_data/bot_list"
SCORE_LIMIT = 0

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
                        count +=1
    return count

# Create Reddit instance
reddit = praw.Reddit('nute_gunray_bot', user_agent="script:This is getting out of hand v0.1")

# Read the names of the active bots on PrequelMemes from file
bot_list = get_bot_list()

# Start scanning
for post in reddit.subreddit("prequelmemes").hot(limit=NUM_POSTS):
    print(f"Starting examining post with title \"{post.title}\"")
    comment_list = post.comments.list()

    ca_dict = comment_author_dict(comment_list)

    count =get_double_bot_comments(comment_list, ca_dict)
    print(f"{count} bot-on-bot conversations")