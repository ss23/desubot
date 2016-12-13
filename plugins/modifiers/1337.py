from motobot import command
from random import choice
from re import compile, IGNORECASE


leet_map = {
    'a': ('/-\\', '/\\', '4', '@'),
    'b': ('|3', '8', '|o'),
    'c': ('<', '(', 'K', 'S'),
    'd': ('|)','o|', '|>', '<|'),
    'e': ('3',),
    'f': ('|=', 'ph'),
    'g': (')', '9', '6'),
    'h': ('|-|', '}-{', ']-[', ')-(', '#'),
    'i': ('l', '1', '|', '!', ']['),
    'j': ('_|',),
    'k': ('|<', '/<', '\<', '|{'),
    'l': ('|_', '|', '1'),
    'm': ('|\\/|', '/\\/\\', '(\\/)', '/|\\', '/V\\'),
    'n': ('|\\|', '/\\/', '/|/'),
    'o': ('0', '()', '[]'),
    'p': ('|2', '|D'),
    'q': ('(,)', 'kw'),
    'r': ('|2', '|Z', '|?'),
    's': ('5', '$'),
    't': ('+', '\'][\'', '7'),
    'u': ('|_|', '(_)'),
    'v': ('|/', '\|', '\/'),
    'w': ('\/\/', '\|\|', 'VV', '\\\'', '\^/'),
    'x': ('><', '}{'),
    'y': ('`/', '\'/', 'j'),
    'z': ('2', '(\)')
}


@command('leet')
@command('1337')
def leet_command(bot, context, message, args):
    """ Convert something to 13375|D34|< """
    return ''.join(map(lambda c: choice(leet_map.get(c.lower(), (c,))), ' '.join(args[1:])))


@command('unleet')
def unleet_command(bot, context, message, args):
    """ Reverse the leet process using mad hax. """
    return capitalize(''.join(unleet(' '.join(args[1:]))))


@command('capitalize')
@command('capitalise')
def capitalize_command(bot, context, message, args):
    return capitalize(' '.join(args[1:]))


@command('bell')
def bell_command(bot, context, message, args):
    return ' '.join(args[1:]) + '\x07'


def unleet(input):
    i = 0
    while input[i:]:
        try:
            c, advance = max(((c, len(leet)) for c, leets in leet_map.items()
                             for leet in leets if input[i:].startswith(leet)),
                             key=lambda x: x[1])
        except ValueError:
            c = input[i]
            advance = len(c)
        yield c
        i += advance


capitalize_expression = compile(r'(^\w|\bi\b|(?:\.|\?|\!) \w|\b\w\.)', IGNORECASE)


def capitalize(input):
    return capitalize_expression.sub(lambda m: m.group(1).upper(), input)
