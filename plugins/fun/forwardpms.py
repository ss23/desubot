from motobot import command, sink, IRCLevel, Target, Notice


@command('forwardpms', level=IRCLevel.master)
def forwardpms_command(bot, context, message, args):
    forwarding = context.session.get(set())
    nick = context.nick.lower()
    if nick in forwarding:
        forwarding.remove(nick)
        response = "I will no longer forward PMs to you."
    else:
        forwarding.add(nick)
        response = "I will forward PMs to you."
    context.session.set(forwarding)
    return response, Notice(nick)


@sink()
def forwardpms_sink(bot, context, message):
    if context.channel.lower() == bot.nick:
        forwarding = context.session.get(set())
        msg = "<{}> {}".format(context.nick, message)
        return [(msg, Target(nick)) for nick in forwarding]
