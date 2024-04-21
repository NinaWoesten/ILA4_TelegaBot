import os
import dotenv

dotenv.load_dotenv('.env')
bot_name = "telegaBot"
model_engine = "gpt-3.5-turbo"
API_KEY = os.environ['API_KEY']
BOT_TOKEN = os.environ['TELEGA_TOKEN']
API_ID = os.environ['API_ID']
API_HASH = os.environ['API_HASH']

#das = zu überspringen, ab da wird alles zurückgegeben

#Es ist nicht sicher Schlüssel in einem "offenen" File aufzubwahren, 
#darum kann man Environement Variables benutzen. environ ist wie ein Wörterbuch
