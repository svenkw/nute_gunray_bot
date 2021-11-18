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
re: regex for Python. Used to find the triggers in comments
"""
import praw
from os import chdir
from praw.models import MoreComments
import json
import re
import random

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
    TRIGGER_FILE = config["trigger_file"]
    ANTI_TRIGGER_FILE = config["anti_trigger_file"]
    IGNORE_COMMAND = config["ignore_command"]
    MAX_SESSION_COMMENTS = config["max_session_comments"]

def get_triggers():
    with open(TRIGGER_FILE, 'r') as f:
        trigger_data = json.load(f)

    return trigger_data

def get_anti_triggers():
    with open(ANTI_TRIGGER_FILE, 'r') as f:
        anti_triggers = f.read().splitlines()

    return anti_triggers

def get_replied():
    with open(REPLIED_FILE, 'r') as f:
        replied = f.read().splitlines()

    return replied

def get_ignore():
    with open(IGNORE_FILE, 'r') as f:
        ignore_list = f.read().splitlines()

    return ignore_list

def add_to_replied_file(id):
    with open(REPLIED_FILE, 'a+') as f:
        f.write(id + "\n")

def add_to_ignore_list(author):
    with open(IGNORE_FILE, 'a+') as f:
        f.write(author + "\n")

# Create Reddit instance
reddit = praw.Reddit('nute_gunray_bot', user_agent=f"script:This is getting out of hand {VERSION}")

# Get anti-triggers
anti_triggers = get_anti_triggers()

# Get trigger data
trigger_data = get_triggers()
triggers = []
for t in trigger_data:
    triggers.append(t.lower())

# Get ignore list
ignore_list = get_ignore()

# Get replied IDs
replied = get_replied()

# Debugging variables
replied_comments = 0
total_comments = 0

# Loop over all posts (limited by NUM_POSTS)
for post in reddit.subreddit("prequelmemes").hot(limit=NUM_POSTS):
    comments = post.comments.list()

    # Loop over all comments on the post
    for comment in comments:
        if replied_comments > MAX_SESSION_COMMENTS:
            break

        # SEt anti-trigger flag to False
        a_t = False

        # Ignore MoreComments instances
        if isinstance(comment, MoreComments):
            continue
        else:
            # Skip to next comment if comment is made by blacklisted author
            if comment.author in ignore_list:
                continue

            # Check if the comment is an ignore-command
            comment_text = comment.body.lower()
            if comment_text == IGNORE_COMMAND:
                # Check if the ignore command is a reply to this bot
                parent = comment.parent_id[3:]
                parent_comment = reddit.comment(id=parent)
                parent_author = parent_comment.author
                if parent_author == "nute_gunray_bot":
                    # Add the user to the ignore list
                    add_to_ignore_list(comment.author)

            # Skip to next comment if comment is in replied
            if comment.id in replied:
                continue
            
            # Skip to next comment if parent comment is already replied to (aka skip thread)
            elif comment.parent_id[3:] in replied:
                add_to_replied_file(comment.id)
                replied.append(comment.id)
                continue
            
            for trigger in anti_triggers:
                if re.search(trigger, comment_text):
                    print("anti-trigger found")
                    a_t = True

            # using anti-trigger flag to go to next comment if anti-trigger is found
            if a_t:
                continue

            # Look if comments contains trigger
            for trigger in triggers:
                if re.search(trigger, comment_text):
                    total_comments += 1

                    add_to_replied_file(comment.id)
                    replied.append(comment.id)

                    probability = trigger_data[trigger]["prob"]
                    responses = trigger_data[trigger]["responses"]
                    num_responses = len(responses)

                    # If the trigger has defined responses, choose one
                    try:
                        response = random.choice(responses)
                    except:
                        # No responses defined? Go to next trigger
                        continue

                    # Each trigger has a probability to give a response
                    if random.random() < probability:
                        print("Replying") # debugging
                        replied_comments += 1
                        if REPLY:
                            new_comment = comment.reply(response)
                            # Make sure own comment is also added to replied-list to prevent infinite loops
                            add_to_replied_file(new_comment.id)
                            replied.append(new_comment.id)
                    
                    # debugging and logging
                    print(f"Original comment\n{comment_text}\nResponse chosen\n{response}\n\n")


                    # Break the loop after finding a trigger
                    # Order of triggers in the json file determines which triggers get priority
                    break

print(f"\n\nTotal comments: {total_comments}\nReplied comments: {replied_comments}")