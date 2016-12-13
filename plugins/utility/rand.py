from motobot import command, Notice
from random import randint


@command('rand')
@command('roll')
def rand_command(bot, context, message, args):
    try:
        max = abs(int(args[1]))
        max = max if max > 0 else 1
    except ValueError:
        return "Argument has to be a valid integer.", Notice(context.nick)
    except IndexError:
        max = 6
    result = randint(1, max)
    return "Result of {max}: {result}".format(**locals())
