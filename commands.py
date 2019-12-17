response = None
message = None


def get_response(mess):
    global message
    message = mess
    if message.startswith('help'):
        info()
    if message.startswith('eval'):
        evaluate()
    if message.startswith('exec_func'):
        execute()
    if message.startswith('test'):
        test()
    return response


def info():
    global message
    global response
    response ="""
All bot commands must begin with "!"

!eval CODE
Evaluates a single line of Python code


!exec_func
CODE
CODE
CODE

Runs a Python program (Multiline included)
Bot says value of variable response

Useful for testing functions before adding them to the bot


!def_func FUNC_NAME KEY_WORD
CODE
CODE
CODE

Makes a function called FUNC_NAME
That is called when a message begins with !KEYWORD

When !KEYWORD is called CODE runs
Bot says value of variable response
"""
    
def evaluate():
    global message
    global response
    code = message[5:] # Removes 'eval '
    response = eval(code)


def execute():
    global message
    global response
    code = '\n'.join(message.split('\n')[1:])
    ns = {}
    exec(code, ns)
    response = ns['response']


def test():
    global message
    global response
    a = 10
    b = 20
    response = a + b
