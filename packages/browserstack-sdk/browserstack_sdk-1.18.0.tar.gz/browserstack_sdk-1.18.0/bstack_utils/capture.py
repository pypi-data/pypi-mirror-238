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
import sys
class bstack1l1lll11ll_opy_:
    def __init__(self, handler):
        self._1l1lll1lll_opy_ = sys.stdout.write
        self._1l1lll1l11_opy_ = sys.stderr.write
        self.handler = handler
        self._started = False
    def start(self):
        if self._started:
            return
        self._started = True
        sys.stdout.write = self.bstack1l1lll1l1l_opy_
        sys.stdout.error = self.bstack1l1lll1ll1_opy_
    def bstack1l1lll1l1l_opy_(self, _str):
        self._1l1lll1lll_opy_(_str)
        if self.handler:
            self.handler({bstack1ll111l_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪത"): bstack1ll111l_opy_ (u"ࠬࡏࡎࡇࡑࠪഥ"), bstack1ll111l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧദ"): _str})
    def bstack1l1lll1ll1_opy_(self, _str):
        self._1l1lll1l11_opy_(_str)
        if self.handler:
            self.handler({bstack1ll111l_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ധ"): bstack1ll111l_opy_ (u"ࠨࡇࡕࡖࡔࡘࠧന"), bstack1ll111l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪഩ"): _str})
    def reset(self):
        if not self._started:
            return
        self._started = False
        sys.stdout.write = self._1l1lll1lll_opy_
        sys.stderr.write = self._1l1lll1l11_opy_