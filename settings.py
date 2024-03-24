import os
import dotenv

dotenv.load_dotenv('.env')

API_KEY = os.environ['API_KEY']

#das = zu überspringen, ab da wird alles zurückgegeben

#Es ist nicht sicher Schlüssel in einem "offenen" File aufzubwahren, 
#darum kann man Environement Variables benutzen. environ ist wie ein Wörterbuch
