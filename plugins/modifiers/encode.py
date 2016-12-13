from motobot import command, Notice, split_response
from codecs import encode
from base64 import b64encode, b64decode
from hashlib import new, algorithms_available


encoding = 'UTF-8'


@command('rot13')
def rot13_command(bot, context, message, args):
    return encode(' '.join(args[1:]), 'rot13')


@command('rot47')
def rot47_command(bot, context, message, args):
    def rot47_imp(s):
        for c in s:
            x = ord(c)
            if x >= 33 and x <= 126:
                yield chr(33 + ((x + 14) % 94))
            else:
                yield c
    return ''.join(rot47_imp(' '.join(args[1:])))


@command('base64')
def base64_command(bot, context, message, args):
    return b64encode(bytes(' '.join(args[1:]), encoding)).decode(encoding)


@command('base64decode')
def base64_decode_command(bot, context, message, args):
    return b64decode(bytes(' '.join(args[1:]), encoding)).decode(encoding)


@command('hash')
def hash_command(bot, context, message, args):
    """ Hash a message.

    Usage: hash <algorithm> [message];
    Pass 'list' or 'show' for a list of algorithms.
    """
    try:
        if args[1] in ('list', 'show'):
            response = split_response(algorithms_available,
                                      "I support the following hashing algorithms: {}.")
        else:
            hash = new(args[1], bytes(' '.join(args[2:]), encoding))
            response = hash.hexdigest()
    except ValueError:
        response = "Error: Unsupported hashing algorithm.", Notice(context.nick)
    except IndexError:
        response = "Error: Please provide a hashing algorithm to use.", Notice(context.nick)
    return response
