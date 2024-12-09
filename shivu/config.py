class Config(object):
    LOGGER = True

    # Get this value from my.telegram.org/apps
    OWNER_ID = "7180469677"
    sudo_users = "7078181502", "5884969921", "5289413488", "7180469677", "1843986084"
    GROUP_ID = -1002009280180
    TOKEN = "7698227314:AAFXpcHqU2ThPMaZK2DByzedj0Ma0ruVVnc"
    mongo_url = "mongodb+srv://bikash:bikash@bikash.3jkvhp7.mongodb.net/?retryWrites=true&w=majority"
    PHOTO_URL = ["https://files.catbox.moe/ji0au6.jpg", "https://files.catbox.moe/gs0okz.jpg"]
    SUPPORT_CHAT = "PiratesMainchat"
    UPDATE_CHAT = "PiratesBotRepo"
    BOT_USERNAME = "WaifuGrabberXtreme_bot"
    CHARA_CHANNEL_ID = "-1002412957777"
    api_id = 26626068
    api_hash = "bf423698bcbe33cfd58b11c78c42caa2"

    
class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True
