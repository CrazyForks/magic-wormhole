from twisted.internet import defer, reactor
from twisted.trial import unittest

from pytest_twisted import ensureDeferred

from .. import xfer_util


APPID = u"appid"


@ensureDeferred
async def test_xfer(reactor, mailbox):
    code = u"1-code"
    data = u"data"
    d1 = xfer_util.send(reactor, APPID, mailbox.url, data, code)
    d2 = xfer_util.receive(reactor, APPID, mailbox.url, code)
    send_result = await d1
    receive_result = await d2
    assert send_result == None
    assert receive_result == data


@ensureDeferred
async def test_on_code(reactor, mailbox):
    code = u"1-code"
    data = u"data"
    send_code = []
    receive_code = []
    d1 = xfer_util.send(
        reactor,
        APPID,
        mailbox.url,
        data,
        code,
        on_code=send_code.append)
    d2 = xfer_util.receive(
        reactor, APPID, mailbox.url, code, on_code=receive_code.append)
    send_result = await d1
    receive_result = await d2
    assert send_code == [code]
    assert receive_code == [code]
    assert send_result == None
    assert receive_result == data


@ensureDeferred
async def test_make_code(reactor, mailbox):
    data = u"data"
    got_code = defer.Deferred()
    d1 = xfer_util.send(
        reactor,
        APPID,
        mailbox.url,
        data,
        code=None,
        on_code=got_code.callback)
    code = await got_code
    d2 = xfer_util.receive(reactor, APPID, mailbox.url, code)
    send_result = await d1
    receive_result = await d2
    assert send_result == None
    assert receive_result == data
