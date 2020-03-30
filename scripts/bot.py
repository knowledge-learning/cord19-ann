import os
import yaml

from pathlib import Path
from telegram.ext import Updater, CommandHandler


PACKS = Path(__file__).parent / "packs.yml"

with open(PACKS) as fp:
    packs = yaml.safe_load(fp)



def status(update, context):
    

    update.message.reply_text(
        "caca"
    )


updater = Updater(os.environ["TOKEN"], use_context=True)

updater.dispatcher.add_handler(CommandHandler('status', status))

updater.start_polling()
updater.idle()
