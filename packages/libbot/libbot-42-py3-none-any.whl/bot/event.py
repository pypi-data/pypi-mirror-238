# This file is placed in the Public Domain.
#
# pylint: disable=C0115,C0116,E0402,R0902


"messages"


import threading


from .broker import Broker
from .object import Default


def __dir__():
    return (
            'Event',
           )


class Event(Default):

    __slots__ = ('_ready', "_thr")

    def __init__(self):
        Default.__init__(self)
        self._ready  = threading.Event()
        self._thr    = None
        self.channel = ""
        self.orig    = ""
        self.result  = []
        self.txt     = ""
        self.type    = "command"

    def ready(self) -> None:
        self._ready.set()

    def reply(self, txt) -> None:
        self.result.append(txt)

    def show(self) -> None:
        for txt in self.result:
            Broker.say(self.orig, self.channel, txt)

    def wait(self) -> None:
        self._ready.wait()
        if self._thr:
            self._thr.join()
