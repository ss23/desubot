from motobot import command
from random import randint


@command('rainbow', hidden=True)
def rainbow_command(bot, context, message, args):
    return rainbow(' '.join(args[1:]))


def rainbow(string):
    rainbow_colours = (4, 7, 8, 3, 2, 13, 6)
    return '\x02' + ''.join('\x0300,{:02}{}'.format(c, s) for c, s in
        zip(rainbow_colours, split(string, len(rainbow_colours))))


def split(string, no_groups):
    group_size = len(string) // no_groups
    extra = len(string) % no_groups

    last_end = 0
    for i in range(no_groups):
        end = last_end + group_size + (1 if i < extra else 0)
        yield string[last_end:end]
        last_end = end
