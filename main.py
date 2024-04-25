import asyncio
import openai
from settings import API_KEY, API_ID, API_HASH, BOT_TOKEN, bot_name, model_engine
from telethon import TelegramClient, events

# Konfiguration API Key
openai.api_key = API_KEY
print(API_KEY)


client = TelegramClient('telegaBot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)


async def send_input_and_get_response(prompt, conversation):
    message = await conversation.send_message(prompt)
    task_wait = asyncio.create_task(conversation.wait_event(events.CallbackQuery()))
    task_respond = asyncio.create_task(conversation.get_response())

    done, _ = await asyncio.wait(
        {
            task_wait, task_respond
        },
        return_when=asyncio.FIRST_COMPLETED)
    
    response = done.pop().result()
    #Nachricht wird gelöscht sobald eine Antwort erhalten wurde
    await message.delete()
    #None wenn Antwort ein Callback ist
    if isinstance(response, events.CallbackQuery.Event):
        return None
    else:
        return response.message.strip()
        

@client.on(events.NewMessage(pattern="(?i)/start"))
async def respond(event):
    try:
        async with client.conversation(await event.get_chat(), timeout=600) as conversation:
            history = []

            while True:
                user_input = event.message.text
                response = await send_input_and_get_response(user_input, conversation)
                
                #User beendet Konversation
                if user_input is None:
                    prompt ="Conversation ended. Type /start to start a new one"
                    await client.send_message(prompt)
                    break
                else:
                    #prompt = "I'm thinking about the response..."
                    #thinking_message = await client.send_message(prompt)

                    history.append({"role": "user", "content": user_input})

                    chat_completion = openai.ChatCompletion.create(
                        model= model_engine,
                        messages = history,
                        max_tokens=500,
                        n=1,
                        temperature=0.1
                    )
                    response = chat_completion.choices[0].message.content
                    history.append({"role": "bot", "content": response})
                    await thinking_message.delete()
                    await client.send_message(response, parse_mode='Markdown')

    #Zeitüberschreitungsfehler
    except asyncio.TimeoutError:
        await event.send_message("Timeout: Conversation ended.")
    #Andere Ausnahmen
    except Exception as e:
        print(f"Error: {e}")
        await event.respond("Sorry, something went wrong.")


if __name__ == "__main__":
        #Start client
        print("Starting...")
        client.run_until_disconnected()


'''
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
client = TelegramClient(settings.name_bot, settings.API_ID, settings.API_HASH).start(bot_token=settings.BOT_TOKEN)
#keyboard_stop = [[buttons.inline ("Stop and delete conversation for conversation", b "stop" )]]

@client.on(events.NewMessage(pattern="(?i)/start"))
async def handle_start_command(event):
    SENDER = event.sender_id

if __name__ == "__main__":
    print("Starting...")
    client.run_until_disconnected()
: '''

