BOT_FILE = "bot_data/bot_list"

with open(BOT_FILE, 'r') as f:
    bot_list = []
    
    bot = f.read().splitlines()
    print(bot)
