# Server manager Discord Bot

# Setup
## Prerequisites
* **Python 3.9 or later**
* **discord.py 2.3.0 or later**
* **python-dotenv 1.0**
* **Rename the file `.env.example` to `.env`**

## Step 1: Create a Discord bot

1. Go to https://discord.com/developers/applications create an application
2. Build a Discord bot under the application
3. Get the token from bot setting
![alt text](image.png)
4. Store the token to `.env` under the `DISCORD_BOT_TOKEN`
![alt text](image-1.png)
5. Turn MESSAGE CONTENT INTENT `ON`
![alt text](image-2.png)
6. Invite your bot to your server via OAuth2 URL Generator
![alt text](image-4.png)
![alt text](image-5.png)
![alt text](image-3.png)

## Step 2: Run the bot on the desktop

1. Open a terminal or command prompt

2. Navigate to the directory where you put your manager_bot.py file

3. Run `python3 manager_bot.py` or `python manager_bot.py` to run the bot

## Commands
--updating--