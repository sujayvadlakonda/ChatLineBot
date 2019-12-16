import os
import time
import re
import requests
import importlib
from slackclient import SlackClient
import commands 

# This file is not included as it is classified information
# It sets the OAuth and SSL Certificate
# os.system('python3 set_env_variables.py')

command_dict = {}
api_dict = {}

# instantiate Slack client
slack_client = SlackClient(os.environ.get('CHAT_LINE_BOT_TOKEN'))
# starterbot's user ID in Slack: value is assigned after the bot starts up
starterbot_id = None

# constants
# Making this value 0 makes the server overheat
RTM_READ_DELAY = 1 # 1 second delay between reading from RTM


def parse_bot_commands(slack_events):
    """
        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.
    """
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            identifier, message = parse_direct_mention(event["text"])
            # if user_id == starterbot_id:
            if message:
                return message, event["channel"]
    return None, None

def parse_direct_mention(message_text):
    # Checks if the message begins with an exclamation mark
    return ('!', message_text[1:]) if message_text[0] == '!' else (None, None)

def handle_command(command, channel):
    """
        Executes bot command if the command is known
        Command only contains the message (The @bot part is removed somehow)
        Actually its because the first method only return the message, not user_id
    """
    # Default response is help text for the user
    default_response = "No command was found. Type !help for help"

    # Finds and executes the given command, filling in response
    print('Command is')
    print(command)
    response = None

    try:
        response = commands.get_response(command)

        if command.startswith('def_func'):
            lines = command.split("\n")
            first_line = lines[0]
            content = lines[1:]
            parameters = first_line.split(" ")
            def_command(parameters[1], parameters[2], content)

            

        # Add a method to handle !help


        if command.startswith('add_command'):
            command_parts = command.split(' ')
            key_word = command_parts[1]
            output = command_parts[2]
            command_dict[key_word] = output

        if command.startswith('add_api'):
            command_parts = command.split(' ')
            key_word = command_parts[1]
            api = command_parts[2][1:-1]
            api = api.replace("&amp;", "&")
            command_dict[key_word] = api

        if command.startswith('call_api'):
            command_parts = command.split(' ')
            key_word = command_parts[1]
            query = command_parts[2]
            api = command_dict[key_word]
            url = api + query
            print(url)
            response = requests.get(url)

    except Exception as error:
            response = "Error: " + str(error)
    

    # for key_word, output in command_dict.items():
    #     if identify_command(command, key_word):
    #         response = output

    # Sends the response back to the channel
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response or default_response
    )
# Looks for the word KEY_WORD anywhere in COMMAND
def identify_command(command, key_word):
    return command.startswith(key_word) or command.endswith(key_word) or key_word in command

def def_command(function_name, key_word, content):
    print("Function Name: {}".format(function_name))
    print("Key Word: {}".format(key_word))
    print("Content: \n{}".format(content))
    
    lines = None

    with open('commands.py', 'r') as file:
        lines = file.readlines()

    with open('commands.py', 'w') as file:
        lines.insert(10, "    if message.startswith('{}'):\n        {}()\n".format(key_word, function_name))
        file.write("".join(lines))

    with open('commands.py', 'a') as file:
        print(lines)
        func_text = "\n\ndef {}():\n    global message\n    global response\n    {}"
        file.write(func_text.format(function_name, "\n    ".join(content)))

    importlib.reload(commands)

if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            command, channel = parse_bot_commands(slack_client.rtm_read())
            if command:
                handle_command(command, channel)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")

