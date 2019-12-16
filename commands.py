default_response = "No command was found :|"
response = None
message = None


def get_response(mess):
    global message
    message = mess
    evaluate()
    execute()
    if message.startswith('test'):
        test()
    return response or default_response


def evaluate():
    global message
    global response
    if message.startswith('eval'):
        code = message[5:] # Removes 'eval '
        response = eval(code)


def execute():
    global message
    global response
    if message.startswith('exec_func'):
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