from motobot import command, sink, Priority, IRCLevel, Notice
from random import choice
from collections import defaultdict


last_blames = defaultdict(lambda: None)
next_blame = None


@command('blame')
def blame_command(bot, context, message, args):
    """ Blame the person who we all know did it! """
    global next_blame

    if next_blame is not None:
        target = next_blame
        next_blame = None
    elif last_blames[context.channel] is None:
        target = context.nick
    else:
        target = last_blames[context.channel]
    last_blames[context.channel] = context.nick

    return 'It was ' + target + '!'


@command('setblame', level=IRCLevel.master)
@command('nextblame', level=IRCLevel.master)
def setblame_command(bot, context, message, args):
    global next_blame
    response = ''
    try:
        target = ' '.join(args[1:])
        next_blame = target
        response = "Next blame set to blame {}.".format(target)
    except IndexError:
        response = "Error: Please supply a user to blame."
    return response, Notice(context.nick)
