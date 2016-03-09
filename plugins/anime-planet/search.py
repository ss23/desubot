from motobot import command
from requests import get
from bs4 import BeautifulSoup


base_url = 'https://www.anime-planet.com'
results_cache = iter(())
search_format = "Search result: {}"
rec_format = "Recommendations: {}"
top_format = "Top Anime: {}"


@command('a')
@command('anime')
def anime_search_command(bot, context, message, args):
    """ Search for an anime on anime-planet.com. """
    query = ' '.join(args[1:])
    if query:
        response = search_format.format(search_ap(query, 'anime'))
    else:
        response = "Please supply a search term."
    return response


@command('m')
@command('manga')
def manga_search_command(bot, context, message, args):
    """ Search for a manga on anime-planet.com. """
    query = ' '.join(args[1:])
    if query:
        response = search_format.format(search_ap(query, 'manga'))
    else:
        response = "Please supply a search term."
    return response


@command('u')
@command('user')
def user_search_command(bot, context, message, args):
    """ Search for a user on anime-planet.com. """
    query = ' '.join(args[1:])
    if not query:
        query = context.nick
    return search_format.format(search_ap(query, 'users'))


@command('c')
@command('char')
@command('character')
def character_search_command(bot, context, message, args):
    """ Search for a character on anime-planet.com. """
    query = ' '.join(args[1:])
    if query:
        response = search_format.format(search_ap(query, 'characters'))
    else:
        response = "Please supply a search term."
    return response


@command('rec')
@command('arec')
def anime_recommendations_search_command(bot, context, message, args):
    """ Search for an anime recommendation on anime-planet.com. """
    query = ' '.join(args[1:])
    if query:
        response = rec_format.format(search_ap(query, 'anime', '/recommendations'))
    else:
        response = "Please supply a search term."
    return response


@command('mrec')
def manga_recommendations_search_command(bot, context, message, args):
    """ Search for a manga recommendation on anime-planet.com. """
    query = ' '.join(args[1:])
    if query:
        response = rec_format.format(search_ap(query, 'manga', '/recommendations'))
    else:
        response = "Please supply a search term."
    return response


@command('top')
def top_anime_command(bot, context, message, args):
    """ Search for a user's lists on anime-planet.com. """
    query = ' '.join(args[1:])
    if query:
        response = top_format.format(search_ap(query, 'users', '/lists'))
    else:
        response = "Please supply a search term."
    return response


@command('tag')
@command('atag')
def atag_command(bot, context, message, args):
    """ Search for anime of the given tag. """
    tag = '-'.join(args[1:])
    return search_tag(tag, 'anime')


@command('mtag')
def mtag_command(bot, context, message, args):
    """ Search for manga of the given tag. """
    tag = '-'.join(args[1:])
    return search_tag(tag, 'manga')


def search_tag(tag, type):
    url = base_url + '/' + type + '/tags/' + tag.lower()

    response = get(url, timeout=5)

    if len(response.history) > 1:
        return "{} is not a valid tag.".format(tag.replace('-', ' '))
    else:
        return "Search results: {}".format(response.url)


@command('more')
def more_command(bot, context, message, args):
    """ Return more results for the most recent anime-planet.com search. """
    try:
        return "More results: {}".format(next(results_cache))
    except StopIteration:
        return "There are no more results."


def search_ap(search_term, type, append=''):
    global results_cache
    results_cache = iter(())
    url = base_url + '/' + type + '/all'

    response = get(url, params={'name': search_term}, timeout=5)

    if len(response.history) > 1:
        result = response.url + append
    else:
        bs = BeautifulSoup(response.text)

        if bs.find('div', {'class': 'error'}, recursive=True):
            result = "No results found."
        else:
            if type == 'anime' or type == 'manga':
                results = bs('li', {'class': 'card'})
            elif type == 'users':
                results = bs('td', {'class': 'tableUserName'})
            elif type == 'characters':
                results = bs('td', {'class': 'tableCharInfo'})

            def parse_card(card):
                return base_url + card.find('a')['href'] + append

            results_cache = map(parse_card, results)
            result = next(results_cache)

    return result
