from motobot import match, command
from requests import get


def format_duration(duration):
    x = i = h = m = s = 0

    for c in duration:
        if c.isdigit():
            x = x * 10 + int(c)
            i += 1
        elif c == 'H':
            h = x
            i = x = 0
        elif c == 'M':
            m = x
            i = x = 0
        elif c == 'S':
            s = x
            i = x = 0

    time = '' if h == 0 else '{}:'.format(h)
    return time + "{:02d}:{:02d}".format(m, s)


@match(r'((youtube\.com\/watch\?\S*v=)|(youtu\.be/))([a-zA-Z0-9-_]+)')
def youtube_match(bot, context, message, match):
    video_link = match.group(4)
    title, duration = get_video_details(video_link, bot.youtube_api_key)
    return "{}'s video: {} - {}".format(context.nick, title, duration)


def get_video_details(video_id, api_key):
    params = {
        'id': video_id,
        'part': 'contentDetails,snippet',
        'key': api_key
    }
    response = get('https://www.googleapis.com/youtube/v3/videos', params=params, timeout=5)
    if response.status_code == 400:
        return "{}: invalid id".format(context.nick)
    video = response.json()['items'][0]
    title = video['snippet']['title']
    duration = format_duration(video['contentDetails']['duration'])
    return title, duration


@command('yt')
@command('youtube')
def youtube_command(bot, context, message, args):
    search = ' '.join(args[1:])
    params = {
        'part': 'id',
        'type': 'video',
        'key': bot.youtube_api_key,
        'q': search
    }
    data = get('https://www.googleapis.com/youtube/v3/search', params=params, timeout=5).json()
    try:
        video_id = data['items'][0]['id']['videoId']
        title, duration = get_video_details(video_id, bot.youtube_api_key)
        video_link = 'http://www.youtube.com/watch?v={}'.format(video_id)
        return "{} - {} - {}".format(title, duration, video_link)
    except IndexError:
        return "No results found."
