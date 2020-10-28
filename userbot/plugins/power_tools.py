import sys
from os import execl
from time import sleep

from ..utils import admin_cmd, edit_or_reply, sudo_cmd
from . import BOTLOG, BOTLOG_CHATID, CMD_HELP, bot


@borg.on(admin_cmd(pattern="restart$"))
@borg.on(sudo_cmd(pattern="restart$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, "#RESTART \n" "Bot Restarted")
    await edit_or_reply(
        event,
        "Reiniciado. `.ping` ou `.help` para verificar se estou online, na verdade, leva 1-2 minutos para reiniciar",
    )
    await bot.disconnect()
    execl(sys.executable, sys.executable, *sys.argv)


@borg.on(admin_cmd(pattern="shutdown$"))
@borg.on(sudo_cmd(pattern="shutdown$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, "#SHUTDOWN \n" "Bot shut down")
    await edit_or_reply(event, "Turning off ...Manually turn me on later")
    await bot.disconnect()


@borg.on(admin_cmd(pattern="sleep( [0-9]+)?$"))
@borg.on(sudo_cmd(pattern="sleep( [0-9]+)?$", allow_sudo=True))
async def _(event):
    if " " not in event.pattern_match.group(1):
        return await edit_or_reply(event, "Syntax: `.sleep time`")
    counter = int(event.pattern_match.group(1))
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "Você colocou o bot para dormir por " + str(counter) + " segundos",
        )
    event = await edit_or_reply(event, f"`ok, let me sleep for {counter} segundos`")
    sleep(counter)
    await event.edit("`OK, I'm awake now.`")


CMD_HELP.update(
    {
        "power_tools": "**Plugin : **`power_tools`\
                \n\n**Syntax : **`.restart`\
                \n**Uso : **Restarts the bot !!\
                \n\n**Syntax : **'.sleep <seconds>\
                \n**Uso: **Userbots get tired too. Let yours snooze for a few seconds.\
                \n\n**Syntax : **`.shutdown`\
                \n**Uso : **Sometimes you need to shut down your bot. Sometimes you just hope to\
                hear Windows XP shutdown sound... but you don't."
    }
)
