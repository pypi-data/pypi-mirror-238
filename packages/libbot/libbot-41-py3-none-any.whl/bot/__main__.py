# This file is placed in the Public Domain.
#
# pylint: disable=C0412,C0115,C0116,W0212,R0903,C0207,C0413,W0611
# pylint: disable=C0411,E0402,E0611,C2801,W0718


"runtime"


import getpass
import importlib
import os
import pwd
import readline
import shutil
import sys
import termios
import time
import threading
import traceback


sys.path.insert(0, os.getcwd())


from obj.spec import Object, Storage, fmt, keys, update, spl


from bot.spec import Broker, Censor, Cfg, Client, Errors, Event, CLI, Handler
from bot.spec import command, cprint, daemon, debug, parse, scan, forever
from bot.spec import launch, mods, name, privileges, shutdown


from bot import modules


Storage.wd = Cfg.wd


class Console(CLI):

    def dispatch(self, evt):
        parse(evt)
        command(evt)
        evt.wait()

    def poll(self) -> Event:
        return self.event(input("> "))

    def raw(self, txt):
        print(txt)


def scandir(path, init=False, wait=False):
    mns = []
    if not os.path.exists(path):
        return mns
    threads = []
    pname = path.split(os.sep)[-1]
    for fnm in os.listdir(path):
        if fnm.startswith("__"):
            continue
        if not fnm.endswith(".py"):
            continue
        fnn = fnm[:-3]
        fqn = f"{pname}.{fnn}"
        mod = importlib.import_module(fqn, pname)
        mns.append(fqn)
        Storage.scan(mod)
        Handler.scan(mod)
        if init and "init" in dir(mod):
            try:
                threads.append(launch(mod.init))
            except Exception as ex:
                Errors.add(ex)
    if wait:
        for thr in threads:
            thr.join()
    return mns


def wrap(func) -> None:
    old = None
    try:
        old = termios.tcgetattr(sys.stdin.fileno())
    except termios.error:
        pass
    try:
        func()
    except (EOFError, KeyboardInterrupt):
        print("")
        sys.stdout.flush()
    finally:
        if old:
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, old)
    shutdown()


def main():
    parse(Cfg, " ".join(sys.argv[1:]))
    update(Cfg, Cfg.sets)
    Cfg.mod = ",".join(modules.__dir__())
    if "v" in Cfg.opts:
        Censor.output = print
    if Cfg.wd:
        Storage.wd = Cfg.wd
    if Cfg.md:
        Cfg.mod += "," + ",".join(mods(Cfg.md))
    if "v" in Cfg.opts:
        dtime = time.ctime(time.time()).replace("  ", " ")
        cprint(f"{Cfg.name.upper()} started at {dtime} {Cfg.opts.upper()} {Cfg.mod.upper()}")
    if "n" in Cfg.opts:
        Cfg.commands = False
    if Cfg.md:
        scandir(Cfg.md, "x" not in Cfg.opts, "w" in Cfg.opts)
    if "d" in Cfg.opts:
        daemon(Cfg.pidfile)
    if "d" in Cfg.opts or "s" in Cfg.opts:
        privileges(Cfg.user)
        scan(modules, Cfg.mod, True)
        forever()
    elif "c" in Cfg.opts:
        thrs = scan(modules, Cfg.mod, True)
        if "w" in Cfg.opts:
            for thr in thrs:
                thr.join()
                cprint(f"ready {thr.name}")
        csl = Console()
        csl.start()
        csl.forever()
    else:
        scan(modules, Cfg.mod)
        cli = Console()
        evt = cli.event(Cfg.otxt)
        parse(evt)
        command(evt)


def wrapped():
    wrap(main)


if __name__ == "__main__":
    wrapped()
