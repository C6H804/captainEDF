import subprocess
import json
import discord
from discord.ext import commands
import datetime
import locale


def getColorFromClassName(className):
    match className:
        case "jtp-tempodays__item jtp-tempodays__item--blue":
            return "bleu :blue_square:"
        case "jtp-tempodays__item jtp-tempodays__item--white":
            return "blanc :white_large_square:"
        case "jtp-tempodays__item jtp-tempodays__item--red":
            return "rouge :red_square:"
        case "jtp-tempodays__item jtp-tempodays__item--indet":
            return "indéterminé :question:"
        case _:
            return "inconnu"


locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
current_date = datetime.datetime.now()
month_number = current_date.month
formatted_date = current_date.strftime("%A %d")


numeroMois = ["None", "janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]
nomMois = numeroMois[month_number]


script_path = 'C:/Users/alanp/OneDrive/Bureau/EDF/py/06/getClassName.js'
result = subprocess.run(['node', script_path], capture_output=True, text=True)


# Vérifier si l'exécution a réussi
if result.returncode == 0:
    output = result.stdout.strip()
    class_names = json.loads(output)
    print("Class names:", class_names)
    couleurToday = getColorFromClassName(class_names[0])
    couleurTomorrow = getColorFromClassName(class_names[1])
else:
    print("Erreur lors de l'exécution du script JavaScript:", result.stderr)


print("Couleur d'aujourd'hui:", couleurToday)
print("Couleur de demain:", couleurTomorrow)


with open("TOKEN.txt", "r", encoding="utf-8") as file:
    Token = file.read().strip()
    
with open("liste_adresses.txt", "r", encoding="utf-8") as file:
    USER_ID = [ligne.strip() for ligne in file.readlines()]


MESSAGE_CONTENT = f'{formatted_date} {nomMois} :\nCouleur d\'aujourd\'hui: {couleurToday}\nCouleur de demain: {couleurTomorrow}'


intents = discord.Intents.default()
intents.messages = True


bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'Bot connecté en tant que {bot.user}')
    for i in range(len(USER_ID)):
        user = await bot.fetch_user(USER_ID[i])
        await user.send(MESSAGE_CONTENT)
    await bot.close()

bot.run(TOKEN)