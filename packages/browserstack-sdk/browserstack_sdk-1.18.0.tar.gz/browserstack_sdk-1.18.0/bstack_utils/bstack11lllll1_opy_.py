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
import datetime
import json
import logging
import os
import threading
from bstack_utils.helper import bstack1ll11111ll_opy_, bstack1llll1ll1_opy_, get_host_info, bstack1ll1111l11_opy_, bstack1ll11111l1_opy_, bstack1l1l1lllll_opy_, \
    bstack1l1l1l1ll1_opy_, bstack1l1ll11lll_opy_, bstack1l1l11l11_opy_, bstack1l1ll11l11_opy_, bstack1l1ll11l1l_opy_, bstack1l1l1l1l1l_opy_
from bstack_utils.bstack11ll1llll1_opy_ import bstack11ll1lll1l_opy_
from bstack_utils.bstack11ll111111_opy_ import bstack11ll111l11_opy_
bstack11l1ll111l_opy_ = [
    bstack1ll111l_opy_ (u"࠭ࡌࡰࡩࡆࡶࡪࡧࡴࡦࡦࠪቘ"), bstack1ll111l_opy_ (u"ࠧࡄࡄࡗࡗࡪࡹࡳࡪࡱࡱࡇࡷ࡫ࡡࡵࡧࡧࠫ቙"), bstack1ll111l_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪቚ"), bstack1ll111l_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖ࡯࡮ࡶࡰࡦࡦࠪቛ"),
    bstack1ll111l_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬቜ"), bstack1ll111l_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬቝ"), bstack1ll111l_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭቞")
]
bstack11l1l1ll1l_opy_ = bstack1ll111l_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡤࡱ࡯ࡰࡪࡩࡴࡰࡴ࠰ࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠭቟")
logger = logging.getLogger(__name__)
class bstack11llllll1_opy_:
    bstack11ll1llll1_opy_ = None
    bs_config = None
    @classmethod
    @bstack1l1l1l1l1l_opy_(class_method=True)
    def launch(cls, bs_config, bstack11l1l1l1l1_opy_):
        cls.bs_config = bs_config
        if not cls.bstack11l1l1lll1_opy_():
            return
        cls.bstack11l1l11l11_opy_()
        bstack1l1llll1ll_opy_ = bstack1ll1111l11_opy_(bs_config)
        bstack1l1lllll1l_opy_ = bstack1ll11111l1_opy_(bs_config)
        data = {
            bstack1ll111l_opy_ (u"ࠧࡧࡱࡵࡱࡦࡺࠧበ"): bstack1ll111l_opy_ (u"ࠨ࡬ࡶࡳࡳ࠭ቡ"),
            bstack1ll111l_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡢࡲࡦࡳࡥࠨቢ"): bs_config.get(bstack1ll111l_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨባ"), bstack1ll111l_opy_ (u"ࠫࠬቤ")),
            bstack1ll111l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪብ"): bs_config.get(bstack1ll111l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩቦ"), os.path.basename(os.path.abspath(os.getcwd()))),
            bstack1ll111l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪቧ"): bs_config.get(bstack1ll111l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪቨ")),
            bstack1ll111l_opy_ (u"ࠩࡧࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧቩ"): bs_config.get(bstack1ll111l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡆࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭ቪ"), bstack1ll111l_opy_ (u"ࠫࠬቫ")),
            bstack1ll111l_opy_ (u"ࠬࡹࡴࡢࡴࡷࡣࡹ࡯࡭ࡦࠩቬ"): datetime.datetime.now().isoformat(),
            bstack1ll111l_opy_ (u"࠭ࡴࡢࡩࡶࠫቭ"): bstack1l1l1lllll_opy_(bs_config),
            bstack1ll111l_opy_ (u"ࠧࡩࡱࡶࡸࡤ࡯࡮ࡧࡱࠪቮ"): get_host_info(),
            bstack1ll111l_opy_ (u"ࠨࡥ࡬ࡣ࡮ࡴࡦࡰࠩቯ"): bstack1llll1ll1_opy_(),
            bstack1ll111l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡴࡸࡲࡤ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩተ"): os.environ.get(bstack1ll111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅ࡙ࡎࡒࡄࡠࡔࡘࡒࡤࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠩቱ")),
            bstack1ll111l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࡣࡹ࡫ࡳࡵࡵࡢࡶࡪࡸࡵ࡯ࠩቲ"): os.environ.get(bstack1ll111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡗࡋࡒࡖࡐࠪታ"), False),
            bstack1ll111l_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴ࡟ࡤࡱࡱࡸࡷࡵ࡬ࠨቴ"): bstack1ll11111ll_opy_(),
            bstack1ll111l_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨት"): {
                bstack1ll111l_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡒࡦࡳࡥࠨቶ"): bstack11l1l1l1l1_opy_.get(bstack1ll111l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࠪቷ"), bstack1ll111l_opy_ (u"ࠪࡔࡾࡺࡥࡴࡶࠪቸ")),
                bstack1ll111l_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࡖࡦࡴࡶ࡭ࡴࡴࠧቹ"): bstack11l1l1l1l1_opy_.get(bstack1ll111l_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩቺ")),
                bstack1ll111l_opy_ (u"࠭ࡳࡥ࡭࡙ࡩࡷࡹࡩࡰࡰࠪቻ"): bstack11l1l1l1l1_opy_.get(bstack1ll111l_opy_ (u"ࠧࡴࡦ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬቼ"))
            }
        }
        config = {
            bstack1ll111l_opy_ (u"ࠨࡣࡸࡸ࡭࠭ች"): (bstack1l1llll1ll_opy_, bstack1l1lllll1l_opy_),
            bstack1ll111l_opy_ (u"ࠩ࡫ࡩࡦࡪࡥࡳࡵࠪቾ"): cls.default_headers()
        }
        response = bstack1l1l11l11_opy_(bstack1ll111l_opy_ (u"ࠪࡔࡔ࡙ࡔࠨቿ"), cls.request_url(bstack1ll111l_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡧࡻࡩ࡭ࡦࡶࠫኀ")), data, config)
        if response.status_code != 200:
            os.environ[bstack1ll111l_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡅࡒࡑࡕࡒࡅࡕࡇࡇࠫኁ")] = bstack1ll111l_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬኂ")
            os.environ[bstack1ll111l_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡏ࡝ࡔࠨኃ")] = bstack1ll111l_opy_ (u"ࠨࡰࡸࡰࡱ࠭ኄ")
            os.environ[bstack1ll111l_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡎࡁࡔࡊࡈࡈࡤࡏࡄࠨኅ")] = bstack1ll111l_opy_ (u"ࠥࡲࡺࡲ࡬ࠣኆ")
            os.environ[bstack1ll111l_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡃࡏࡐࡔ࡝࡟ࡔࡅࡕࡉࡊࡔࡓࡉࡑࡗࡗࠬኇ")] = bstack1ll111l_opy_ (u"ࠧࡴࡵ࡭࡮ࠥኈ")
            bstack11l11lllll_opy_ = response.json()
            if bstack11l11lllll_opy_ and bstack11l11lllll_opy_[bstack1ll111l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ኉")]:
                error_message = bstack11l11lllll_opy_[bstack1ll111l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨኊ")]
                if bstack11l11lllll_opy_[bstack1ll111l_opy_ (u"ࠨࡧࡵࡶࡴࡸࡔࡺࡲࡨࠫኋ")] == bstack1ll111l_opy_ (u"ࠩࡈࡖࡗࡕࡒࡠࡋࡑ࡚ࡆࡒࡉࡅࡡࡆࡖࡊࡊࡅࡏࡖࡌࡅࡑ࡙ࠧኌ"):
                    logger.error(error_message)
                elif bstack11l11lllll_opy_[bstack1ll111l_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࡖࡼࡴࡪ࠭ኍ")] == bstack1ll111l_opy_ (u"ࠫࡊࡘࡒࡐࡔࡢࡅࡈࡉࡅࡔࡕࡢࡈࡊࡔࡉࡆࡆࠪ኎"):
                    logger.info(error_message)
                elif bstack11l11lllll_opy_[bstack1ll111l_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࡘࡾࡶࡥࠨ኏")] == bstack1ll111l_opy_ (u"࠭ࡅࡓࡔࡒࡖࡤ࡙ࡄࡌࡡࡇࡉࡕࡘࡅࡄࡃࡗࡉࡉ࠭ነ"):
                    logger.error(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack1ll111l_opy_ (u"ࠢࡅࡣࡷࡥࠥࡻࡰ࡭ࡱࡤࡨࠥࡺ࡯ࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡕࡧࡶࡸࠥࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡪࡵࡦࠢࡷࡳࠥࡹ࡯࡮ࡧࠣࡩࡷࡸ࡯ࡳࠤኑ"))
            return [None, None, None]
        logger.debug(bstack1ll111l_opy_ (u"ࠨࡖࡨࡷࡹࠦࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾࠦࡂࡶ࡫࡯ࡨࠥࡩࡲࡦࡣࡷ࡭ࡴࡴࠠࡔࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࠥࠬኒ"))
        os.environ[bstack1ll111l_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡉࡏࡎࡒࡏࡉ࡙ࡋࡄࠨና")] = bstack1ll111l_opy_ (u"ࠪࡸࡷࡻࡥࠨኔ")
        bstack11l11lllll_opy_ = response.json()
        if bstack11l11lllll_opy_.get(bstack1ll111l_opy_ (u"ࠫ࡯ࡽࡴࠨን")):
            os.environ[bstack1ll111l_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡍ࡛࡙࠭ኖ")] = bstack11l11lllll_opy_[bstack1ll111l_opy_ (u"࠭ࡪࡸࡶࠪኗ")]
            os.environ[bstack1ll111l_opy_ (u"ࠧࡄࡔࡈࡈࡊࡔࡔࡊࡃࡏࡗࡤࡌࡏࡓࡡࡆࡖࡆ࡙ࡈࡠࡔࡈࡔࡔࡘࡔࡊࡐࡊࠫኘ")] = json.dumps({
                bstack1ll111l_opy_ (u"ࠨࡷࡶࡩࡷࡴࡡ࡮ࡧࠪኙ"): bstack1l1llll1ll_opy_,
                bstack1ll111l_opy_ (u"ࠩࡳࡥࡸࡹࡷࡰࡴࡧࠫኚ"): bstack1l1lllll1l_opy_
            })
        if bstack11l11lllll_opy_.get(bstack1ll111l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬኛ")):
            os.environ[bstack1ll111l_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡄࡘࡍࡑࡊ࡟ࡉࡃࡖࡌࡊࡊ࡟ࡊࡆࠪኜ")] = bstack11l11lllll_opy_[bstack1ll111l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧኝ")]
        if bstack11l11lllll_opy_.get(bstack1ll111l_opy_ (u"࠭ࡡ࡭࡮ࡲࡻࡤࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪኞ")):
            os.environ[bstack1ll111l_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡆࡒࡌࡐ࡙ࡢࡗࡈࡘࡅࡆࡐࡖࡌࡔ࡚ࡓࠨኟ")] = str(bstack11l11lllll_opy_[bstack1ll111l_opy_ (u"ࠨࡣ࡯ࡰࡴࡽ࡟ࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࡷࠬአ")])
        return [bstack11l11lllll_opy_[bstack1ll111l_opy_ (u"ࠩ࡭ࡻࡹ࠭ኡ")], bstack11l11lllll_opy_[bstack1ll111l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬኢ")], bstack11l11lllll_opy_[bstack1ll111l_opy_ (u"ࠫࡦࡲ࡬ࡰࡹࡢࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡳࠨኣ")]]
    @classmethod
    @bstack1l1l1l1l1l_opy_(class_method=True)
    def stop(cls):
        if not cls.on():
            return
        if os.environ[bstack1ll111l_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡍ࡛࡙࠭ኤ")] == bstack1ll111l_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦእ") or os.environ[bstack1ll111l_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡌࡆ࡙ࡈࡆࡆࡢࡍࡉ࠭ኦ")] == bstack1ll111l_opy_ (u"ࠣࡰࡸࡰࡱࠨኧ"):
            print(bstack1ll111l_opy_ (u"ࠩࡈ࡜ࡈࡋࡐࡕࡋࡒࡒࠥࡏࡎࠡࡵࡷࡳࡵࡈࡵࡪ࡮ࡧ࡙ࡵࡹࡴࡳࡧࡤࡱࠥࡘࡅࡒࡗࡈࡗ࡙ࠦࡔࡐࠢࡗࡉࡘ࡚ࠠࡐࡄࡖࡉࡗ࡜ࡁࡃࡋࡏࡍ࡙࡟ࠠ࠻ࠢࡐ࡭ࡸࡹࡩ࡯ࡩࠣࡥࡺࡺࡨࡦࡰࡷ࡭ࡨࡧࡴࡪࡱࡱࠤࡹࡵ࡫ࡦࡰࠪከ"))
            return {
                bstack1ll111l_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪኩ"): bstack1ll111l_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪኪ"),
                bstack1ll111l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ካ"): bstack1ll111l_opy_ (u"࠭ࡔࡰ࡭ࡨࡲ࠴ࡨࡵࡪ࡮ࡧࡍࡉࠦࡩࡴࠢࡸࡲࡩ࡫ࡦࡪࡰࡨࡨ࠱ࠦࡢࡶ࡫࡯ࡨࠥࡩࡲࡦࡣࡷ࡭ࡴࡴࠠ࡮࡫ࡪ࡬ࡹࠦࡨࡢࡸࡨࠤ࡫ࡧࡩ࡭ࡧࡧࠫኬ")
            }
        else:
            cls.bstack11ll1llll1_opy_.shutdown()
            data = {
                bstack1ll111l_opy_ (u"ࠧࡴࡶࡲࡴࡤࡺࡩ࡮ࡧࠪክ"): datetime.datetime.now().isoformat()
            }
            config = {
                bstack1ll111l_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩኮ"): cls.default_headers()
            }
            bstack1l1l11ll11_opy_ = bstack1ll111l_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡥࡹ࡮ࡲࡤࡴ࠱ࡾࢁ࠴ࡹࡴࡰࡲࠪኯ").format(os.environ[bstack1ll111l_opy_ (u"ࠥࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡈࡂࡕࡋࡉࡉࡥࡉࡅࠤኰ")])
            bstack11l11ll1l1_opy_ = cls.request_url(bstack1l1l11ll11_opy_)
            response = bstack1l1l11l11_opy_(bstack1ll111l_opy_ (u"ࠫࡕ࡛ࡔࠨ኱"), bstack11l11ll1l1_opy_, data, config)
            if not response.ok:
                raise Exception(bstack1ll111l_opy_ (u"࡙ࠧࡴࡰࡲࠣࡶࡪࡷࡵࡦࡵࡷࠤࡳࡵࡴࠡࡱ࡮ࠦኲ"))
    @classmethod
    def bstack11l1l1llll_opy_(cls):
        if cls.bstack11ll1llll1_opy_ is None:
            return
        cls.bstack11ll1llll1_opy_.shutdown()
    @classmethod
    def bstack1llll111_opy_(cls):
        if cls.on():
            print(
                bstack1ll111l_opy_ (u"࠭ࡖࡪࡵ࡬ࡸࠥ࡮ࡴࡵࡲࡶ࠾࠴࠵࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡥࡹ࡮ࡲࡤࡴ࠱ࡾࢁࠥࡺ࡯ࠡࡸ࡬ࡩࡼࠦࡢࡶ࡫࡯ࡨࠥࡸࡥࡱࡱࡵࡸ࠱ࠦࡩ࡯ࡵ࡬࡫࡭ࡺࡳ࠭ࠢࡤࡲࡩࠦ࡭ࡢࡰࡼࠤࡲࡵࡲࡦࠢࡧࡩࡧࡻࡧࡨ࡫ࡱ࡫ࠥ࡯࡮ࡧࡱࡵࡱࡦࡺࡩࡰࡰࠣࡥࡱࡲࠠࡢࡶࠣࡳࡳ࡫ࠠࡱ࡮ࡤࡧࡪࠧ࡜࡯ࠩኳ").format(os.environ[bstack1ll111l_opy_ (u"ࠢࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡌࡆ࡙ࡈࡆࡆࡢࡍࡉࠨኴ")]))
    @classmethod
    def bstack11l1l11l11_opy_(cls):
        if cls.bstack11ll1llll1_opy_ is not None:
            return
        cls.bstack11ll1llll1_opy_ = bstack11ll1lll1l_opy_(cls.bstack11l1ll1ll1_opy_)
        cls.bstack11ll1llll1_opy_.start()
    @classmethod
    def bstack11l1l1l1ll_opy_(cls, bstack11l11lll11_opy_, bstack11l1l11111_opy_=bstack1ll111l_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡤࡤࡸࡨ࡮ࠧኵ")):
        if not cls.on():
            return
        bstack1ll11l1l_opy_ = bstack11l11lll11_opy_[bstack1ll111l_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭኶")]
        bstack11l11llll1_opy_ = {
            bstack1ll111l_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫ኷"): bstack1ll111l_opy_ (u"࡙ࠫ࡫ࡳࡵࡡࡖࡸࡦࡸࡴࡠࡗࡳࡰࡴࡧࡤࠨኸ"),
            bstack1ll111l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧኹ"): bstack1ll111l_opy_ (u"࠭ࡔࡦࡵࡷࡣࡊࡴࡤࡠࡗࡳࡰࡴࡧࡤࠨኺ"),
            bstack1ll111l_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔ࡭࡬ࡴࡵ࡫ࡤࠨኻ"): bstack1ll111l_opy_ (u"ࠨࡖࡨࡷࡹࡥࡓ࡬࡫ࡳࡴࡪࡪ࡟ࡖࡲ࡯ࡳࡦࡪࠧኼ"),
            bstack1ll111l_opy_ (u"ࠩࡏࡳ࡬ࡉࡲࡦࡣࡷࡩࡩ࠭ኽ"): bstack1ll111l_opy_ (u"ࠪࡐࡴ࡭࡟ࡖࡲ࡯ࡳࡦࡪࠧኾ"),
            bstack1ll111l_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬ኿"): bstack1ll111l_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡢࡗࡹࡧࡲࡵࡡࡘࡴࡱࡵࡡࡥࠩዀ"),
            bstack1ll111l_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ዁"): bstack1ll111l_opy_ (u"ࠧࡉࡱࡲ࡯ࡤࡋ࡮ࡥࡡࡘࡴࡱࡵࡡࡥࠩዂ"),
            bstack1ll111l_opy_ (u"ࠨࡅࡅࡘࡘ࡫ࡳࡴ࡫ࡲࡲࡈࡸࡥࡢࡶࡨࡨࠬዃ"): bstack1ll111l_opy_ (u"ࠩࡆࡆ࡙ࡥࡕࡱ࡮ࡲࡥࡩ࠭ዄ")
        }.get(bstack1ll11l1l_opy_)
        if bstack11l1l11111_opy_ == bstack1ll111l_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠳࠲ࡦࡦࡺࡣࡩࠩዅ"):
            cls.bstack11l1l11l11_opy_()
            cls.bstack11ll1llll1_opy_.add(bstack11l11lll11_opy_)
        elif bstack11l1l11111_opy_ == bstack1ll111l_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡴࠩ዆"):
            cls.bstack11l1ll1ll1_opy_([bstack11l11lll11_opy_], bstack11l1l11111_opy_)
    @classmethod
    @bstack1l1l1l1l1l_opy_(class_method=True)
    def bstack11l1ll1ll1_opy_(cls, bstack11l11lll11_opy_, bstack11l1l11111_opy_=bstack1ll111l_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡨࡡࡵࡥ࡫ࠫ዇")):
        config = {
            bstack1ll111l_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧወ"): cls.default_headers()
        }
        response = bstack1l1l11l11_opy_(bstack1ll111l_opy_ (u"ࠧࡑࡑࡖࡘࠬዉ"), cls.request_url(bstack11l1l11111_opy_), bstack11l11lll11_opy_, config)
        bstack1ll1111111_opy_ = response.json()
    @classmethod
    @bstack1l1l1l1l1l_opy_(class_method=True)
    def bstack11l1ll11ll_opy_(cls, bstack11l1ll1111_opy_):
        bstack11l1l11ll1_opy_ = []
        for log in bstack11l1ll1111_opy_:
            bstack11l11ll11l_opy_ = {
                bstack1ll111l_opy_ (u"ࠨ࡭࡬ࡲࡩ࠭ዊ"): bstack1ll111l_opy_ (u"ࠩࡗࡉࡘ࡚࡟ࡍࡑࡊࠫዋ"),
                bstack1ll111l_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩዌ"): log[bstack1ll111l_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪው")],
                bstack1ll111l_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨዎ"): log[bstack1ll111l_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩዏ")],
                bstack1ll111l_opy_ (u"ࠧࡩࡶࡷࡴࡤࡸࡥࡴࡲࡲࡲࡸ࡫ࠧዐ"): {},
                bstack1ll111l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩዑ"): log[bstack1ll111l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪዒ")],
            }
            if bstack1ll111l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪዓ") in log:
                bstack11l11ll11l_opy_[bstack1ll111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫዔ")] = log[bstack1ll111l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬዕ")]
            elif bstack1ll111l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ዖ") in log:
                bstack11l11ll11l_opy_[bstack1ll111l_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ዗")] = log[bstack1ll111l_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨዘ")]
            bstack11l1l11ll1_opy_.append(bstack11l11ll11l_opy_)
        cls.bstack11l1l1l1ll_opy_({
            bstack1ll111l_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭ዙ"): bstack1ll111l_opy_ (u"ࠪࡐࡴ࡭ࡃࡳࡧࡤࡸࡪࡪࠧዚ"),
            bstack1ll111l_opy_ (u"ࠫࡱࡵࡧࡴࠩዛ"): bstack11l1l11ll1_opy_
        })
    @classmethod
    @bstack1l1l1l1l1l_opy_(class_method=True)
    def bstack11l1ll11l1_opy_(cls, steps):
        bstack11l1l1ll11_opy_ = []
        for step in steps:
            bstack11l1l111ll_opy_ = {
                bstack1ll111l_opy_ (u"ࠬࡱࡩ࡯ࡦࠪዜ"): bstack1ll111l_opy_ (u"࠭ࡔࡆࡕࡗࡣࡘ࡚ࡅࡑࠩዝ"),
                bstack1ll111l_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ዞ"): step[bstack1ll111l_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧዟ")],
                bstack1ll111l_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬዠ"): step[bstack1ll111l_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ዡ")],
                bstack1ll111l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬዢ"): step[bstack1ll111l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ዣ")],
                bstack1ll111l_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࠨዤ"): step[bstack1ll111l_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࠩዥ")]
            }
            if bstack1ll111l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨዦ") in step:
                bstack11l1l111ll_opy_[bstack1ll111l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩዧ")] = step[bstack1ll111l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪየ")]
            elif bstack1ll111l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫዩ") in step:
                bstack11l1l111ll_opy_[bstack1ll111l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬዪ")] = step[bstack1ll111l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ያ")]
            bstack11l1l1ll11_opy_.append(bstack11l1l111ll_opy_)
        cls.bstack11l1l1l1ll_opy_({
            bstack1ll111l_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫዬ"): bstack1ll111l_opy_ (u"ࠨࡎࡲ࡫ࡈࡸࡥࡢࡶࡨࡨࠬይ"),
            bstack1ll111l_opy_ (u"ࠩ࡯ࡳ࡬ࡹࠧዮ"): bstack11l1l1ll11_opy_
        })
    @classmethod
    @bstack1l1l1l1l1l_opy_(class_method=True)
    def bstack11l1l1l11l_opy_(cls, screenshot):
        cls.bstack11l1l1l1ll_opy_({
            bstack1ll111l_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧዯ"): bstack1ll111l_opy_ (u"ࠫࡑࡵࡧࡄࡴࡨࡥࡹ࡫ࡤࠨደ"),
            bstack1ll111l_opy_ (u"ࠬࡲ࡯ࡨࡵࠪዱ"): [{
                bstack1ll111l_opy_ (u"࠭࡫ࡪࡰࡧࠫዲ"): bstack1ll111l_opy_ (u"ࠧࡕࡇࡖࡘࡤ࡙ࡃࡓࡇࡈࡒࡘࡎࡏࡕࠩዳ"),
                bstack1ll111l_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫዴ"): datetime.datetime.utcnow().isoformat() + bstack1ll111l_opy_ (u"ࠩ࡝ࠫድ"),
                bstack1ll111l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫዶ"): screenshot[bstack1ll111l_opy_ (u"ࠫ࡮ࡳࡡࡨࡧࠪዷ")],
                bstack1ll111l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬዸ"): screenshot[bstack1ll111l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ዹ")]
            }]
        }, bstack11l1l11111_opy_=bstack1ll111l_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࡷࠬዺ"))
    @classmethod
    @bstack1l1l1l1l1l_opy_(class_method=True)
    def bstack1l111ll1l_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack11l1l1l1ll_opy_({
            bstack1ll111l_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬዻ"): bstack1ll111l_opy_ (u"ࠩࡆࡆ࡙࡙ࡥࡴࡵ࡬ࡳࡳࡉࡲࡦࡣࡷࡩࡩ࠭ዼ"),
            bstack1ll111l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࠬዽ"): {
                bstack1ll111l_opy_ (u"ࠦࡺࡻࡩࡥࠤዾ"): cls.current_test_uuid(),
                bstack1ll111l_opy_ (u"ࠧ࡯࡮ࡵࡧࡪࡶࡦࡺࡩࡰࡰࡶࠦዿ"): cls.bstack11l11lll1l_opy_(driver)
            }
        })
    @classmethod
    def on(cls):
        if os.environ.get(bstack1ll111l_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡎ࡜࡚ࠧጀ"), None) is None or os.environ[bstack1ll111l_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡏ࡝ࡔࠨጁ")] == bstack1ll111l_opy_ (u"ࠣࡰࡸࡰࡱࠨጂ"):
            return False
        return True
    @classmethod
    def bstack11l1l1lll1_opy_(cls):
        return bstack1l1ll11l1l_opy_(cls.bs_config.get(bstack1ll111l_opy_ (u"ࠩࡷࡩࡸࡺࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭ጃ"), False))
    @staticmethod
    def request_url(url):
        return bstack1ll111l_opy_ (u"ࠪࡿࢂ࠵ࡻࡾࠩጄ").format(bstack11l1l1ll1l_opy_, url)
    @staticmethod
    def default_headers():
        headers = {
            bstack1ll111l_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪጅ"): bstack1ll111l_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨጆ"),
            bstack1ll111l_opy_ (u"࠭ࡘ࠮ࡄࡖࡘࡆࡉࡋ࠮ࡖࡈࡗ࡙ࡕࡐࡔࠩጇ"): bstack1ll111l_opy_ (u"ࠧࡵࡴࡸࡩࠬገ")
        }
        if os.environ.get(bstack1ll111l_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡐࡗࡕࠩጉ"), None):
            headers[bstack1ll111l_opy_ (u"ࠩࡄࡹࡹ࡮࡯ࡳ࡫ࡽࡥࡹ࡯࡯࡯ࠩጊ")] = bstack1ll111l_opy_ (u"ࠪࡆࡪࡧࡲࡦࡴࠣࡿࢂ࠭ጋ").format(os.environ[bstack1ll111l_opy_ (u"ࠦࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡌ࡚ࡘࠧጌ")])
        return headers
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack1ll111l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩግ"), None)
    @staticmethod
    def bstack11l11lll1l_opy_(driver):
        return {
            bstack1l1ll11lll_opy_(): bstack1l1l1l1ll1_opy_(driver)
        }
    @staticmethod
    def bstack11l1l111l1_opy_(exception_info, report):
        return [{bstack1ll111l_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩጎ"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack1l1ll11111_opy_(typename):
        if bstack1ll111l_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࠥጏ") in typename:
            return bstack1ll111l_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࡉࡷࡸ࡯ࡳࠤጐ")
        return bstack1ll111l_opy_ (u"ࠤࡘࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࡊࡸࡲࡰࡴࠥ጑")
    @staticmethod
    def bstack11l1l1111l_opy_(func):
        def wrap(*args, **kwargs):
            if bstack11llllll1_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack11l1l11lll_opy_(test, hook_name=None):
        bstack11l11ll1ll_opy_ = test.parent
        if hook_name in [bstack1ll111l_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡦࡰࡦࡹࡳࠨጒ"), bstack1ll111l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡣ࡭ࡣࡶࡷࠬጓ"), bstack1ll111l_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࠫጔ"), bstack1ll111l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࠨጕ")]:
            bstack11l11ll1ll_opy_ = test
        scope = []
        while bstack11l11ll1ll_opy_ is not None:
            scope.append(bstack11l11ll1ll_opy_.name)
            bstack11l11ll1ll_opy_ = bstack11l11ll1ll_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack11l1ll1l11_opy_(hook_type):
        if hook_type == bstack1ll111l_opy_ (u"ࠢࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠧ጖"):
            return bstack1ll111l_opy_ (u"ࠣࡕࡨࡸࡺࡶࠠࡩࡱࡲ࡯ࠧ጗")
        elif hook_type == bstack1ll111l_opy_ (u"ࠤࡄࡊ࡙ࡋࡒࡠࡇࡄࡇࡍࠨጘ"):
            return bstack1ll111l_opy_ (u"ࠥࡘࡪࡧࡲࡥࡱࡺࡲࠥ࡮࡯ࡰ࡭ࠥጙ")
    @staticmethod
    def bstack11l1l1l111_opy_(bstack111l1l1ll_opy_):
        try:
            if not bstack11llllll1_opy_.on():
                return bstack111l1l1ll_opy_
            if os.environ.get(bstack1ll111l_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡖࡊࡘࡕࡏࠤጚ"), None) == bstack1ll111l_opy_ (u"ࠧࡺࡲࡶࡧࠥጛ"):
                tests = os.environ.get(bstack1ll111l_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡘࡅࡓࡗࡑࡣ࡙ࡋࡓࡕࡕࠥጜ"), None)
                if tests is None or tests == bstack1ll111l_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧጝ"):
                    return bstack111l1l1ll_opy_
                bstack111l1l1ll_opy_ = tests.split(bstack1ll111l_opy_ (u"ࠨ࠮ࠪጞ"))
                return bstack111l1l1ll_opy_
        except Exception as exc:
            print(bstack1ll111l_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡴࡨࡶࡺࡴࠠࡩࡣࡱࡨࡱ࡫ࡲ࠻ࠢࠥጟ"), str(exc))
        return bstack111l1l1ll_opy_
    @classmethod
    def bstack11l1l11l1l_opy_(cls, event: str, bstack11l11lll11_opy_: bstack11ll111l11_opy_):
        bstack11l1ll1l1l_opy_ = {
            bstack1ll111l_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧጠ"): event,
            bstack11l11lll11_opy_.bstack11ll11lll1_opy_(): bstack11l11lll11_opy_.bstack11ll11ll11_opy_(event)
        }
        bstack11llllll1_opy_.bstack11l1l1l1ll_opy_(bstack11l1ll1l1l_opy_)