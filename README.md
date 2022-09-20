# Wilson
Tired of proprietary discord bots? Looking for something that's free and open source? This is the bot for you!
## About Wilson
Wilson started as a simple college project which grew in size and went under a few rewrites, each as a closed-source codebase. With the recent revival of discord.py and the 2.0 update, I decided that for the next rewrite coinciding with the discord.py 2.0 update I would make Wilson entirely free and open source, especially since I myself was sick of proprietary closed-source bots (which for all I knew, just farmed data or hid features behind a paywall).

I encourage you to clone, modify and contribute to the project yourself, or just take the source code and make your own bot from it. I don't mind, so long as you adhere to the GNU GPLv3 as specified in the `LICENSE`. Happy hacking :)
## Configuring and Running
Get started by installing the requirements listed in requirements.txt:
```shell
# Linux/macOS
python3 -m pip install -r requirements.txt

# Windows
py -3 -m pip install -r requirements.txt
```
To run with your own bot, you'll need your discord user id and bot token. You will also need to create a configuration file named `config.py`, either by copying the `config.def.txt` file and renaming it, or simply running the `main.py` file, to automatically generate it.
```shell
# Linux/macOS
python3 ./main.py

# Windows
py -3 ./main.py
```
You'll need to ammend the following lines in the config with your user id and bot token:
```py
bot_settings.owner_id = 0 # Discord User ID
bot_settings.bot_token = '' # Bot token assigned from developer portal
```
Make any other changes you want to the config, then you can then re-run `main.py` and your bot is ready to go!