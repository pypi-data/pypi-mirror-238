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
import re
from bstack_utils.bstack11llll11ll_opy_ import bstack11lll1ll1l_opy_
def bstack11lll11lll_opy_(fixture_name):
    if fixture_name.startswith(bstack1ll111l_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡵࡨࡸࡺࡶ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᇇ")):
        return bstack1ll111l_opy_ (u"ࠩࡶࡩࡹࡻࡰ࠮ࡨࡸࡲࡨࡺࡩࡰࡰࠪᇈ")
    elif fixture_name.startswith(bstack1ll111l_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᇉ")):
        return bstack1ll111l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲ࠰ࡱࡴࡪࡵ࡭ࡧࠪᇊ")
    elif fixture_name.startswith(bstack1ll111l_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᇋ")):
        return bstack1ll111l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮࠮ࡨࡸࡲࡨࡺࡩࡰࡰࠪᇌ")
    elif fixture_name.startswith(bstack1ll111l_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᇍ")):
        return bstack1ll111l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰ࠰ࡱࡴࡪࡵ࡭ࡧࠪᇎ")
def bstack11lll1llll_opy_(fixture_name):
    return bool(re.match(bstack1ll111l_opy_ (u"ࠩࡡࡣࡽࡻ࡮ࡪࡶࡢࠬࡸ࡫ࡴࡶࡲࡿࡸࡪࡧࡲࡥࡱࡺࡲ࠮ࡥࠨࡧࡷࡱࡧࡹ࡯࡯࡯ࡾࡰࡳࡩࡻ࡬ࡦࠫࡢࡪ࡮ࡾࡴࡶࡴࡨࡣ࠳࠰ࠧᇏ"), fixture_name))
def bstack11llll1l1l_opy_(fixture_name):
    return bool(re.match(bstack1ll111l_opy_ (u"ࠪࡢࡤࡾࡵ࡯࡫ࡷࡣ࠭ࡹࡥࡵࡷࡳࢀࡹ࡫ࡡࡳࡦࡲࡻࡳ࠯࡟࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠ࠰࠭ࠫᇐ"), fixture_name))
def bstack11lll1l1l1_opy_(fixture_name):
    return bool(re.match(bstack1ll111l_opy_ (u"ࠫࡣࡥࡸࡶࡰ࡬ࡸࡤ࠮ࡳࡦࡶࡸࡴࢁࡺࡥࡢࡴࡧࡳࡼࡴࠩࡠࡥ࡯ࡥࡸࡹ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠ࠰࠭ࠫᇑ"), fixture_name))
def bstack11llll111l_opy_(fixture_name):
    if fixture_name.startswith(bstack1ll111l_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡹࡥࡵࡷࡳࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᇒ")):
        return bstack1ll111l_opy_ (u"࠭ࡳࡦࡶࡸࡴ࠲࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧᇓ"), bstack1ll111l_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬᇔ")
    elif fixture_name.startswith(bstack1ll111l_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᇕ")):
        return bstack1ll111l_opy_ (u"ࠩࡶࡩࡹࡻࡰ࠮࡯ࡲࡨࡺࡲࡥࠨᇖ"), bstack1ll111l_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡅࡑࡒࠧᇗ")
    elif fixture_name.startswith(bstack1ll111l_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᇘ")):
        return bstack1ll111l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࠭ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩᇙ"), bstack1ll111l_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠪᇚ")
    elif fixture_name.startswith(bstack1ll111l_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᇛ")):
        return bstack1ll111l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰ࠰ࡱࡴࡪࡵ࡭ࡧࠪᇜ"), bstack1ll111l_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡃࡏࡐࠬᇝ")
    return None, None
def bstack11lll1lll1_opy_(hook_name):
    if hook_name in [bstack1ll111l_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩᇞ"), bstack1ll111l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭ᇟ")]:
        return hook_name.capitalize()
    return hook_name
def bstack11llll11l1_opy_(hook_name):
    if hook_name in [bstack1ll111l_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭ᇠ"), bstack1ll111l_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳࡥࡵࡪࡲࡨࠬᇡ")]:
        return bstack1ll111l_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬᇢ")
    elif hook_name in [bstack1ll111l_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫ࠧᇣ"), bstack1ll111l_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡥ࡯ࡥࡸࡹࠧᇤ")]:
        return bstack1ll111l_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡅࡑࡒࠧᇥ")
    elif hook_name in [bstack1ll111l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨᇦ"), bstack1ll111l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡧࡷ࡬ࡴࡪࠧᇧ")]:
        return bstack1ll111l_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠪᇨ")
    elif hook_name in [bstack1ll111l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡳࡩࡻ࡬ࡦࠩᇩ"), bstack1ll111l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡧࡱࡧࡳࡴࠩᇪ")]:
        return bstack1ll111l_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡃࡏࡐࠬᇫ")
    return hook_name
def bstack11lll1l11l_opy_(node, scenario):
    if hasattr(node, bstack1ll111l_opy_ (u"ࠪࡧࡦࡲ࡬ࡴࡲࡨࡧࠬᇬ")):
        parts = node.nodeid.rsplit(bstack1ll111l_opy_ (u"ࠦࡠࠨᇭ"))
        params = parts[-1]
        return bstack1ll111l_opy_ (u"ࠧࢁࡽࠡ࡝ࡾࢁࠧᇮ").format(scenario.name, params)
    return scenario.name
def bstack11lll1ll11_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack1ll111l_opy_ (u"࠭ࡣࡢ࡮࡯ࡷࡵ࡫ࡣࠨᇯ")):
            examples = list(node.callspec.params[bstack1ll111l_opy_ (u"ࠧࡠࡲࡼࡸࡪࡹࡴࡠࡤࡧࡨࡤ࡫ࡸࡢ࡯ࡳࡰࡪ࠭ᇰ")].values())
        return examples
    except:
        return []
def bstack11lll1l1ll_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack11llll1l11_opy_(report):
    try:
        status = bstack1ll111l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᇱ")
        if report.passed or (report.failed and hasattr(report, bstack1ll111l_opy_ (u"ࠤࡺࡥࡸࡾࡦࡢ࡫࡯ࠦᇲ"))):
            status = bstack1ll111l_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᇳ")
        elif report.skipped:
            status = bstack1ll111l_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬᇴ")
        bstack11lll1ll1l_opy_(status)
    except:
        pass
def bstack111ll1lll_opy_(status):
    try:
        bstack11lll1l111_opy_ = bstack1ll111l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᇵ")
        if status == bstack1ll111l_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ᇶ"):
            bstack11lll1l111_opy_ = bstack1ll111l_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᇷ")
        elif status == bstack1ll111l_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩᇸ"):
            bstack11lll1l111_opy_ = bstack1ll111l_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪᇹ")
        bstack11lll1ll1l_opy_(bstack11lll1l111_opy_)
    except:
        pass
def bstack11llll1111_opy_(item=None, report=None, summary=None, extra=None):
    return