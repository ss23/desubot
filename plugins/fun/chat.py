from motobot import command, sink, Action, Notice, Priority, IRCLevel, Eat, Target, split_response
from cleverbot import Cleverbot


def begin_chat(session, nick, channel):
    active_chats = session.get({})
    request = (channel.lower(), nick.lower())

    if request in active_chats:
        return False
    else:
        active_chats[request] = Cleverbot()
        session.set(active_chats)
        return True


def end_chat(session, nick, channel):
    active_chats = session.get({})
    request = (channel.lower(), nick.lower())

    try:
        del active_chats[request]
        session.set(active_chats)
        return True
    except KeyError:
        return False


def get_chat(session, nick, channel):
    return session.get({}).get((channel.lower(), nick.lower()))


@command('chat')
def chat_command(bot, context, message, args):
    if begin_chat(context.session, context.nick, context.channel):
        return "Hi {}!".format(context.nick)
    else:
        return "I'm already chatting with you.", Notice(context.nick)


@command('stopchat')
def stopchat_command(bot, context, message, args):
    if end_chat(context.session, context.nick, context.channel):
        return "Nice chatting with you {}!".format(context.nick)
    else:
        return "I wasn't chatting with you.", Notice(context.nick)


@sink(priority=Priority.high)
def chat_sink(bot, context, message):
    if not message.startswith(bot.command_prefix):
        chat = get_chat(context.session, context.nick, context.channel)
        if chat is not None:
            response = chat.ask(message)
            if response.startswith('*') and response.endswith('*.'):
                response = (response.strip('*.'), Action)
            return response, Eat


@command('chatwith', level=IRCLevel.master)
def chatwith_command(bot, context, message, args):
    try:
        target = args[1]
    except IndexError:
        return "You must give me someone to chat with.", Notice(context.nick)

    try:
        target_channel = args[2]
    except IndexError:
        target_channel = context.channel

    if begin_chat(context.session, target, target_channel):
        return (("I'm now chatting with {} on {}.".format(target, target_channel), Notice(context.nick)),
                ("Hi {}!".format(target), Target(target_channel)))
    else:
        return "I'm already chatting with {} on {}.".format(target, target_channel), Notice(context.nick)


@command('stopchatwith', level=IRCLevel.master)
def stopchatwith_command(bot, context, message, args):
    try:
        target = args[1]
    except IndexError:
        return "You must give me someone to chat with.", Notice(context.nick)

    try:
        target_channel = args[2]
    except IndexError:
        target_channel = context.channel

    if end_chat(context.session, target, target_channel):
        return "I'm no longer chatting with {} on {}.".format(target, target_channel), Notice(context.nick)
    else:
        return "I wasn't chatting with {} on {}.".format(target, target_channel), Notice(context.nick)


@command('listchat', level=IRCLevel.master)
@command('chatlist', level=IRCLevel.master)
def listchat_command(bot, context, message, args):
    chats = context.session.get({})
    if chats:
        response = split_response("I'm chatting with {} on {}".format(nick, chan)
                                  for chan, nick in chats.keys())
    else:
        response = "I'm not chatting with anyone anywhere."
    return response, Notice(context.nick)
