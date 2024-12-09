from pymongo import MongoClient
from pyrogram import Client, filters
from shivu import shivuu as app

# Set your admin user ID
ADMIN_USER_ID = 7078181502

# Connect to MongoDB
client = MongoClient('mongodb+srv://bikash:bikash@bikash.3jkvhp7.mongodb.net/?retryWrites=true&w=majority')  # Adjust the connection string as needed
db = client['character_catcherr']
banned_users_collection = db['pban']

def load_banned_users():
    banned_users = banned_users_collection.find({}, {'_id': 0, 'user_id': 1})
    return {str(user['user_id']) for user in banned_users}

def save_banned_user(user_id):
    banned_users_collection.insert_one({'user_id': user_id})

def remove_banned_user(user_id):
    banned_users_collection.delete_one({'user_id': user_id})

def get_banned_users_list():
    return banned_users_collection.find({}, {'_id': 0, 'user_id': 1})

banned_users = load_banned_users()

@app.on_message(filters.command("pban") & filters.user(ADMIN_USER_ID))
def pban(client, message):
    user = message.reply_to_message.from_user if message.reply_to_message else None
    if user:
        user_id = user.id
        first_name = user.first_name
        save_banned_user(user_id)
        banned_users.add(str(user_id))
        user_link = f"[{first_name}](tg://user?id={user_id})"
        response_message = f"User {user_link} (ID: {user_id}) has been permanently banned."
        message.reply(response_message, disable_web_page_preview=True)
    else:
        message.reply("Please reply to a user message to ban them.")

@app.on_message(filters.command("unpban") & filters.user(ADMIN_USER_ID))
def unban(client, message):
    if message.reply_to_message:
        user = message.reply_to_message.from_user
        user_id = user.id
        if str(user_id) in banned_users:
            remove_banned_user(user_id)
            banned_users.remove(str(user_id))
            user_link = f"[{user.first_name}](tg://user?id={user_id})"
            response_message = f"User {user_link} (ID: {user_id}) has been unbanned."
            message.reply(response_message, disable_web_page_preview=True)
        else:
            message.reply("This user is not banned.")
    else:
        message.reply("Please reply to a user message to unban them.")

@app.on_message(filters.command("pbanlist") & filters.user(ADMIN_USER_ID))
def pbanlist(client, message):
    banned_users = get_banned_users_list()
    user_links = []

    for user in banned_users:
        user_links.append(f"[User ID: {user['user_id']}](tg://user?id={user['user_id']})")

    if user_links:
        response_message = "Here is the list of permanently banned users:\n\n"
        response_message += "\n".join(user_links)
    else:
        response_message = "There are currently no banned users."

    message.reply(response_message, disable_web_page_preview=True)

@app.on_message(filters.all)
def check_ban(client, message):
    if message.from_user and str(message.from_user.id) in banned_users:
        message.reply("lawde tu bot se ban ho gaya pahle @xeno_kakarot ko papa bol 👎.")
