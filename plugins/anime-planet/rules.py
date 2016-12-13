from motobot import command, strip_control_codes
from re import compile, IGNORECASE
from functools import wraps


punctuation = r'.!?;\b'
remove_pants = compile(r'([{0}])[a-z ]*?pant[a-z ]*?[{0}]'.format(punctuation), IGNORECASE)
rules_url = 'http://bit.ly/1L1tnfV'


def targetted(func):
    @wraps(func)
    def wrapped(bot, context, message, args):
        response = func(bot, context, message, args)
        if len(args) > 1:
            response = "{}: {}".format(' '.join(args[1:]), response)
        return response
    return wrapped


def channel(channel):
    def decorator(func):
        @wraps(func)
        def wrapped(bot, context, *args, **kwargs):
            if context.channel.lower() == channel.lower():
                return func(bot, context, *args, **kwargs)
        return wrapped
    return decorator


@command('welcome')
@targetted
def welcome_command(bot, context, message, args):
    """ Welcome a user to anime-planet.com and possibly read them the topic. """
    response = bot.request('TOPIC', context.channel)
    response = "Welcome to {}!".format(context.channel) \
        if response is None else remove_pants.sub(r'\1', response)
    return strip_control_codes(response)


@command('stats')
@channel('#anime-planet.com')
def stats_command(bot, context, message, args):
    """ Return the stats link for #anime-planet.com. """
    if context.channel.lower() == '#anime-planet.com':
        stats_url = 'https://www.chalamius.se/stats/ap.html'
        return "Channel Stats: {}".format(stats_url)


@command('rules')
@targetted
def rules_command(bot, context, message, args):
    """ Return the rules link. """
    return 'Please read the channel rules: {}'.format(rules_url)


@command('rr')
@targetted
def rr_command(bot, context, message, args):
    """ Return the recommendations response. """
    return ("If you are looking for anime/manga recommendations we have a database created "
            "specifically for that! Just visit www.anime-planet.com and let us do the hard "
            "work for you! For channel rules, please go to {}".format(rules_url))


@command('mib')
@targetted
def mib_command(bot, context, message, args):
    """ Help mibs get a real nick. Takes single arg for target. """
    return ("To change your nick to something you'd like type: /nick new_name; "
            "If you like that name and it is unregistered. "
            "To register it use: /ns REGISTER password [email]; "
            "More information can be found here: "
            "https://wiki.rizon.net/index.php?title=Register_your_nickname")


@command('worstcharacterofalltime')
def sothis_wishes(bot, context, message, args):
    """ Return the worse character of all time. So says sothis. """
    url = 'http://www.anime-planet.com/characters/makoto-itou'
    return "Behold, the worst anime character of all time, Makoto Itou! {}".format(url)
