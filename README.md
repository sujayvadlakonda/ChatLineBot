The Chat Line Bot aims to allows developers to create functions for a Slack bot using the chat line in Slack.

Python code is directly evaluated to edit the source code of the bot

## HOW TO RUN THE BOT

In order to make the bot work you must type the following into your terminal

1. `export CHAT_LINE_BOT_TOKEN='Bot User OAuth Access Token'`

2. `export WEBSOCKET_CLIENT_CA_BUNDLE=DigiCertGlobalRootCA.crt`

3. `python3 bot.py`


Commands are differentiated from regular messages by adding an "!" at the beginning

## CREATING FUNCTIONS

"""
!def_func FUNCTION_NAME KEY_WORD
CODE
"""

A function called FUNCTION_NAME is added to commands.py
CODE is executed whenever the user begins a message with !KEYWORD
The function returns a response by setting a response variable equal to something in CODE
(E.g. response = "The bot says whatever is here")
