# coding: UTF-8
import sys
bstack11111l_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack11l11l1_opy_ = 7
def bstack1ll111l_opy_ (bstack1111_opy_):
    global bstack1lllllll_opy_
    bstack1llllll_opy_ = ord (bstack1111_opy_ [-1])
    bstack111l11_opy_ = bstack1111_opy_ [:-1]
    bstack11lll_opy_ = bstack1llllll_opy_ % len (bstack111l11_opy_)
    bstack1l111l_opy_ = bstack111l11_opy_ [:bstack11lll_opy_] + bstack111l11_opy_ [bstack11lll_opy_:]
    if bstack11111l_opy_:
        bstack1l1llll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack11_opy_ + bstack1llllll_opy_) % bstack11l11l1_opy_) for bstack11_opy_, char in enumerate (bstack1l111l_opy_)])
    else:
        bstack1l1llll_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack11_opy_ + bstack1llllll_opy_) % bstack11l11l1_opy_) for bstack11_opy_, char in enumerate (bstack1l111l_opy_)])
    return eval (bstack1l1llll_opy_)
import threading
bstack11lll111l1_opy_ = 1000
bstack11lll11l1l_opy_ = 5
bstack11ll1lll11_opy_ = 30
bstack11lll11l11_opy_ = 2
class bstack11ll1lll1l_opy_:
    def __init__(self, handler, bstack11lll11111_opy_=bstack11lll111l1_opy_, bstack11ll1lllll_opy_=bstack11lll11l1l_opy_):
        self.queue = []
        self.handler = handler
        self.bstack11lll11111_opy_ = bstack11lll11111_opy_
        self.bstack11ll1lllll_opy_ = bstack11ll1lllll_opy_
        self.lock = threading.Lock()
        self.timer = None
    def start(self):
        if not self.timer:
            self.bstack11lll11ll1_opy_()
    def bstack11lll11ll1_opy_(self):
        self.timer = threading.Timer(self.bstack11ll1lllll_opy_, self.bstack11ll1ll1ll_opy_)
        self.timer.start()
    def bstack11lll111ll_opy_(self):
        self.timer.cancel()
    def bstack11lll1111l_opy_(self):
        self.bstack11lll111ll_opy_()
        self.bstack11lll11ll1_opy_()
    def add(self, event):
        with self.lock:
            self.queue.append(event)
            if len(self.queue) >= self.bstack11lll11111_opy_:
                t = threading.Thread(target=self.bstack11ll1ll1ll_opy_)
                t.start()
                self.bstack11lll1111l_opy_()
    def bstack11ll1ll1ll_opy_(self):
        if len(self.queue) <= 0:
            return
        data = self.queue[:self.bstack11lll11111_opy_]
        del self.queue[:self.bstack11lll11111_opy_]
        self.handler(data)
    def shutdown(self):
        self.bstack11lll111ll_opy_()
        while len(self.queue) > 0:
            self.bstack11ll1ll1ll_opy_()