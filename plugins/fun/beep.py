from motobot import command


@command('beep')
def beep_command(bot, context, message, args):
    return 'BEEP!\x07'
