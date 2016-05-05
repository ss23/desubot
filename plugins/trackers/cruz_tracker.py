from motobot import command, sink


@command('trackcruz', hidden=True)
def trackcruz_command(bot, context, message, args):
    last = context.database.get()
    if last is None:
        response = "I don't currently know where cruz is."
    else:
        response = "I last saw cruz using '{}' as his nick.".format(last)
    return response


@sink()
def trackcruz_sink(bot, context, message):
    user = 'cruz'
    host = 'Chiaki.Loves.Marika.Sama'
    if test(user, host, context.host):
        context.database.set(context.nick)


def test(test_user, test_host, fullhost):
    user, host = fullhost.split('@')
    return test_user.lower() in user.lower() or test_host.lower() in host.lower()
