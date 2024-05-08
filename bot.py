import logging
from pyrogram import Client, filters
from decouple import config

logging.basicConfig(
    level=logging.INFO, format="[%(levelname)s] %(asctime)s - %(message)s"
)
log = logging.getLogger("ChannelAutoPost")

# Start the bot
log.info("Starting...")

try:
    app = Client(
        "my_bot",  # Session name for Pyrogram (you can choose your own)
        api_id=config("APP_ID", cast=int),
        api_hash=config("API_HASH"),
        bot_token=config("BOT_TOKEN")
    )
    tochnls = config("TO_CHANNEL", cast=lambda x: [int(_) for _ in x.split(" ")])
except Exception as exc:
    log.error("Environment variables are missing! Kindly recheck.")
    log.info("Bot is quiting...")
    log.error(exc)
    exit()

# Event handler for private messages
@app.on_message(filters.private)
async def forward_messages(_, message):
    for target_channel in tochnls:
        try:
            if message.photo:
                await app.send_photo(target_channel, message.photo.file_id, caption=message.text)
            elif message.media:
                # Handle other media types as needed (e.g., document, video)
                if message.document:
                    await app.send_document(target_channel, message.document.file_id, caption=message.text)
                # ... add more cases for specific media types
            else:  # Plain text message
                await app.send_message(target_channel, message.text)
        except Exception as exc:
            log.error(
                "TO_CHANNEL ID is wrong or I can't send messages there (make me admin).\nTraceback:\n%s",
                exc
            )

log.info("Bot has started.")
log.info("Do visit https://xditya.me !")

