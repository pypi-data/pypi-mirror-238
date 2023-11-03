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
import os
import json
import requests
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import logging
from urllib.parse import urlparse
from datetime import datetime
from bstack_utils.constants import bstack1l1lllllll_opy_ as bstack1ll1111lll_opy_
from bstack_utils.helper import bstack1lll111l1l_opy_, bstack111llllll_opy_, bstack1ll1111l11_opy_, bstack1ll11111l1_opy_, bstack1llll1ll1_opy_, get_host_info, bstack1ll11111ll_opy_, bstack1l1l11l11_opy_
from browserstack_sdk._version import __version__
logger = logging.getLogger(__name__)
def bstack1111l1ll_opy_(config):
  try:
    if not bstack111llllll_opy_(config):
      return False
    bstack1ll111111l_opy_ = os.getenv(bstack1ll111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟࡚ࡏࡏࠫ಺")) == bstack1ll111l_opy_ (u"ࠦࡹࡸࡵࡦࠤ಻") or os.getenv(bstack1ll111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡓࡐࡆ࡚ࡆࡐࡔࡐ಼ࠫ")) == bstack1ll111l_opy_ (u"ࠨࡴࡳࡷࡨࠦಽ")
    bstack1l1llllll1_opy_ = os.getenv(bstack1ll111l_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬಾ")) is not None and len(os.getenv(bstack1ll111l_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ಿ"))) > 0 and os.getenv(bstack1ll111l_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧೀ")) != bstack1ll111l_opy_ (u"ࠪࡲࡺࡲ࡬ࠨು")
    return bstack1ll111111l_opy_ and bstack1l1llllll1_opy_
  except Exception as error:
    logger.debug(bstack1ll111l_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡺࡪࡸࡩࡧࡻ࡬ࡲ࡬ࠦࡴࡩࡧࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡷࡪࡹࡳࡪࡱࡱࠤࡼ࡯ࡴࡩࠢࡨࡶࡷࡵࡲࠡ࠼ࠣࠫೂ") + str(error))
  return False
def bstack111l111l1_opy_(config, bstack1ll1111ll1_opy_, bstack1l1llll1l1_opy_):
  bstack1l1llll1ll_opy_ = bstack1ll1111l11_opy_(config)
  bstack1l1lllll1l_opy_ = bstack1ll11111l1_opy_(config)
  if bstack1l1llll1ll_opy_ is None or bstack1l1lllll1l_opy_ is None:
    logger.error(bstack1ll111l_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡤࡴࡨࡥࡹ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡳࡷࡱࠤ࡫ࡵࡲࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱ࠾ࠥࡓࡩࡴࡵ࡬ࡲ࡬ࠦࡡࡶࡶ࡫ࡩࡳࡺࡩࡤࡣࡷ࡭ࡴࡴࠠࡵࡱ࡮ࡩࡳ࠭ೃ"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack1ll111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧೄ"), bstack1ll111l_opy_ (u"ࠧࡼࡿࠪ೅")))
    data = {
        bstack1ll111l_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭ೆ"): config[bstack1ll111l_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧೇ")],
        bstack1ll111l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ೈ"): config.get(bstack1ll111l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ೉"), os.path.basename(os.getcwd())),
        bstack1ll111l_opy_ (u"ࠬࡹࡴࡢࡴࡷࡘ࡮ࡳࡥࠨೊ"): bstack1lll111l1l_opy_(),
        bstack1ll111l_opy_ (u"࠭ࡤࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫೋ"): config.get(bstack1ll111l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡊࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪೌ"), bstack1ll111l_opy_ (u"ࠨ್ࠩ")),
        bstack1ll111l_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩ೎"): {
            bstack1ll111l_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡔࡡ࡮ࡧࠪ೏"): bstack1ll1111ll1_opy_,
            bstack1ll111l_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࡖࡦࡴࡶ࡭ࡴࡴࠧ೐"): bstack1l1llll1l1_opy_,
            bstack1ll111l_opy_ (u"ࠬࡹࡤ࡬ࡘࡨࡶࡸ࡯࡯࡯ࠩ೑"): __version__
        },
        bstack1ll111l_opy_ (u"࠭ࡳࡦࡶࡷ࡭ࡳ࡭ࡳࠨ೒"): settings,
        bstack1ll111l_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࡄࡱࡱࡸࡷࡵ࡬ࠨ೓"): bstack1ll11111ll_opy_(),
        bstack1ll111l_opy_ (u"ࠨࡥ࡬ࡍࡳ࡬࡯ࠨ೔"): bstack1llll1ll1_opy_(),
        bstack1ll111l_opy_ (u"ࠩ࡫ࡳࡸࡺࡉ࡯ࡨࡲࠫೕ"): get_host_info(),
        bstack1ll111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬೖ"): bstack111llllll_opy_(config)
    }
    headers = {
        bstack1ll111l_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪ೗"): bstack1ll111l_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨ೘"),
    }
    config = {
        bstack1ll111l_opy_ (u"࠭ࡡࡶࡶ࡫ࠫ೙"): (bstack1l1llll1ll_opy_, bstack1l1lllll1l_opy_),
        bstack1ll111l_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨ೚"): headers
    }
    response = bstack1l1l11l11_opy_(bstack1ll111l_opy_ (u"ࠨࡒࡒࡗ࡙࠭೛"), bstack1ll1111lll_opy_ + bstack1ll111l_opy_ (u"ࠩ࠲ࡸࡪࡹࡴࡠࡴࡸࡲࡸ࠭೜"), data, config)
    try:
      bstack1ll1111111_opy_ = response.json()
      parsed = json.loads(os.getenv(bstack1ll111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫೝ"), bstack1ll111l_opy_ (u"ࠫࢀࢃࠧೞ")))
      parsed[bstack1ll111l_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭೟")] = bstack1ll1111111_opy_[bstack1ll111l_opy_ (u"࠭ࡤࡢࡶࡤࠫೠ")][bstack1ll111l_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨೡ")]
      os.environ[bstack1ll111l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩೢ")] = json.dumps(parsed)
      return bstack1ll1111111_opy_[bstack1ll111l_opy_ (u"ࠩࡧࡥࡹࡧࠧೣ")][bstack1ll111l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡗࡳࡰ࡫࡮ࠨ೤")], bstack1ll1111111_opy_[bstack1ll111l_opy_ (u"ࠫࡩࡧࡴࡢࠩ೥")][bstack1ll111l_opy_ (u"ࠬ࡯ࡤࠨ೦")]
    except Exception as e:
      raise Exception(e)
  except Exception as error:
    logger.error(bstack1ll111l_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡥࡵࡩࡦࡺࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡴࡸࡲࠥ࡬࡯ࡳࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࠿ࠦࠢ೧") +  str(error))
    return None, None
def bstack1lll111ll_opy_():
  if os.getenv(bstack1ll111l_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬ೨")) is None:
    return {
        bstack1ll111l_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ೩"): bstack1ll111l_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ೪"),
        bstack1ll111l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ೫"): bstack1ll111l_opy_ (u"ࠫࡇࡻࡩ࡭ࡦࠣࡧࡷ࡫ࡡࡵ࡫ࡲࡲࠥ࡮ࡡࡥࠢࡩࡥ࡮ࡲࡥࡥ࠰ࠪ೬")
    }
  data = {bstack1ll111l_opy_ (u"ࠬ࡫࡮ࡥࡖ࡬ࡱࡪ࠭೭"): bstack1lll111l1l_opy_()}
  headers = {
      bstack1ll111l_opy_ (u"࠭ࡁࡶࡶ࡫ࡳࡷ࡯ࡺࡢࡶ࡬ࡳࡳ࠭೮"): bstack1ll111l_opy_ (u"ࠧࡃࡧࡤࡶࡪࡸࠠࠨ೯") + os.getenv(bstack1ll111l_opy_ (u"ࠣࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙ࠨ೰")),
      bstack1ll111l_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠨೱ"): bstack1ll111l_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ೲ")
  }
  response = bstack1l1l11l11_opy_(bstack1ll111l_opy_ (u"ࠫࡕ࡛ࡔࠨೳ"), bstack1ll1111lll_opy_ + bstack1ll111l_opy_ (u"ࠬ࠵ࡴࡦࡵࡷࡣࡷࡻ࡮ࡴ࠱ࡶࡸࡴࡶࠧ೴"), data, { bstack1ll111l_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧ೵"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack1ll111l_opy_ (u"ࠢࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡘࡪࡹࡴࠡࡔࡸࡲࠥࡳࡡࡳ࡭ࡨࡨࠥࡧࡳࠡࡥࡲࡱࡵࡲࡥࡵࡧࡧࠤࡦࡺࠠࠣ೶") + datetime.utcnow().isoformat() + bstack1ll111l_opy_ (u"ࠨ࡜ࠪ೷"))
      return {bstack1ll111l_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ೸"): bstack1ll111l_opy_ (u"ࠪࡷࡺࡩࡣࡦࡵࡶࠫ೹"), bstack1ll111l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ೺"): bstack1ll111l_opy_ (u"ࠬ࠭೻")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack1ll111l_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡ࡯ࡤࡶࡰ࡯࡮ࡨࠢࡦࡳࡲࡶ࡬ࡦࡶ࡬ࡳࡳࠦ࡯ࡧࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࡚ࠥࡥࡴࡶࠣࡖࡺࡴ࠺ࠡࠤ೼") + str(error))
    return {
        bstack1ll111l_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ೽"): bstack1ll111l_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧ೾"),
        bstack1ll111l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ೿"): str(error)
    }
def bstack1ll1111l1l_opy_(caps):
  try:
    bstack1l1llll111_opy_ = caps.get(bstack1ll111l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫഀ"), {}).get(bstack1ll111l_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨഁ"), caps.get(bstack1ll111l_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࠬം"), bstack1ll111l_opy_ (u"࠭ࠧഃ")))
    if bstack1l1llll111_opy_:
      logger.error(bstack1ll111l_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡵࡹࡳࠦ࡯࡯࡮ࡼࠤࡴࡴࠠࡅࡧࡶ࡯ࡹࡵࡰࠡࡤࡵࡳࡼࡹࡥࡳࡵ࠱ࠦഄ"))
      return False
    browser = caps.get(bstack1ll111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭അ"), bstack1ll111l_opy_ (u"ࠩࠪആ")).lower()
    if browser != bstack1ll111l_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪഇ"):
      logger.error(bstack1ll111l_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦࡲࡶࡰࠣࡳࡳࡲࡹࠡࡱࡱࠤࡈ࡮ࡲࡰ࡯ࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࡸ࠴ࠢഈ"))
      return False
    browser_version = caps.get(bstack1ll111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ഉ"), caps.get(bstack1ll111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨഊ")))
    if browser_version and browser_version != bstack1ll111l_opy_ (u"ࠧ࡭ࡣࡷࡩࡸࡺࠧഋ") and int(browser_version) <= 94:
      logger.error(bstack1ll111l_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡶࡺࡴࠠࡰࡰ࡯ࡽࠥࡵ࡮ࠡࡅ࡫ࡶࡴࡳࡥࠡࡤࡵࡳࡼࡹࡥࡳࠢࡹࡩࡷࡹࡩࡰࡰࠣ࡫ࡷ࡫ࡡࡵࡧࡵࠤࡹ࡮ࡡ࡯ࠢ࠼࠸࠳ࠨഌ"))
      return False
    chrome_options = webdriver.ChromeOptions()
    if bstack1ll111l_opy_ (u"ࠩ࠰࠱࡭࡫ࡡࡥ࡮ࡨࡷࡸ࠭഍") in chrome_options.arguments:
      logger.error(bstack1ll111l_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡴ࡯ࡵࠢࡵࡹࡳࠦ࡯࡯ࠢ࡯ࡩ࡬ࡧࡣࡺࠢ࡫ࡩࡦࡪ࡬ࡦࡵࡶࠤࡲࡵࡤࡦ࠰ࠣࡗࡼ࡯ࡴࡤࡪࠣࡸࡴࠦ࡮ࡦࡹࠣ࡬ࡪࡧࡤ࡭ࡧࡶࡷࠥࡳ࡯ࡥࡧࠣࡳࡷࠦࡡࡷࡱ࡬ࡨࠥࡻࡳࡪࡰࡪࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨ࠲ࠧഎ"))
      return False
    return True
  except Exception as error:
    logger.debug(bstack1ll111l_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡪࡺࠠࡦࡺࡷࡩࡳࡹࡩࡰࡰࠣࡉࡷࡸ࡯ࡳ࠼ࠥഏ") + str(error))
    return False
def bstack1lll1l111l_opy_(caps, config):
  try:
    if bstack1ll111l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬഐ") in config and config[bstack1ll111l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭഑")] == True:
      bstack1l1llll11l_opy_ = config.get(bstack1ll111l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧഒ"), {})
      bstack1l1llll11l_opy_[bstack1ll111l_opy_ (u"ࠨࡣࡸࡸ࡭࡚࡯࡬ࡧࡱࠫഓ")] = os.getenv(bstack1ll111l_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧഔ"))
      bstack1l1lllll11_opy_ = json.loads(os.getenv(bstack1ll111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫക"), bstack1ll111l_opy_ (u"ࠫࢀࢃࠧഖ"))).get(bstack1ll111l_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ഗ"))
      if bstack1ll111l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧഘ") in caps:
        caps[bstack1ll111l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨങ")][bstack1ll111l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨച")] = bstack1l1llll11l_opy_
        caps[bstack1ll111l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪഛ")][bstack1ll111l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪജ")][bstack1ll111l_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬഝ")] = bstack1l1lllll11_opy_
      else:
        bstack1l1llll11l_opy_[bstack1ll111l_opy_ (u"ࠬࡧࡵࡵࡪࡗࡳࡰ࡫࡮ࠨഞ")] = os.getenv(bstack1ll111l_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫട"))
        caps[bstack1ll111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ഠ")] = bstack1l1llll11l_opy_
        caps[bstack1ll111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧഡ")][bstack1ll111l_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪഢ")] = bstack1l1lllll11_opy_
  except Exception as error:
    logger.debug(bstack1ll111l_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴ࠰ࠣࡉࡷࡸ࡯ࡳࠤണ") + str(error))