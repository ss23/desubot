from motobot import command, Action
from requests import get
from praw import Reddit
from random import shuffle


@command('fap', hidden=True)
@command('sendnude', hidden=True)
@command('sendnudes', hidden=True)
def sendnudes_command(bot, context, message, args):
    nick = ' '.join(args[1:])
    if not nick:
        nick = context.nick
    link = get_nude(bot.reddit_api_key, context.session)
    return "{}: {}".format(nick, link)


@command('blowload', hidden=True)
def blow_load_command(bot, context, message, args):
    context.session.set(None)
    target = ' '.join(args[1:])
    target = target if target else context.nick
    return "splooges all over {}!".format(target), Action


def get_nude(api_key, session):
    if not session.get([]):
        reddit = Reddit(client_id='UrExvPI1zjBAiQ',
                        client_secret=api_key,
                        user_agent='python:desubot URL: http://github.com/Motoko11/desubot:v2.0')
        subreddit = reddit.subreddit('gonewild')
        submissions = subreddit.top(limit=64)
        links = [submission.url for submission in submissions if not submission.stickied]
        shuffle(links)
        session.set(links)
    return session.get([]).pop(0)
