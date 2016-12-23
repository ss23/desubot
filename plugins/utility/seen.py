from motobot import command, hook, sink, Priority
from time import strftime, gmtime
from collections import defaultdict


def get_data(database):
    return defaultdict(dict, database.get({}))


@command('seen')
def seen_command(bot, context, message, args):
    response = None
    try:
        query = args[1].lower()
        if query == bot.nick.lower():
            response = "I have never seen myself; it's too dark in {}'s slave labour camp.".format(
                context.channel)
        else:
            response = get_data(context.database)[context.channel][query]
    except IndexError:
        response = "I see you!"
    except KeyError:
        response = "I've never seen {}.".format(args[1])
    return response


@sink(priority=Priority.max)
def seen_sink(bot, context, message):
    msg = "{} was last seen on {} saying \"{}\".".format(
        context.nick, get_time(), message)
    data = get_data(context.database)
    data[context.channel][context.nick.lower()] = msg
    context.database.set(data)


@hook('JOIN')
def join_hook(bot, context, message):
    msg = "{} was last seen on {} joining the channel.".format(
        message.nick, get_time())
    data = get_data(context.database)
    data[message.params[0]][message.nick.lower()] = msg
    context.database.set(data)


@hook('NICK')
def nick_hook(bot, context, message):
    data = get_data(context.database)

    msg = "{} was last seen on {} when they changed their nick to {}.".format(
        message.nick, get_time(), message.params[0])
    for channel, nicks in data.items():
        for nick in nicks.keys():
            if nick == message.nick.lower():
                data[channel][nick] = msg

    msg = "{} was last seen on {} when they changed their nick from {}.".format(
        message.params[0], get_time(), message.nick)
    for channel, nicks in data.items():
        for nick in nicks.keys():
            if nick == message.params[0].lower():
                data[channel][nick] = msg
    context.database.set(data)


@hook('QUIT')
def quit_hook(bot, context, message):
    msg = "{} was last seen on {} when they quit.".format(
        message.nick, get_time())
    data = get_data(context.database)
    for channel, nicks in data.items():
        for nick in nicks.keys():
            if nick == message.nick.lower():
                data[channel][nick] = msg
    context.database.set(data)


@hook('PART')
def part_hook(bot, context, message):
    msg = "{} was last seen on {} when they part the channel.".format(
        message.nick, get_time())
    data = get_data(context.database)
    data[message.params[0]][message.nick.lower()] = msg
    context.database.set(data)


def get_time():
    return strftime('%a %b %d %H:%M:%S UTC', gmtime())
