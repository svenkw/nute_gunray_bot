import json
import re

jsonfile = "bot_data/triggers.json"

comment = "I would like to speak to the trade federation"

with open(jsonfile, 'r') as f:
    trigger_data = json.load(f)


triggers = []
for trig in trigger_data:
    triggers.append(trig)

for trigger in triggers:
    print(f"trigger: {trigger}")
    if re.search(trigger.lower(), comment.lower()):
        print(trigger_data[trigger]["responses"])
    else: 
        print("no match")