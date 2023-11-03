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
conf = {
    bstack1ll111l_opy_ (u"ࠪࡥࡵࡶ࡟ࡢࡷࡷࡳࡲࡧࡴࡦࠩപ"): False,
    bstack1ll111l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠬഫ"): True,
}
class Config(object):
    instance = None
    def __init__(self):
        self._1l1lll111l_opy_ = conf
    @classmethod
    def get_instance(cls):
        if cls.instance:
            return cls.instance
        return Config()
    def get_property(self, property_name):
        return self._1l1lll111l_opy_.get(property_name, None)
    def bstack1ll11ll1ll_opy_(self, property_name, bstack1l1lll11l1_opy_):
        self._1l1lll111l_opy_[property_name] = bstack1l1lll11l1_opy_