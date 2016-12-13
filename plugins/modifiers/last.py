from motobot import command, sink, Priority, split_response, Notice, request
from collections import defaultdict


MAX_LINES = 50
lines = defaultdict(lambda: [])


@sink(priority=Priority.high)
def last_sink(bot, context, message):
    lines[context.channel].append((context.nick, message))

    while len(lines[context.channel]) > MAX_LINES:
        lines[context.channel].pop(0)


@request('LINES')
def lines_request(bot, context, channel, start=None, end=None):
    channel_lines = lines[channel]
    requested = (channel_lines if start is None else
                 (channel_lines[start],) if end is None else
                 channel_lints[start:end])
    return list(format_lines(requested))


def format_lines(l):
    for nick, msg in l:
        yield "<{}> {}".format(nick, msg)


@command('last', priority=Priority.higher)
def last_command(bot, context, message, args):
    global lines
    response = None

    try:
        n = int(args[1])
        l = lines[context.channel][-n:]
        response = split_response(format_lines(l), separator=' ')
    except (ValueError, IndexError):
        response = ("Error: Must supply integer argument.", Notice(context.nick))

    return response
