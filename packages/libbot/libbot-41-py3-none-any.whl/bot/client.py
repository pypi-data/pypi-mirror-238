# This file is placed in the Public Domain.
#
# pylint: disable=C0115,C0116,W0718,E0402,W0613


"clients"


from .broker  import Broker
from .error   import Errors, cprint
from .handler import Handler


def __dir__():
    return (
            'Client',
            'CLI'
           )


class Client(Handler):

    def __init__(self):
        Handler.__init__(self)
        self.register("command", command)
        Broker.add(self)

    def announce(self, txt) -> None:
        self.raw(txt)

    def dosay(self, channel, txt) -> None:
        self.raw(txt)

    def raw(self, txt) -> None:
        pass


class CLI(Client):

    def announce(self, txt):
        pass

    def raw(self, txt):
        cprint(txt)


def command(evt) -> None:
    func = getattr(Handler.cmds, evt.cmd, None)
    if not func:
        evt.ready()
        return
    try:
        func(evt)
        evt.show()
    except Exception as ex:
        Errors.add(ex)
    evt.ready()
