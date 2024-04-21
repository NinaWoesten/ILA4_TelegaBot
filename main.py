import asyncio
import openai
from settings import API_KEY, API_ID, API_HASH, BOT_TOKEN
from telethon import TelegramClient, events

# Konfiguration des API-Schlüssels
openai.api_key = API_KEY
print(API_KEY)
client = TelegramClient('telegaBot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

async def send_input_and_get_result(prompt, conversation):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error in sending input to OpenAI: {e}")
        return "Sorry, I couldn't process your request at the moment."


@client.on(events.NewMessage(pattern="(?i)/start"))
async def start_message(event):
    try:
        await event.resond('Hey you new message here')
        async with client.conversation(await event.get_conversation(), exclusive=True, exclusive=True, timeout=600) as conversation:
            history = []

            while True:
                prompt = "Ask something"
                user_prompt = await send_input_and_get_result(prompt, conversation)

    except asyncio.TimeoutError:
        await client.send_message("Ended message")
        return
    except Exception as e:
        print(e)
        await client.send_message("Something went wrong")
        return
if __name__ == "__main__":
        print("Starting...")
        client.run_until_disconnected()
# Erstellen eines OpenAI-Clients
client = openai.completions.create(
    engine="davinci-codex",
    prompt="Hey",
    temperature=1,
    max_tokens=2048,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
)

# Ausführen der Anfrage
response = client

print(response)

'''
client = TelegramClient(settings.name_bot, settings.API_ID, settings.API_HASH).start(bot_token=settings.BOT_TOKEN)
#keyboard_stop = [[buttons.inline ("Stop and delete conversation for conversation", b "stop" )]]

@client.on(events.NewMessage(pattern="(?i)/start"))
async def handle_start_command(event):
    SENDER = event.sender_id

if __name__ == "__main__":
    print("Starting...")
    client.run_until_disconnected()
: '''

