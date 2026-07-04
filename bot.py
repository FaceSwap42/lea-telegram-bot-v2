import asyncio
import logging
import os

from telegram import Update
from telegram.ext import Application, ChatJoinRequestHandler, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN", "COLLE_TON_TOKEN_ICI")

DELAI_APPROBATION = 8

MESSAGE_BIENVENUE = """Hey ! 🍓

Bienvenue dans mon petit coin perso 💫

Ici c'est différent d'Insta et Threads je peux être plus moi-même, partager des trucs que je montre pas ailleurs (dessins, coulisses, humeurs du jour, et... le reste 😏) Reste dans le coin, ça va être sympa

Envoie moi un message sur telegram 👉 @Leaa6231 pour me dire que tu t'es abonné et je t'enverrais une surprise 💗

A tout de suite 😚❤️"""

PHOTO_URL = "https://raw.githubusercontent.com/FaceSwap42/lea-telegram-bot-v2/main/8d982696-9a3f-43de-8daf-fde2b93c1a72.jpeg"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


async def gerer_demande_adhesion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    demande = update.chat_join_request
    user = demande.from_user
    chat = demande.chat

    logger.info(f"Nouvelle demande d'adhesion : {user.id} ({user.first_name}) -> {chat.title}")

    try:
        if PHOTO_URL:
            await context.bot.send_photo(
                chat_id=user.id,
                photo=PHOTO_URL,
                caption=MESSAGE_BIENVENUE,
            )
        else:
            await context.bot.send_message(
                chat_id=user.id,
                text=MESSAGE_BIENVENUE,
            )
        logger.info(f"Message de bienvenue envoye a {user.id}")

    except Exception as e:
        logger.warning(f"Impossible d'envoyer le message a {user.id} : {e}")

    await asyncio.sleep(DELAI_APPROBATION)

    try:
        await context.bot.approve_chat_join_request(
            chat_id=chat.id,
            user_id=user.id,
        )
        logger.info(f"Demande approuvee pour {user.id}")
    except Exception as e:
        logger.error(f"Erreur lors de l'approbation pour {user.id} : {e}")


def main():
    if BOT_TOKEN == "COLLE_TON_TOKEN_ICI":
        raise RuntimeError("Tu dois definir la variable d'environnement BOT_TOKEN.")

    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(ChatJoinRequestHandler(gerer_demande_adhesion))

    logger.info("Bot demarre, en ecoute des demandes d'adhesion...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
