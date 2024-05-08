import asyncio
import logging
import time
from telethon import TelegramClient, events, Button
from decouple import config

logging.basicConfig(
    level=logging.INFO, format="[%(levelname)s] %(asctime)s - %(message)s"
)
log = logging.getLogger("ChannelAutoPost")

# Start the bot
log.info("Starting...")
try:
    apiid = config("APP_ID", cast=int)
    apihash = config("API_HASH")
    bottoken = config("BOT_TOKEN")
    frm = config("FROM_CHANNEL", cast=lambda x: [int(_) for _ in x.split(" ")])
    tochnls = config("TO_CHANNEL", cast=lambda x: [int(_) for _ in x.split(" ")])
    datgbot = TelegramClient(None, apiid, apihash).start(bot_token=bottoken)
except Exception as exc:
    log.error("Environment vars are missing! Kindly recheck.")
    log.info("Bot is quiting...")
    log.error(exc)
    exit()

# Task queue untuk memproses pesan secara asynchronous
task_queue = asyncio.Queue()

@datgbot.on(events.NewMessage(pattern="/start"))
async def _(event):
    await event.reply(
        f"Hi `{event.sender.first_name}`!\n\nI am a channel auto-post bot!! Read /help to know more!\n\nI can be used in only two channels (one user) at a time. Kindly deploy your own bot.\n\n[More bots](https://t.me/its_xditya)..",
        buttons=[
            Button.url("Repo", url="https://github.com/xditya/ChannelAutoForwarder"),
            Button.url("Dev", url="https://xditya.me"),
        ],
        link_preview=False,
    )


@datgbot.on(events.NewMessage(pattern="/help"))
async def helpp(event):
    await event.reply(
        "**Help**\n\nThis bot will send all new posts in one channel to the other channel. (without forwarded tag)!\nIt can be used only in two channels at a time, so kindly deploy your own bot from [here](https://github.com/xditya/ChannelAutoForwarder).\n\nAdd me to both the channels and make me an admin in both, and all new messages would be autoposted on the linked channel!!\n\nLiked the bot? Drop a ♥ to @xditya_Bot :)"
    )


async def process_message(message_id, chat_id, message_text, tochnls, event):
    for tochnl in tochnls:
        try:
            if event.poll:
                continue
            elif event.photo:
                photo = event.media.photo
                await datgbot.send_file(
                    tochnl, photo, caption=message_text, link_preview=False
                )
            elif event.media:
                try:
                    if event.media.webpage:
                        await datgbot.send_message(
                            tochnl, message_text, link_preview=False
                        )
                except Exception:
                    media = event.media.document
                    await datgbot.send_file(
                        tochnl, media, caption=message_text, link_preview=False
                    )
            else:
                await datgbot.send_message(tochnl, message_text, link_preview=False)
        except Exception as exc:
            log.error(
                f"TO_CHANNEL ID salah atau saya tidak dapat mengirim pesan di sana (jadikan saya admin). Message ID: {message_id} Chat ID: {chat_id}\nTraceback:\n{exc}"
            )


@datgbot.on(events.NewMessage(incoming=True)) 
async def _(event):
    if event.is_private:  # From a private chat
        tochnls = config("TO_CHANNEL", cast=int)  # Load channel ID from config
    else:  # From one of the source channels ('frm')
        if event.chat_id not in frm:
            return  # Ignore if not in the source channel list

    message_id = event.id
    chat_id = event
    
    
log.info("Bot has started.")
log.info("Do visit https://xditya.me !")
datgbot.run_until_disconnected()
