from motobot import command, IRCLevel, Target, Notice


@command('copy', level=IRCLevel.master)
def copy_command(bot, context, message, args):
    try:
        target = args[1]
        message = ' '.join(args[2:])
        if message:
            response = (message, (message, Target(target)))
        else:
            response = ("Error: Message must be supplied.", Notice(context.nick))
    except IndexError:
        response = ("Error: Target must be supplied.", Notice(context.nick))
    return response
