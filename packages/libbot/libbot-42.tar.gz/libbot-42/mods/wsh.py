# This file is placed in the Public Domain.
#
# pylint: disable=C0115,C0116


"wish list"


import time


from bot.spec import Object, find, fntime, laps, sync


class Wish(Object):

    def __init__(self):
        Object.__init__(self)
        self.txt = ''

    def gettxt(self):
        return self.txt

    def settxt(self, txt):
        self.txt = txt


def ful(event):
    if not event.args:
        return
    selector = {'txt': event.args[0]}
    for fnm, obj in find('wish', selector):
        obj.__deleted__ = True
        sync(obj)
        event.reply('done')


def wsh(event):
    if not event.rest:
        nmr = 0
        for fnm, obj in find('wish'):
            lap = laps(time.time()-fntime(obj.__oid__))
            event.reply(f'{nmr} {obj.txt} {lap}')
            nmr += 1
        if not nmr:
            event.reply("no wishes")
        return
    obj = Wish()
    obj.txt = event.rest
    sync(obj)
    event.reply('ok')
