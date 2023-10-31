# This file is placed in the Public Domain.
#
# pylint: disable=C0116,E0402


"introspection"


from obj.disk  import Storage
from obj.utils import spl


from .handler import Handler
from .thread  import launch


def __dir__():
    return (
            'scan',
           )


def scan(pkg, modnames="", initer=False) -> []:
    if not pkg:
        return []
    threads = []
    for modname in spl(modnames):
        module = getattr(pkg, modname, None)
        if not module:
            continue
        Handler.scan(module)
        Storage.scan(module)
        if initer:
            try:
                module.init
            except AttributeError:
                continue
            threads.append(launch(module.init, name=f"init {modname}"))
    return threads
