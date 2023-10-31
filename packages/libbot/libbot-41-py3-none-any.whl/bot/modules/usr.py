# This file is placed in the Public Domain.
#
# pylint: disable=C0115,C0116,W0612


"users"


import time


from obj.spec import  find, fntime, laps, sync
from bot.spec import User


def dlt(event):
    if not event.args:
        event.reply('dlt <username>')
        return
    selector = {'user': event.args[0]}
    nrs = 0
    for fnm, obj in find('user', selector):
        nrs += 1
        obj.__deleted__ = True
        sync(obj)
        event.reply('ok')
        break
    if not nrs:
        event.reply( "no users")


def met(event):
    if not event.args:
        nmr = 0
        for fnm, obj in find('user'):
            lap = laps(time.time() - fntime(fnm))
            event.reply(f'{nmr} {obj.user} {obj.perms} {lap}s')
            nmr += 1
        if not nmr:
            event.reply('no user')
        return
    user = User()
    user.user = event.rest
    user.perms = ['USER']
    sync(user)
    event.reply('ok')
