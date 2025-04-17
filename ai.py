from chatterbot import ChatBot

# Uncomment the following lines to enable verbose logging
# import logging
# logging.basicConfig(level=logging.INFO)

# NOTE: The order of logic adapters is important
# because the first logic adapter takes precedence
# if a good response cannot be determined.

# Create a new instance of a ChatBot
bot = ChatBot('Terminal',
              storage_adapter='chatterbot.storage.SQLStorageAdapter',
              logic_adapters=[
                  'chatterbot.logic.BestMatch',
                  'chatterbot.logic.TimeLogicAdapter',
                  'chatterbot.logic.MathematicalEvaluation'
              ],
              database_uri='sqlite:///database.sqlite3')

print('Type something to begin...')

while True:
	try:
		user_input = input()

		bot_response = bot.get_response(user_input)

		print(bot_response)

	except (KeyboardInterrupt, EOFError, SystemExit):
		break
