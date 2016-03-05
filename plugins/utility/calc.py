from motobot import command
from requests import get
from untangle import parse


@command('calc')
def calc_command(bot, context, message, args):
    query = ' '.join(args[1:])
    result = get_result(query, bot.wolfram_api_key)
    return result


def get_result(query, api_key):
    try:
        url = 'http://api.wolframalpha.com/v2/query'
        params = {
            'appid': api_key,
            'includepodid': 'Result',
            'input': query
        }
        response = parse(get(url, params=params).text)
        result = response.queryresult.pod.subpod.plaintext.cdata
        result = "Calculation Result: {}".format(result)
    except IndexError:
        result = "Error calculating result."
    return result
