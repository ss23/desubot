from motobot import command, match
from re import compile, IGNORECASE


sed_pattern = compile(r'^(?:.+)sed(?: ?)(?:s?)\/(.*?)\/(.*?)\/(?:.*?) (.+)$', IGNORECASE)


@command('sed')
def sed_command(bot, context, message, args):
    match = sed_pattern.match(message)
    if match is not None:
        pattern, replace, arg = match.groups()
        pattern = compile(pattern, IGNORECASE)
        return pattern.sub(replace, arg)


@match(r'^s/(.+?)/(.+?)(?:/)?$')
def sed_match(bot, context, message, match):
    regex, replacement = match.groups()
    pattern = compile(regex, IGNORECASE)
    lines = bot.request('LINES', context.channel)[1::-1]

    for line in lines:
        new_str, i = pattern.subn(replacement, line)
        if i != 0:
            return new_str
