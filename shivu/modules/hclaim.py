import asyncio
import logging
from datetime import datetime, timedelta
from pyrogram import Client, filters, types as t
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from shivu import shivuu as bot, user_collection, collection
from shivu import LOGGER
# Constants
DEVS = (7078181502)
CHAT_ID = "-1002428503112"
JOIN_URL = "https://t.me/PiratesMainchat"
CHARACTERS_PER_PAGE = 10

@bot.on_message(filters.command(["check"]))
async def hfind(_, message: t.Message):
    if len(message.command) < 2:
        return await message.reply_text("📌 Please provide the ID 🆔", quote=True)
    
    waifu_id = message.command[1]
    waifu = await collection.find_one({'id': waifu_id})
    
    if not waifu:
        return await message.reply_text("🔍 No character found with that ID ❌", quote=True)
    
    top_users = await user_collection.aggregate([
        {'$match': {'characters.id': waifu_id}},
        {'$unwind': '$characters'},
        {'$match': {'characters.id': waifu_id}},
        {'$group': {'_id': '$id', 'count': {'$sum': 1}}},
        {'$sort': {'count': -1}},
        {'$limit': 10}
    ]).to_list(length=10)
    
    usernames = []
    for user_info in top_users:
        user_id = user_info['_id']
        try:
            user = await bot.get_users(user_id)
            usernames.append(user.username if user.username else f"➥ {user_id}")
        except Exception:
            usernames.append(f"➥ {user_id}")
    
    caption = (
        f"📜 *Character Info*\n"
        f"🧩 *Name*: {waifu['name']}\n"
        f"🧬 *Rarity*: {waifu['rarity']}\n"
        f"📺 *Anime*: {waifu['anime']}\n"
        f"🆔 *ID*: {waifu['id']}\n\n"
        f"🏆 *Top Collectors*:\n\n"
    )
    for i, user_info in enumerate(top_users):
        count = user_info['count']
        username = usernames[i]
        caption += f"{i + 1}. {username} x{count}\n"
    
    await message.reply_photo(photo=waifu['img_url'], caption=caption)
