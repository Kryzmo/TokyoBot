# TokyoBot

TokyoBot is a Discord bot that provides various features including chat supervision, channel and role configuration, user avatar display, music playback, server information display, art display, moderation commands, and easy addition or removal of functionalities.

## Features

- **Chat Supervisor**: TokyoBot can supervise the chat and filter out inappropriate or offensive content.
- **Channel and Role Configuration**: TokyoBot allows you to configure channels and roles easily.
- **Supervisor Commands**: TokyoBot provides supervisor commands to manage the server effectively.
- **User Avatar Display**: TokyoBot can display the avatar of any user.
- **Music Playback**: TokyoBot can play music in voice channels.
- **Server Information Display**: TokyoBot can show various information about the server.
- **Art**: TokyoBot can display arts from various sources.
- **Moderation Commands**: TokyoBot provides moderation commands to manage the server's members.
- **Easy Addition or Removal of Functionalities**: TokyoBot allows you to easily add or remove functionalities as the bot is build modularly, and new function can be added without affecting already written code.

## Installation

To install TokyoBot, follow these steps:

1. Clone the repository: `git clone https://github.com/Kryzmo/TokyoBot.git`
2. Install the required dependencies: `python -m pip install -r requirements.txt`
3. Configure the bot by adding your Discord bot token and other necessary details in the configuration files.
4. Make sure that you are in the directory the bot is installed in.

#### Windows

5. Start the bot: `python master.py`

#### Linux

5. Start the bot: `./run.sh`

## Usage

Once the bot is running, you can use commands such as:

- `!dev h`: Show configuration of channels, roles and messages.
- `!avatar <user>`: Displays the avatar of the specified user.
- `!play <song>`: Plays the specified song in a voice channel.
- `!serverinfo`: Displays information about the server.
- `!art <keyword>`: Displays an image related to the specified keyword.
- `!mute <user> <duration> <reason>`: Kicks the specified user from the server.
- `!kick <user> <reason>`: Kicks the specified user from the server.
- `!ban <user> <reason>`: Bans the specified user from the server.

And many more...

## License

TokyoBot is released under the [MIT License](https://opensource.org/licenses/MIT).
