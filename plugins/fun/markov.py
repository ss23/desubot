from motobot import command, sink, Notice
from random import randint
from collections import Counter, defaultdict
from itertools import islice


class Markov:
    def __init__(self):
        self.words = defaultdict(Counter)
        self.word_count = Counter()

    def train(self, message):
        words = [word for word in message.split(' ') if word != '']

        if words:
            self.word_count[words[0]] += 1
            for word, next in zip(words, words[1:]):
                self.words[word][next] += 1
            self.words[words[-1]][None] += 1

    def generate(self, root=None):
        print("Root: ", root)
        def generate_imp():
            cur = self.choose_root(root)
            while cur is not None:
                yield cur
                cur = Markov.weighted_choice(self.words[cur])
        return ' '.join(generate_imp())

    def choose_root(self, root):
        if root is None:
            return Markov.weighted_choice(self.word_count)
        else:
            root = root.lower()
            words = Counter({word: self.word_count[word] for word in self.word_count if word.lower() == root})
            return Markov.weighted_choice(words)

    @staticmethod
    def weighted_choice(counter):
        size = sum(counter.values())
        print("Size: ", size)
        print("Counter: ", counter)
        i = randint(0, size-1)
        return next(islice(counter.elements(), i, None))


@command('update', hidden=True)
def update(bot, context, message, args):
    pass


@sink()
def mk_sink(bot, context, message):
    if not message.startswith(bot.command_prefix):
        markov = context.session.get(Markov())
        markov.train(message)
        context.session.set(markov)


@command('mk', hidden=True)
def mk_command(bot, context, message, args):
    markov = context.session.get(Markov())
    try:
        root = args[1:][-1]
    except IndexError:
        root = None
    response = markov.generate(root)
    return response


@command('mkcount', hidden=True)
def mkcount_command(bot, context, message, args):
    markov = context.session.get(Markov())
    word_count = set()

    for word, words in markov.words.items():
        word_count.add(word)
        for word in words:
            word_count.add(word)

    return "I know {} words!".format(len(word_count))
