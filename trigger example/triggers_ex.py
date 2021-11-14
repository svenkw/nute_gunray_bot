"""
Example implementation of the triggers.json file structure for use in reddit prequelmemes bots.

All triggers can be defined in the triggers.json file. 
Each trigger is basically an object, containing the probability the bot will actually reply to the trigger, and all possible replies to the trigger. 
If one trigger has multiple responses, the script will automatically choose one at random with equal probability.
The probability in triggers.json is the chance that the bot will even consider replying.

Triggers can easily be added and removed from the file without influencing the rest of the bot, and each trigger can have its own probability. This makes this a very versatile and easily shareable way of adding triggers.
"""

import re
import json
import random

trigger_file = "trigger example/triggers.json"

example_comment = "peace is a lie. there is only passion.\nthrough passion i gain strength.\nthrough strength i gain power.\nthrough power i gain victory.\nthrough victory my chains are broken.\nthe force shall free me."

with open(trigger_file, 'r') as f:
    trigger_data = json.load(f)

triggers = []
for t in trigger_data:
    triggers.append(t)

for trigger in triggers:
    if re.search(trigger, example_comment):
        print("Found a match!")

        reply_prob = trigger_data[trigger]["prob"]
        responses = trigger_data[trigger]["responses"]

        if random.random() > reply_prob:
            response = random.choice(responses)
            print(f"pretend the script just replied. reply chosen: \n{response}")
        else:
            print("the bot did not reply")
        