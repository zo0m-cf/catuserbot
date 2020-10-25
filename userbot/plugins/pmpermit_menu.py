"""
Support chatbox for pmpermit.
Used by incoming messages with trigger as /start
Will not work for already approved people.
Credits: written by ༺αиυвιѕ༻ {@A_Dark_Princ3}
"""
import asyncio

from telethon import events, functions

import userbot.plugins.sql_helper.pmpermit_sql as pmpermit_sql

from . import ALIVE_NAME, PM_START

DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else "cat"
PREV_REPLY_MESSAGE = {}


@bot.on(events.NewMessage(pattern=r"\/start", incoming=True))
async def _(event):
    chat_id = event.from_id
    if not pmpermit_sql.is_approved(chat_id):
        chat = await event.get_chat()
        if chat_id not in PM_START:
            PM_START.append(chat_id)
        if event.fwd_from:
            return
        if not event.is_private:
            return
        PM = (
            "Olá. Você está acessando o menu de solicitação de contato., "
            f"{DEFAULTUSER}.\n"
            "__Agora você pode me dizer porque está aqui.__\n"
            "**Escolha um dos seguintes motivos pelos quais você está aqui:**\n\n"
            "`a`. Para conversar comigo\n"
            "`b`. Para fazer spam = AUTOBLOCK.\n"
            "`c`. Para perguntar algo\n"
            "`d`. Para pedir algo\n"
        )
        ONE = (
            "__OK. Sua solicitação foi registrada. Em breve será aprovado e poderá conversar comigo.__\n\n"
            "**⚠️ Por favor não envie SPAM. ⚠️**\n\n"
            "__Use__ `/start` __para voltar ao menu principal.__"
        )
        TWO = "**OK, Como você já deve imaginar SPAM=AUTOBLOCK.**"
        THREE = "OK. Sua solicitação foi registrada. Em breve será aprovado e poderá fazer sua pergunta.\n **Não pergunte repetidamente, senão você será bloqueado e denunciado.**"
        FOUR = "OK. Sua solicitação foi registrada. Em breve será aprovado e poderá fazer seu pedido.\n**Não faça pedidos repetidamente, senão você será bloqueado e denunciado.**"
        LWARN = "**Este é o seu último aviso. NÃO envie outra mensagem, aguarde aprovação, senão você será bloqueado e denunciado pelo sistema automaticamente.**\n__Use__ `/start` __para voltar ao menu principal.__"
        try:
            async with event.client.conversation(chat) as conv:
                if pmpermit_sql.is_approved(chat_id):
                    return
                await event.client.send_message(chat, PM)
                chat_id = event.from_id
                response = await conv.get_response(chat)
                y = response.text
                if y == "a":
                    if pmpermit_sql.is_approved(chat_id):
                        return
                    await event.client.send_message(chat, ONE)
                    response = await conv.get_response(chat)
                    if not response.text == "/start":
                        if pmpermit_sql.is_approved(chat_id):
                            return
                        await event.client.send_message(chat, LWARN)
                        response = await conv.get_response(chat)
                        if not response.text == "/start":
                            if pmpermit_sql.is_approved(chat_id):
                                return
                            await event.client.send_message(chat, TWO)
                            await asyncio.sleep(3)
                            await event.client(functions.contacts.BlockRequest(chat_id))
                elif y == "b":
                    if pmpermit_sql.is_approved(chat_id):
                        return
                    await event.client.send_message(chat, LWARN)
                    response = await conv.get_response(chat)
                    if not response.text == "/start":
                        if pmpermit_sql.is_approved(chat_id):
                            return
                        await event.client.send_message(chat, TWO)
                        await asyncio.sleep(3)
                        await event.client(functions.contacts.BlockRequest(chat_id))
                elif y == "c":
                    if pmpermit_sql.is_approved(chat_id):
                        return
                    await event.client.send_message(chat, THREE)
                    response = await conv.get_response(chat)
                    if not response.text == "/start":
                        if pmpermit_sql.is_approved(chat_id):
                            return
                        await event.client.send_message(chat, LWARN)
                        response = await conv.get_response(chat)
                        if not response.text == "/start":
                            if pmpermit_sql.is_approved(chat_id):
                                return
                            await event.client.send_message(chat, TWO)
                            await asyncio.sleep(3)
                            await event.client(functions.contacts.BlockRequest(chat_id))
                elif y == "d":
                    if pmpermit_sql.is_approved(chat_id):
                        return
                    await event.client.send_message(chat, FOUR)
                    response = await conv.get_response(chat)
                    if not response.text == "/start":
                        if pmpermit_sql.is_approved(chat_id):
                            return
                        await event.client.send_message(chat, LWARN)
                        response = await conv.get_response(chat)
                        if not response.text == "/start":
                            if pmpermit_sql.is_approved(chat_id):
                                return
                            await event.client.send_message(chat, TWO)
                            await asyncio.sleep(3)
                            await event.client(functions.contacts.BlockRequest(chat_id))
                else:
                    if pmpermit_sql.is_approved(chat_id):
                        return
                    await event.client.send_message(
                        chat,
                        "Você digitou um comando inválido. Por favor envie `/start` novamente ou não envie outra mensagem se você não deseja ser bloqueado e denunciado.",
                    )
                    response = await conv.get_response(chat)
                    z = response.text
                    if not z == "/start":
                        if pmpermit_sql.is_approved(chat_id):
                            return
                        await event.client.send_message(chat, LWARN)
                        await conv.get_response(chat)
                        if not response.text == "/start":
                            if pmpermit_sql.is_approved(chat_id):
                                return
                            await event.client.send_message(chat, TWO)
                            await asyncio.sleep(3)
                            await event.client(functions.contacts.BlockRequest(chat_id))
        except:
            pass
