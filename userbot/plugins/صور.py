import os
import shutil

from userbot import jmthon

from ..core.managers import edit_or_reply
from ..helpers.google_image_download import googleimagesdownload
from ..helpers.utils import reply_id

plugin_category = "misc"


@jmthon.ar_cmd(
    pattern="صور(?: |$)(\d*)? ?([\s\S]*)",
    command=("صور", plugin_category),
    info={
        "header": "Google image search.",
        "description": "To search images in google. By default will send 3 images.you can get more images(upto 10 only by changing limit value as shown in usage and examples.",
        "usage": ["{tr}img <1-10> <query>", "{tr}img <query>"],
        "examples": [
            "{tr}img 10 JMTHON",
            "{tr}img JMTHON ",
            "{tr}img 7 JMTHON ",
        ],
    },
)
async def img_sampler(event):
    "Google image search."
    reply_to_id = await reply_id(event)
    if event.is_reply and not event.pattern_match.group(2):
        query = await event.get_reply_message()
        query = str(query.message)
    else:
        query = str(event.pattern_match.group(2))
    if not query:
        return await edit_or_reply(
            event, "**يجب كـتابة نـص او بالـرد عـلى نـص اولا ⌬**"
        )
    cat = await edit_or_reply(event, "**⌔︙ يـتم الـتعـرف انتـظر قلـيلا ⏱")
    if event.pattern_match.group(1) != "":
        lim = int(event.pattern_match.group(1))
        if lim > 10:
            lim = int(10)
        if lim <= 0:
            lim = int(1)
    else:
        lim = int(3)
    response = googleimagesdownload()
    arguments = {
        "keywords": query,
        "limit": lim,
        "format": "jpg",
        "no_directory": "no_directory",
    }
    try:
        paths = response.download(arguments)
    except Exception as e:
        return await cat.edit(f"**خـطـأ**: \n`{e}`")
    lst = paths[0][query]
    await event.client.send_file(event.chat_id, lst, reply_to=reply_to_id)
    shutil.rmtree(os.path.dirname(os.path.abspath(lst[0])))
    await cat.delete()
