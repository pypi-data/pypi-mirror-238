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
import multiprocessing
import os
from browserstack_sdk.bstack1lll11ll1l_opy_ import *
from bstack_utils.helper import bstack1llllllll_opy_
from bstack_utils.messages import bstack1l1111l1_opy_
from bstack_utils.constants import bstack111l11l11_opy_
class bstack1111ll1l_opy_:
    def __init__(self, args, logger, bstack1ll111l1l1_opy_, bstack1ll111l111_opy_):
        self.args = args
        self.logger = logger
        self.bstack1ll111l1l1_opy_ = bstack1ll111l1l1_opy_
        self.bstack1ll111l111_opy_ = bstack1ll111l111_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack111l1l1ll_opy_ = []
        self.bstack1ll11l11l1_opy_ = None
        self.bstack1ll1l1lll1_opy_ = []
        self.bstack1ll111llll_opy_ = self.bstack1l1llll1_opy_()
        self.bstack1l1l111ll_opy_ = -1
    def bstack1ll1ll11_opy_(self, bstack1ll111lll1_opy_):
        self.parse_args()
        self.bstack1ll111l11l_opy_()
        self.bstack1ll11l1111_opy_(bstack1ll111lll1_opy_)
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    def bstack1ll111l1ll_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack1l1l111ll_opy_ = -1
        if bstack1ll111l_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬಧ") in self.bstack1ll111l1l1_opy_:
            self.bstack1l1l111ll_opy_ = self.bstack1ll111l1l1_opy_[bstack1ll111l_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭ನ")]
        try:
            bstack1ll11l11ll_opy_ = [bstack1ll111l_opy_ (u"ࠧ࠮࠯ࡧࡶ࡮ࡼࡥࡳࠩ಩"), bstack1ll111l_opy_ (u"ࠨ࠯࠰ࡴࡱࡻࡧࡪࡰࡶࠫಪ"), bstack1ll111l_opy_ (u"ࠩ࠰ࡴࠬಫ")]
            if self.bstack1l1l111ll_opy_ >= 0:
                bstack1ll11l11ll_opy_.extend([bstack1ll111l_opy_ (u"ࠪ࠱࠲ࡴࡵ࡮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫಬ"), bstack1ll111l_opy_ (u"ࠫ࠲ࡴࠧಭ")])
            for arg in bstack1ll11l11ll_opy_:
                self.bstack1ll111l1ll_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack1ll111l11l_opy_(self):
        bstack1ll11l11l1_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack1ll11l11l1_opy_ = bstack1ll11l11l1_opy_
        return bstack1ll11l11l1_opy_
    def bstack11111111l_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            import importlib
            bstack1ll111ll1l_opy_ = importlib.find_loader(bstack1ll111l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࡤࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠧಮ"))
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warn(e, bstack1l1111l1_opy_)
    def bstack1ll11l1111_opy_(self, bstack1ll111lll1_opy_):
        if bstack1ll111lll1_opy_:
            self.bstack1ll11l11l1_opy_.append(bstack1ll111l_opy_ (u"࠭࠭࠮ࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪಯ"))
            self.bstack1ll11l11l1_opy_.append(bstack1ll111l_opy_ (u"ࠧࡕࡴࡸࡩࠬರ"))
        self.bstack1ll11l11l1_opy_.append(bstack1ll111l_opy_ (u"ࠨ࠯ࡳࠫಱ"))
        self.bstack1ll11l11l1_opy_.append(bstack1ll111l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡱ࡮ࡸ࡫࡮ࡴࠧಲ"))
        self.bstack1ll11l11l1_opy_.append(bstack1ll111l_opy_ (u"ࠪ࠱࠲ࡪࡲࡪࡸࡨࡶࠬಳ"))
        self.bstack1ll11l11l1_opy_.append(bstack1ll111l_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫ಴"))
        if self.bstack1l1l111ll_opy_ > 1:
            self.bstack1ll11l11l1_opy_.append(bstack1ll111l_opy_ (u"ࠬ࠳࡮ࠨವ"))
            self.bstack1ll11l11l1_opy_.append(str(self.bstack1l1l111ll_opy_))
    def bstack1ll11l111l_opy_(self):
        bstack1ll1l1lll1_opy_ = []
        for spec in self.bstack111l1l1ll_opy_:
            bstack1l1llll11_opy_ = [spec]
            bstack1l1llll11_opy_ += self.bstack1ll11l11l1_opy_
            bstack1ll1l1lll1_opy_.append(bstack1l1llll11_opy_)
        self.bstack1ll1l1lll1_opy_ = bstack1ll1l1lll1_opy_
        return bstack1ll1l1lll1_opy_
    def bstack1l1llll1_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack1ll111llll_opy_ = True
            return True
        except Exception as e:
            self.bstack1ll111llll_opy_ = False
        return self.bstack1ll111llll_opy_
    def bstack111l111ll_opy_(self, bstack1ll111ll11_opy_, bstack1ll1ll11_opy_):
        bstack1ll1ll11_opy_[bstack1ll111l_opy_ (u"࠭ࡃࡐࡐࡉࡍࡌ࠭ಶ")] = self.bstack1ll111l1l1_opy_
        if bstack1ll111l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪಷ") in self.bstack1ll111l1l1_opy_:
            bstack11111l11_opy_ = []
            manager = multiprocessing.Manager()
            bstack111l1l11_opy_ = manager.list()
            for index, platform in enumerate(self.bstack1ll111l1l1_opy_[bstack1ll111l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫಸ")]):
                bstack11111l11_opy_.append(multiprocessing.Process(name=str(index),
                                                           target=bstack1ll111ll11_opy_,
                                                           args=(self.bstack1ll11l11l1_opy_, bstack1ll1ll11_opy_)))
            i = 0
            for t in bstack11111l11_opy_:
                os.environ[bstack1ll111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩಹ")] = str(i)
                i += 1
                t.start()
            for t in bstack11111l11_opy_:
                t.join()
            return bstack111l1l11_opy_