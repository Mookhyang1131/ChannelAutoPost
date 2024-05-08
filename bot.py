import logging
from telethon import TelegramClient, events
from decouple import config

logging.basicConfig(
    level=logging.INFO, format="[%(levelname)s] %(asctime)s - %(message)s"
)
log = logging.getLogger("ChannelAutoPost")

# Memulai bot
log.info("Memulai...")
try:
    apiid = config("APP_ID", cast=int)
    apihash = config("API_HASH")
    bottoken = config("BOT_TOKEN")
    tochnls = config("TO_CHANNEL", cast=lambda x: [int(_) for _ in x.split(" ")])
    datgbot = TelegramClient(None, apiid, apihash).start(bot_token=bottoken)
except Exception as exc:
    log.error("Variabel lingkungan hilang! Silakan periksa kembali.")
    log.info("Bot keluar...")
    log.error(exc)
    exit()


@datgbot.on(events.NewMessage(incoming=True, chats=datgbot))
async def _(event):
    if event.is_private:  # Periksa apakah pesan berasal dari obrolan pribadi
        for tochnl in tochnls:
            try:
                if event.poll:
                    return
                if event.photo:
                    photo = event.media.photo
                    await datgbot.send_file(
                        tochnl, photo, caption=event.text, link_preview=False
                    )
                elif event.media:
                    try:
                        if event.media.webpage:
                            await datgbot.send_message(
                                tochnl, event.text, link_preview=False
                            )
                    except Exception:
                        media = event.media.document
                        await datgbot.send_file(
                            tochnl, media, caption=event.text, link_preview=False
                        )
                    finally:
                        return
                else:
                    await datgbot.send_message(tochnl, event.text, link_preview=False)
            except Exception as exc:
                log.error(
                    "ID TO_CHANNEL salah atau saya tidak dapat mengirim pesan di sana (jadikan saya admin).\nTraceback:\n%s",
                    exc,
                )

log.info("Bot telah dimulai.")
log.info("Kunjungi https://xditya.me !")
datgbot.run_until_disconnected()
