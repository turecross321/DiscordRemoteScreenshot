import discord
from discord.ext import commands
import pyautogui
from playsound import playsound
import cv2
from PIL import Image

intents = discord.Intents.default()

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

try:
    with open('token.txt', 'r', encoding="utf-8") as token:
        bot_token = token.read()
except:
    print("No token.txt file found. Creating one...")
    with open('token.txt', 'w') as file:
        file.write("")
    print("Done. Please paste your bot token in the token.txt file.")
    input("")

syncTree = input("Do you wish to sync the command tree?\nOnly do this once. (y/n) ")
useCamera = input("Do you wish to use a webcam? (y/n) ")

if (useCamera.lower() == "y"):
    cam_port = input("camera port: ")
    cam = cv2.VideoCapture(int(cam_port))
    cam.set(cv2.CAP_PROP_AUTO_EXPOSURE, 3)

@bot.event
async def on_ready():
    print("Signed in as " + str(bot.user))
    if syncTree.lower() == "y":
        print("Syncing command tree...")
        await bot.tree.sync()
        print("The command tree has been synced.")

@bot.tree.command(name="screenshot", description="sends a screenshot of what host is currently doing on their pc")
async def Screenshot(interaction: discord.Interaction):

    if (useCamera.lower() == "y"):
        cam.read() # crank it on beforehands so the exposure isnt dfucked

    await interaction.response.defer()

    print("The screenshot command has been triggered by " + str(interaction.user))
    print("Attempting to play the notification sound effect.")

    try:
        playsound('./screenshot_notification.wav')
    except:
        await interaction.response.send_message("Failed to play screenshot_notification.wav. Make sure it is in the same folder as the python file!")
        return

    screenshot_file_name = "./screenshot.png"
    webcam_file_name = "./webcam.png"

    if (useCamera.lower() == "y"):
        result, image = cam.read()
        cv2.imwrite(webcam_file_name, image)

    image = pyautogui.screenshot()
    image.save("./" + screenshot_file_name)

    if (useCamera.lower() == "y"):
        img1 = Image.open(screenshot_file_name)
        img2 = Image.open(webcam_file_name)

        img2 = img2.resize((int(img1.width / 3), int(img1.height / 3)), Image.LANCZOS)

        img1.paste(img2, (0, 0))
        img1.save("combined.png")

        print(img2.size)

        await interaction.followup.send(file=discord.File("./combined.png"))

    else:
        await interaction.followup.send(file=discord.File(screenshot_file_name))

    print("Screenshot succesfully sent. (triggered by " + str(interaction.user) + ")")


bot.run(bot_token)
