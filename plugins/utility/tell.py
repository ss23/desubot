from motobot import command, sink, Notice


@command('tell')
def tell_command(bot, context, message, args):
    """ Send a message to a user the next time they're active.

    Usage: tell <nick> <message>
    """
    try:
        nick = args[1]
        message = ' '.join(args[2:])
        if message:
            tells = context.database.get({})
            messages = tells.get(nick.lower(), [])
            messages.append((context.nick, message))
            tells[nick.lower()] = messages
            context.database.set(tells)
            response = "I will tell {} \"{}\" next time I see them.".format(
                nick, message)
        else:
            response = "Error: Please provide a message to tell."
    except IndexError:
        response = "Error: Please provide a nick to tell to."
    return response, Notice(context.nick)


@sink()
def tell_sink(bot, context, message):
    try:
        target = context.nick
        tells = context.database.get({})
        messages = tells.pop(target.lower())
        context.database.set(tells)
        response = (format_messages(messages), Notice(target))
    except KeyError:
        response = None
    return response


def format_messages(messages):
    for sender, message in messages:
        yield "{} said: {}".format(sender, message)
