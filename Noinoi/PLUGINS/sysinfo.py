# Copyright (C) 2021 Veez Project

import re
import uuid
import socket

import psutil
import platform
from Noinoi.config import BOT_USERNAME
from Noinoi.DREAMS.filters import command
from pyrogram import Client, filters
from Noinoi.DREAMS.decorators import sudo_users_only, humanbytes


# SYSTEM STATS

@Client.on_message(command(["gstats", f"gstats@{BOT_USERNAME}"]) & ~filters.edited)
@sudo_users_only
async def give_sysinfo(client, message):
    splatform = platform.system()
    platform_release = platform.release()
    platform_version = platform.version()
    architecture = platform.machine()
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(socket.gethostname())
    mac_address = ":".join(re.findall("..", "%012x" % uuid.getnode()))
    processor = platform.processor()
    ram = humanbytes(round(psutil.virtual_memory().total))
    cpu_freq = psutil.cpu_freq().current
    if cpu_freq >= 1000:
        cpu_freq = f"{round(cpu_freq / 1000, 2)}GHz"
    else:
        cpu_freq = f"{round(cpu_freq, 2)}MHz"
    du = psutil.disk_usage(client.workdir)
    psutil.disk_io_counters()
    disk = f"{humanbytes(du.used)} / {humanbytes(du.total)} " f"({du.percent}%)"
    cpu_len = len(psutil.Process().cpu_affinity())
    somsg = f"""π **ππππππ πππππππππππ **
    
**πππππππππ :** `{splatform}`
**πΏπππππππ - Release :** `{platform_release}`
**πΏπππππππ - Version :** `{platform_version}`
**π°πππππππππππ :** `{architecture}`
**π·πππππππ :** `{hostname}`
**πΈπΏ :** `{ip_address}`
**πΌππ :** `{mac_address}`
**πΏππππππππ :** `{processor}`
**πππ : ** `{ram}`
**π²πΏπ :** `{cpu_len}`
**π²πΏπ π΅ππ΄π :** `{cpu_freq}`
**π³πΈππΊ :** `{disk}`
    """
    await message.reply(somsg)
