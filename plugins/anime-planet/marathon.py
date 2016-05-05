from motobot import command
from requests import get
from itertools import groupby


base_url = 'https://marathon.chalamius.se/'


@command('marathonlist')
def marathonlist_command(bot, context, message, args):
    """ Return the marathon website. """
    return "The marathon list can be found at {}.".format(base_url)


@command('marathon')
def marathon_command(bot, context, message, args):
    """ Return details of the current show on the marathon list. """
    return get_current_marathons()


def get_current_marathons():
    try:
        response = []
        url = base_url + 'calendar.json'
        key = lambda x: x['date']
        entries = sorted(get(url, timeout=5).json()['items'], key=key)

        for _, group in groupby(entries, key=key):
            latest_entries = list(group)

        main_picks = []
        other_picks = []
        for entry in latest_entries:
            if entry['note'].lower().startswith('main pick'):
                main_picks.append(entry)
            else:
                other_picks.append(entry)

        for entry in main_picks if main_picks else other_picks:
            response.append("Today's marathon ({date}) is {name} ({url}) {note}".format(**entry))

        if main_picks and other_picks:
            response.append(
                "There are more picks today. Check {} for more details.".format(base_url))
    except IndexError:
        response = "There are currently no marathons active."
    return response


@command('pantsu')
@command('pants')
@command('panties')
def pants_command(bot, context, message, args):
    """ PANTIES! Need moar? """
    url = 'https://www.youtube.com/watch?v=T_tAoo787q4'
    title = 'Sora no Otoshimono #2 Creditless ED'
    return '{}! {} - {}'.format(args[0].capitalize(), title, url)


@command('bewbs')
@command('boobs')
@command('boobies')
def boobs_command(bot, context, message, args):
    """ BOOBS! Need moar? """
    url = 'https://www.youtube.com/watch?v=Pw5lu06LvH4'
    title = 'Oppai Dragon Song'
    return '{}! {} - {}'.format(args[0].capitalize(), title, url)


@command('butts')
def butts_command(bot, context, message, args):
    """ BUTTS! Need moar? """
    url = 'http://i219.photobucket.com/albums/cc65/_chii69_/AnimalButts.jpg'
    return '{}! {}'.format(args[0].capitalize(), url)
