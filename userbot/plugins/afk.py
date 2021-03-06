# Afk plugin from catuserbot ported from uniborg
import asyncio
from datetime import datetime

from telethon import events
from telethon.tl import functions, types

from ..utils import admin_cmd
from . import BOTLOG, BOTLOG_CHATID, CMD_HELP

global USERAFK_ON
global afk_time
global last_afk_message
global afk_start
global afk_end
USERAFK_ON = {}
afk_time = None
last_afk_message = {}
afk_start = {}


@borg.on(events.NewMessage(outgoing=True))
async def set_not_afk(event):
    if event.chat_id in Config.UB_BLACK_LIST_CHAT:
        return
    global USERAFK_ON
    global afk_time
    global last_afk_message
    global afk_start
    global afk_end
    back_alive = datetime.now()
    afk_end = back_alive.replace(microsecond=0)
    if afk_start != {}:
        total_afk_time = str((afk_end - afk_start))
    current_message = event.message.message
    if "afk" not in current_message and "on" in USERAFK_ON:
        shite = await borg.send_message(
            event.chat_id,
            "__Estou de volta!__\n**Não estou mais AFK.**\n `Fiquei AFK por:``"
            + total_afk_time
            + "`",
        )
        if BOTLOG:
            await borg.send_message(
                BOTLOG_CHATID,
                "#AFKFALSE \nModo AFK desativado!\n"
                + "__Estou de volta!__\n**Modo AFK desativado.**\n `Fiquei em AFK por:``"
                + total_afk_time
                + "`",
            )
        await asyncio.sleep(5)
        await shite.delete()
        USERAFK_ON = {}
        afk_time = None


@borg.on(
    events.NewMessage(incoming=True, func=lambda e: bool(e.mentioned or e.is_private))
)
async def on_afk(event):
    if event.fwd_from:
        return
    global USERAFK_ON
    global afk_time
    global last_afk_message
    global afk_start
    global afk_end
    back_alivee = datetime.now()
    afk_end = back_alivee.replace(microsecond=0)
    if afk_start != {}:
        total_afk_time = str((afk_end - afk_start))
    current_message_text = event.message.message.lower()
    if "afk" in current_message_text:
        # userbot's should not reply to other userbot's
        # https://core.telegram.org/bots/faq#why-doesn-39t-my-bot-see-messages-from-other-bots
        return False
    if USERAFK_ON and not (await event.get_sender()).bot:
        msg = None
        message_to_reply = (
            f"__Modo AFK Ativado.__ "
            + f"\n__Retorno assim que possível.__\n**MOTIVO**: {reason}"
            if reason
            else f"**Ei! No momento estou indisponível.**\n__Retorno assim que possível.__  "
        )
        if event.chat_id not in Config.UB_BLACK_LIST_CHAT:
            msg = await event.reply(message_to_reply)
        if event.chat_id in last_afk_message:
            await last_afk_message[event.chat_id].delete()
        last_afk_message[event.chat_id] = msg
        await asyncio.sleep(5)
        hmm = await event.get_chat()
        if Config.PM_LOGGR_BOT_API_ID:
            await asyncio.sleep(5)
            if not event.is_private:
                await event.client.send_message(
                    Config.PM_LOGGR_BOT_API_ID,
                    f"#AFK_TAGS \n<b>Grupo : </b><code>{hmm.title}</code>\
                            \n<b>Mensagem : </b><a href = 'https://t.me/c/{hmm.id}/{event.message.id}'> link</a>",
                    parse_mode="html",
                    link_preview=False,
                )


@borg.on(admin_cmd(pattern=r"afk ?(.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    global USERAFK_ON
    global afk_time
    global last_afk_message
    global afk_start
    global afk_end
    global reason
    USERAFK_ON = {}
    afk_time = None
    last_afk_message = {}
    afk_end = {}
    start_1 = datetime.now()
    afk_start = start_1.replace(microsecond=0)
    if not USERAFK_ON:
        reason = event.pattern_match.group(1)
        last_seen_status = await borg(
            functions.account.GetPrivacyRequest(types.InputPrivacyKeyStatusTimestamp())
        )
        if isinstance(last_seen_status.rules, types.PrivacyValueAllowAll):
            afk_time = datetime.now()
        USERAFK_ON = f"on: {reason}"
        if reason:
            await borg.send_message(
                event.chat_id, f"**Tô saindo!** __motivo ~ {reason}__"
            )
        else:
            await borg.send_message(event.chat_id, f"**Modo AFK Ativado!**")
        await asyncio.sleep(5)
        await event.delete()
        if BOTLOG:
            await borg.send_message(
                BOTLOG_CHATID,
                f"#AFKTRUE \nModo AFK Ativado e a Razão é {reason}",
            )


CMD_HELP.update(
    {
        "afk": "**Plugin : **`afk`\
        \n\n**Syntax : **`.afk [Razão]`\
\n**Uso : **Define você como afk.\nRespostas para quem marca/PM's \
você dizendo a eles que você está AFK(motivo).\n\nDesliga o AFK quando você digita qualquer coisa, em qualquer lugar.\
\nafk significa longe do teclado.\
"
    }
)
