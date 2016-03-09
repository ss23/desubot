from motobot import command, sink


@command('trackdrah')
def trackdrah_command(bot, context, message, args):
    last = context.database.get()
    if last is None:
        response = "I don't currently know where drah is."
    else:
        response = "I last saw drah using '{}' as his nick.".format(last)
    return response


@sink()
def trackdrah_sink(bot, context, message):
    user = 'sgfhfhd'
    host = 'trapped.in.the.80s'
    if test(user, host, context.host):
        context.database.set(context.nick)


def test(test_user, test_host, fullhost):
    user, host = fullhost.split('@')
    return test_user.lower() in user.lower() or test_host.lower() in host.lower()
