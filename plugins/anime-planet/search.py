from motobot import command
from cfscrape import create_scraper
from bs4 import BeautifulSoup
from requests.exceptions import ReadTimeout
from time import time


base_url = 'http://www.anime-planet.com'
results_cache = iter(())
last_result = ('', 0)
search_format = "Search result: {}"
rec_format = "Recommendations: {}"
top_format = "Top Anime: {}"
scraper = None


def get(*args, **kwargs):
    global scraper
    if scraper is None:
        scraper = create_scraper()
    return scraper.get(*args, **kwargs)


@command('search')
def search_command(bot, context, message, args):
    """ Search for anything on anime-planet.com. """
    query = ' '.join(args[1:])
    if query:
        response = search_format.format(search_ap(query, 'all'))
    else:
        response = "Please supply a search term."
    return response


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
    query = query if query else context.nick
    response = search_format.format(search_ap(query, 'users'))
    return response


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
    global last_result
    results_cache = iter(())
    url = base_url + '/search.php'

    try:
        response = get(url, params={'search': search_term}, timeout=5)
        bs = BeautifulSoup(response.text, 'lxml')
        sections = bs.find_all('section', {'class': type} if type != 'all' else None)

        cards = sorted(
            (card for section in sections for card in section.find_all('li', {'class': 'card'})),
            key=lambda x: search_term.lower() != x.find('h4').text.lower())
        results_cache = (base_url + card.find('a')['href'] + append for card in cards)
        result = next(results_cache, None)
        result = result if result is not None else "No results found."
        if result == last_result[0] and time() - last_result[1] < 30:
            raise "Who the fuck cares, I'm not gonna catch this."
        else:
            last_result = (result, time())
    except ReadTimeout:
        result = "Search request timed out..."
    return result
