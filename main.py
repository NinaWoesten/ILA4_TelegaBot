import json
from dotenv import load_dotenv
from settings import API_KEY, API_ID, API_HASH, BOT_TOKEN, model_engine
from telegram import (
    ReplyKeyboardMarkup,
    Update,
    KeyboardButton, 
)
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
from openai import OpenAI

client = OpenAI(api_key=API_KEY)
print(API_KEY)
(ENTRY_STATE, QUESTION_STATE,) = range(2)

class Bot:
    def get_response(self, question):
        prompt = question
        load_dotenv()
        client.api_key = API_KEY
        response = client.completions.create(
            model=model_engine,
            prompt=prompt,
            max_tokens=51,
            temperature=0.5
        )
        json_object = response

        json_string = json.dumps(json_object)
        parsed_json = json.loads(json_string)
        text = parsed_json['choices'][0]['text']
        cleared_text = self.clear_text(text)
        return cleared_text


def _generate_bot(prompt:str):
    bot = Bot()
    b = bot.get_response(prompt)
    return b

async def start(update: Update, context: ContextTypes):
    button = [[KeyboardButton(text="Ask-a-question")]]
    reply_markup = ReplyKeyboardMarkup(
        button, resize_keyboard=True
    )
    await update.message.reply_text(
        "Hello, would you like to ask me a question? "
        "Choose an option to continue",
        reply_markup=reply_markup,
    )
    return ENTRY_STATE

async def pre_query_handler(update: Update, context: ContextTypes):
    button = [[KeyboardButton(text="Back")]]
    reply_markup = ReplyKeyboardMarkup(
        button, resize_keyboard=True
    )
    await update.message.reply_text(
        "Enter text",
        reply_markup=reply_markup,
    )
    return QUESTION_STATE

async def pre_query_response_handler(update: Update, context: ContextTypes):
    try:
        button = [[KeyboardButton(text="Back")]]
        reply_markup = ReplyKeyboardMarkup(
            button, resize_keyboard=True
        )
        question = update.message.text 
        response = _generate_bot(question)
        context.user_data['response'] = response

        await update.message.reply_text(
            response, reply_markup=reply_markup,
        )
        return QUESTION_STATE
    # Fehlermeldung 
    except Exception as e:
        error_message = "Sorry, something went wrong."
        await update.message.reply_text(error_message)
        print(f"Error: {e}")

#Bot starten
if __name__ == "__main__":
    load_dotenv()
    application = Application.builder().token(BOT_TOKEN).read_timeout(100).get_updates_read_timeout(100).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            ENTRY_STATE:[
                MessageHandler(filters.Regex('^Back$'), start),
                MessageHandler(filters.Regex('^Ask-a-question$'), pre_query_handler),
            ],
            QUESTION_STATE: [
                MessageHandler(filters.Regex('^Back$'), start),
                MessageHandler(filters.TEXT, pre_query_response_handler),
            ],
        },
        fallbacks=[],
    )
    application.add_handler(conv_handler)
    print("Starting....")
    application.run_polling()


