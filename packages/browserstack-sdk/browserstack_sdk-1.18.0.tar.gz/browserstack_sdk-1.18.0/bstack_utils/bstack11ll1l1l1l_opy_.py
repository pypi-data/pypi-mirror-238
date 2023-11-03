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
class bstack11ll1l1lll_opy_:
    def __init__(self, handler):
        self._11ll1ll1l1_opy_ = None
        self.handler = handler
        self._11ll1ll111_opy_ = self.bstack11ll1ll11l_opy_()
        self.patch()
    def patch(self):
        self._11ll1ll1l1_opy_ = self._11ll1ll111_opy_.execute
        self._11ll1ll111_opy_.execute = self.bstack11ll1l1ll1_opy_()
    def bstack11ll1l1ll1_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            response = self._11ll1ll1l1_opy_(this, driver_command, *args, **kwargs)
            self.handler(driver_command, response)
            return response
        return execute
    def reset(self):
        self._11ll1ll111_opy_.execute = self._11ll1ll1l1_opy_
    @staticmethod
    def bstack11ll1ll11l_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver