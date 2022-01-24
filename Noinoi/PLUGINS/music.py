# © NOINOI MUSIC @CFC_BOT_SUPPORT

import re
import asyncio

from Noinoi.config import ASSISTANT_NAME, BOT_USERNAME, IMG_1, IMG_2
from Noinoi.DREAMS.thumbnail import thumb
from Noinoi.DREAMS.chatname import CHAT_TITLE
from Noinoi.DREAMS.filters import command, other_filters
from Noinoi.DREAMS.queues import QUEUE, add_to_queue
from Noinoi.DREAMS.cfc import call_py, user
from Noinoi.DREAMS.utils import bash
from pyrogram import Client
from pyrogram.errors import UserAlreadyParticipant, UserNotParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pytgcalls import StreamType
from pytgcalls.types.input_stream import AudioPiped
from youtubesearchpython import VideosSearch


def ytsearch(query: str):
    try:
        search = VideosSearch(query, limit=1).result()
        data = search["result"][0]
        songname = data["title"]
        url = data["link"]
        duration = data["duration"]
        thumbnail = f"https://i.ytimg.com/vi/{data['id']}/hqdefault.jpg"
        return [songname, url, duration, thumbnail]
    except Exception as e:
        print(e)
        return 0


async def ytdl(format: str, link: str):
    stdout, stderr = await bash(f'youtube-dl -g -f "{format}" {link}')
    if stdout:
        return 1, stdout.split("\n")[0]
    return 0, stderr


@Client.on_message(command(["play", f"play@{BOT_USERNAME}"]) & other_filters)
async def play(c: Client, m: Message):
    await m.delete()
    replied = m.reply_to_message
    chat_id = m.chat.id
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("• Gʀᴏᴜᴘ", url=f"https://t.me/SUBHI_WORLD"),
                InlineKeyboardButton(
                    "• Cʜᴀɴɴᴇʟ", url=f"https://t.me/A_BUT/32"),
            ]
        ]
    )
    if m.sender_chat:
        return await m.reply_text("**you're an Anonymous Admin revert back to user account from admin rights.**")
    try:
        aing = await c.get_me()
    except Exception as e:
        return await m.reply_text(f"error:\n\n{e}")
    a = await c.get_chat_member(chat_id, aing.id)
    if a.status != "administrator":
        await m.reply_text(
            f"💡 **To use me, I need to be an Administrator with the following permissions** : \n» 📢 **Delete messages**\n» 📢 **Add users**\n» 📢 **Manage video chat**\n\n**Data is updated** automatically after you **promote me**"
        )
        return
    if not a.can_manage_voice_chats:
        await m.reply_text(
            "💬 Missing voice chat permission."
        )
        return
    if not a.can_delete_messages:
        await m.reply_text(
            "💬 Missing delete chat permission."
        )
        return
    if not a.can_invite_users:
        await m.reply_text("💬 Missing add user permission.")
        return
    try:
        ubot = (await user.get_me()).id
        b = await c.get_chat_member(chat_id, ubot)
        if b.status == "kicked":
            await m.reply_text(
                f"@{ASSISTANT_NAME} **𝐢𝐬 𝐛𝐚𝐧𝐧𝐞𝐝 𝐢𝐧 𝐠𝐫𝐨𝐮𝐩** {m.chat.title}\n\n» **𝐮𝐧𝐛𝐚𝐧𝐭𝐡𝐞 𝐮𝐬𝐞𝐫𝐨𝐭 𝐟𝐢𝐫𝐬𝐭 𝐢𝐟 𝐲𝐨𝐮 𝐰𝐚𝐧𝐭 𝐭𝐨 𝐮𝐬𝐞 𝐭𝐡𝐢𝐬 𝐛𝐨𝐭🔥.**"
            )
            return
    except UserNotParticipant:
        if m.chat.username:
            try:
                await user.join_chat(m.chat.username)
            except Exception as e:
                await m.reply_text(f"💬 **𝐌𝐘 𝐀𝐒𝐒𝐈𝐒𝐓𝐀𝐍𝐓 𝐅𝐀𝐈𝐋𝐃 𝐓𝐎 𝐉𝐎𝐈𝐍 𝐓𝐇𝐈𝐒 𝐂𝐇𝐀𝐓**\n\n**reason**: `{e}`")
                return
        else:
            try:
                invitelink = await c.export_chat_invite_link(
                    m.chat.id
                )
                if invitelink.startswith("https://t.me/+"):
                    invitelink = invitelink.replace(
                        "https://t.me/+", "https://t.me/joinchat/"
                    )
                await user.join_chat(invitelink)
            except UserAlreadyParticipant:
                pass
            except Exception as e:
                return await m.reply_text(
                    f"💬 **𝐔𝐒𝐄𝐑 𝐁𝐎𝐓 𝐅𝐀𝐈𝐋𝐃 𝐓𝐎 𝐉𝐎𝐈𝐍 **\n\n**reason**: `{e}`"
                )
    if replied:
        if replied.audio or replied.voice:
            suhu = await replied.reply("📥 **𝐃𝐎𝐖𝐍𝐋𝐎𝐀𝐃𝐈𝐍𝐆...**")
            dl = await replied.download()
            link = replied.link
            if replied.audio:
                if replied.audio.title:
                    songname = replied.audio.title[:70]
                else:
                    if replied.audio.file_name:
                        songname = replied.audio.file_name[:70]
                    else:
                        songname = "Audio"
            elif replied.voice:
                songname = "Voice Note"
            if chat_id in QUEUE:
                pos = add_to_queue(chat_id, songname, dl, link, "Audio", 0)
                await suhu.delete()
                await m.reply_photo(
                    photo=f"{IMG_1}",
                    caption=f"💡 **Track added to queue »** `{pos}`\n\n🏷 **Name:** [{songname[:22]}]({link}) | `music`\n💭 **Chat:** `{chat_id}`\n🎧 **Request by:** {m.from_user.mention()}",
                    reply_markup=keyboard,
                )
            else:
             try:
                await suhu.edit("🔄 **𝐂𝐎𝐍𝐍𝐄𝐂𝐓𝐈𝐍𝐆 𝐓𝐎 𝐕𝐂...**")
                await call_py.join_group_call(
                    chat_id,
                    AudioPiped(
                        dl,
                    ),
                    stream_type=StreamType().local_stream,
                )
                add_to_queue(chat_id, songname, dl, link, "Audio", 0)
                await suhu.delete()
                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                await m.reply_photo(
                    photo=f"{IMG_2}",
                    caption=f"🏷 **Name:** [{songname[:22]}]({link})\n💭 **Chat:** `{chat_id}`\n💡 **Status:** `Playing`\n🎧 **Request by:** {requester}",
                    reply_markup=keyboard,
                )
             except Exception as e:
                await suhu.delete()
                await m.reply_text(f"💬 error:\n\n» {e}")
        else:
            if len(m.command) < 2:
                await m.reply(
                    "💬 reply to an **audio file** or **give something to search.**"
                )
            else:
                suhu = await c.send_message(chat_id, "🔍")
                query = m.text.split(None, 1)[1]
                search = ytsearch(query)
                if search == 0:
                    await suhu.edit("💬 **𝐍𝐎 𝐑𝐄𝐒𝐔𝐋𝐓 𝐅𝐎𝐔𝐍𝐃.**")
                else:
                    songname = search[0]
                    title = search[0]
                    url = search[1]
                    duration = search[2]
                    thumbnail = search[3]
                    userid = m.from_user.id
                    gcname = m.chat.title
                    ctitle = await CHAT_TITLE(gcname)
                    image = await thumb(thumbnail, title, userid, ctitle)
                    format = "bestaudio[ext=m4a]"
                    veez, ytlink = await ytdl(format, url)
                    if veez == 0:
                        await suhu.edit(f"💬 yt-dl issues detected\n\n» `{ytlink}`")
                    else:
                        if chat_id in QUEUE:
                            pos = add_to_queue(
                                chat_id, songname, ytlink, url, "Audio", 0
                            )
                            await suhu.delete()
                            requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                            await m.reply_photo(
                                photo=image,
                                caption=f"💡 **Track added to queue »** `{pos}`\n\n🏷 **Name:** [{songname[:22]}]({url}) | `music`\n**⏱ Duration:** `{duration}`\n🎧 **Request by:** {requester}",
                                reply_markup=keyboard,
                            )
                        else:
                            try:
                                await suhu.edit("🔄 **𝐜𝐨𝐧𝐧𝐞𝐜𝐭𝐢𝐧𝐠 𝐭𝐨 𝐯𝐜...**")
                                await call_py.join_group_call(
                                    chat_id,
                                    AudioPiped(
                                        ytlink,
                                    ),
                                    stream_type=StreamType().local_stream,
                                )
                                add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                                await suhu.delete()
                                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                                await m.reply_photo(
                                    photo=image,
                                    caption=f"🏷 **Name:** [{songname[:22]}]({url})\n**⏱ Duration:** `{duration}`\n💡 **Status:** `Playing`\n🎧 **Request by:** {requester}",
                                    reply_markup=keyboard,
                                )
                            except Exception as ep:
                                await suhu.delete()
                                await m.reply_text(f"💬 error: `{ep}`")

    else:
        if len(m.command) < 2:
            await m.reply(
                "💬 **Reply to an audio file or give something to search.**"
            )
        else:
            suhu = await c.send_message(chat_id, "🔍 ")
            query = m.text.split(None, 1)[1]
            search = ytsearch(query)
            if search == 0:
                await suhu.edit("💬 **no results found.**")
            else:
                songname = search[0]
                title = search[0]
                url = search[1]
                duration = search[2]
                thumbnail = search[3]
                userid = m.from_user.id
                gcname = m.chat.title
                ctitle = await CHAT_TITLE(gcname)
                image = await thumb(thumbnail, title, userid, ctitle)
                format = "bestaudio[ext=m4a]"
                veez, ytlink = await ytdl(format, url)
                if veez == 0:
                    await suhu.edit(f"💬 yt-dl issues detected\n\n» `{ytlink}`")
                else:
                    if chat_id in QUEUE:
                        pos = add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                        await suhu.delete()
                        requester = (
                            f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                        )
                        await m.reply_photo(
                            photo=image,
                            caption=f"💡 **Track added to queue »** `{pos}`\n\n🏷 **Name:** [{songname[:22]}]({url}) | `music`\n**⏱ Duration:** `{duration}`\n🎧 **Request by:** {requester}",
                            reply_markup=keyboard,
                        )
                    else:
                        try:
                            await suhu.edit("🔄 **Connecting to vc...**")
                            await call_py.join_group_call(
                                chat_id,
                                AudioPiped(
                                    ytlink,
                                ),
                                stream_type=StreamType().local_stream,
                            )
                            add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                            await suhu.delete()
                            requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                            await m.reply_photo(
                                photo=image,
                                caption=f"🏷 **Name:** [{songname[:22]}]({url})\n**⏱ Duration:** `{duration}`\n💡 **Status:** `Playing`\n🎧 **Request by:** {requester}",
                                reply_markup=keyboard,
                            )
                        except Exception as ep:
                            await suhu.delete()
                            await m.reply_text(f"💬 error: `{ep}`")
