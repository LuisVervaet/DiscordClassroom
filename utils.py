import discord
import config
import io
import requests


def get_profile(user_id):
    document = config.USERS.find_one({'user_id': user_id})
    if document is None:
        document = {'user_id': user_id, 'premium': False, 'is_student': True, 'google_classroom': None, 'note': None, 'classes': [], 'teacher_notifications': True, 'student_notifications': True}
        config.USERS.insert_one(document)
        return document, True
    return document, False


def get_user_classes(user_id):
    return config.CLASSES.find({'members': user_id})


def get_teaching_classes(user_id):
    return config.CLASSES.find({'owner': user_id})

def emoji(emoji):
    emoji_dict = {"leave": "<:leave:732461354065330266>", "time": "<:time:732461354014998619>",
                 "pin": "<:pin:732461353830449173>", "info": "<:info:732116410553073674>",
                 "bug": "<:bug:732105781025046578>", "gift": "<:gift:732105778055610428>",
                 "enter": "<:enter:732105777577459723>", "auth": "<:auth:732103030110945332>",
                 "on_b": "<:on_b:732103029930590229>", "off": "<:off:732103029892841564>",
                 "check_verify_b": "<:check_verify_b:732103029800697886>", "check": "<:check:732103029733720134>",
                 "announce": "<:announce:732103029725200425>", "cross": "<:cross:732103029712617482>",
                 "on": "<:on:732103029624537109>", "dev": "<:dev:732103029620211783>",
                 "people": "<:people:732103029565947934>", "news": "<:news:732103029565685770>",
                 "poo": "<:poo:732103029553364992>", "card": "<:card:732103029523873823>",
                 "plus": "<:plus:732103029435924491>", "inv": "<:inv:732103029213364295>",
                 "check_verify": "<:check_verify:732103029121089638>", "checkb": "<:checkb:732103029020557323>",
                 "online": "<:online:732103028873756683>", "crown": "<:crown:732103028781613117>",
                 "minus": "<:minus:732103028726824982>", "dbl": "<a:dbl:732105777703288883>",
                 "loading": "<a:loading:732103030799073291>", "bell": "<a:bell:732103030488432720>",
                 "error": "<:error:732714132461191330>", "settings": "<:settings:732811659118379008>"}
    try:
        theEmoji = emoji_dict[emoji.lower()]
    except:
        theEmoji = emoji_dict['error']
    return(theEmoji)

def get_file_version():
    versionfile = open('version.txt',mode='r')
    version = versionfile.read()
    versionfile.close()
    return version

def get_new_version():
    url = "https://raw.githubusercontent.com/LuisVervaet/DiscordClassroom/master/version.txt"
    read_data=str(requests.get(url).content)
    return_data=read_data.replace("b'","")
    return_data = return_data[:-3]
    return(return_data)
