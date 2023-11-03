# This file is placed in the Public Domain.
#
# pylint: disable=C0115,C0116,C0209,W0212


"mailbox"


import mailbox
import os
import time


from bot.spec import Object, find, fmt, fntime, laps, sync, update


bdmonths = [
            'Bo',
            'Jan',
            'Feb',
            'Mar',
            'Apr',
            'May',
            'Jun',
            'Jul',
            'Aug',
            'Sep',
            'Oct',
            'Nov',
            'Dec'
           ]


monthint = {
            'Jan': 1,
            'Feb': 2,
            'Mar': 3,
            'Apr': 4,
            'May': 5,
            'Jun': 6,
            'Jul': 7,
            'Aug': 8,
            'Sep': 9,
            'Oct': 10,
            'Nov': 11,
            'Dec': 12
           }


class Email(Object):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text = ""

    def len(self):
        return len(self.__dict__)

    def size(self):
        return len(self.__dict__)


def to_date(date):
    date = date.replace("_", ":")
    res = date.split()
    ddd = ""
    try:
        if "+" in res[3]:
            raise ValueError
        if "-" in res[3]:
            raise ValueError
        int(res[3])
        ddd = "{:4}-{:#02}-{:#02} {:6}".format(res[3], monthint[res[2]], int(res[1]), res[4])
    except (IndexError, KeyError, ValueError) as ex:
        try:
            if "+" in res[4]:
                raise ValueError from ex
            if "-" in res[4]:
                raise ValueError from ex
            int(res[4])
            ddd = "{:4}-{:#02}-{:02} {:6}".format(res[4], monthint[res[1]], int(res[2]), res[3])
        except (IndexError, KeyError, ValueError):
            try:
                ddd = "{:4}-{:#02}-{:02} {:6}".format(res[2], monthint[res[1]], int(res[0]), res[3])
            except (IndexError, KeyError):
                try:
                    ddd = "{:4}-{:#02}-{:02}".format(res[2], monthint[res[1]], int(res[0]))
                except (IndexError, KeyError):
                    try:
                        ddd = "{:4}-{:#02}".format(res[2], monthint[res[1]])
                    except (IndexError, KeyError):
                        try:
                            ddd = "{:4}".format(res[2])
                        except (IndexError, KeyError):
                            ddd = ""
    return ddd


def cor(event):
    if not event.args:
        event.reply("cor <email>")
        return
    nrs = -1
    for fnm, email in find("email", {"From": event.args[0]}):
        nrs += 1
        txt = ""
        if len(event.args) > 1:
            txt = ",".join(event.args[1:])
        else:
            txt = "From,Subject"
        lsp = laps(time.time() - fntime(email.__oid__))
        txt = fmt(email)
        event.reply(f"{nrs} {txt} {lsp}")


def eml(event):
    if not event.args:
        event.reply("eml <txtinemail>")
        return
    nrs = -1
    for fnm, email in find("email"):
        if event.rest in email.text:
            nrs += 1
            txt = fmt(email, "From,Subject")
            lsp = laps(time.time() - fntime(email.__oid__))
            event.reply(f"{nrs} {txt} {lsp}")


def mbx(event):
    if not event.args:
        return
    path = os.path.expanduser(event.args[0])
    event.reply("reading from {path}")
    nrs = 0
    if os.path.isdir(path):
        thing = mailbox.Maildir(path, create=False)
    elif os.path.isfile(path):
        thing = mailbox.mbox(path, create=False)
    else:
        return
    try:
        thing.lock()
    except FileNotFoundError:
        pass
    for mail in thing:
        email = Email()
        update(email, mail._headers)
        email.text = ""
        for payload in mail.walk():
            if payload.get_content_type() == 'text/plain':
                email.text += payload.get_payload()
        email.text = email.text.replace("\\n", "\n")
        sync(email)
        nrs += 1
    if nrs:
        event.reply(f"ok {nrs}")
