import asyncio
import json
import os
import subprocess
import time
from datetime import datetime
from pathlib import Path

from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from telethon.tl.types import DocumentAttributeVideo

from ..utils import admin_cmd, edit_or_reply, sudo_cmd
from . import CMD_HELP, LOGS, progress

thumb_image_path = Config.TMP_DOWNLOAD_DIRECTORY + "/thumb_image.jpg"


async def catlst_of_files(path):
    files = []
    for dirname, dirnames, filenames in os.walk(path):
        # print path to all filenames.
        for filename in filenames:
            files.append(os.path.join(dirname, filename))
    return files


def get_video_thumb(file, output=None, width=320):
    output = file + ".jpg"
    metadata = extractMetadata(createParser(file))
    p = subprocess.Popen(
        [
            "ffmpeg",
            "-i",
            file,
            "-ss",
            str(
                int((0, metadata.get("duration").seconds)[metadata.has("duration")] / 2)
            ),
            # '-filter:v', 'scale={}:-1'.format(width),
            "-vframes",
            "1",
            output,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )
    p.communicate()
    if not p.returncode and os.path.lexists(file):
        return output


def extract_w_h(file):
    """ Get width and height of media """
    command_to_run = [
        "ffprobe",
        "-v",
        "quiet",
        "-print_format",
        "json",
        "-show_format",
        "-show_streams",
        file,
    ]
    # https://stackoverflow.com/a/11236144/4723940
    try:
        t_response = subprocess.check_output(command_to_run, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as exc:
        LOGS.warning(exc)
    else:
        x_reponse = t_response.decode("UTF-8")
        response_json = json.loads(x_reponse)
        width = int(response_json["streams"][0]["width"])
        height = int(response_json["streams"][0]["height"])
        return width, height


def sortthings(contents, path):
    catsort = []
    contents.sort()
    for file in contents:
        catpath = os.path.join(path, file)
        if os.path.isfile(catpath):
            catsort.append(file)
    for file in contents:
        catpath = os.path.join(path, file)
        if os.path.isdir(catpath):
            catsort.append(file)
    return catsort


async def upload(path, event, udir_event):
    global uploaded
    if os.path.isdir(path):
        await event.client.send_message(
            event.chat_id,
            f"**Pasta : **`{str(path)}`",
        )
        Files = os.listdir(path)
        Files = sortthings(Files, path)
        for file in Files:
            catpath = os.path.join(path, file)
            await upload(catpath, event, udir_event)
    elif os.path.isfile(path):
        caption_rts = os.path.basename(path)
        c_time = time.time()
        thumb = None
        if os.path.exists(thumb_image_path):
            thumb = thumb_image_path
        if not caption_rts.lower().endswith(".mp4"):
            await event.client.send_file(
                event.chat_id,
                path,
                caption=f"**Nome do arquivo : **`{caption_rts}`",
                force_document=False,
                thumb=thumb,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, udir_event, c_time, "Carregando...", caption_rts)
                ),
            )
        else:
            metadata = extractMetadata(createParser(str(path)))
            duration = 0
            width = 0
            height = 0
            if metadata.has("duration"):
                duration = metadata.get("duration").seconds
            if metadata.has("width"):
                width = metadata.get("width")
            if metadata.has("height"):
                height = metadata.get("height")
            await event.client.send_file(
                event.chat_id,
                path,
                caption=f"**Nome do arquivo : **`{caption_rts}`",
                thumb=thumb,
                force_document=False,
                supports_streaming=True,
                attributes=[
                    DocumentAttributeVideo(
                        duration=duration,
                        w=width,
                        h=height,
                        round_message=False,
                        supports_streaming=True,
                    )
                ],
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, udir_event, c_time, "Carregando...", caption_rts)
                ),
            )
        uploaded += 1


@bot.on(admin_cmd(pattern="upload (.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="upload (.*)", allow_sudo=True))
async def uploadir(event):
    global uploaded
    input_str = "".join(event.text.split(maxsplit=1)[1:])
    path = Path(input_str)
    start = datetime.now()
    if not os.path.exists(path):
        await edit_or_reply(
            event,
            f"`não existe tal diretório/arquivo com o nome {path} para enviar`",
        )
        return
    udir_event = await edit_or_reply(event, "Carregando....")
    if os.path.isdir(path):
        udir_event = await edit_or_reply(
            event, f"`Coletando detalhes do arquivo no diretório {path}`"
        )
        uploaded = 0
        await upload(path, event, udir_event)
        end = datetime.now()
        ms = (end - start).seconds
        await udir_event.edit(
            f"`Carregado {uploaded} arquivos com sucesso em {ms} segundos. `"
        )
    else:
        udir_event = await edit_or_reply(event, f"`Carregando.....`")
        uploaded = 0
        await upload(path, event, udir_event)
        end = datetime.now()
        ms = (end - start).seconds
        await udir_event.edit(
            f"`Carregado arquivo {str(path)} com sucesso em {ms} segundos. `"
        )
    await asyncio.sleep(5)
    await udir_event.delete()


@bot.on(admin_cmd(pattern="uploadas(stream|vn|all) (.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="uploadas(stream|vn|all) (.*)", allow_sudo=True))
async def uploadas(event):
    # For .uploadas command, allows you to specify some arguments for upload.
    type_of_upload = event.pattern_match.group(1)
    input_str = event.pattern_match.group(2)
    uas_event = await edit_or_reply(event, "enviando.....")
    supports_streaming = False
    round_message = False
    spam_big_messages = False
    if type_of_upload == "all":
        spam_big_messages = True
    elif type_of_upload == "stream":
        supports_streaming = True
    elif type_of_upload == "vn":
        round_message = True
    thumb = None
    file_name = None
    if "|" in input_str:
        file_name, thumb = input_str.split("|")
        file_name = file_name.strip()
        thumb = thumb.strip()
    else:
        file_name = input_str
        thumb = vthumb = get_video_thumb(file_name)
    if not thumb and os.path.exists(thumb_image_path):
        thumb = thumb_image_path
    if os.path.exists(file_name):
        metadata = extractMetadata(createParser(file_name))
        duration = 0
        width = 0
        height = 0
        if metadata.has("duration"):
            duration = metadata.get("duration").seconds
        if metadata.has("width"):
            width = metadata.get("width")
        if metadata.has("height"):
            height = metadata.get("height")
        try:
            if supports_streaming:
                c_time = time.time()
                await borg.send_file(
                    uas_event.chat_id,
                    file_name,
                    thumb=thumb,
                    caption=input_str,
                    force_document=False,
                    allow_cache=False,
                    reply_to=event.message.id,
                    attributes=[
                        DocumentAttributeVideo(
                            duration=duration,
                            w=width,
                            h=height,
                            round_message=False,
                            supports_streaming=True,
                        )
                    ],
                    progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                        progress(d, t, uas_event, c_time, "Carregando...", file_name)
                    ),
                )
            elif round_message:
                c_time = time.time()
                await borg.send_file(
                    uas_event.chat_id,
                    file_name,
                    thumb=thumb,
                    allow_cache=False,
                    reply_to=event.message.id,
                    video_note=True,
                    attributes=[
                        DocumentAttributeVideo(
                            duration=60,
                            w=1,
                            h=1,
                            round_message=True,
                            supports_streaming=True,
                        )
                    ],
                    progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                        progress(d, t, uas_event, c_time, "Carregado...", file_name)
                    ),
                )
            elif spam_big_messages:
                await uas_event.edit("TBD: Ainda não implementado")
                return
            try:
                os.remove(vthumb)
            except BaseException:
                pass
            await uas_event.edit("Carregado com sucesso !!")
        except FileNotFoundError as err:
            await uas_event.edit(str(err))
    else:
        await uas_event.edit("404: Arquivo não encontrado")


CMD_HELP.update(
    {
        "upload": "**Plugin :** `upload`\
    \n\n**Syntax :** `.upload caminho do arquivo/pasta`\
    \n**Uso : **Carrega o arquivo do servidor ou lista de arquivos dessa pasta\
    \n\n**Syntax : **`.uploadasstream caminho de vídeo/áudio`\
    \n**Uso : **Carrega vídeo/áudio como reproduzível no servidor\
    \n\n**Syntax : **`.uploadasvn caminho do vídeo`\
    \n**Uso : **Carrega vídeo/áudio como vídeo redondo do servidor **O presente oferece suporte a poucos vídeos que precisam ser executados; leva algum tempo para desenvolvê-lo **\
    "
    }
)
