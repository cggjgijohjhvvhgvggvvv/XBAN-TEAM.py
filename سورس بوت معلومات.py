import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram.ext import Updater, MessageHandler, Filters
import datetime
import pytz

print('run')
TOKEN = "BOT TOKEN"

def handle_message(update, context):
    text = update.message.text

    if text.startswith("#"):
        context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        xyz = text[1:]
        server = text[12:]
        api_url = f"http://freefireapi.com.br/api/search_id?id={xyz}&region={server}"

        try:
            response = requests.get(api_url)
            api_response = response.json()

            if api_response.get('basicInfo') is None:
                message = "No results found."
            else:
                uid = xyz
                name = api_response['basicInfo']['nickname']
                level = api_response['basicInfo']['level']
                likes = api_response['basicInfo'].get('liked', 'Not found')
                last_login_unix = int(api_response['basicInfo']['lastLoginAt'])
                xp = api_response['basicInfo'].get('exp', 'Not found')
                br_points = api_response['basicInfo']['rankingPoints']
                bio = api_response['socialInfo'].get('signature', 'Not found')

                ist = pytz.timezone('Europe/Moscow')
                last_login_utc = datetime.datetime.utcfromtimestamp(last_login_unix)
                last_login_ist = last_login_utc.replace(tzinfo=pytz.utc).astimezone(ist)
                last_login = last_login_ist.strftime('%d %B %Y %I:%M %p')

                created_at_unix = int(api_response['basicInfo']['createAt'])
                created_at_utc = datetime.datetime.utcfromtimestamp(created_at_unix)
                created_at_ist = created_at_utc.replace(tzinfo=pytz.utc).astimezone(ist)
                created_at = created_at_ist.strftime('%d %B %Y %I:%M %p')

                if 1000 <= br_points <= 1100:
                    br = "Bronze 1"
                elif 1100 < br_points <= 1200:
                    br = "Bronze 2"
                elif 1200 < br_points <= 1300:
                        br_rank = "Bronze 3"
                elif 1300 < br_points <= 1400:
                        br_rank = "Silver 1"
                elif 1400 < br_points <= 1500:
                        br_rank = "Silver 2"
                elif 1500 < br_points <= 1600:
                        br_rank = "Silver 3"
                elif 1600 < br_points <= 1725:
                        br_rank = "Gold 1"
                elif 1725 < br_points <= 1850:
                        br_rank = "Gold 2"
                elif 1850 < br_points <= 1975:
                        br_rank = "Gold 3"
                elif 1975 < br_points <= 2100:
                        br_rank = "Platinum 1"
                elif 2100 < br_points <= 2350:
                        br_rank = "Platinum 2"
                elif 2350 < br_points <= 2475:
                        br_rank = "Platinum 3"
                elif 2475 < br_points <= 2600:
                        br_rank = "Platinum 4"
                elif 2600 < br_points <= 2750:
                        br_rank = "Diamond 1"
                elif 2750 < br_points <= 2900:
                        br_rank = "Diamond 2"
                elif 2900 < br_points <= 3050:
                        br_rank = "Diamond 3"
                elif 3050 < br_points <= 3200:
                        br_rank = "Diamond 4"
                else:
                        br_rank = "Heroic"
                        
                        
                message = (f"```SATURN444\n"
                           f"ㅤ\n"
                           f"🎮UID  {uid}\n"
                           f"ㅤ\n"
                           f"👤NAME  {name}\n"
                           f"ㅤ\n"
                           f"🎖️Level  {level}\n"
                           f"ㅤ\n"
                           f"❤️Likes  {likes}\n"
                           f"ㅤ\n"
                           f"🕰️Created On {created_at} Russia time 🇷🇺\n"
                           f"ㅤ\n"
                           f"🔍Last Login  {last_login} Russia time 🇷🇺;\n"
                           f"ㅤ\n"
                           f"🔥Exp {xp}\n"
                           f"ㅤ\n"
                           f"🏆BR Rank {br}\n"
                           f"ㅤ\n"
                           f"📓 Bio {bio}```")

                context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode='MarkdownV2')
        except Exception as e:
            print(f"An error occurred: {e}")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()