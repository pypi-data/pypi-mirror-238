# This file is placed in the Public Domain.
#
# pylint: disable=E0402,C0115,R0902,R0903,W0201,C0103


"configuration"


import getpass
import os
import time


from obj.spec import Default


def __dir__():
    return (
            'Config',
            'Cfg'
           )


class Config(Default):

    pass


Cfg = Config()
Cfg.commands  = True
Cfg.debug     = False
Cfg.md        = ""
Cfg.name      = __file__.split(os.sep)[-2].lower()
Cfg.wd        = os.path.expanduser(f"~/.{Cfg.name}")
Cfg.pidfile   = os.path.join(Cfg.wd, f"{Cfg.name}.pid")
Cfg.starttime = time.time()
Cfg.user      = getpass.getuser()
