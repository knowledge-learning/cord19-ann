import os
import yaml
import logging
import textwrap
from inspect import cleandoc

logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

from pathlib import Path
from telegram.ext import Updater, CommandHandler
from telegram.utils.helpers import escape_markdown as _

PACKS = Path(__file__).parent / "packs.yml"
packs = None


def _load_yaml():
    global packs

    with open(PACKS) as fp:
        packs = yaml.safe_load(fp)['packs']


_load_yaml()


def status(update, context):
    _load_yaml()

    status_report = []
    dones = 0
    progress = 0
    opens = 0

    for pack in packs:
        for version in ['first', 'second']:
            status_code = packs[pack][version]['status']
            if status_code == 'In progress':
                progress += 1
                status_report.append(f"`{pack}-{version:6} ->` {_(packs[pack][version]['assigned'])}")
            elif status_code == "Open":
                opens += 1
            elif status_code == "Done":
                dones += 1

    status_report = cleandoc(
        f"""*Status report*:

        - *Done*: {dones}
        - *In progress*: {progress}
        - *Open*: {opens}

        *Currently in progress*:
        """ + '\n\t'.join(status_report))    

    update.message.reply_markdown(
        status_report
    )

    _save_packs()


def pack(update, context):
    user = "@" + update.effective_user.username
    assigned_pack = _get_pack(user)

    if assigned_pack is not None:
        update.message.reply_markdown(cleandoc(
            f"""Hello {_(user)}. You are currently assigned to *{assigned_pack[0]}-{assigned_pack[1]}*
            
            The link is:
            {_get_link(*assigned_pack)}.

            If you already finished send me a /done and then ask for a /pack
            If you cannot finish it and want to release it, send /cancel
            """
        ))
    else:
        new_pack = _assign_pack(user)
        
        if new_pack is None:
            update.message.reply_markdown(
                f"Hello {_(user)}. There are currently no open packs 🙈!!\nStick around, we'll have more soon 🚀."
            )
      
        else:
            update.message.reply_markdown(
                f"Hello {_(user)}. Here is a new pack ✊!!\n{_get_link(*new_pack)}\n\nKeep up the good work ⚔!!"
            )


def cancel(update, context):
    user = "@" + update.effective_user.username
    assigned_pack = _get_pack(user)

    if assigned_pack is None:
        update.message.reply_markdown(
            f"Hello {_(user)}. You don't have a pack assigned 😱!!\nMaybe you meant to say /pack 😎??"
        )
    else:
        pack, version = assigned_pack
        packs[pack][version]['status'] = 'Open'
        packs[pack][version]['assigned'] = None
        _save_packs()

        update.message.reply_markdown(
            f"Hello {_(user)}. You just canceled *{pack}-{version}* 😭!!\nYou are always welcome to come back whenever you want another /pack 😎!!"
        )


def done(update, context):
    user = "@" + update.effective_user.username
    assigned_pack = _get_pack(user)

    if assigned_pack is None:
        update.message.reply_markdown(
            f"Hello {_(user)}. You don't have a pack assigned 😱!!\nMaybe you meant to say /pack 😎??"
        )
    else:
        pack, version = assigned_pack
        packs[pack][version]['status'] = 'Done'
        _save_packs()

        update.message.reply_markdown(
            f"Hello {_(user)}. You just finished *{pack}-{version}* 😁!!\nWhenever you are ready, just ask for another /pack 😎!!"
        )

def _get_pack(user):
    for pack_id, pack in packs.items():
        for version_id, version in pack.items():
            if version['status'] != 'In progress':
                continue

            if version['assigned'] == user:
                return (pack_id, version_id)

    return None


def _get_link(pack, version):
    return f"http://ssh.apiad.net:8080/#/cord19/packs/{pack}/{version}/{pack}-{version}"


def _assign_pack(user):
    for pack_id, pack in packs.items():
        for version_id, version in pack.items():
            if version['status'] == 'Open':
                version['assigned'] = user
                version['status'] = "In progress"
                _save_packs()
                return pack_id, version_id

    return None


def _save_packs():
    with open(PACKS, "w") as fp:
        yaml.dump({'packs': packs}, fp)


updater = Updater(os.environ["TOKEN"], use_context=True)

updater.dispatcher.add_handler(CommandHandler('status', status))
updater.dispatcher.add_handler(CommandHandler('pack', pack))
updater.dispatcher.add_handler(CommandHandler('cancel', cancel))
updater.dispatcher.add_handler(CommandHandler('done', done))

updater.start_polling()
updater.idle()
