import os
import time
import re
import requests
import importlib
from slackclient import SlackClient
import commands # The commands.py file

# This file is not included as it is classified information
# It sets the OAuth and SSL Certificate
# os.system('python3 set_env_variables.py')

command_dict = {}
api_dict = {}

# instantiate Slack client
slack_client = SlackClient(os.environ.get('CHAT_LINE_BOT_TOKEN'))

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
            if event["text"][0] == '!':
                return event["text"][1:], event["channel"]
    return None, None


def handle_command(command, channel):
    default_response = "No command was found. Type !help for help"

    print('Command is')
    print(command)
    response = None

    try:
        response = commands.get_response(command)
        print(response)

        if command.startswith('def_func'):
            lines = command.split("\n")
            first_line = lines[0]
            content = lines[1:]
            parameters = first_line.split(" ")
            def_command(parameters[1], parameters[2], content)

            

        # Add a method to handle !help


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
    

    # Sends the response back to the channel
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response or default_response
    )


def def_command(function_name, key_word, content):
    print("Function Name: {}".format(function_name))
    print("Key Word: {}".format(key_word))
    print("Content: \n{}".format(content))
    
    lines = None

    with open('commands.py', 'r') as file:
        lines = file.readlines()

    with open('commands.py', 'w') as file:
        if_statement = "    if message.startswith('{}'):\n        {}()\n"
        lines.insert(12, if_statement.format(key_word, function_name))
        file.write("".join(lines))

    with open('commands.py', 'a') as file:
        print(lines)
        func_text = "\n\ndef {}():\n    global message\n    global response\n    {}"
        file.write(func_text.format(function_name, "\n    ".join(content)))

    importlib.reload(commands) # The bot reloads the commands.py file
                               # Prevents restart of bot to update



if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")
        while True:
            command, channel = parse_bot_commands(slack_client.rtm_read())
            if command:
                handle_command(command, channel)
                time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")
