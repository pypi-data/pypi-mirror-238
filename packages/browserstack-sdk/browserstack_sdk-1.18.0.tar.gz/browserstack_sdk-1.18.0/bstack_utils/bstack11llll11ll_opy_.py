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
import json
import os
import threading
from bstack_utils.helper import bstack1l1ll1111l_opy_, bstack1llll1ll1l_opy_, bstack1lll1111_opy_, bstack1lll1l11l1_opy_, \
    bstack1l1l11l11l_opy_
def bstack1l11l11l_opy_(bstack11ll1l111l_opy_):
    for driver in bstack11ll1l111l_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1l11ll1l1_opy_(type, name, status, reason, bstack1llll11ll_opy_, bstack1ll111l1l_opy_):
    bstack1ll111ll1_opy_ = {
        bstack1ll111l_opy_ (u"ࠪࡥࡨࡺࡩࡰࡰࠪᇺ"): type,
        bstack1ll111l_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧᇻ"): {}
    }
    if type == bstack1ll111l_opy_ (u"ࠬࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠧᇼ"):
        bstack1ll111ll1_opy_[bstack1ll111l_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩᇽ")][bstack1ll111l_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ᇾ")] = bstack1llll11ll_opy_
        bstack1ll111ll1_opy_[bstack1ll111l_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫᇿ")][bstack1ll111l_opy_ (u"ࠩࡧࡥࡹࡧࠧሀ")] = json.dumps(str(bstack1ll111l1l_opy_))
    if type == bstack1ll111l_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫሁ"):
        bstack1ll111ll1_opy_[bstack1ll111l_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧሂ")][bstack1ll111l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪሃ")] = name
    if type == bstack1ll111l_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩሄ"):
        bstack1ll111ll1_opy_[bstack1ll111l_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪህ")][bstack1ll111l_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨሆ")] = status
        if status == bstack1ll111l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩሇ") and str(reason) != bstack1ll111l_opy_ (u"ࠥࠦለ"):
            bstack1ll111ll1_opy_[bstack1ll111l_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧሉ")][bstack1ll111l_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬሊ")] = json.dumps(str(reason))
    bstack11l111l1l_opy_ = bstack1ll111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫላ").format(json.dumps(bstack1ll111ll1_opy_))
    return bstack11l111l1l_opy_
def bstack1lllll111_opy_(url, config, logger, bstack11l1llll1_opy_=False):
    hostname = bstack1llll1ll1l_opy_(url)
    is_private = bstack1lll1l11l1_opy_(hostname)
    try:
        if is_private or bstack11l1llll1_opy_:
            file_path = bstack1l1ll1111l_opy_(bstack1ll111l_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧሌ"), bstack1ll111l_opy_ (u"ࠨ࠰ࡥࡷࡹࡧࡣ࡬࠯ࡦࡳࡳ࡬ࡩࡨ࠰࡭ࡷࡴࡴࠧል"), logger)
            if os.environ.get(bstack1ll111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡇࡆࡒ࡟ࡏࡑࡗࡣࡘࡋࡔࡠࡇࡕࡖࡔࡘࠧሎ")) and eval(
                    os.environ.get(bstack1ll111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࡠࡐࡒࡘࡤ࡙ࡅࡕࡡࡈࡖࡗࡕࡒࠨሏ"))):
                return
            if (bstack1ll111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨሐ") in config and not config[bstack1ll111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩሑ")]):
                os.environ[bstack1ll111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࡣࡓࡕࡔࡠࡕࡈࡘࡤࡋࡒࡓࡑࡕࠫሒ")] = str(True)
                bstack11ll1l1111_opy_ = {bstack1ll111l_opy_ (u"ࠧࡩࡱࡶࡸࡳࡧ࡭ࡦࠩሓ"): hostname}
                bstack1l1l11l11l_opy_(bstack1ll111l_opy_ (u"ࠨ࠰ࡥࡷࡹࡧࡣ࡬࠯ࡦࡳࡳ࡬ࡩࡨ࠰࡭ࡷࡴࡴࠧሔ"), bstack1ll111l_opy_ (u"ࠩࡱࡹࡩ࡭ࡥࡠ࡮ࡲࡧࡦࡲࠧሕ"), bstack11ll1l1111_opy_, logger)
    except Exception as e:
        pass
def bstack11l1l1ll_opy_(caps, bstack11ll1l11l1_opy_):
    if bstack1ll111l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫሖ") in caps:
        caps[bstack1ll111l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬሗ")][bstack1ll111l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࠫመ")] = True
        if bstack11ll1l11l1_opy_:
            caps[bstack1ll111l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧሙ")][bstack1ll111l_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩሚ")] = bstack11ll1l11l1_opy_
    else:
        caps[bstack1ll111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡭ࡱࡦࡥࡱ࠭ማ")] = True
        if bstack11ll1l11l1_opy_:
            caps[bstack1ll111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪሜ")] = bstack11ll1l11l1_opy_
def bstack11lll1ll1l_opy_(bstack11ll11llll_opy_):
    bstack11ll1l1l11_opy_ = bstack1lll1111_opy_(threading.current_thread(), bstack1ll111l_opy_ (u"ࠪࡸࡪࡹࡴࡔࡶࡤࡸࡺࡹࠧም"), bstack1ll111l_opy_ (u"ࠫࠬሞ"))
    if bstack11ll1l1l11_opy_ == bstack1ll111l_opy_ (u"ࠬ࠭ሟ") or bstack11ll1l1l11_opy_ == bstack1ll111l_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧሠ"):
        threading.current_thread().bstack11ll1l11ll_opy_ = bstack11ll11llll_opy_
    else:
        if bstack11ll11llll_opy_ == bstack1ll111l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧሡ"):
            threading.current_thread().bstack11ll1l11ll_opy_ = bstack11ll11llll_opy_