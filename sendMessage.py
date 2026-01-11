import subprocess
import json
import discord
from discord.ext import commands
import datetime
import locale

def createTextMessage(couleurToday, couleurTomorrow):
    date = getDateInfo()
    smileyToday = getSmileyFromColor(couleurToday.split()[0])
    smileyTomorrow = getSmileyFromColor(couleurTomorrow.split()[0])
    message = f'{date[0]} {date[1]} :\nCouleur d\'aujourd\'hui : {couleurToday.split()[0]} {smileyToday}\nCouleur de demain : {couleurTomorrow.split()[0]} {smileyTomorrow}'
    return message

def getDateInfo():
    locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
    current_date = datetime.datetime.now()
    month_number = current_date.month
    formatted_date = current_date.strftime("%A %d")

    numeroMois = ["None", "janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]
    nomMois = numeroMois[month_number]

    return formatted_date, nomMois

def getSmileyFromColor(color):
    match color:
        case "Bleu":
            return ":blue_square:"
        case "Blanc":
            return ":white_large_square:"
        case "Rouge":
            return ":red_square:"
        case "Inconnu":
            return ":question:"
        case _:
            return ""
        
def prepareMessage():
    script_path = "./getColor.js"
    result = subprocess.run(['node', script_path], capture_output=True, text=True)

    # Vérifier si l'exécution a réussi
    if result.returncode == 0:
        output = result.stdout.strip()
        today = output.split()[0]
        tomorrow = output.split()[1]
        MESSAGE_CONTENT = createTextMessage(today, tomorrow)
        # envoyer message via discord bot
        return MESSAGE_CONTENT
    else:
        print("Erreur lors de l'exécution du script JavaScript:", result.stderr)
        return None

def getToken():
    with open("TOKEN.txt", "r", encoding="utf-8") as file:
        Token = file.read().strip()
    return Token

def getUserIDs():
    with open("liste_adresses.txt", "r", encoding="utf-8") as file:
        USER_ID = [ligne.strip() for ligne in file.readlines()]
    return USER_ID

def sendMessageToUsers(message):
    token = getToken()
    user_ids = getUserIDs()
    bot = connectDiscordBot()
    
    @bot.event
    async def on_ready():
        print(f"Bot connecté en tant que {bot.user}")
        for user_id in user_ids:
            try:
                user = await bot.fetch_user(int(user_id))
                await user.send(message)
                print(f"Message envoyé à {user.name}")
            except Exception as e:
                print(f"Erreur lors de l'envoi à {user_id}: {e}")
        await bot.close()
    
    bot.run(token)

def connectDiscordBot():
    intents = discord.Intents.default()
    bot = commands.Bot(command_prefix='!', intents=intents)
    return bot

def main():
    message = prepareMessage()
    if message:
        print(f"Message préparé: {message}")
        sendMessageToUsers(message)
        print("Messages envoyés avec succès.")
    else:
        print("Le message n'a pas pu être préparé.")

main()