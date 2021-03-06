import asyncio

import requests
from telethon import functions

from ..utils import admin_cmd, edit_or_reply, sudo_cmd
from . import ALIVE_NAME, CMD_HELP, CMD_LIST, SUDO_LIST, yaml_format

DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else "cat"

HELPTYPE = Config.HELP_INLINETYPE or True


@bot.on(admin_cmd(outgoing=True, pattern="help ?(.*)"))
async def cmd_list(event):
    global HELPTYPE
    reply_to_id = None
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    input_str = event.pattern_match.group(1)
    if input_str == "text":
        string = (
            "Total {count} comandos encontrados em {plugincount} plugins de catuserbot\n\n"
        )
        catcount = 0
        plugincount = 0
        for i in sorted(CMD_LIST):
            plugincount += 1
            string += f"{plugincount}) Comandos encontrados no Plugin " + i + " sao \n"
            for iter_list in CMD_LIST[i]:
                string += "    " + str(iter_list)
                string += "\n"
                catcount += 1
            string += "\n"
        if len(string) > 4095:
            data = string.format(count=catcount, plugincount=plugincount)
            key = (
                requests.post(
                    "https://nekobin.com/api/documents", json={"content": data}
                )
                .json()
                .get("result")
                .get("key")
            )
            url = f"https://nekobin.com/{key}"
            reply_text = f"**Todos os comandos do catuserbot podem ser vistos [here]({url})**"
            await event.edit(reply_text)
            return
        await event.edit(string.format(count=catcount, plugincount=plugincount))
        return
    if input_str:
        if input_str in CMD_LIST:
            string = "<b>{count} Comandos encontrados no plugin {input_str}:</b>\n\n"
            catcount = 0
            for i in CMD_LIST[input_str]:
                string += f"  ◆  <code>{i}</code>"
                string += "\n"
                catcount += 1
            await event.edit(
                string.format(count=catcount, input_str=input_str), parse_mode="HTML"
            )
        else:
            await event.edit(input_str + " não é um plugin válido!")
            await asyncio.sleep(3)
            await event.delete()
    else:
        if HELPTYPE is True:
            help_string = f"Userbot Helper .. Fornecido por {DEFAULTUSER}\
                          \nUserbot Helper para revelar todos os nomes de plug-ins\
                          \n__Envie__ `.help` __plugin_name para comandos, caso o pop-up não apareça.__\
                          \nOu `.info` plugin_name para uso"
            tgbotusername = Var.TG_BOT_USER_NAME_BF_HER
            results = await bot.inline_query(  # pylint:disable=E0602
                tgbotusername, help_string
            )
            await results[0].click(event.chat_id, reply_to=reply_to_id, hide_via=True)
            await event.delete()
        else:
            string = "<b>Por favor, especifique para qual plugin você quer ajuda !!\
                \nNúmero de plugins : </b><code>{count}</code>\
                \n<b>Uso:</b> <code>.help</code> nome plugin\n\n"
            catcount = 0
            for i in sorted(CMD_LIST):
                string += "◆" + f"<code>{str(i)}</code>"
                string += "   "
                catcount += 1
            await event.edit(string.format(count=catcount), parse_mode="HTML")


@bot.on(sudo_cmd(allow_sudo=True, pattern="help ?(.*)"))
async def info(event):
    input_str = event.pattern_match.group(1)
    if input_str == "text":
        string = "Total {count} comandos encontrados em {plugincount} sudo plugins of catuserbot\n\n"
        catcount = 0
        plugincount = 0
        for i in sorted(SUDO_LIST):
            plugincount += 1
            string += f"{plugincount}) Comandos encontrados no Plugin " + i + " are \n"
            for iter_list in SUDO_LIST[i]:
                string += "    " + str(iter_list)
                string += "\n"
                catcount += 1
            string += "\n"
        if len(string) > 4095:
            data = string.format(count=catcount, plugincount=plugincount)
            key = (
                requests.post(
                    "https://nekobin.com/api/documents", json={"content": data}
                )
                .json()
                .get("result")
                .get("key")
            )
            url = f"https://nekobin.com/{key}"
            reply_text = f"Todos os comandos do catuserbot são [here]({url})"
            await event.reply(reply_text)
            return
        await event.reply(string.format(count=catcount, plugincount=plugincount))
        return
    if input_str:
        if input_str in SUDO_LIST:
            string = "<b>{count} Comandos encontrados no plugin {input_str}:</b>\n\n"
            catcount = 0
            for i in SUDO_LIST[input_str]:
                string += f"  ◆  <code>{i}</code>"
                string += "\n"
                catcount += 1
            await event.reply(
                string.format(count=catcount, input_str=input_str), parse_mode="HTML"
            )
        else:
            reply = await event.reply(input_str + " não é um plugin válido!")
            await asyncio.sleep(3)
            await event.delete()
            await reply.delete()
    else:
        string = "<b>Por favor, especifique para qual plugin você quer ajuda !!\
            \nNúmero de plugins : </b><code>{count}</code>\
            \n<b>Uso:</b> <code>.help</code> plugin name\n\n"
        catcount = 0
        for i in sorted(SUDO_LIST):
            string += "◆" + f"<code>{str(i)}</code>"
            string += "   "
            catcount += 1
        await event.reply(string.format(count=catcount), parse_mode="HTML")


@bot.on(admin_cmd(outgoing=True, pattern="info ?(.*)"))
@bot.on(sudo_cmd(pattern="info ?(.*)", allow_sudo=True))
async def info(event):
    """ For .info command,"""
    args = event.pattern_match.group(1).lower()
    if args:
        if args in CMD_HELP:
            await edit_or_reply(event, str(CMD_HELP[args]))
        else:
            event = await edit_or_reply(event, "Especifique um nome de plugin válido.")
            await asyncio.sleep(3)
            await event.delete()
    else:
        string = "<b>Por favor, especifique para qual plugin você quer ajuda !!\
            \nNúmero de plugins : </b><code>{count}</code>\
            \n<b>Uso : </b><code>.info</code> <plugin name>\n\n"
        catcount = 0
        for i in sorted(CMD_HELP):
            string += "◆ " + f"<code>{str(i)}</code>"
            string += "   "
            catcount += 1
        if event.from_id in Config.SUDO_USERS:
            await event.reply(string.format(count=catcount), parse_mode="HTML")
        else:
            await event.edit(string.format(count=catcount), parse_mode="HTML")


@bot.on(admin_cmd(pattern="dc$"))
@bot.on(sudo_cmd(pattern="dc$", allow_sudo=True))
async def _(event):
    result = await bot(functions.help.GetNearestDcRequest())
    result = (
        yaml_format(result)
        + "\n\n**Lista de data centers do Telegram:**\
                \nDC1 : Miami FL, USA\
                \nDC2 : Amsterdam, NL\
                \nDC3 : Miami FL, USA\
                \nDC4 : Amsterdam, NL\
                \nDC5 : Singapore, SG\
                "
    )
    await edit_or_reply(event, result)


@bot.on(admin_cmd(outgoing=True, pattern="setinline (true|false)"))
async def _(event):
    global HELPTYPE
    input_str = event.pattern_match.group(1)
    if input_str == "true":
        type = True
    else:
        type = False
    if HELPTYPE is True:
        if type is True:
            await event.edit("`inline mode is already enabled`")
        else:
            HELPTYPE = type
            await event.edit("`inline mode is disabled`")
    else:
        if type is True:
            HELPTYPE = type
            await event.edit("`inline mode is enabled`")
        else:
            await event.edit("`inline mode is already disabled`")
