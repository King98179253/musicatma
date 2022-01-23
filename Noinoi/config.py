import os
from os import getenv
from dotenv import load_dotenv
from Noinoi.DREAMS.uptools import fetch_heroku_git_url

if os.path.exists("local.env"):
    load_dotenv("local.env")

load_dotenv()
admins = {}
SESSION_NAME = getenv("SESSION_NAME", "session")
BOT_TOKEN = getenv("BOT_TOKEN")
BOT_NAME = getenv("BOT_NAME", "ɴᴏɪ ɴᴏɪ ᴍᴜsɪᴄ 🌸")
API_ID = int(getenv("API_ID"))
API_HASH = getenv("API_HASH")
IMG_1 = getenv("IMG_1", "https://telegra.ph/file/7d0ea6c4ebf78c401ee94.jpg")
IMG_2 = getenv("IMG_2", "https://telegra.ph/file/7d0ea6c4ebf78c401ee94.jpg")
IMG_3 = getenv("IMG_3", "https://telegra.ph/file/7d0ea6c4ebf78c401ee94.jpg")
IMG_4 = getenv("IMG_4", "https://telegra.ph/file/7d0ea6c4ebf78c401ee94.jpg")
OWNER_NAME = getenv("OWNER_NAME", "BHATAKTI")
ALIVE_NAME = getenv("ALIVE_NAME", "BHATAKTI ATMA ᴍᴜsɪᴄ 🔥")
BOT_USERNAME = getenv("BOT_USERNAME", "MUSIC_ATMA_BOT")
ASSISTANT_NAME = getenv("ASSISTANT_NAME", "ZINDA_H_TU_MERE_LIYE_HEART_HACK)
GROUP_SUPPORT = getenv("GROUP_SUPPORT", "SUBHI_WORLD)
UPDATES_CHANNEL = getenv("UPDATES_CHANNEL", "A_BUT)
SUDO_USERS = list(map(int, getenv("SUDO_USERS").split()))
COMMAND_PREFIXES = list(getenv("COMMAND_PREFIXES", "/ ! .").split())
ALIVE_IMG = getenv("ALIVE_IMG", "https://telegra.ph/file/1970b4029ec6d293b9a37.mp4")
DURATION_LIMIT = int(getenv("DURATION_LIMIT", "60"))
UPSTREAM_REPO = getenv("UPSTREAM_REPO", "https://github.com/King98179253/musicatma")
DATABASE_URL = os.environ.get("DATABASE_URL")  # fill with your mongodb url
