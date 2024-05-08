import logging
from telethon import TelegramClient, events, Button
from decouple import config

logging.basicConfig(
    level=logging.INFO, format="[%(levelname)s] %(asctime)s - %(message)s"
)
log = logging.getLogger("ChannelAutoPost")

# start the bot
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



@datgbot.on(events.NewMessage(incoming=True))  # Menangkap pesan dari kedua sumber
async def _(event):
    if event.is_private:  # Dari chat pribadi
        channel_id = config("CHANNEL_ID", cast=int)  # Memuat ID channel dari konfigurasi
    else:  # Dari salah satu channel sumber ('frm')
        if event.chat_id not in frm:
            return  # Abaikan jika bukan dari daftar channel sumber

    try:
        if event.poll:
            return
        elif event.photo:
            photo = event.media.photo
            await datgbot.send_file(
                channel_id, photo, caption=event.text, link_preview=False
            )
        elif event.media:
            try:
                if event.media.webpage:
                    await datgbot.send_message(
                        channel_id, event.text, link_preview=False
                    )
            except Exception:
                media = event.media.document
                await datgbot.send_file(
                    channel_id, media, caption=event.text, link_preview=False
                )
            finally:
                return
        else:
            await datgbot.send_message(channel_id, event.text, link_preview=False)
    except Exception as exc:
        log.error(
            "ID TO_CHANNEL salah atau saya tidak dapat mengirim pesan di sana (jadikan saya admin).\nTraceback:\n%s",
            exc,
        )


log.info("Bot has started.")
log.info("Do visit https://xditya.me !")
datgbot.run_until_disconnected()
