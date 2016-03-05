from motobot import match, Action
from random import uniform


@match(r'\*(.+? )(stabs) desubot')
def stab_match(bot, context, message, match):
    if uniform(0, 100) >= 50:
        response = ["parries {}".format(context.nick)]
        if uniform(0, 100) >= 50:
            response.append("ripostes {}".format(context.nick))
    else:
        response = "dies"
    return response, Action
