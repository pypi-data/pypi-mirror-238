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
import atexit
import os
import signal
import sys
import yaml
import requests
import logging
import threading
import socket
import datetime
import string
import random
import json
import collections.abc
import re
import multiprocessing
import traceback
import copy
from packaging import version
from browserstack.local import Local
from urllib.parse import urlparse
from bstack_utils.constants import *
from bstack_utils.percy import *
import time
import requests
def bstack1ll1l1l1_opy_():
  global CONFIG
  headers = {
        bstack1ll111l_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨࡵ"): bstack1ll111l_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ࡶ"),
      }
  proxies = bstack11ll11l1_opy_(CONFIG, bstack1ll1lllll_opy_)
  try:
    response = requests.get(bstack1ll1lllll_opy_, headers=headers, proxies=proxies, timeout=5)
    if response.json():
      bstack1l1111111_opy_ = response.json()[bstack1ll111l_opy_ (u"ࠫ࡭ࡻࡢࡴࠩࡷ")]
      logger.debug(bstack111lll1ll_opy_.format(response.json()))
      return bstack1l1111111_opy_
    else:
      logger.debug(bstack111l1111l_opy_.format(bstack1ll111l_opy_ (u"ࠧࡘࡥࡴࡲࡲࡲࡸ࡫ࠠࡋࡕࡒࡒࠥࡶࡡࡳࡵࡨࠤࡪࡸࡲࡰࡴࠣࠦࡸ")))
  except Exception as e:
    logger.debug(bstack111l1111l_opy_.format(e))
def bstack11l1l1l1_opy_(hub_url):
  global CONFIG
  url = bstack1ll111l_opy_ (u"ࠨࡨࡵࡶࡳࡷ࠿࠵࠯ࠣࡹ")+  hub_url + bstack1ll111l_opy_ (u"ࠢ࠰ࡥ࡫ࡩࡨࡱࠢࡺ")
  headers = {
        bstack1ll111l_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡷࡽࡵ࡫ࠧࡻ"): bstack1ll111l_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬࡼ"),
      }
  proxies = bstack11ll11l1_opy_(CONFIG, url)
  try:
    start_time = time.perf_counter()
    requests.get(url, headers=headers, proxies=proxies, timeout=5)
    latency = time.perf_counter() - start_time
    logger.debug(bstack1l111lll_opy_.format(hub_url, latency))
    return dict(hub_url=hub_url, latency=latency)
  except Exception as e:
    logger.debug(bstack1ll1l1111l_opy_.format(hub_url, e))
def bstack1ll1ll1lll_opy_():
  try:
    global bstack1llll11l_opy_
    bstack1l1111111_opy_ = bstack1ll1l1l1_opy_()
    bstack1lll111l_opy_ = []
    results = []
    for bstack1l11l111_opy_ in bstack1l1111111_opy_:
      bstack1lll111l_opy_.append(bstack111lll111_opy_(target=bstack11l1l1l1_opy_,args=(bstack1l11l111_opy_,)))
    for t in bstack1lll111l_opy_:
      t.start()
    for t in bstack1lll111l_opy_:
      results.append(t.join())
    bstack1111l11ll_opy_ = {}
    for item in results:
      hub_url = item[bstack1ll111l_opy_ (u"ࠪ࡬ࡺࡨ࡟ࡶࡴ࡯ࠫࡽ")]
      latency = item[bstack1ll111l_opy_ (u"ࠫࡱࡧࡴࡦࡰࡦࡽࠬࡾ")]
      bstack1111l11ll_opy_[hub_url] = latency
    bstack11l1l111_opy_ = min(bstack1111l11ll_opy_, key= lambda x: bstack1111l11ll_opy_[x])
    bstack1llll11l_opy_ = bstack11l1l111_opy_
    logger.debug(bstack1l111111_opy_.format(bstack11l1l111_opy_))
  except Exception as e:
    logger.debug(bstack1lll1l11ll_opy_.format(e))
from bstack_utils.messages import *
from bstack_utils.config import Config
from bstack_utils.helper import bstack1l1l11l11_opy_, bstack1ll1ll1111_opy_, bstack1lll1111_opy_, bstack111llllll_opy_, Notset, bstack1111l11l_opy_, \
  bstack111l1ll1l_opy_, bstack11111lll1_opy_, bstack1ll1ll111l_opy_, bstack1llll1ll1_opy_, bstack111l1ll1_opy_
from bstack_utils.bstack11lllll1_opy_ import bstack11llllll1_opy_
from bstack_utils.proxy import bstack11l1l1l1l_opy_, bstack11ll11l1_opy_, bstack111llll11_opy_, bstack1ll1l1l1ll_opy_
from bstack_utils.bstack1l11ll11_opy_ import bstack111l111l1_opy_, bstack1lll111ll_opy_, bstack1lll1l111l_opy_, bstack1111l1ll_opy_
from browserstack_sdk.bstack1l111l1ll_opy_ import *
from browserstack_sdk.bstack1lll11ll1l_opy_ import *
from bstack_utils.bstack11111ll11_opy_ import bstack111ll1lll_opy_
bstack111111l11_opy_ = bstack1ll111l_opy_ (u"ࠬࠦࠠ࠰ࠬࠣࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃࠠࠫ࠱࡟ࡲࠥࠦࡩࡧࠪࡳࡥ࡬࡫ࠠ࠾࠿ࡀࠤࡻࡵࡩࡥࠢ࠳࠭ࠥࢁ࡜࡯ࠢࠣࠤࡹࡸࡹࡼ࡞ࡱࠤࡨࡵ࡮ࡴࡶࠣࡪࡸࠦ࠽ࠡࡴࡨࡵࡺ࡯ࡲࡦࠪ࡟ࠫ࡫ࡹ࡜ࠨࠫ࠾ࡠࡳࠦࠠࠡࠢࠣࡪࡸ࠴ࡡࡱࡲࡨࡲࡩࡌࡩ࡭ࡧࡖࡽࡳࡩࠨࡣࡵࡷࡥࡨࡱ࡟ࡱࡣࡷ࡬࠱ࠦࡊࡔࡑࡑ࠲ࡸࡺࡲࡪࡰࡪ࡭࡫ࡿࠨࡱࡡ࡬ࡲࡩ࡫ࡸࠪࠢ࠮ࠤࠧࡀࠢࠡ࠭ࠣࡎࡘࡕࡎ࠯ࡵࡷࡶ࡮ࡴࡧࡪࡨࡼࠬࡏ࡙ࡏࡏ࠰ࡳࡥࡷࡹࡥࠩࠪࡤࡻࡦ࡯ࡴࠡࡰࡨࡻࡕࡧࡧࡦ࠴࠱ࡩࡻࡧ࡬ࡶࡣࡷࡩ࠭ࠨࠨࠪࠢࡀࡂࠥࢁࡽࠣ࠮ࠣࡠࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧ࡭ࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡆࡨࡸࡦ࡯࡬ࡴࠤࢀࡠࠬ࠯ࠩࠪ࡝ࠥ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩࠨ࡝ࠪࠢ࠮ࠤࠧ࠲࡜࡝ࡰࠥ࠭ࡡࡴࠠࠡࠢࠣࢁࡨࡧࡴࡤࡪࠫࡩࡽ࠯ࡻ࡝ࡰࠣࠤࠥࠦࡽ࡝ࡰࠣࠤࢂࡢ࡮ࠡࠢ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࠬࡿ")
bstack11llll1l_opy_ = bstack1ll111l_opy_ (u"࠭࡜࡯࠱࠭ࠤࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽ࠡࠬ࠲ࡠࡳࡩ࡯࡯ࡵࡷࠤࡧࡹࡴࡢࡥ࡮ࡣࡵࡧࡴࡩࠢࡀࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࡞ࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࠰࡯ࡩࡳ࡭ࡴࡩࠢ࠰ࠤ࠸ࡣ࡜࡯ࡥࡲࡲࡸࡺࠠࡣࡵࡷࡥࡨࡱ࡟ࡤࡣࡳࡷࠥࡃࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻࡡࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠲࡟࡟ࡲࡨࡵ࡮ࡴࡶࠣࡴࡤ࡯࡮ࡥࡧࡻࠤࡂࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺࡠࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡱ࡫࡮ࡨࡶ࡫ࠤ࠲ࠦ࠲࡞࡞ࡱࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷࠢࡀࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡷࡱ࡯ࡣࡦࠪ࠳࠰ࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡱ࡫࡮ࡨࡶ࡫ࠤ࠲ࠦ࠳ࠪ࡞ࡱࡧࡴࡴࡳࡵࠢ࡬ࡱࡵࡵࡲࡵࡡࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠺࡟ࡣࡵࡷࡥࡨࡱࠠ࠾ࠢࡵࡩࡶࡻࡩࡳࡧࠫࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣࠫ࠾ࡠࡳ࡯࡭ࡱࡱࡵࡸࡤࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵ࠶ࡢࡦࡸࡺࡡࡤ࡭࠱ࡧ࡭ࡸ࡯࡮࡫ࡸࡱ࠳ࡲࡡࡶࡰࡦ࡬ࠥࡃࠠࡢࡵࡼࡲࡨࠦࠨ࡭ࡣࡸࡲࡨ࡮ࡏࡱࡶ࡬ࡳࡳࡹࠩࠡ࠿ࡁࠤࢀࡢ࡮࡭ࡧࡷࠤࡨࡧࡰࡴ࠽࡟ࡲࡹࡸࡹࠡࡽ࡟ࡲࡨࡧࡰࡴࠢࡀࠤࡏ࡙ࡏࡏ࠰ࡳࡥࡷࡹࡥࠩࡤࡶࡸࡦࡩ࡫ࡠࡥࡤࡴࡸ࠯࡜࡯ࠢࠣࢁࠥࡩࡡࡵࡥ࡫ࠬࡪࡾࠩࠡࡽ࡟ࡲࠥࠦࠠࠡࡿ࡟ࡲࠥࠦࡲࡦࡶࡸࡶࡳࠦࡡࡸࡣ࡬ࡸࠥ࡯࡭ࡱࡱࡵࡸࡤࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵ࠶ࡢࡦࡸࡺࡡࡤ࡭࠱ࡧ࡭ࡸ࡯࡮࡫ࡸࡱ࠳ࡩ࡯࡯ࡰࡨࡧࡹ࠮ࡻ࡝ࡰࠣࠤࠥࠦࡷࡴࡇࡱࡨࡵࡵࡩ࡯ࡶ࠽ࠤࡥࡽࡳࡴ࠼࠲࠳ࡨࡪࡰ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡀࡥࡤࡴࡸࡃࠤࡼࡧࡱࡧࡴࡪࡥࡖࡔࡌࡇࡴࡳࡰࡰࡰࡨࡲࡹ࠮ࡊࡔࡑࡑ࠲ࡸࡺࡲࡪࡰࡪ࡭࡫ࡿࠨࡤࡣࡳࡷ࠮࠯ࡽࡡ࠮࡟ࡲࠥࠦࠠࠡ࠰࠱࠲ࡱࡧࡵ࡯ࡥ࡫ࡓࡵࡺࡩࡰࡰࡶࡠࡳࠦࠠࡾࠫ࡟ࡲࢂࡢ࡮࠰ࠬࠣࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃࠠࠫ࠱࡟ࡲࠬࢀ")
from ._version import __version__
bstack1l11ll1l_opy_ = None
CONFIG = {}
bstack1ll1ll1l1_opy_ = {}
bstack1lllll1l11_opy_ = {}
bstack1ll1l1l111_opy_ = None
bstack1l1ll11l1_opy_ = None
bstack1ll11ll111_opy_ = None
bstack1llllll111_opy_ = -1
bstack1ll1l1111_opy_ = bstack1ll1lll1_opy_
bstack1lll1ll11_opy_ = 1
bstack11l1111l_opy_ = False
bstack11l11ll1l_opy_ = False
bstack1l1ll1lll_opy_ = bstack1ll111l_opy_ (u"ࠧࠨࢁ")
bstack11lll1lll_opy_ = bstack1ll111l_opy_ (u"ࠨࠩࢂ")
bstack1lll11l1l1_opy_ = False
bstack1ll1llllll_opy_ = True
bstack1l1l1ll1_opy_ = bstack1ll111l_opy_ (u"ࠩࠪࢃ")
bstack1l11lllll_opy_ = []
bstack1llll11l_opy_ = bstack1ll111l_opy_ (u"ࠪࠫࢄ")
bstack11lll1ll_opy_ = False
bstack11ll1ll1_opy_ = None
bstack1ll1l1l11l_opy_ = None
bstack11l1ll1l1_opy_ = -1
bstack1l1111ll1_opy_ = os.path.join(os.path.expanduser(bstack1ll111l_opy_ (u"ࠫࢃ࠭ࢅ")), bstack1ll111l_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬࢆ"), bstack1ll111l_opy_ (u"࠭࠮ࡳࡱࡥࡳࡹ࠳ࡲࡦࡲࡲࡶࡹ࠳ࡨࡦ࡮ࡳࡩࡷ࠴ࡪࡴࡱࡱࠫࢇ"))
bstack11ll1111_opy_ = []
bstack1ll111l11_opy_ = []
bstack11l1111l1_opy_ = False
bstack1llll1111_opy_ = False
bstack11l1l1ll1_opy_ = None
bstack1ll11lll_opy_ = None
bstack1ll111l1_opy_ = None
bstack1llll1111l_opy_ = None
bstack111lllll1_opy_ = None
bstack1llll1l1ll_opy_ = None
bstack11ll11111_opy_ = None
bstack111ll1l11_opy_ = None
bstack111ll11l_opy_ = None
bstack1ll1lllll1_opy_ = None
bstack11l1llll_opy_ = None
bstack111ll111l_opy_ = None
bstack11l1l11l1_opy_ = None
bstack1ll1ll11l_opy_ = None
bstack1ll11lll11_opy_ = None
bstack1lll11l11_opy_ = None
bstack1lllllll1_opy_ = None
bstack1lllll11ll_opy_ = None
bstack1l1l11111_opy_ = bstack1ll111l_opy_ (u"ࠢࠣ࢈")
logger = logging.getLogger(__name__)
logging.basicConfig(level=bstack1ll1l1111_opy_,
                    format=bstack1ll111l_opy_ (u"ࠨ࡞ࡱࠩ࠭ࡧࡳࡤࡶ࡬ࡱࡪ࠯ࡳࠡ࡝ࠨࠬࡳࡧ࡭ࡦࠫࡶࡡࡠࠫࠨ࡭ࡧࡹࡩࡱࡴࡡ࡮ࡧࠬࡷࡢࠦ࠭ࠡࠧࠫࡱࡪࡹࡳࡢࡩࡨ࠭ࡸ࠭ࢉ"),
                    datefmt=bstack1ll111l_opy_ (u"ࠩࠨࡌ࠿ࠫࡍ࠻ࠧࡖࠫࢊ"),
                    stream=sys.stdout)
bstack1ll1ll111_opy_ = Config.get_instance()
percy = bstack111lll11l_opy_()
def bstack1ll1l1l1l_opy_():
  global CONFIG
  global bstack1ll1l1111_opy_
  if bstack1ll111l_opy_ (u"ࠪࡰࡴ࡭ࡌࡦࡸࡨࡰࠬࢋ") in CONFIG:
    bstack1ll1l1111_opy_ = bstack11l11111l_opy_[CONFIG[bstack1ll111l_opy_ (u"ࠫࡱࡵࡧࡍࡧࡹࡩࡱ࠭ࢌ")]]
    logging.getLogger().setLevel(bstack1ll1l1111_opy_)
def bstack1ll1l1l1l1_opy_():
  global CONFIG
  global bstack11l1111l1_opy_
  bstack111111111_opy_ = bstack1ll111111_opy_(CONFIG)
  if (bstack1ll111l_opy_ (u"ࠬࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧࢍ") in bstack111111111_opy_ and str(bstack111111111_opy_[bstack1ll111l_opy_ (u"࠭ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨࢎ")]).lower() == bstack1ll111l_opy_ (u"ࠧࡵࡴࡸࡩࠬ࢏")):
    bstack11l1111l1_opy_ = True
def bstack1ll1llll_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack1l1111lll_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack111ll1l1_opy_():
  args = sys.argv
  for i in range(len(args)):
    if bstack1ll111l_opy_ (u"ࠣ࠯࠰ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡥࡲࡲ࡫࡯ࡧࡧ࡫࡯ࡩࠧ࢐") == args[i].lower() or bstack1ll111l_opy_ (u"ࠤ࠰࠱ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡴࡦࡪࡩࠥ࢑") == args[i].lower():
      path = args[i + 1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      global bstack1l1l1ll1_opy_
      bstack1l1l1ll1_opy_ += bstack1ll111l_opy_ (u"ࠪ࠱࠲ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡇࡴࡴࡦࡪࡩࡉ࡭ࡱ࡫ࠠࠨ࢒") + path
      return path
  return None
bstack11ll1lll_opy_ = re.compile(bstack1ll111l_opy_ (u"ࡶࠧ࠴ࠪࡀ࡞ࠧࡿ࠭࠴ࠪࡀࠫࢀ࠲࠯ࡅࠢ࢓"))
def bstack1ll11l111_opy_(loader, node):
  value = loader.construct_scalar(node)
  for group in bstack11ll1lll_opy_.findall(value):
    if group is not None and os.environ.get(group) is not None:
      value = value.replace(bstack1ll111l_opy_ (u"ࠧࠪࡻࠣ࢔") + group + bstack1ll111l_opy_ (u"ࠨࡽࠣ࢕"), os.environ.get(group))
  return value
def bstack1ll11l1l11_opy_():
  bstack11ll1lll1_opy_ = bstack111ll1l1_opy_()
  if bstack11ll1lll1_opy_ and os.path.exists(os.path.abspath(bstack11ll1lll1_opy_)):
    fileName = bstack11ll1lll1_opy_
  if bstack1ll111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡐࡐࡉࡍࡌࡥࡆࡊࡎࡈࠫ࢖") in os.environ and os.path.exists(
          os.path.abspath(os.environ[bstack1ll111l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡑࡑࡊࡎࡍ࡟ࡇࡋࡏࡉࠬࢗ")])) and not bstack1ll111l_opy_ (u"ࠩࡩ࡭ࡱ࡫ࡎࡢ࡯ࡨࠫ࢘") in locals():
    fileName = os.environ[bstack1ll111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡓࡓࡌࡉࡈࡡࡉࡍࡑࡋ࢙ࠧ")]
  if bstack1ll111l_opy_ (u"ࠫ࡫࡯࡬ࡦࡐࡤࡱࡪ࢚࠭") in locals():
    bstack1l1l_opy_ = os.path.abspath(fileName)
  else:
    bstack1l1l_opy_ = bstack1ll111l_opy_ (u"࢛ࠬ࠭")
  bstack1l11111l1_opy_ = os.getcwd()
  bstack11lll1111_opy_ = bstack1ll111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡿ࡭࡭ࠩ࢜")
  bstack1lll1111l1_opy_ = bstack1ll111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹࡢ࡯࡯ࠫ࢝")
  while (not os.path.exists(bstack1l1l_opy_)) and bstack1l11111l1_opy_ != bstack1ll111l_opy_ (u"ࠣࠤ࢞"):
    bstack1l1l_opy_ = os.path.join(bstack1l11111l1_opy_, bstack11lll1111_opy_)
    if not os.path.exists(bstack1l1l_opy_):
      bstack1l1l_opy_ = os.path.join(bstack1l11111l1_opy_, bstack1lll1111l1_opy_)
    if bstack1l11111l1_opy_ != os.path.dirname(bstack1l11111l1_opy_):
      bstack1l11111l1_opy_ = os.path.dirname(bstack1l11111l1_opy_)
    else:
      bstack1l11111l1_opy_ = bstack1ll111l_opy_ (u"ࠤࠥ࢟")
  if not os.path.exists(bstack1l1l_opy_):
    bstack1llllll11l_opy_(
      bstack11l1l111l_opy_.format(os.getcwd()))
  try:
    with open(bstack1l1l_opy_, bstack1ll111l_opy_ (u"ࠪࡶࠬࢠ")) as stream:
      yaml.add_implicit_resolver(bstack1ll111l_opy_ (u"ࠦࠦࡶࡡࡵࡪࡨࡼࠧࢡ"), bstack11ll1lll_opy_)
      yaml.add_constructor(bstack1ll111l_opy_ (u"ࠧࠧࡰࡢࡶ࡫ࡩࡽࠨࢢ"), bstack1ll11l111_opy_)
      config = yaml.load(stream, yaml.FullLoader)
      return config
  except:
    with open(bstack1l1l_opy_, bstack1ll111l_opy_ (u"࠭ࡲࠨࢣ")) as stream:
      try:
        config = yaml.safe_load(stream)
        return config
      except yaml.YAMLError as exc:
        bstack1llllll11l_opy_(bstack1ll1lll11_opy_.format(str(exc)))
def bstack1ll11l11_opy_(config):
  bstack1lll111111_opy_ = bstack1ll11ll1l_opy_(config)
  for option in list(bstack1lll111111_opy_):
    if option.lower() in bstack11ll1llll_opy_ and option != bstack11ll1llll_opy_[option.lower()]:
      bstack1lll111111_opy_[bstack11ll1llll_opy_[option.lower()]] = bstack1lll111111_opy_[option]
      del bstack1lll111111_opy_[option]
  return config
def bstack1l1111l11_opy_():
  global bstack1lllll1l11_opy_
  for key, bstack1llll111ll_opy_ in bstack1ll1l1ll1_opy_.items():
    if isinstance(bstack1llll111ll_opy_, list):
      for var in bstack1llll111ll_opy_:
        if var in os.environ and os.environ[var] and str(os.environ[var]).strip():
          bstack1lllll1l11_opy_[key] = os.environ[var]
          break
    elif bstack1llll111ll_opy_ in os.environ and os.environ[bstack1llll111ll_opy_] and str(os.environ[bstack1llll111ll_opy_]).strip():
      bstack1lllll1l11_opy_[key] = os.environ[bstack1llll111ll_opy_]
  if bstack1ll111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠩࢤ") in os.environ:
    bstack1lllll1l11_opy_[bstack1ll111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬࢥ")] = {}
    bstack1lllll1l11_opy_[bstack1ll111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࢦ")][bstack1ll111l_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࢧ")] = os.environ[bstack1ll111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭ࢨ")]
def bstack111l11l1l_opy_():
  global bstack1ll1ll1l1_opy_
  global bstack1l1l1ll1_opy_
  for idx, val in enumerate(sys.argv):
    if idx < len(sys.argv) and bstack1ll111l_opy_ (u"ࠬ࠳࠭ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨࢩ").lower() == val.lower():
      bstack1ll1ll1l1_opy_[bstack1ll111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪࢪ")] = {}
      bstack1ll1ll1l1_opy_[bstack1ll111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫࢫ")][bstack1ll111l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪࢬ")] = sys.argv[idx + 1]
      del sys.argv[idx:idx + 2]
      break
  for key, bstack1l11llll_opy_ in bstack111l1ll11_opy_.items():
    if isinstance(bstack1l11llll_opy_, list):
      for idx, val in enumerate(sys.argv):
        for var in bstack1l11llll_opy_:
          if idx < len(sys.argv) and bstack1ll111l_opy_ (u"ࠩ࠰࠱ࠬࢭ") + var.lower() == val.lower() and not key in bstack1ll1ll1l1_opy_:
            bstack1ll1ll1l1_opy_[key] = sys.argv[idx + 1]
            bstack1l1l1ll1_opy_ += bstack1ll111l_opy_ (u"ࠪࠤ࠲࠳ࠧࢮ") + var + bstack1ll111l_opy_ (u"ࠫࠥ࠭ࢯ") + sys.argv[idx + 1]
            del sys.argv[idx:idx + 2]
            break
    else:
      for idx, val in enumerate(sys.argv):
        if idx < len(sys.argv) and bstack1ll111l_opy_ (u"ࠬ࠳࠭ࠨࢰ") + bstack1l11llll_opy_.lower() == val.lower() and not key in bstack1ll1ll1l1_opy_:
          bstack1ll1ll1l1_opy_[key] = sys.argv[idx + 1]
          bstack1l1l1ll1_opy_ += bstack1ll111l_opy_ (u"࠭ࠠ࠮࠯ࠪࢱ") + bstack1l11llll_opy_ + bstack1ll111l_opy_ (u"ࠧࠡࠩࢲ") + sys.argv[idx + 1]
          del sys.argv[idx:idx + 2]
def bstack11l11l11l_opy_(config):
  bstack111l1lll_opy_ = config.keys()
  for bstack1ll1l1llll_opy_, bstack1l11ll1ll_opy_ in bstack1l11l1111_opy_.items():
    if bstack1l11ll1ll_opy_ in bstack111l1lll_opy_:
      config[bstack1ll1l1llll_opy_] = config[bstack1l11ll1ll_opy_]
      del config[bstack1l11ll1ll_opy_]
  for bstack1ll1l1llll_opy_, bstack1l11ll1ll_opy_ in bstack1ll11l1l1_opy_.items():
    if isinstance(bstack1l11ll1ll_opy_, list):
      for bstack1ll11ll1l1_opy_ in bstack1l11ll1ll_opy_:
        if bstack1ll11ll1l1_opy_ in bstack111l1lll_opy_:
          config[bstack1ll1l1llll_opy_] = config[bstack1ll11ll1l1_opy_]
          del config[bstack1ll11ll1l1_opy_]
          break
    elif bstack1l11ll1ll_opy_ in bstack111l1lll_opy_:
      config[bstack1ll1l1llll_opy_] = config[bstack1l11ll1ll_opy_]
      del config[bstack1l11ll1ll_opy_]
  for bstack1ll11ll1l1_opy_ in list(config):
    for bstack11lll11l1_opy_ in bstack1l1l1l111_opy_:
      if bstack1ll11ll1l1_opy_.lower() == bstack11lll11l1_opy_.lower() and bstack1ll11ll1l1_opy_ != bstack11lll11l1_opy_:
        config[bstack11lll11l1_opy_] = config[bstack1ll11ll1l1_opy_]
        del config[bstack1ll11ll1l1_opy_]
  bstack11l11ll11_opy_ = []
  if bstack1ll111l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫࢳ") in config:
    bstack11l11ll11_opy_ = config[bstack1ll111l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬࢴ")]
  for platform in bstack11l11ll11_opy_:
    for bstack1ll11ll1l1_opy_ in list(platform):
      for bstack11lll11l1_opy_ in bstack1l1l1l111_opy_:
        if bstack1ll11ll1l1_opy_.lower() == bstack11lll11l1_opy_.lower() and bstack1ll11ll1l1_opy_ != bstack11lll11l1_opy_:
          platform[bstack11lll11l1_opy_] = platform[bstack1ll11ll1l1_opy_]
          del platform[bstack1ll11ll1l1_opy_]
  for bstack1ll1l1llll_opy_, bstack1l11ll1ll_opy_ in bstack1ll11l1l1_opy_.items():
    for platform in bstack11l11ll11_opy_:
      if isinstance(bstack1l11ll1ll_opy_, list):
        for bstack1ll11ll1l1_opy_ in bstack1l11ll1ll_opy_:
          if bstack1ll11ll1l1_opy_ in platform:
            platform[bstack1ll1l1llll_opy_] = platform[bstack1ll11ll1l1_opy_]
            del platform[bstack1ll11ll1l1_opy_]
            break
      elif bstack1l11ll1ll_opy_ in platform:
        platform[bstack1ll1l1llll_opy_] = platform[bstack1l11ll1ll_opy_]
        del platform[bstack1l11ll1ll_opy_]
  for bstack111l1llll_opy_ in bstack11l11l1l_opy_:
    if bstack111l1llll_opy_ in config:
      if not bstack11l11l1l_opy_[bstack111l1llll_opy_] in config:
        config[bstack11l11l1l_opy_[bstack111l1llll_opy_]] = {}
      config[bstack11l11l1l_opy_[bstack111l1llll_opy_]].update(config[bstack111l1llll_opy_])
      del config[bstack111l1llll_opy_]
  for platform in bstack11l11ll11_opy_:
    for bstack111l1llll_opy_ in bstack11l11l1l_opy_:
      if bstack111l1llll_opy_ in list(platform):
        if not bstack11l11l1l_opy_[bstack111l1llll_opy_] in platform:
          platform[bstack11l11l1l_opy_[bstack111l1llll_opy_]] = {}
        platform[bstack11l11l1l_opy_[bstack111l1llll_opy_]].update(platform[bstack111l1llll_opy_])
        del platform[bstack111l1llll_opy_]
  config = bstack1ll11l11_opy_(config)
  return config
def bstack1111ll1ll_opy_(config):
  global bstack11lll1lll_opy_
  if bstack1ll111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧࢵ") in config and str(config[bstack1ll111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨࢶ")]).lower() != bstack1ll111l_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫࢷ"):
    if not bstack1ll111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪࢸ") in config:
      config[bstack1ll111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫࢹ")] = {}
    if not bstack1ll111l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪࢺ") in config[bstack1ll111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࢻ")]:
      bstack1lll111l1l_opy_ = datetime.datetime.now()
      bstack1111l1l11_opy_ = bstack1lll111l1l_opy_.strftime(bstack1ll111l_opy_ (u"ࠪࠩࡩࡥࠥࡣࡡࠨࡌࠪࡓࠧࢼ"))
      hostname = socket.gethostname()
      bstack11ll111l1_opy_ = bstack1ll111l_opy_ (u"ࠫࠬࢽ").join(random.choices(string.ascii_lowercase + string.digits, k=4))
      identifier = bstack1ll111l_opy_ (u"ࠬࢁࡽࡠࡽࢀࡣࢀࢃࠧࢾ").format(bstack1111l1l11_opy_, hostname, bstack11ll111l1_opy_)
      config[bstack1ll111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪࢿ")][bstack1ll111l_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩࣀ")] = identifier
    bstack11lll1lll_opy_ = config[bstack1ll111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬࣁ")][bstack1ll111l_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫࣂ")]
  return config
def bstack11l1ll111_opy_():
  bstack1ll1lll1l_opy_ =  bstack1llll1ll1_opy_()[bstack1ll111l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠩࣃ")]
  return bstack1ll1lll1l_opy_ if bstack1ll1lll1l_opy_ else -1
def bstack1lll1111ll_opy_(bstack1ll1lll1l_opy_):
  global CONFIG
  if not bstack1ll111l_opy_ (u"ࠫࠩࢁࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࢂ࠭ࣄ") in CONFIG[bstack1ll111l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࣅ")]:
    return
  CONFIG[bstack1ll111l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨࣆ")] = CONFIG[bstack1ll111l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩࣇ")].replace(
    bstack1ll111l_opy_ (u"ࠨࠦࡾࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࡿࠪࣈ"),
    str(bstack1ll1lll1l_opy_)
  )
def bstack1lll111ll1_opy_():
  global CONFIG
  if not bstack1ll111l_opy_ (u"ࠩࠧࡿࡉࡇࡔࡆࡡࡗࡍࡒࡋࡽࠨࣉ") in CONFIG[bstack1ll111l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ࣊")]:
    return
  bstack1lll111l1l_opy_ = datetime.datetime.now()
  bstack1111l1l11_opy_ = bstack1lll111l1l_opy_.strftime(bstack1ll111l_opy_ (u"ࠫࠪࡪ࠭ࠦࡤ࠰ࠩࡍࡀࠥࡎࠩ࣋"))
  CONFIG[bstack1ll111l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ࣌")] = CONFIG[bstack1ll111l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ࣍")].replace(
    bstack1ll111l_opy_ (u"ࠧࠥࡽࡇࡅ࡙ࡋ࡟ࡕࡋࡐࡉࢂ࠭࣎"),
    bstack1111l1l11_opy_
  )
def bstack111ll1111_opy_():
  global CONFIG
  if bstack1ll111l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴ࣏ࠪ") in CONFIG and not bool(CONFIG[bstack1ll111l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵ࣐ࠫ")]):
    del CONFIG[bstack1ll111l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶ࣑ࠬ")]
    return
  if not bstack1ll111l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࣒࠭") in CONFIG:
    CONFIG[bstack1ll111l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸ࣓ࠧ")] = bstack1ll111l_opy_ (u"࠭ࠣࠥࡽࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࡾࠩࣔ")
  if bstack1ll111l_opy_ (u"ࠧࠥࡽࡇࡅ࡙ࡋ࡟ࡕࡋࡐࡉࢂ࠭ࣕ") in CONFIG[bstack1ll111l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪࣖ")]:
    bstack1lll111ll1_opy_()
    os.environ[bstack1ll111l_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡡࡆࡓࡒࡈࡉࡏࡇࡇࡣࡇ࡛ࡉࡍࡆࡢࡍࡉ࠭ࣗ")] = CONFIG[bstack1ll111l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࣘ")]
  if not bstack1ll111l_opy_ (u"ࠫࠩࢁࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࢂ࠭ࣙ") in CONFIG[bstack1ll111l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࣚ")]:
    return
  bstack1ll1lll1l_opy_ = bstack1ll111l_opy_ (u"࠭ࠧࣛ")
  bstack1111lll1_opy_ = bstack11l1ll111_opy_()
  if bstack1111lll1_opy_ != -1:
    bstack1ll1lll1l_opy_ = bstack1ll111l_opy_ (u"ࠧࡄࡋࠣࠫࣜ") + str(bstack1111lll1_opy_)
  if bstack1ll1lll1l_opy_ == bstack1ll111l_opy_ (u"ࠨࠩࣝ"):
    bstack11l11llll_opy_ = bstack1ll1l11l1_opy_(CONFIG[bstack1ll111l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬࣞ")])
    if bstack11l11llll_opy_ != -1:
      bstack1ll1lll1l_opy_ = str(bstack11l11llll_opy_)
  if bstack1ll1lll1l_opy_:
    bstack1lll1111ll_opy_(bstack1ll1lll1l_opy_)
    os.environ[bstack1ll111l_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡢࡇࡔࡓࡂࡊࡐࡈࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠧࣟ")] = CONFIG[bstack1ll111l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭࣠")]
def bstack1lllll1lll_opy_(bstack1l1ll1ll1_opy_, bstack1ll11lll1_opy_, path):
  bstack1llll1l11_opy_ = {
    bstack1ll111l_opy_ (u"ࠬ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ࣡"): bstack1ll11lll1_opy_
  }
  if os.path.exists(path):
    bstack11l1lllll_opy_ = json.load(open(path, bstack1ll111l_opy_ (u"࠭ࡲࡣࠩ࣢")))
  else:
    bstack11l1lllll_opy_ = {}
  bstack11l1lllll_opy_[bstack1l1ll1ll1_opy_] = bstack1llll1l11_opy_
  with open(path, bstack1ll111l_opy_ (u"ࠢࡸࣣ࠭ࠥ")) as outfile:
    json.dump(bstack11l1lllll_opy_, outfile)
def bstack1ll1l11l1_opy_(bstack1l1ll1ll1_opy_):
  bstack1l1ll1ll1_opy_ = str(bstack1l1ll1ll1_opy_)
  bstack1ll1ll11ll_opy_ = os.path.join(os.path.expanduser(bstack1ll111l_opy_ (u"ࠨࢀࠪࣤ")), bstack1ll111l_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩࣥ"))
  try:
    if not os.path.exists(bstack1ll1ll11ll_opy_):
      os.makedirs(bstack1ll1ll11ll_opy_)
    file_path = os.path.join(os.path.expanduser(bstack1ll111l_opy_ (u"ࠪࢂࣦࠬ")), bstack1ll111l_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫࣧ"), bstack1ll111l_opy_ (u"ࠬ࠴ࡢࡶ࡫࡯ࡨ࠲ࡴࡡ࡮ࡧ࠰ࡧࡦࡩࡨࡦ࠰࡭ࡷࡴࡴࠧࣨ"))
    if not os.path.isfile(file_path):
      with open(file_path, bstack1ll111l_opy_ (u"࠭ࡷࠨࣩ")):
        pass
      with open(file_path, bstack1ll111l_opy_ (u"ࠢࡸ࠭ࠥ࣪")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstack1ll111l_opy_ (u"ࠨࡴࠪ࣫")) as bstack11ll1l1l1_opy_:
      bstack1ll1l111ll_opy_ = json.load(bstack11ll1l1l1_opy_)
    if bstack1l1ll1ll1_opy_ in bstack1ll1l111ll_opy_:
      bstack1ll1l11lll_opy_ = bstack1ll1l111ll_opy_[bstack1l1ll1ll1_opy_][bstack1ll111l_opy_ (u"ࠩ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭࣬")]
      bstack111ll11l1_opy_ = int(bstack1ll1l11lll_opy_) + 1
      bstack1lllll1lll_opy_(bstack1l1ll1ll1_opy_, bstack111ll11l1_opy_, file_path)
      return bstack111ll11l1_opy_
    else:
      bstack1lllll1lll_opy_(bstack1l1ll1ll1_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warn(bstack1ll1ll1l_opy_.format(str(e)))
    return -1
def bstack111l11lll_opy_(config):
  if not config[bstack1ll111l_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩ࣭ࠬ")] or not config[bstack1ll111l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿ࣮ࠧ")]:
    return True
  else:
    return False
def bstack111l11ll_opy_(config, index=0):
  global bstack1lll11l1l1_opy_
  bstack1111ll111_opy_ = {}
  caps = bstack1llllll1l1_opy_ + bstack1111ll11l_opy_
  if bstack1lll11l1l1_opy_:
    caps += bstack1l1l1l1l1_opy_
  for key in config:
    if key in caps + [bstack1ll111l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ࣯")]:
      continue
    bstack1111ll111_opy_[key] = config[key]
  if bstack1ll111l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࣰࠩ") in config:
    for bstack1ll1ll1ll1_opy_ in config[bstack1ll111l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࣱࠪ")][index]:
      if bstack1ll1ll1ll1_opy_ in caps + [bstack1ll111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪࣲ࠭"), bstack1ll111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪࣳ")]:
        continue
      bstack1111ll111_opy_[bstack1ll1ll1ll1_opy_] = config[bstack1ll111l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ࣴ")][index][bstack1ll1ll1ll1_opy_]
  bstack1111ll111_opy_[bstack1ll111l_opy_ (u"ࠫ࡭ࡵࡳࡵࡐࡤࡱࡪ࠭ࣵ")] = socket.gethostname()
  if bstack1ll111l_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳࣶ࠭") in bstack1111ll111_opy_:
    del (bstack1111ll111_opy_[bstack1ll111l_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࠧࣷ")])
  return bstack1111ll111_opy_
def bstack1lll111lll_opy_(config):
  global bstack1lll11l1l1_opy_
  bstack1lllllllll_opy_ = {}
  caps = bstack1111ll11l_opy_
  if bstack1lll11l1l1_opy_:
    caps += bstack1l1l1l1l1_opy_
  for key in caps:
    if key in config:
      bstack1lllllllll_opy_[key] = config[key]
  return bstack1lllllllll_opy_
def bstack11lllllll_opy_(bstack1111ll111_opy_, bstack1lllllllll_opy_):
  bstack1lll1l11l_opy_ = {}
  for key in bstack1111ll111_opy_.keys():
    if key in bstack1l11l1111_opy_:
      bstack1lll1l11l_opy_[bstack1l11l1111_opy_[key]] = bstack1111ll111_opy_[key]
    else:
      bstack1lll1l11l_opy_[key] = bstack1111ll111_opy_[key]
  for key in bstack1lllllllll_opy_:
    if key in bstack1l11l1111_opy_:
      bstack1lll1l11l_opy_[bstack1l11l1111_opy_[key]] = bstack1lllllllll_opy_[key]
    else:
      bstack1lll1l11l_opy_[key] = bstack1lllllllll_opy_[key]
  return bstack1lll1l11l_opy_
def bstack1ll1l11111_opy_(config, index=0):
  global bstack1lll11l1l1_opy_
  config = copy.deepcopy(config)
  caps = {}
  bstack1lllllllll_opy_ = bstack1lll111lll_opy_(config)
  bstack1l111l111_opy_ = bstack1111ll11l_opy_
  bstack1l111l111_opy_ += bstack111111l1_opy_
  if bstack1lll11l1l1_opy_:
    bstack1l111l111_opy_ += bstack1l1l1l1l1_opy_
  if bstack1ll111l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪࣸ") in config:
    if bstack1ll111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪࣹ࠭") in config[bstack1ll111l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࣺࠬ")][index]:
      caps[bstack1ll111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨࣻ")] = config[bstack1ll111l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧࣼ")][index][bstack1ll111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪࣽ")]
    if bstack1ll111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧࣾ") in config[bstack1ll111l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪࣿ")][index]:
      caps[bstack1ll111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩऀ")] = str(config[bstack1ll111l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬँ")][index][bstack1ll111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫं")])
    bstack1ll1llll1l_opy_ = {}
    for bstack111111ll1_opy_ in bstack1l111l111_opy_:
      if bstack111111ll1_opy_ in config[bstack1ll111l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧः")][index]:
        if bstack111111ll1_opy_ == bstack1ll111l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠧऄ"):
          try:
            bstack1ll1llll1l_opy_[bstack111111ll1_opy_] = str(config[bstack1ll111l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩअ")][index][bstack111111ll1_opy_] * 1.0)
          except:
            bstack1ll1llll1l_opy_[bstack111111ll1_opy_] = str(config[bstack1ll111l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪआ")][index][bstack111111ll1_opy_])
        else:
          bstack1ll1llll1l_opy_[bstack111111ll1_opy_] = config[bstack1ll111l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫइ")][index][bstack111111ll1_opy_]
        del (config[bstack1ll111l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬई")][index][bstack111111ll1_opy_])
    bstack1lllllllll_opy_ = update(bstack1lllllllll_opy_, bstack1ll1llll1l_opy_)
  bstack1111ll111_opy_ = bstack111l11ll_opy_(config, index)
  for bstack1ll11ll1l1_opy_ in bstack1111ll11l_opy_ + [bstack1ll111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨउ"), bstack1ll111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬऊ")]:
    if bstack1ll11ll1l1_opy_ in bstack1111ll111_opy_:
      bstack1lllllllll_opy_[bstack1ll11ll1l1_opy_] = bstack1111ll111_opy_[bstack1ll11ll1l1_opy_]
      del (bstack1111ll111_opy_[bstack1ll11ll1l1_opy_])
  if bstack1111l11l_opy_(config):
    bstack1111ll111_opy_[bstack1ll111l_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬऋ")] = True
    caps.update(bstack1lllllllll_opy_)
    caps[bstack1ll111l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧऌ")] = bstack1111ll111_opy_
  else:
    bstack1111ll111_opy_[bstack1ll111l_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧऍ")] = False
    caps.update(bstack11lllllll_opy_(bstack1111ll111_opy_, bstack1lllllllll_opy_))
    if bstack1ll111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ऎ") in caps:
      caps[bstack1ll111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪए")] = caps[bstack1ll111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨऐ")]
      del (caps[bstack1ll111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩऑ")])
    if bstack1ll111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ऒ") in caps:
      caps[bstack1ll111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨओ")] = caps[bstack1ll111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨऔ")]
      del (caps[bstack1ll111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩक")])
  return caps
def bstack1lll1lll1_opy_():
  global bstack1llll11l_opy_
  if bstack1l1111lll_opy_() <= version.parse(bstack1ll111l_opy_ (u"ࠩ࠶࠲࠶࠹࠮࠱ࠩख")):
    if bstack1llll11l_opy_ != bstack1ll111l_opy_ (u"ࠪࠫग"):
      return bstack1ll111l_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧघ") + bstack1llll11l_opy_ + bstack1ll111l_opy_ (u"ࠧࡀ࠸࠱࠱ࡺࡨ࠴࡮ࡵࡣࠤङ")
    return bstack11111l1l1_opy_
  if bstack1llll11l_opy_ != bstack1ll111l_opy_ (u"࠭ࠧच"):
    return bstack1ll111l_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤछ") + bstack1llll11l_opy_ + bstack1ll111l_opy_ (u"ࠣ࠱ࡺࡨ࠴࡮ࡵࡣࠤज")
  return bstack1l111111l_opy_
def bstack1l1llllll_opy_(options):
  return hasattr(options, bstack1ll111l_opy_ (u"ࠩࡶࡩࡹࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵࡻࠪझ"))
def update(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = update(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack1lll1lllll_opy_(options, bstack11ll1111l_opy_):
  for bstack1lll1lll1l_opy_ in bstack11ll1111l_opy_:
    if bstack1lll1lll1l_opy_ in [bstack1ll111l_opy_ (u"ࠪࡥࡷ࡭ࡳࠨञ"), bstack1ll111l_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨट")]:
      continue
    if bstack1lll1lll1l_opy_ in options._experimental_options:
      options._experimental_options[bstack1lll1lll1l_opy_] = update(options._experimental_options[bstack1lll1lll1l_opy_],
                                                         bstack11ll1111l_opy_[bstack1lll1lll1l_opy_])
    else:
      options.add_experimental_option(bstack1lll1lll1l_opy_, bstack11ll1111l_opy_[bstack1lll1lll1l_opy_])
  if bstack1ll111l_opy_ (u"ࠬࡧࡲࡨࡵࠪठ") in bstack11ll1111l_opy_:
    for arg in bstack11ll1111l_opy_[bstack1ll111l_opy_ (u"࠭ࡡࡳࡩࡶࠫड")]:
      options.add_argument(arg)
    del (bstack11ll1111l_opy_[bstack1ll111l_opy_ (u"ࠧࡢࡴࡪࡷࠬढ")])
  if bstack1ll111l_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬण") in bstack11ll1111l_opy_:
    for ext in bstack11ll1111l_opy_[bstack1ll111l_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭त")]:
      options.add_extension(ext)
    del (bstack11ll1111l_opy_[bstack1ll111l_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧथ")])
def bstack1111ll1l1_opy_(options, bstack1l111ll1_opy_):
  if bstack1ll111l_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪद") in bstack1l111ll1_opy_:
    for bstack111l111l_opy_ in bstack1l111ll1_opy_[bstack1ll111l_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫध")]:
      if bstack111l111l_opy_ in options._preferences:
        options._preferences[bstack111l111l_opy_] = update(options._preferences[bstack111l111l_opy_], bstack1l111ll1_opy_[bstack1ll111l_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬन")][bstack111l111l_opy_])
      else:
        options.set_preference(bstack111l111l_opy_, bstack1l111ll1_opy_[bstack1ll111l_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭ऩ")][bstack111l111l_opy_])
  if bstack1ll111l_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭प") in bstack1l111ll1_opy_:
    for arg in bstack1l111ll1_opy_[bstack1ll111l_opy_ (u"ࠩࡤࡶ࡬ࡹࠧफ")]:
      options.add_argument(arg)
def bstack1lll1ll1_opy_(options, bstack111l11l1_opy_):
  if bstack1ll111l_opy_ (u"ࠪࡻࡪࡨࡶࡪࡧࡺࠫब") in bstack111l11l1_opy_:
    options.use_webview(bool(bstack111l11l1_opy_[bstack1ll111l_opy_ (u"ࠫࡼ࡫ࡢࡷ࡫ࡨࡻࠬभ")]))
  bstack1lll1lllll_opy_(options, bstack111l11l1_opy_)
def bstack1111111ll_opy_(options, bstack11l11lll_opy_):
  for bstack111ll1ll1_opy_ in bstack11l11lll_opy_:
    if bstack111ll1ll1_opy_ in [bstack1ll111l_opy_ (u"ࠬࡺࡥࡤࡪࡱࡳࡱࡵࡧࡺࡒࡵࡩࡻ࡯ࡥࡸࠩम"), bstack1ll111l_opy_ (u"࠭ࡡࡳࡩࡶࠫय")]:
      continue
    options.set_capability(bstack111ll1ll1_opy_, bstack11l11lll_opy_[bstack111ll1ll1_opy_])
  if bstack1ll111l_opy_ (u"ࠧࡢࡴࡪࡷࠬर") in bstack11l11lll_opy_:
    for arg in bstack11l11lll_opy_[bstack1ll111l_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ऱ")]:
      options.add_argument(arg)
  if bstack1ll111l_opy_ (u"ࠩࡷࡩࡨ࡮࡮ࡰ࡮ࡲ࡫ࡾࡖࡲࡦࡸ࡬ࡩࡼ࠭ल") in bstack11l11lll_opy_:
    options.bstack1llll1l1_opy_(bool(bstack11l11lll_opy_[bstack1ll111l_opy_ (u"ࠪࡸࡪࡩࡨ࡯ࡱ࡯ࡳ࡬ࡿࡐࡳࡧࡹ࡭ࡪࡽࠧळ")]))
def bstack1lllll1ll1_opy_(options, bstack1lll1l1l_opy_):
  for bstack1lll11lll_opy_ in bstack1lll1l1l_opy_:
    if bstack1lll11lll_opy_ in [bstack1ll111l_opy_ (u"ࠫࡦࡪࡤࡪࡶ࡬ࡳࡳࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨऴ"), bstack1ll111l_opy_ (u"ࠬࡧࡲࡨࡵࠪव")]:
      continue
    options._options[bstack1lll11lll_opy_] = bstack1lll1l1l_opy_[bstack1lll11lll_opy_]
  if bstack1ll111l_opy_ (u"࠭ࡡࡥࡦ࡬ࡸ࡮ࡵ࡮ࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪश") in bstack1lll1l1l_opy_:
    for bstack1l1ll1l1_opy_ in bstack1lll1l1l_opy_[bstack1ll111l_opy_ (u"ࠧࡢࡦࡧ࡭ࡹ࡯࡯࡯ࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫष")]:
      options.bstack1ll1ll1l11_opy_(
        bstack1l1ll1l1_opy_, bstack1lll1l1l_opy_[bstack1ll111l_opy_ (u"ࠨࡣࡧࡨ࡮ࡺࡩࡰࡰࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬस")][bstack1l1ll1l1_opy_])
  if bstack1ll111l_opy_ (u"ࠩࡤࡶ࡬ࡹࠧह") in bstack1lll1l1l_opy_:
    for arg in bstack1lll1l1l_opy_[bstack1ll111l_opy_ (u"ࠪࡥࡷ࡭ࡳࠨऺ")]:
      options.add_argument(arg)
def bstack11ll1l1l_opy_(options, caps):
  if not hasattr(options, bstack1ll111l_opy_ (u"ࠫࡐࡋ࡙ࠨऻ")):
    return
  if options.KEY == bstack1ll111l_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵ़ࠪ") and options.KEY in caps:
    bstack1lll1lllll_opy_(options, caps[bstack1ll111l_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫऽ")])
  elif options.KEY == bstack1ll111l_opy_ (u"ࠧ࡮ࡱࡽ࠾࡫࡯ࡲࡦࡨࡲࡼࡔࡶࡴࡪࡱࡱࡷࠬा") and options.KEY in caps:
    bstack1111ll1l1_opy_(options, caps[bstack1ll111l_opy_ (u"ࠨ࡯ࡲࡾ࠿࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭ि")])
  elif options.KEY == bstack1ll111l_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪ࠰ࡲࡴࡹ࡯࡯࡯ࡵࠪी") and options.KEY in caps:
    bstack1111111ll_opy_(options, caps[bstack1ll111l_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫࠱ࡳࡵࡺࡩࡰࡰࡶࠫु")])
  elif options.KEY == bstack1ll111l_opy_ (u"ࠫࡲࡹ࠺ࡦࡦࡪࡩࡔࡶࡴࡪࡱࡱࡷࠬू") and options.KEY in caps:
    bstack1lll1ll1_opy_(options, caps[bstack1ll111l_opy_ (u"ࠬࡳࡳ࠻ࡧࡧ࡫ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ृ")])
  elif options.KEY == bstack1ll111l_opy_ (u"࠭ࡳࡦ࠼࡬ࡩࡔࡶࡴࡪࡱࡱࡷࠬॄ") and options.KEY in caps:
    bstack1lllll1ll1_opy_(options, caps[bstack1ll111l_opy_ (u"ࠧࡴࡧ࠽࡭ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ॅ")])
def bstack11l11l1l1_opy_(caps):
  global bstack1lll11l1l1_opy_
  if isinstance(os.environ.get(bstack1ll111l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩॆ")), str):
    bstack1lll11l1l1_opy_ = eval(os.getenv(bstack1ll111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪे")))
  if bstack1lll11l1l1_opy_:
    if bstack1ll1llll_opy_() < version.parse(bstack1ll111l_opy_ (u"ࠪ࠶࠳࠹࠮࠱ࠩै")):
      return None
    else:
      from appium.options.common.base import AppiumOptions
      options = AppiumOptions().load_capabilities(caps)
      return options
  else:
    browser = bstack1ll111l_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫॉ")
    if bstack1ll111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪॊ") in caps:
      browser = caps[bstack1ll111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫो")]
    elif bstack1ll111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨौ") in caps:
      browser = caps[bstack1ll111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳ्ࠩ")]
    browser = str(browser).lower()
    if browser == bstack1ll111l_opy_ (u"ࠩ࡬ࡴ࡭ࡵ࡮ࡦࠩॎ") or browser == bstack1ll111l_opy_ (u"ࠪ࡭ࡵࡧࡤࠨॏ"):
      browser = bstack1ll111l_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬ࠫॐ")
    if browser == bstack1ll111l_opy_ (u"ࠬࡹࡡ࡮ࡵࡸࡲ࡬࠭॑"):
      browser = bstack1ll111l_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ॒࠭")
    if browser not in [bstack1ll111l_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧ॓"), bstack1ll111l_opy_ (u"ࠨࡧࡧ࡫ࡪ࠭॔"), bstack1ll111l_opy_ (u"ࠩ࡬ࡩࠬॕ"), bstack1ll111l_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫ࠪॖ"), bstack1ll111l_opy_ (u"ࠫ࡫࡯ࡲࡦࡨࡲࡼࠬॗ")]:
      return None
    try:
      package = bstack1ll111l_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࠮ࡸࡧࡥࡨࡷ࡯ࡶࡦࡴ࠱ࡿࢂ࠴࡯ࡱࡶ࡬ࡳࡳࡹࠧक़").format(browser)
      name = bstack1ll111l_opy_ (u"࠭ࡏࡱࡶ࡬ࡳࡳࡹࠧख़")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack1l1llllll_opy_(options):
        return None
      for bstack1ll11ll1l1_opy_ in caps.keys():
        options.set_capability(bstack1ll11ll1l1_opy_, caps[bstack1ll11ll1l1_opy_])
      bstack11ll1l1l_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack1l1ll1ll_opy_(options, bstack1lllll1l1l_opy_):
  if not bstack1l1llllll_opy_(options):
    return
  for bstack1ll11ll1l1_opy_ in bstack1lllll1l1l_opy_.keys():
    if bstack1ll11ll1l1_opy_ in bstack111111l1_opy_:
      continue
    if bstack1ll11ll1l1_opy_ in options._caps and type(options._caps[bstack1ll11ll1l1_opy_]) in [dict, list]:
      options._caps[bstack1ll11ll1l1_opy_] = update(options._caps[bstack1ll11ll1l1_opy_], bstack1lllll1l1l_opy_[bstack1ll11ll1l1_opy_])
    else:
      options.set_capability(bstack1ll11ll1l1_opy_, bstack1lllll1l1l_opy_[bstack1ll11ll1l1_opy_])
  bstack11ll1l1l_opy_(options, bstack1lllll1l1l_opy_)
  if bstack1ll111l_opy_ (u"ࠧ࡮ࡱࡽ࠾ࡩ࡫ࡢࡶࡩࡪࡩࡷࡇࡤࡥࡴࡨࡷࡸ࠭ग़") in options._caps:
    if options._caps[bstack1ll111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ज़")] and options._caps[bstack1ll111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧड़")].lower() != bstack1ll111l_opy_ (u"ࠪࡪ࡮ࡸࡥࡧࡱࡻࠫढ़"):
      del options._caps[bstack1ll111l_opy_ (u"ࠫࡲࡵࡺ࠻ࡦࡨࡦࡺ࡭ࡧࡦࡴࡄࡨࡩࡸࡥࡴࡵࠪफ़")]
def bstack11111l11l_opy_(proxy_config):
  if bstack1ll111l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩय़") in proxy_config:
    proxy_config[bstack1ll111l_opy_ (u"࠭ࡳࡴ࡮ࡓࡶࡴࡾࡹࠨॠ")] = proxy_config[bstack1ll111l_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫॡ")]
    del (proxy_config[bstack1ll111l_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬॢ")])
  if bstack1ll111l_opy_ (u"ࠩࡳࡶࡴࡾࡹࡕࡻࡳࡩࠬॣ") in proxy_config and proxy_config[bstack1ll111l_opy_ (u"ࠪࡴࡷࡵࡸࡺࡖࡼࡴࡪ࠭।")].lower() != bstack1ll111l_opy_ (u"ࠫࡩ࡯ࡲࡦࡥࡷࠫ॥"):
    proxy_config[bstack1ll111l_opy_ (u"ࠬࡶࡲࡰࡺࡼࡘࡾࡶࡥࠨ०")] = bstack1ll111l_opy_ (u"࠭࡭ࡢࡰࡸࡥࡱ࠭१")
  if bstack1ll111l_opy_ (u"ࠧࡱࡴࡲࡼࡾࡇࡵࡵࡱࡦࡳࡳ࡬ࡩࡨࡗࡵࡰࠬ२") in proxy_config:
    proxy_config[bstack1ll111l_opy_ (u"ࠨࡲࡵࡳࡽࡿࡔࡺࡲࡨࠫ३")] = bstack1ll111l_opy_ (u"ࠩࡳࡥࡨ࠭४")
  return proxy_config
def bstack1l1lll1ll_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack1ll111l_opy_ (u"ࠪࡴࡷࡵࡸࡺࠩ५") in config:
    return proxy
  config[bstack1ll111l_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࠪ६")] = bstack11111l11l_opy_(config[bstack1ll111l_opy_ (u"ࠬࡶࡲࡰࡺࡼࠫ७")])
  if proxy == None:
    proxy = Proxy(config[bstack1ll111l_opy_ (u"࠭ࡰࡳࡱࡻࡽࠬ८")])
  return proxy
def bstack1ll1l11ll1_opy_(self):
  global CONFIG
  global bstack11l1llll_opy_
  try:
    proxy = bstack111llll11_opy_(CONFIG)
    if proxy:
      if proxy.endswith(bstack1ll111l_opy_ (u"ࠧ࠯ࡲࡤࡧࠬ९")):
        proxies = bstack11l1l1l1l_opy_(proxy, bstack1lll1lll1_opy_())
        if len(proxies) > 0:
          protocol, bstack11ll1ll11_opy_ = proxies.popitem()
          if bstack1ll111l_opy_ (u"ࠣ࠼࠲࠳ࠧ॰") in bstack11ll1ll11_opy_:
            return bstack11ll1ll11_opy_
          else:
            return bstack1ll111l_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥॱ") + bstack11ll1ll11_opy_
      else:
        return proxy
  except Exception as e:
    logger.error(bstack1ll111l_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡰࡳࡱࡻࡽࠥࡻࡲ࡭ࠢ࠽ࠤࢀࢃࠢॲ").format(str(e)))
  return bstack11l1llll_opy_(self)
def bstack1llllll1l_opy_():
  global CONFIG
  return bstack1ll1l1l1ll_opy_(CONFIG) and bstack1l1111lll_opy_() >= version.parse(bstack1ll1lll1ll_opy_)
def bstack1ll11ll1l_opy_(config):
  bstack1lll111111_opy_ = {}
  if bstack1ll111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨॳ") in config:
    bstack1lll111111_opy_ = config[bstack1ll111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩॴ")]
  if bstack1ll111l_opy_ (u"࠭࡬ࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬॵ") in config:
    bstack1lll111111_opy_ = config[bstack1ll111l_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ॶ")]
  proxy = bstack111llll11_opy_(config)
  if proxy:
    if proxy.endswith(bstack1ll111l_opy_ (u"ࠨ࠰ࡳࡥࡨ࠭ॷ")) and os.path.isfile(proxy):
      bstack1lll111111_opy_[bstack1ll111l_opy_ (u"ࠩ࠰ࡴࡦࡩ࠭ࡧ࡫࡯ࡩࠬॸ")] = proxy
    else:
      parsed_url = None
      if proxy.endswith(bstack1ll111l_opy_ (u"ࠪ࠲ࡵࡧࡣࠨॹ")):
        proxies = bstack11ll11l1_opy_(config, bstack1lll1lll1_opy_())
        if len(proxies) > 0:
          protocol, bstack11ll1ll11_opy_ = proxies.popitem()
          if bstack1ll111l_opy_ (u"ࠦ࠿࠵࠯ࠣॺ") in bstack11ll1ll11_opy_:
            parsed_url = urlparse(bstack11ll1ll11_opy_)
          else:
            parsed_url = urlparse(protocol + bstack1ll111l_opy_ (u"ࠧࡀ࠯࠰ࠤॻ") + bstack11ll1ll11_opy_)
      else:
        parsed_url = urlparse(proxy)
      if parsed_url and parsed_url.hostname: bstack1lll111111_opy_[bstack1ll111l_opy_ (u"࠭ࡰࡳࡱࡻࡽࡍࡵࡳࡵࠩॼ")] = str(parsed_url.hostname)
      if parsed_url and parsed_url.port: bstack1lll111111_opy_[bstack1ll111l_opy_ (u"ࠧࡱࡴࡲࡼࡾࡖ࡯ࡳࡶࠪॽ")] = str(parsed_url.port)
      if parsed_url and parsed_url.username: bstack1lll111111_opy_[bstack1ll111l_opy_ (u"ࠨࡲࡵࡳࡽࡿࡕࡴࡧࡵࠫॾ")] = str(parsed_url.username)
      if parsed_url and parsed_url.password: bstack1lll111111_opy_[bstack1ll111l_opy_ (u"ࠩࡳࡶࡴࡾࡹࡑࡣࡶࡷࠬॿ")] = str(parsed_url.password)
  return bstack1lll111111_opy_
def bstack1ll111111_opy_(config):
  if bstack1ll111l_opy_ (u"ࠪࡸࡪࡹࡴࡄࡱࡱࡸࡪࡾࡴࡐࡲࡷ࡭ࡴࡴࡳࠨঀ") in config:
    return config[bstack1ll111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡅࡲࡲࡹ࡫ࡸࡵࡑࡳࡸ࡮ࡵ࡮ࡴࠩঁ")]
  return {}
def bstack11l1l1ll_opy_(caps):
  global bstack11lll1lll_opy_
  if bstack1ll111l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ং") in caps:
    caps[bstack1ll111l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧঃ")][bstack1ll111l_opy_ (u"ࠧ࡭ࡱࡦࡥࡱ࠭঄")] = True
    if bstack11lll1lll_opy_:
      caps[bstack1ll111l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩঅ")][bstack1ll111l_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫআ")] = bstack11lll1lll_opy_
  else:
    caps[bstack1ll111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳࡨࡧ࡬ࠨই")] = True
    if bstack11lll1lll_opy_:
      caps[bstack1ll111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬঈ")] = bstack11lll1lll_opy_
def bstack1ll1l111l_opy_():
  global CONFIG
  if bstack1ll111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩউ") in CONFIG and CONFIG[bstack1ll111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪঊ")]:
    bstack1lll111111_opy_ = bstack1ll11ll1l_opy_(CONFIG)
    bstack1lll11ll_opy_(CONFIG[bstack1ll111l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪঋ")], bstack1lll111111_opy_)
def bstack1lll11ll_opy_(key, bstack1lll111111_opy_):
  global bstack1l11ll1l_opy_
  logger.info(bstack1l1l1l1l_opy_)
  try:
    bstack1l11ll1l_opy_ = Local()
    bstack111lll1l1_opy_ = {bstack1ll111l_opy_ (u"ࠨ࡭ࡨࡽࠬঌ"): key}
    bstack111lll1l1_opy_.update(bstack1lll111111_opy_)
    logger.debug(bstack11llll11_opy_.format(str(bstack111lll1l1_opy_)))
    bstack1l11ll1l_opy_.start(**bstack111lll1l1_opy_)
    if bstack1l11ll1l_opy_.isRunning():
      logger.info(bstack1111l111l_opy_)
  except Exception as e:
    bstack1llllll11l_opy_(bstack1lllll111l_opy_.format(str(e)))
def bstack1lll11l1l_opy_():
  global bstack1l11ll1l_opy_
  if bstack1l11ll1l_opy_.isRunning():
    logger.info(bstack1l11lll11_opy_)
    bstack1l11ll1l_opy_.stop()
  bstack1l11ll1l_opy_ = None
def bstack1lll1ll111_opy_(bstack1ll11l1ll1_opy_=[]):
  global CONFIG
  bstack1lll1l1l11_opy_ = []
  bstack11ll1l11l_opy_ = [bstack1ll111l_opy_ (u"ࠩࡲࡷࠬ঍"), bstack1ll111l_opy_ (u"ࠪࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳ࠭঎"), bstack1ll111l_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨএ"), bstack1ll111l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠧঐ"), bstack1ll111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫ঑"), bstack1ll111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ঒")]
  try:
    for err in bstack1ll11l1ll1_opy_:
      bstack1l11llll1_opy_ = {}
      for k in bstack11ll1l11l_opy_:
        val = CONFIG[bstack1ll111l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫও")][int(err[bstack1ll111l_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨঔ")])].get(k)
        if val:
          bstack1l11llll1_opy_[k] = val
      bstack1l11llll1_opy_[bstack1ll111l_opy_ (u"ࠪࡸࡪࡹࡴࡴࠩক")] = {
        err[bstack1ll111l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩখ")]: err[bstack1ll111l_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫগ")]
      }
      bstack1lll1l1l11_opy_.append(bstack1l11llll1_opy_)
  except Exception as e:
    logger.debug(bstack1ll111l_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡨࡲࡶࡲࡧࡴࡵ࡫ࡱ࡫ࠥࡪࡡࡵࡣࠣࡪࡴࡸࠠࡦࡸࡨࡲࡹࡀࠠࠨঘ") + str(e))
  finally:
    return bstack1lll1l1l11_opy_
def bstack1l11l11l_opy_():
  global bstack1l1l11111_opy_
  global bstack1l11lllll_opy_
  global bstack11ll1111_opy_
  percy.shutdown()
  if bstack1l1l11111_opy_:
    logger.warning(bstack1l11lll1_opy_.format(str(bstack1l1l11111_opy_)))
  else:
    try:
      bstack11l1lllll_opy_ = bstack111l1ll1l_opy_(bstack1ll111l_opy_ (u"ࠧ࠯ࡤࡶࡸࡦࡩ࡫࠮ࡥࡲࡲ࡫࡯ࡧ࠯࡬ࡶࡳࡳ࠭ঙ"), logger)
      if bstack11l1lllll_opy_.get(bstack1ll111l_opy_ (u"ࠨࡰࡸࡨ࡬࡫࡟࡭ࡱࡦࡥࡱ࠭চ")) and bstack11l1lllll_opy_.get(bstack1ll111l_opy_ (u"ࠩࡱࡹࡩ࡭ࡥࡠ࡮ࡲࡧࡦࡲࠧছ")).get(bstack1ll111l_opy_ (u"ࠪ࡬ࡴࡹࡴ࡯ࡣࡰࡩࠬজ")):
        logger.warning(bstack1l11lll1_opy_.format(str(bstack11l1lllll_opy_[bstack1ll111l_opy_ (u"ࠫࡳࡻࡤࡨࡧࡢࡰࡴࡩࡡ࡭ࠩঝ")][bstack1ll111l_opy_ (u"ࠬ࡮࡯ࡴࡶࡱࡥࡲ࡫ࠧঞ")])))
    except Exception as e:
      logger.error(e)
  logger.info(bstack1ll1l1ll11_opy_)
  global bstack1l11ll1l_opy_
  if bstack1l11ll1l_opy_:
    bstack1lll11l1l_opy_()
  try:
    for driver in bstack1l11lllll_opy_:
      driver.quit()
  except Exception as e:
    pass
  logger.info(bstack1l1l11ll_opy_)
  bstack11ll1l1ll_opy_()
  if len(bstack11ll1111_opy_) > 0:
    message = bstack1lll1ll111_opy_(bstack11ll1111_opy_)
    bstack11ll1l1ll_opy_(message)
  else:
    bstack11ll1l1ll_opy_()
  bstack11111lll1_opy_(bstack1111l1l1_opy_, logger)
def bstack1ll1111l1_opy_(self, *args):
  logger.error(bstack1ll1l11l11_opy_)
  bstack1l11l11l_opy_()
  sys.exit(1)
def bstack1llllll11l_opy_(err):
  logger.critical(bstack111l1l111_opy_.format(str(err)))
  bstack11ll1l1ll_opy_(bstack111l1l111_opy_.format(str(err)))
  atexit.unregister(bstack1l11l11l_opy_)
  sys.exit(1)
def bstack1l1lll1l1_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack11ll1l1ll_opy_(message)
  atexit.unregister(bstack1l11l11l_opy_)
  sys.exit(1)
def bstack1111l11l1_opy_():
  global CONFIG
  global bstack1ll1ll1l1_opy_
  global bstack1lllll1l11_opy_
  global bstack1ll1llllll_opy_
  CONFIG = bstack1ll11l1l11_opy_()
  bstack1l1111l11_opy_()
  bstack111l11l1l_opy_()
  CONFIG = bstack11l11l11l_opy_(CONFIG)
  update(CONFIG, bstack1lllll1l11_opy_)
  update(CONFIG, bstack1ll1ll1l1_opy_)
  CONFIG = bstack1111ll1ll_opy_(CONFIG)
  bstack1ll1llllll_opy_ = bstack111llllll_opy_(CONFIG)
  bstack1ll1ll111_opy_.bstack1ll11ll1ll_opy_(bstack1ll111l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧট"), bstack1ll1llllll_opy_)
  if (bstack1ll111l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪঠ") in CONFIG and bstack1ll111l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫড") in bstack1ll1ll1l1_opy_) or (
          bstack1ll111l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬঢ") in CONFIG and bstack1ll111l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ণ") not in bstack1lllll1l11_opy_):
    if os.getenv(bstack1ll111l_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡣࡈࡕࡍࡃࡋࡑࡉࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠨত")):
      CONFIG[bstack1ll111l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧথ")] = os.getenv(bstack1ll111l_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡥࡃࡐࡏࡅࡍࡓࡋࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠪদ"))
    else:
      bstack111ll1111_opy_()
  elif (bstack1ll111l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪধ") not in CONFIG and bstack1ll111l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪন") in CONFIG) or (
          bstack1ll111l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ঩") in bstack1lllll1l11_opy_ and bstack1ll111l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭প") not in bstack1ll1ll1l1_opy_):
    del (CONFIG[bstack1ll111l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ফ")])
  if bstack111l11lll_opy_(CONFIG):
    bstack1llllll11l_opy_(bstack1l1ll111_opy_)
  bstack111l11111_opy_()
  bstack1l11l1ll_opy_()
  if bstack1lll11l1l1_opy_:
    CONFIG[bstack1ll111l_opy_ (u"ࠬࡧࡰࡱࠩব")] = bstack1111l1111_opy_(CONFIG)
    logger.info(bstack111ll1ll_opy_.format(CONFIG[bstack1ll111l_opy_ (u"࠭ࡡࡱࡲࠪভ")]))
def bstack1l1l1lll_opy_(config, bstack11111111_opy_):
  global CONFIG
  global bstack1lll11l1l1_opy_
  CONFIG = config
  bstack1lll11l1l1_opy_ = bstack11111111_opy_
def bstack1l11l1ll_opy_():
  global CONFIG
  global bstack1lll11l1l1_opy_
  if bstack1ll111l_opy_ (u"ࠧࡢࡲࡳࠫম") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack1l1lll1l1_opy_(e, bstack11lll1l1l_opy_)
    bstack1lll11l1l1_opy_ = True
    bstack1ll1ll111_opy_.bstack1ll11ll1ll_opy_(bstack1ll111l_opy_ (u"ࠨࡣࡳࡴࡤࡧࡵࡵࡱࡰࡥࡹ࡫ࠧয"), True)
def bstack1111l1111_opy_(config):
  bstack1l1l111l1_opy_ = bstack1ll111l_opy_ (u"ࠩࠪর")
  app = config[bstack1ll111l_opy_ (u"ࠪࡥࡵࡶࠧ঱")]
  if isinstance(app, str):
    if os.path.splitext(app)[1] in bstack1111llll1_opy_:
      if os.path.exists(app):
        bstack1l1l111l1_opy_ = bstack1111l1lll_opy_(config, app)
      elif bstack1ll1l1ll1l_opy_(app):
        bstack1l1l111l1_opy_ = app
      else:
        bstack1llllll11l_opy_(bstack1llll1llll_opy_.format(app))
    else:
      if bstack1ll1l1ll1l_opy_(app):
        bstack1l1l111l1_opy_ = app
      elif os.path.exists(app):
        bstack1l1l111l1_opy_ = bstack1111l1lll_opy_(app)
      else:
        bstack1llllll11l_opy_(bstack1llll111l1_opy_)
  else:
    if len(app) > 2:
      bstack1llllll11l_opy_(bstack1ll1l111l1_opy_)
    elif len(app) == 2:
      if bstack1ll111l_opy_ (u"ࠫࡵࡧࡴࡩࠩল") in app and bstack1ll111l_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡤ࡯ࡤࠨ঳") in app:
        if os.path.exists(app[bstack1ll111l_opy_ (u"࠭ࡰࡢࡶ࡫ࠫ঴")]):
          bstack1l1l111l1_opy_ = bstack1111l1lll_opy_(config, app[bstack1ll111l_opy_ (u"ࠧࡱࡣࡷ࡬ࠬ঵")], app[bstack1ll111l_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡠ࡫ࡧࠫশ")])
        else:
          bstack1llllll11l_opy_(bstack1llll1llll_opy_.format(app))
      else:
        bstack1llllll11l_opy_(bstack1ll1l111l1_opy_)
    else:
      for key in app:
        if key in bstack1111111l_opy_:
          if key == bstack1ll111l_opy_ (u"ࠩࡳࡥࡹ࡮ࠧষ"):
            if os.path.exists(app[key]):
              bstack1l1l111l1_opy_ = bstack1111l1lll_opy_(config, app[key])
            else:
              bstack1llllll11l_opy_(bstack1llll1llll_opy_.format(app))
          else:
            bstack1l1l111l1_opy_ = app[key]
        else:
          bstack1llllll11l_opy_(bstack1l1l1llll_opy_)
  return bstack1l1l111l1_opy_
def bstack1ll1l1ll1l_opy_(bstack1l1l111l1_opy_):
  import re
  bstack1ll11ll1_opy_ = re.compile(bstack1ll111l_opy_ (u"ࡵࠦࡣࡡࡡ࠮ࡼࡄ࠱࡟࠶࠭࠺࡞ࡢ࠲ࡡ࠳࡝ࠫࠦࠥস"))
  bstack1ll1lll11l_opy_ = re.compile(bstack1ll111l_opy_ (u"ࡶࠧࡤ࡛ࡢ࠯ࡽࡅ࠲ࡠ࠰࠮࠻࡟ࡣ࠳ࡢ࠭࡞ࠬ࠲࡟ࡦ࠳ࡺࡂ࠯࡝࠴࠲࠿࡜ࡠ࠰࡟࠱ࡢ࠰ࠤࠣহ"))
  if bstack1ll111l_opy_ (u"ࠬࡨࡳ࠻࠱࠲ࠫ঺") in bstack1l1l111l1_opy_ or re.fullmatch(bstack1ll11ll1_opy_, bstack1l1l111l1_opy_) or re.fullmatch(bstack1ll1lll11l_opy_, bstack1l1l111l1_opy_):
    return True
  else:
    return False
def bstack1111l1lll_opy_(config, path, bstack1l11l111l_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstack1ll111l_opy_ (u"࠭ࡲࡣࠩ঻")).read()).hexdigest()
  bstack1l1l11ll1_opy_ = bstack1111llll_opy_(md5_hash)
  bstack1l1l111l1_opy_ = None
  if bstack1l1l11ll1_opy_:
    logger.info(bstack1lll1l1ll_opy_.format(bstack1l1l11ll1_opy_, md5_hash))
    return bstack1l1l11ll1_opy_
  bstack1lll1l1l1l_opy_ = MultipartEncoder(
    fields={
      bstack1ll111l_opy_ (u"ࠧࡧ࡫࡯ࡩ়ࠬ"): (os.path.basename(path), open(os.path.abspath(path), bstack1ll111l_opy_ (u"ࠨࡴࡥࠫঽ")), bstack1ll111l_opy_ (u"ࠩࡷࡩࡽࡺ࠯ࡱ࡮ࡤ࡭ࡳ࠭া")),
      bstack1ll111l_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡢ࡭ࡩ࠭ি"): bstack1l11l111l_opy_
    }
  )
  response = requests.post(bstack1l11lll1l_opy_, data=bstack1lll1l1l1l_opy_,
                           headers={bstack1ll111l_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪী"): bstack1lll1l1l1l_opy_.content_type},
                           auth=(config[bstack1ll111l_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧু")], config[bstack1ll111l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩূ")]))
  try:
    res = json.loads(response.text)
    bstack1l1l111l1_opy_ = res[bstack1ll111l_opy_ (u"ࠧࡢࡲࡳࡣࡺࡸ࡬ࠨৃ")]
    logger.info(bstack1lll11lll1_opy_.format(bstack1l1l111l1_opy_))
    bstack1lllllll1l_opy_(md5_hash, bstack1l1l111l1_opy_)
  except ValueError as err:
    bstack1llllll11l_opy_(bstack1lll1llll1_opy_.format(str(err)))
  return bstack1l1l111l1_opy_
def bstack111l11111_opy_():
  global CONFIG
  global bstack1lll1ll11_opy_
  bstack1lll11l1_opy_ = 0
  bstack1l1ll111l_opy_ = 1
  if bstack1ll111l_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨৄ") in CONFIG:
    bstack1l1ll111l_opy_ = CONFIG[bstack1ll111l_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ৅")]
  if bstack1ll111l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭৆") in CONFIG:
    bstack1lll11l1_opy_ = len(CONFIG[bstack1ll111l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧে")])
  bstack1lll1ll11_opy_ = int(bstack1l1ll111l_opy_) * int(bstack1lll11l1_opy_)
def bstack1111llll_opy_(md5_hash):
  bstack1lll1ll1l_opy_ = os.path.join(os.path.expanduser(bstack1ll111l_opy_ (u"ࠬࢄࠧৈ")), bstack1ll111l_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭৉"), bstack1ll111l_opy_ (u"ࠧࡢࡲࡳ࡙ࡵࡲ࡯ࡢࡦࡐࡈ࠺ࡎࡡࡴࡪ࠱࡮ࡸࡵ࡮ࠨ৊"))
  if os.path.exists(bstack1lll1ll1l_opy_):
    bstack11l1l11ll_opy_ = json.load(open(bstack1lll1ll1l_opy_, bstack1ll111l_opy_ (u"ࠨࡴࡥࠫো")))
    if md5_hash in bstack11l1l11ll_opy_:
      bstack11l111ll_opy_ = bstack11l1l11ll_opy_[md5_hash]
      bstack1ll1lll1l1_opy_ = datetime.datetime.now()
      bstack1111lllll_opy_ = datetime.datetime.strptime(bstack11l111ll_opy_[bstack1ll111l_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬৌ")], bstack1ll111l_opy_ (u"ࠪࠩࡩ࠵ࠥ࡮࠱ࠨ࡝ࠥࠫࡈ࠻ࠧࡐ࠾্࡙ࠪࠧ"))
      if (bstack1ll1lll1l1_opy_ - bstack1111lllll_opy_).days > 60:
        return None
      elif version.parse(str(__version__)) > version.parse(bstack11l111ll_opy_[bstack1ll111l_opy_ (u"ࠫࡸࡪ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩৎ")]):
        return None
      return bstack11l111ll_opy_[bstack1ll111l_opy_ (u"ࠬ࡯ࡤࠨ৏")]
  else:
    return None
def bstack1lllllll1l_opy_(md5_hash, bstack1l1l111l1_opy_):
  bstack1ll1ll11ll_opy_ = os.path.join(os.path.expanduser(bstack1ll111l_opy_ (u"࠭ࡾࠨ৐")), bstack1ll111l_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ৑"))
  if not os.path.exists(bstack1ll1ll11ll_opy_):
    os.makedirs(bstack1ll1ll11ll_opy_)
  bstack1lll1ll1l_opy_ = os.path.join(os.path.expanduser(bstack1ll111l_opy_ (u"ࠨࢀࠪ৒")), bstack1ll111l_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩ৓"), bstack1ll111l_opy_ (u"ࠪࡥࡵࡶࡕࡱ࡮ࡲࡥࡩࡓࡄ࠶ࡊࡤࡷ࡭࠴ࡪࡴࡱࡱࠫ৔"))
  bstack1ll11l1l1l_opy_ = {
    bstack1ll111l_opy_ (u"ࠫ࡮ࡪࠧ৕"): bstack1l1l111l1_opy_,
    bstack1ll111l_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨ৖"): datetime.datetime.strftime(datetime.datetime.now(), bstack1ll111l_opy_ (u"࠭ࠥࡥ࠱ࠨࡱ࠴࡙ࠫࠡࠧࡋ࠾ࠪࡓ࠺ࠦࡕࠪৗ")),
    bstack1ll111l_opy_ (u"ࠧࡴࡦ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ৘"): str(__version__)
  }
  if os.path.exists(bstack1lll1ll1l_opy_):
    bstack11l1l11ll_opy_ = json.load(open(bstack1lll1ll1l_opy_, bstack1ll111l_opy_ (u"ࠨࡴࡥࠫ৙")))
  else:
    bstack11l1l11ll_opy_ = {}
  bstack11l1l11ll_opy_[md5_hash] = bstack1ll11l1l1l_opy_
  with open(bstack1lll1ll1l_opy_, bstack1ll111l_opy_ (u"ࠤࡺ࠯ࠧ৚")) as outfile:
    json.dump(bstack11l1l11ll_opy_, outfile)
def bstack1ll11llll1_opy_(self):
  return
def bstack111111l1l_opy_(self):
  return
def bstack111llll1_opy_(self):
  from selenium.webdriver.remote.webdriver import WebDriver
  WebDriver.quit(self)
def bstack1111ll11_opy_(self):
  global bstack1l1ll1lll_opy_
  global bstack1ll1l1l111_opy_
  global bstack1ll11lll_opy_
  try:
    if bstack1ll111l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ৛") in bstack1l1ll1lll_opy_ and self.session_id != None and bstack1lll1111_opy_(threading.current_thread(), bstack1ll111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡕࡷࡥࡹࡻࡳࠨড়"), bstack1ll111l_opy_ (u"ࠬ࠭ঢ়")) != bstack1ll111l_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧ৞"):
      bstack1l11l11ll_opy_ = bstack1ll111l_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧয়") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack1ll111l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨৠ")
      bstack1llll111l_opy_ = bstack1l11ll1l1_opy_(bstack1ll111l_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠬৡ"), bstack1ll111l_opy_ (u"ࠪࠫৢ"), bstack1l11l11ll_opy_, bstack1ll111l_opy_ (u"ࠫ࠱ࠦࠧৣ").join(
        threading.current_thread().bstackTestErrorMessages), bstack1ll111l_opy_ (u"ࠬ࠭৤"), bstack1ll111l_opy_ (u"࠭ࠧ৥"))
      if self != None:
        self.execute_script(bstack1llll111l_opy_)
  except Exception as e:
    logger.debug(bstack1ll111l_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡳࡡࡳ࡭࡬ࡲ࡬ࠦࡳࡵࡣࡷࡹࡸࡀࠠࠣ০") + str(e))
  bstack1ll11lll_opy_(self)
  self.session_id = None
def bstack1lll11111l_opy_(self, *args, **kwargs):
  bstack1111111l1_opy_ = bstack11l1l1ll1_opy_(self, *args, **kwargs)
  bstack11llllll1_opy_.bstack1l111ll1l_opy_(self)
  return bstack1111111l1_opy_
def bstack11l111ll1_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
  global CONFIG
  global bstack1ll1l1l111_opy_
  global bstack1llllll111_opy_
  global bstack1ll11ll111_opy_
  global bstack11l1111l_opy_
  global bstack11l11ll1l_opy_
  global bstack1l1ll1lll_opy_
  global bstack11l1l1ll1_opy_
  global bstack1l11lllll_opy_
  global bstack11l1ll1l1_opy_
  CONFIG[bstack1ll111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪ১")] = str(bstack1l1ll1lll_opy_) + str(__version__)
  command_executor = bstack1lll1lll1_opy_()
  logger.debug(bstack1l111llll_opy_.format(command_executor))
  proxy = bstack1l1lll1ll_opy_(CONFIG, proxy)
  bstack11lll1ll1_opy_ = 0 if bstack1llllll111_opy_ < 0 else bstack1llllll111_opy_
  try:
    if bstack11l1111l_opy_ is True:
      bstack11lll1ll1_opy_ = int(multiprocessing.current_process().name)
    elif bstack11l11ll1l_opy_ is True:
      bstack11lll1ll1_opy_ = int(threading.current_thread().name)
  except:
    bstack11lll1ll1_opy_ = 0
  bstack1lllll1l1l_opy_ = bstack1ll1l11111_opy_(CONFIG, bstack11lll1ll1_opy_)
  logger.debug(bstack1llllll1ll_opy_.format(str(bstack1lllll1l1l_opy_)))
  if bstack1ll111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭২") in CONFIG and CONFIG[bstack1ll111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ৩")]:
    bstack11l1l1ll_opy_(bstack1lllll1l1l_opy_)
  if desired_capabilities:
    bstack11llll11l_opy_ = bstack11l11l11l_opy_(desired_capabilities)
    bstack11llll11l_opy_[bstack1ll111l_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫ৪")] = bstack1111l11l_opy_(CONFIG)
    bstack11lll11l_opy_ = bstack1ll1l11111_opy_(bstack11llll11l_opy_)
    if bstack11lll11l_opy_:
      bstack1lllll1l1l_opy_ = update(bstack11lll11l_opy_, bstack1lllll1l1l_opy_)
    desired_capabilities = None
  if options:
    bstack1l1ll1ll_opy_(options, bstack1lllll1l1l_opy_)
  if not options:
    options = bstack11l11l1l1_opy_(bstack1lllll1l1l_opy_)
  if proxy and bstack1l1111lll_opy_() >= version.parse(bstack1ll111l_opy_ (u"ࠬ࠺࠮࠲࠲࠱࠴ࠬ৫")):
    options.proxy(proxy)
  if options and bstack1l1111lll_opy_() >= version.parse(bstack1ll111l_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬ৬")):
    desired_capabilities = None
  if (
          not options and not desired_capabilities
  ) or (
          bstack1l1111lll_opy_() < version.parse(bstack1ll111l_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭৭")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack1lllll1l1l_opy_)
  logger.info(bstack11l1lll1l_opy_)
  if bstack1l1111lll_opy_() >= version.parse(bstack1ll111l_opy_ (u"ࠨ࠶࠱࠵࠵࠴࠰ࠨ৮")):
    bstack11l1l1ll1_opy_(self, command_executor=command_executor,
              options=options, keep_alive=keep_alive, file_detector=file_detector)
  elif bstack1l1111lll_opy_() >= version.parse(bstack1ll111l_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨ৯")):
    bstack11l1l1ll1_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities, options=options,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  elif bstack1l1111lll_opy_() >= version.parse(bstack1ll111l_opy_ (u"ࠪ࠶࠳࠻࠳࠯࠲ࠪৰ")):
    bstack11l1l1ll1_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  else:
    bstack11l1l1ll1_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive)
  try:
    bstack111l1l1l_opy_ = bstack1ll111l_opy_ (u"ࠫࠬৱ")
    if bstack1l1111lll_opy_() >= version.parse(bstack1ll111l_opy_ (u"ࠬ࠺࠮࠱࠰࠳ࡦ࠶࠭৲")):
      bstack111l1l1l_opy_ = self.caps.get(bstack1ll111l_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡱࡦࡲࡈࡶࡤࡘࡶࡱࠨ৳"))
    else:
      bstack111l1l1l_opy_ = self.capabilities.get(bstack1ll111l_opy_ (u"ࠢࡰࡲࡷ࡭ࡲࡧ࡬ࡉࡷࡥ࡙ࡷࡲࠢ৴"))
    if bstack111l1l1l_opy_:
      if bstack1l1111lll_opy_() <= version.parse(bstack1ll111l_opy_ (u"ࠨ࠵࠱࠵࠸࠴࠰ࠨ৵")):
        self.command_executor._url = bstack1ll111l_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥ৶") + bstack1llll11l_opy_ + bstack1ll111l_opy_ (u"ࠥ࠾࠽࠶࠯ࡸࡦ࠲࡬ࡺࡨࠢ৷")
      else:
        self.command_executor._url = bstack1ll111l_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࠨ৸") + bstack111l1l1l_opy_ + bstack1ll111l_opy_ (u"ࠧ࠵ࡷࡥ࠱࡫ࡹࡧࠨ৹")
      logger.debug(bstack11l1ll1ll_opy_.format(bstack111l1l1l_opy_))
    else:
      logger.debug(bstack111l1111_opy_.format(bstack1ll111l_opy_ (u"ࠨࡏࡱࡶ࡬ࡱࡦࡲࠠࡉࡷࡥࠤࡳࡵࡴࠡࡨࡲࡹࡳࡪࠢ৺")))
  except Exception as e:
    logger.debug(bstack111l1111_opy_.format(e))
  if bstack1ll111l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭৻") in bstack1l1ll1lll_opy_:
    bstack1lll11l11l_opy_(bstack1llllll111_opy_, bstack11l1ll1l1_opy_)
  bstack1ll1l1l111_opy_ = self.session_id
  if bstack1ll111l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨৼ") in bstack1l1ll1lll_opy_ or bstack1ll111l_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩ৽") in bstack1l1ll1lll_opy_:
    threading.current_thread().bstack11llll111_opy_ = self.session_id
    threading.current_thread().bstackSessionDriver = self
    threading.current_thread().bstackTestErrorMessages = []
    bstack11llllll1_opy_.bstack1l111ll1l_opy_(self)
  bstack1l11lllll_opy_.append(self)
  if bstack1ll111l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭৾") in CONFIG and bstack1ll111l_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ৿") in CONFIG[bstack1ll111l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ਀")][bstack11lll1ll1_opy_]:
    bstack1ll11ll111_opy_ = CONFIG[bstack1ll111l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩਁ")][bstack11lll1ll1_opy_][bstack1ll111l_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬਂ")]
  logger.debug(bstack1l1l1111_opy_.format(bstack1ll1l1l111_opy_))
try:
  try:
    import Browser
    from subprocess import Popen
    def bstack1ll1llll11_opy_(self, args, bufsize=-1, executable=None,
              stdin=None, stdout=None, stderr=None,
              preexec_fn=None, close_fds=True,
              shell=False, cwd=None, env=None, universal_newlines=None,
              startupinfo=None, creationflags=0,
              restore_signals=True, start_new_session=False,
              pass_fds=(), *, user=None, group=None, extra_groups=None,
              encoding=None, errors=None, text=None, umask=-1, pipesize=-1):
      global CONFIG
      global bstack11lll1ll_opy_
      if(bstack1ll111l_opy_ (u"ࠣ࡫ࡱࡨࡪࡾ࠮࡫ࡵࠥਃ") in args[1]):
        with open(os.path.join(os.path.expanduser(bstack1ll111l_opy_ (u"ࠩࢁࠫ਄")), bstack1ll111l_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪਅ"), bstack1ll111l_opy_ (u"ࠫ࠳ࡹࡥࡴࡵ࡬ࡳࡳ࡯ࡤࡴ࠰ࡷࡼࡹ࠭ਆ")), bstack1ll111l_opy_ (u"ࠬࡽࠧਇ")) as fp:
          fp.write(bstack1ll111l_opy_ (u"ࠨࠢਈ"))
        if(not os.path.exists(os.path.join(os.path.dirname(args[1]), bstack1ll111l_opy_ (u"ࠢࡪࡰࡧࡩࡽࡥࡢࡴࡶࡤࡧࡰ࠴ࡪࡴࠤਉ")))):
          with open(args[1], bstack1ll111l_opy_ (u"ࠨࡴࠪਊ")) as f:
            lines = f.readlines()
            index = next((i for i, line in enumerate(lines) if bstack1ll111l_opy_ (u"ࠩࡤࡷࡾࡴࡣࠡࡨࡸࡲࡨࡺࡩࡰࡰࠣࡣࡳ࡫ࡷࡑࡣࡪࡩ࠭ࡩ࡯࡯ࡶࡨࡼࡹ࠲ࠠࡱࡣࡪࡩࠥࡃࠠࡷࡱ࡬ࡨࠥ࠶ࠩࠨ਋") in line), None)
            if index is not None:
                lines.insert(index+2, bstack111111l11_opy_)
            lines.insert(1, bstack11llll1l_opy_)
            f.seek(0)
            with open(os.path.join(os.path.dirname(args[1]), bstack1ll111l_opy_ (u"ࠥ࡭ࡳࡪࡥࡹࡡࡥࡷࡹࡧࡣ࡬࠰࡭ࡷࠧ਌")), bstack1ll111l_opy_ (u"ࠫࡼ࠭਍")) as bstack111llll1l_opy_:
              bstack111llll1l_opy_.writelines(lines)
        CONFIG[bstack1ll111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧ਎")] = str(bstack1l1ll1lll_opy_) + str(__version__)
        bstack11lll1ll1_opy_ = 0 if bstack1llllll111_opy_ < 0 else bstack1llllll111_opy_
        try:
          if bstack11l1111l_opy_ is True:
            bstack11lll1ll1_opy_ = int(multiprocessing.current_process().name)
          elif bstack11l11ll1l_opy_ is True:
            bstack11lll1ll1_opy_ = int(threading.current_thread().name)
        except:
          bstack11lll1ll1_opy_ = 0
        CONFIG[bstack1ll111l_opy_ (u"ࠨࡵࡴࡧ࡚࠷ࡈࠨਏ")] = False
        CONFIG[bstack1ll111l_opy_ (u"ࠢࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨਐ")] = True
        bstack1lllll1l1l_opy_ = bstack1ll1l11111_opy_(CONFIG, bstack11lll1ll1_opy_)
        logger.debug(bstack1llllll1ll_opy_.format(str(bstack1lllll1l1l_opy_)))
        if CONFIG.get(bstack1ll111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬ਑")):
          bstack11l1l1ll_opy_(bstack1lllll1l1l_opy_)
        if bstack1ll111l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ਒") in CONFIG and bstack1ll111l_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨਓ") in CONFIG[bstack1ll111l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧਔ")][bstack11lll1ll1_opy_]:
          bstack1ll11ll111_opy_ = CONFIG[bstack1ll111l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨਕ")][bstack11lll1ll1_opy_][bstack1ll111l_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫਖ")]
        args.append(os.path.join(os.path.expanduser(bstack1ll111l_opy_ (u"ࠧࡿࠩਗ")), bstack1ll111l_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨਘ"), bstack1ll111l_opy_ (u"ࠩ࠱ࡷࡪࡹࡳࡪࡱࡱ࡭ࡩࡹ࠮ࡵࡺࡷࠫਙ")))
        args.append(str(threading.get_ident()))
        args.append(json.dumps(bstack1lllll1l1l_opy_))
        args[1] = os.path.join(os.path.dirname(args[1]), bstack1ll111l_opy_ (u"ࠥ࡭ࡳࡪࡥࡹࡡࡥࡷࡹࡧࡣ࡬࠰࡭ࡷࠧਚ"))
      bstack11lll1ll_opy_ = True
      return bstack1ll1ll11l_opy_(self, args, bufsize=bufsize, executable=executable,
                    stdin=stdin, stdout=stdout, stderr=stderr,
                    preexec_fn=preexec_fn, close_fds=close_fds,
                    shell=shell, cwd=cwd, env=env, universal_newlines=universal_newlines,
                    startupinfo=startupinfo, creationflags=creationflags,
                    restore_signals=restore_signals, start_new_session=start_new_session,
                    pass_fds=pass_fds, user=user, group=group, extra_groups=extra_groups,
                    encoding=encoding, errors=errors, text=text, umask=umask, pipesize=pipesize)
  except Exception as e:
    pass
  import playwright._impl._api_structures
  import playwright._impl._helper
  def bstack1l111l1l_opy_(self,
        executablePath = None,
        channel = None,
        args = None,
        ignoreDefaultArgs = None,
        handleSIGINT = None,
        handleSIGTERM = None,
        handleSIGHUP = None,
        timeout = None,
        env = None,
        headless = None,
        devtools = None,
        proxy = None,
        downloadsPath = None,
        slowMo = None,
        tracesDir = None,
        chromiumSandbox = None,
        firefoxUserPrefs = None
        ):
    global CONFIG
    global bstack1llllll111_opy_
    global bstack1ll11ll111_opy_
    global bstack11l1111l_opy_
    global bstack11l11ll1l_opy_
    global bstack1l1ll1lll_opy_
    CONFIG[bstack1ll111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭ਛ")] = str(bstack1l1ll1lll_opy_) + str(__version__)
    bstack11lll1ll1_opy_ = 0 if bstack1llllll111_opy_ < 0 else bstack1llllll111_opy_
    try:
      if bstack11l1111l_opy_ is True:
        bstack11lll1ll1_opy_ = int(multiprocessing.current_process().name)
      elif bstack11l11ll1l_opy_ is True:
        bstack11lll1ll1_opy_ = int(threading.current_thread().name)
    except:
      bstack11lll1ll1_opy_ = 0
    CONFIG[bstack1ll111l_opy_ (u"ࠧ࡯ࡳࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦਜ")] = True
    bstack1lllll1l1l_opy_ = bstack1ll1l11111_opy_(CONFIG, bstack11lll1ll1_opy_)
    logger.debug(bstack1llllll1ll_opy_.format(str(bstack1lllll1l1l_opy_)))
    if CONFIG.get(bstack1ll111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪਝ")):
      bstack11l1l1ll_opy_(bstack1lllll1l1l_opy_)
    if bstack1ll111l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪਞ") in CONFIG and bstack1ll111l_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ਟ") in CONFIG[bstack1ll111l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬਠ")][bstack11lll1ll1_opy_]:
      bstack1ll11ll111_opy_ = CONFIG[bstack1ll111l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ਡ")][bstack11lll1ll1_opy_][bstack1ll111l_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩਢ")]
    import urllib
    import json
    bstack1lll11111_opy_ = bstack1ll111l_opy_ (u"ࠬࡽࡳࡴ࠼࠲࠳ࡨࡪࡰ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡀࡥࡤࡴࡸࡃࠧਣ") + urllib.parse.quote(json.dumps(bstack1lllll1l1l_opy_))
    browser = self.connect(bstack1lll11111_opy_)
    return browser
except Exception as e:
    pass
def bstack111l1l1l1_opy_():
    global bstack11lll1ll_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        BrowserType.launch = bstack1l111l1l_opy_
        bstack11lll1ll_opy_ = True
    except Exception as e:
        pass
    try:
      import Browser
      from subprocess import Popen
      Popen.__init__ = bstack1ll1llll11_opy_
      bstack11lll1ll_opy_ = True
    except Exception as e:
      pass
def bstack11l1lll1_opy_(context, bstack1l1l11l1_opy_):
  try:
    context.page.evaluate(bstack1ll111l_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢਤ"), bstack1ll111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡳࡧ࡭ࡦࠤ࠽ࠫਥ")+ json.dumps(bstack1l1l11l1_opy_) + bstack1ll111l_opy_ (u"ࠣࡿࢀࠦਦ"))
  except Exception as e:
    logger.debug(bstack1ll111l_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨࠤࢀࢃࠢਧ"), e)
def bstack1ll1ll1l1l_opy_(context, message, level):
  try:
    context.page.evaluate(bstack1ll111l_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦਨ"), bstack1ll111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩ਩") + json.dumps(message) + bstack1ll111l_opy_ (u"ࠬ࠲ࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠨਪ") + json.dumps(level) + bstack1ll111l_opy_ (u"࠭ࡽࡾࠩਫ"))
  except Exception as e:
    logger.debug(bstack1ll111l_opy_ (u"ࠢࡦࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡥࡳࡴ࡯ࡵࡣࡷ࡭ࡴࡴࠠࡼࡿࠥਬ"), e)
def bstack1l1l1l11_opy_(context, status, message = bstack1ll111l_opy_ (u"ࠣࠤਭ")):
  try:
    if(status == bstack1ll111l_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤਮ")):
      context.page.evaluate(bstack1ll111l_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦਯ"), bstack1ll111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡶࡪࡧࡳࡰࡰࠥ࠾ࠬਰ") + json.dumps(bstack1ll111l_opy_ (u"࡙ࠧࡣࡦࡰࡤࡶ࡮ࡵࠠࡧࡣ࡬ࡰࡪࡪࠠࡸ࡫ࡷ࡬࠿ࠦࠢ਱") + str(message)) + bstack1ll111l_opy_ (u"࠭ࠬࠣࡵࡷࡥࡹࡻࡳࠣ࠼ࠪਲ") + json.dumps(status) + bstack1ll111l_opy_ (u"ࠢࡾࡿࠥਲ਼"))
    else:
      context.page.evaluate(bstack1ll111l_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤ਴"), bstack1ll111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡵࡷࡥࡹࡻࡳࠣ࠼ࠪਵ") + json.dumps(status) + bstack1ll111l_opy_ (u"ࠥࢁࢂࠨਸ਼"))
  except Exception as e:
    logger.debug(bstack1ll111l_opy_ (u"ࠦࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡴࡧࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡹࡴࡢࡶࡸࡷࠥࢁࡽࠣ਷"), e)
def bstack1lllll1l1_opy_(self, url):
  global bstack11l1l11l1_opy_
  try:
    bstack1lllll111_opy_(url)
  except Exception as err:
    logger.debug(bstack111ll1l1l_opy_.format(str(err)))
  try:
    bstack11l1l11l1_opy_(self, url)
  except Exception as e:
    try:
      bstack1l1ll11ll_opy_ = str(e)
      if any(err_msg in bstack1l1ll11ll_opy_ for err_msg in bstack1l1111l1l_opy_):
        bstack1lllll111_opy_(url, True)
    except Exception as err:
      logger.debug(bstack111ll1l1l_opy_.format(str(err)))
    raise e
def bstack1lll1l1111_opy_(self):
  global bstack1ll1l1l11l_opy_
  bstack1ll1l1l11l_opy_ = self
  return
def bstack1ll1l11l1l_opy_(self):
  global bstack11ll1ll1_opy_
  bstack11ll1ll1_opy_ = self
  return
def bstack11l11lll1_opy_(self, test):
  global CONFIG
  global bstack11ll1ll1_opy_
  global bstack1ll1l1l11l_opy_
  global bstack1ll1l1l111_opy_
  global bstack1l1ll11l1_opy_
  global bstack1ll11ll111_opy_
  global bstack1ll111l1_opy_
  global bstack1llll1111l_opy_
  global bstack111lllll1_opy_
  global bstack1l11lllll_opy_
  try:
    if not bstack1ll1l1l111_opy_:
      with open(os.path.join(os.path.expanduser(bstack1ll111l_opy_ (u"ࠬࢄࠧਸ")), bstack1ll111l_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ਹ"), bstack1ll111l_opy_ (u"ࠧ࠯ࡵࡨࡷࡸ࡯࡯࡯࡫ࡧࡷ࠳ࡺࡸࡵࠩ਺"))) as f:
        bstack1llll1lll1_opy_ = json.loads(bstack1ll111l_opy_ (u"ࠣࡽࠥ਻") + f.read().strip() + bstack1ll111l_opy_ (u"ࠩࠥࡼࠧࡀࠠࠣࡻ਼ࠥࠫ") + bstack1ll111l_opy_ (u"ࠥࢁࠧ਽"))
        bstack1ll1l1l111_opy_ = bstack1llll1lll1_opy_[str(threading.get_ident())]
  except:
    pass
  if bstack1l11lllll_opy_:
    for driver in bstack1l11lllll_opy_:
      if bstack1ll1l1l111_opy_ == driver.session_id:
        if test:
          bstack1111l111_opy_ = str(test.data)
        if not bstack11l1111l1_opy_ and bstack1111l111_opy_:
          bstack1ll111ll1_opy_ = {
            bstack1ll111l_opy_ (u"ࠫࡦࡩࡴࡪࡱࡱࠫਾ"): bstack1ll111l_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ਿ"),
            bstack1ll111l_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩੀ"): {
              bstack1ll111l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬੁ"): bstack1111l111_opy_
            }
          }
          bstack11l111l1l_opy_ = bstack1ll111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂ࠭ੂ").format(json.dumps(bstack1ll111ll1_opy_))
          driver.execute_script(bstack11l111l1l_opy_)
        if bstack1l1ll11l1_opy_:
          bstack1l1ll1111_opy_ = {
            bstack1ll111l_opy_ (u"ࠩࡤࡧࡹ࡯࡯࡯ࠩ੃"): bstack1ll111l_opy_ (u"ࠪࡥࡳࡴ࡯ࡵࡣࡷࡩࠬ੄"),
            bstack1ll111l_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧ੅"): {
              bstack1ll111l_opy_ (u"ࠬࡪࡡࡵࡣࠪ੆"): bstack1111l111_opy_ + bstack1ll111l_opy_ (u"࠭ࠠࡱࡣࡶࡷࡪࡪࠡࠨੇ"),
              bstack1ll111l_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ੈ"): bstack1ll111l_opy_ (u"ࠨ࡫ࡱࡪࡴ࠭੉")
            }
          }
          bstack1ll111ll1_opy_ = {
            bstack1ll111l_opy_ (u"ࠩࡤࡧࡹ࡯࡯࡯ࠩ੊"): bstack1ll111l_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭ੋ"),
            bstack1ll111l_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧੌ"): {
              bstack1ll111l_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷ੍ࠬ"): bstack1ll111l_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭੎")
            }
          }
          if bstack1l1ll11l1_opy_.status == bstack1ll111l_opy_ (u"ࠧࡑࡃࡖࡗࠬ੏"):
            bstack11l1l1lll_opy_ = bstack1ll111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂ࠭੐").format(json.dumps(bstack1l1ll1111_opy_))
            driver.execute_script(bstack11l1l1lll_opy_)
            bstack11l111l1l_opy_ = bstack1ll111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠧੑ").format(json.dumps(bstack1ll111ll1_opy_))
            driver.execute_script(bstack11l111l1l_opy_)
          elif bstack1l1ll11l1_opy_.status == bstack1ll111l_opy_ (u"ࠪࡊࡆࡏࡌࠨ੒"):
            reason = bstack1ll111l_opy_ (u"ࠦࠧ੓")
            bstack1llllll11_opy_ = bstack1111l111_opy_ + bstack1ll111l_opy_ (u"ࠬࠦࡦࡢ࡫࡯ࡩࡩ࠭੔")
            if bstack1l1ll11l1_opy_.message:
              reason = str(bstack1l1ll11l1_opy_.message)
              bstack1llllll11_opy_ = bstack1llllll11_opy_ + bstack1ll111l_opy_ (u"࠭ࠠࡸ࡫ࡷ࡬ࠥ࡫ࡲࡳࡱࡵ࠾ࠥ࠭੕") + reason
            bstack1l1ll1111_opy_[bstack1ll111l_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪ੖")] = {
              bstack1ll111l_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ੗"): bstack1ll111l_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ੘"),
              bstack1ll111l_opy_ (u"ࠪࡨࡦࡺࡡࠨਖ਼"): bstack1llllll11_opy_
            }
            bstack1ll111ll1_opy_[bstack1ll111l_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧਗ਼")] = {
              bstack1ll111l_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬਜ਼"): bstack1ll111l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ੜ"),
              bstack1ll111l_opy_ (u"ࠧࡳࡧࡤࡷࡴࡴࠧ੝"): reason
            }
            bstack11l1l1lll_opy_ = bstack1ll111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂ࠭ਫ਼").format(json.dumps(bstack1l1ll1111_opy_))
            driver.execute_script(bstack11l1l1lll_opy_)
            bstack11l111l1l_opy_ = bstack1ll111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠧ੟").format(json.dumps(bstack1ll111ll1_opy_))
            driver.execute_script(bstack11l111l1l_opy_)
  elif bstack1ll1l1l111_opy_:
    try:
      data = {}
      bstack1111l111_opy_ = None
      if test:
        bstack1111l111_opy_ = str(test.data)
      if not bstack11l1111l1_opy_ and bstack1111l111_opy_:
        data[bstack1ll111l_opy_ (u"ࠪࡲࡦࡳࡥࠨ੠")] = bstack1111l111_opy_
      if bstack1l1ll11l1_opy_:
        if bstack1l1ll11l1_opy_.status == bstack1ll111l_opy_ (u"ࠫࡕࡇࡓࡔࠩ੡"):
          data[bstack1ll111l_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ੢")] = bstack1ll111l_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭੣")
        elif bstack1l1ll11l1_opy_.status == bstack1ll111l_opy_ (u"ࠧࡇࡃࡌࡐࠬ੤"):
          data[bstack1ll111l_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ੥")] = bstack1ll111l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ੦")
          if bstack1l1ll11l1_opy_.message:
            data[bstack1ll111l_opy_ (u"ࠪࡶࡪࡧࡳࡰࡰࠪ੧")] = str(bstack1l1ll11l1_opy_.message)
      user = CONFIG[bstack1ll111l_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭੨")]
      key = CONFIG[bstack1ll111l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ੩")]
      url = bstack1ll111l_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡼࡿ࠽ࡿࢂࡆࡡࡱ࡫࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡡࡶࡶࡲࡱࡦࡺࡥ࠰ࡵࡨࡷࡸ࡯࡯࡯ࡵ࠲ࡿࢂ࠴ࡪࡴࡱࡱࠫ੪").format(user, key, bstack1ll1l1l111_opy_)
      headers = {
        bstack1ll111l_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡶࡼࡴࡪ࠭੫"): bstack1ll111l_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫ੬"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers)
    except Exception as e:
      logger.error(bstack1l11111l_opy_.format(str(e)))
  if bstack11ll1ll1_opy_:
    bstack1llll1111l_opy_(bstack11ll1ll1_opy_)
  if bstack1ll1l1l11l_opy_:
    bstack111lllll1_opy_(bstack1ll1l1l11l_opy_)
  bstack1ll111l1_opy_(self, test)
def bstack1llll1l1l1_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack1llll1l1ll_opy_
  bstack1llll1l1ll_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack1l1ll11l1_opy_
  bstack1l1ll11l1_opy_ = self._test
def bstack11111l1l_opy_():
  global bstack1l1111ll1_opy_
  try:
    if os.path.exists(bstack1l1111ll1_opy_):
      os.remove(bstack1l1111ll1_opy_)
  except Exception as e:
    logger.debug(bstack1ll111l_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡩ࡫࡬ࡦࡶ࡬ࡲ࡬ࠦࡲࡰࡤࡲࡸࠥࡸࡥࡱࡱࡵࡸࠥ࡬ࡩ࡭ࡧ࠽ࠤࠬ੭") + str(e))
def bstack1lll111l1_opy_():
  global bstack1l1111ll1_opy_
  bstack11l1lllll_opy_ = {}
  try:
    if not os.path.isfile(bstack1l1111ll1_opy_):
      with open(bstack1l1111ll1_opy_, bstack1ll111l_opy_ (u"ࠪࡻࠬ੮")):
        pass
      with open(bstack1l1111ll1_opy_, bstack1ll111l_opy_ (u"ࠦࡼ࠱ࠢ੯")) as outfile:
        json.dump({}, outfile)
    if os.path.exists(bstack1l1111ll1_opy_):
      bstack11l1lllll_opy_ = json.load(open(bstack1l1111ll1_opy_, bstack1ll111l_opy_ (u"ࠬࡸࡢࠨੰ")))
  except Exception as e:
    logger.debug(bstack1ll111l_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡴࡨࡥࡩ࡯࡮ࡨࠢࡵࡳࡧࡵࡴࠡࡴࡨࡴࡴࡸࡴࠡࡨ࡬ࡰࡪࡀࠠࠨੱ") + str(e))
  finally:
    return bstack11l1lllll_opy_
def bstack1lll11l11l_opy_(platform_index, item_index):
  global bstack1l1111ll1_opy_
  try:
    bstack11l1lllll_opy_ = bstack1lll111l1_opy_()
    bstack11l1lllll_opy_[item_index] = platform_index
    with open(bstack1l1111ll1_opy_, bstack1ll111l_opy_ (u"ࠢࡸ࠭ࠥੲ")) as outfile:
      json.dump(bstack11l1lllll_opy_, outfile)
  except Exception as e:
    logger.debug(bstack1ll111l_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡻࡷ࡯ࡴࡪࡰࡪࠤࡹࡵࠠࡳࡱࡥࡳࡹࠦࡲࡦࡲࡲࡶࡹࠦࡦࡪ࡮ࡨ࠾ࠥ࠭ੳ") + str(e))
def bstack1ll11ll11_opy_(bstack1llll1l111_opy_):
  global CONFIG
  bstack1l111l1l1_opy_ = bstack1ll111l_opy_ (u"ࠩࠪੴ")
  if not bstack1ll111l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ੵ") in CONFIG:
    logger.info(bstack1ll111l_opy_ (u"ࠫࡓࡵࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠣࡴࡦࡹࡳࡦࡦࠣࡹࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡧࡦࡰࡨࡶࡦࡺࡥࠡࡴࡨࡴࡴࡸࡴࠡࡨࡲࡶࠥࡘ࡯ࡣࡱࡷࠤࡷࡻ࡮ࠨ੶"))
  try:
    platform = CONFIG[bstack1ll111l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ੷")][bstack1llll1l111_opy_]
    if bstack1ll111l_opy_ (u"࠭࡯ࡴࠩ੸") in platform:
      bstack1l111l1l1_opy_ += str(platform[bstack1ll111l_opy_ (u"ࠧࡰࡵࠪ੹")]) + bstack1ll111l_opy_ (u"ࠨ࠮ࠣࠫ੺")
    if bstack1ll111l_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬ੻") in platform:
      bstack1l111l1l1_opy_ += str(platform[bstack1ll111l_opy_ (u"ࠪࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳ࠭੼")]) + bstack1ll111l_opy_ (u"ࠫ࠱ࠦࠧ੽")
    if bstack1ll111l_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠩ੾") in platform:
      bstack1l111l1l1_opy_ += str(platform[bstack1ll111l_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪ੿")]) + bstack1ll111l_opy_ (u"ࠧ࠭ࠢࠪ઀")
    if bstack1ll111l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠪઁ") in platform:
      bstack1l111l1l1_opy_ += str(platform[bstack1ll111l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠫં")]) + bstack1ll111l_opy_ (u"ࠪ࠰ࠥ࠭ઃ")
    if bstack1ll111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩ઄") in platform:
      bstack1l111l1l1_opy_ += str(platform[bstack1ll111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪઅ")]) + bstack1ll111l_opy_ (u"࠭ࠬࠡࠩઆ")
    if bstack1ll111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨઇ") in platform:
      bstack1l111l1l1_opy_ += str(platform[bstack1ll111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩઈ")]) + bstack1ll111l_opy_ (u"ࠩ࠯ࠤࠬઉ")
  except Exception as e:
    logger.debug(bstack1ll111l_opy_ (u"ࠪࡗࡴࡳࡥࠡࡧࡵࡶࡴࡸࠠࡪࡰࠣ࡫ࡪࡴࡥࡳࡣࡷ࡭ࡳ࡭ࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠢࡶࡸࡷ࡯࡮ࡨࠢࡩࡳࡷࠦࡲࡦࡲࡲࡶࡹࠦࡧࡦࡰࡨࡶࡦࡺࡩࡰࡰࠪઊ") + str(e))
  finally:
    if bstack1l111l1l1_opy_[len(bstack1l111l1l1_opy_) - 2:] == bstack1ll111l_opy_ (u"ࠫ࠱ࠦࠧઋ"):
      bstack1l111l1l1_opy_ = bstack1l111l1l1_opy_[:-2]
    return bstack1l111l1l1_opy_
def bstack1ll111lll_opy_(path, bstack1l111l1l1_opy_):
  try:
    import xml.etree.ElementTree as ET
    bstack1l1llll1l_opy_ = ET.parse(path)
    bstack1ll1111l_opy_ = bstack1l1llll1l_opy_.getroot()
    bstack1l111ll11_opy_ = None
    for suite in bstack1ll1111l_opy_.iter(bstack1ll111l_opy_ (u"ࠬࡹࡵࡪࡶࡨࠫઌ")):
      if bstack1ll111l_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭ઍ") in suite.attrib:
        suite.attrib[bstack1ll111l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ઎")] += bstack1ll111l_opy_ (u"ࠨࠢࠪએ") + bstack1l111l1l1_opy_
        bstack1l111ll11_opy_ = suite
    bstack1lll1l1lll_opy_ = None
    for robot in bstack1ll1111l_opy_.iter(bstack1ll111l_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨઐ")):
      bstack1lll1l1lll_opy_ = robot
    bstack111l1l11l_opy_ = len(bstack1lll1l1lll_opy_.findall(bstack1ll111l_opy_ (u"ࠪࡷࡺ࡯ࡴࡦࠩઑ")))
    if bstack111l1l11l_opy_ == 1:
      bstack1lll1l1lll_opy_.remove(bstack1lll1l1lll_opy_.findall(bstack1ll111l_opy_ (u"ࠫࡸࡻࡩࡵࡧࠪ઒"))[0])
      bstack1111l1ll1_opy_ = ET.Element(bstack1ll111l_opy_ (u"ࠬࡹࡵࡪࡶࡨࠫઓ"), attrib={bstack1ll111l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫઔ"): bstack1ll111l_opy_ (u"ࠧࡔࡷ࡬ࡸࡪࡹࠧક"), bstack1ll111l_opy_ (u"ࠨ࡫ࡧࠫખ"): bstack1ll111l_opy_ (u"ࠩࡶ࠴ࠬગ")})
      bstack1lll1l1lll_opy_.insert(1, bstack1111l1ll1_opy_)
      bstack1l11l1lll_opy_ = None
      for suite in bstack1lll1l1lll_opy_.iter(bstack1ll111l_opy_ (u"ࠪࡷࡺ࡯ࡴࡦࠩઘ")):
        bstack1l11l1lll_opy_ = suite
      bstack1l11l1lll_opy_.append(bstack1l111ll11_opy_)
      bstack1llll1ll_opy_ = None
      for status in bstack1l111ll11_opy_.iter(bstack1ll111l_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫઙ")):
        bstack1llll1ll_opy_ = status
      bstack1l11l1lll_opy_.append(bstack1llll1ll_opy_)
    bstack1l1llll1l_opy_.write(path)
  except Exception as e:
    logger.debug(bstack1ll111l_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡱࡣࡵࡷ࡮ࡴࡧࠡࡹ࡫࡭ࡱ࡫ࠠࡨࡧࡱࡩࡷࡧࡴࡪࡰࡪࠤࡷࡵࡢࡰࡶࠣࡶࡪࡶ࡯ࡳࡶࠪચ") + str(e))
def bstack1llll11lll_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  global bstack1lllllll1_opy_
  global CONFIG
  if bstack1ll111l_opy_ (u"ࠨࡰࡺࡶ࡫ࡳࡳࡶࡡࡵࡪࠥછ") in options:
    del options[bstack1ll111l_opy_ (u"ࠢࡱࡻࡷ࡬ࡴࡴࡰࡢࡶ࡫ࠦજ")]
  bstack1llll1l11_opy_ = bstack1lll111l1_opy_()
  for bstack11ll1ll1l_opy_ in bstack1llll1l11_opy_.keys():
    path = os.path.join(os.getcwd(), bstack1ll111l_opy_ (u"ࠨࡲࡤࡦࡴࡺ࡟ࡳࡧࡶࡹࡱࡺࡳࠨઝ"), str(bstack11ll1ll1l_opy_), bstack1ll111l_opy_ (u"ࠩࡲࡹࡹࡶࡵࡵ࠰ࡻࡱࡱ࠭ઞ"))
    bstack1ll111lll_opy_(path, bstack1ll11ll11_opy_(bstack1llll1l11_opy_[bstack11ll1ll1l_opy_]))
  bstack11111l1l_opy_()
  return bstack1lllllll1_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack1lll1111l_opy_(self, ff_profile_dir):
  global bstack11ll11111_opy_
  if not ff_profile_dir:
    return None
  return bstack11ll11111_opy_(self, ff_profile_dir)
def bstack1ll1ll1ll_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack11lll1lll_opy_
  bstack11lllll11_opy_ = []
  if bstack1ll111l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ટ") in CONFIG:
    bstack11lllll11_opy_ = CONFIG[bstack1ll111l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧઠ")]
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack1ll111l_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࠨડ")],
      pabot_args[bstack1ll111l_opy_ (u"ࠨࡶࡦࡴࡥࡳࡸ࡫ࠢઢ")],
      argfile,
      pabot_args.get(bstack1ll111l_opy_ (u"ࠢࡩ࡫ࡹࡩࠧણ")),
      pabot_args[bstack1ll111l_opy_ (u"ࠣࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠦત")],
      platform[0],
      bstack11lll1lll_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack1ll111l_opy_ (u"ࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡪ࡮ࡲࡥࡴࠤથ")] or [(bstack1ll111l_opy_ (u"ࠥࠦદ"), None)]
    for platform in enumerate(bstack11lllll11_opy_)
  ]
def bstack1ll1l11l_opy_(self, datasources, outs_dir, options,
                        execution_item, command, verbose, argfile,
                        hive=None, processes=0, platform_index=0, bstack11l11111_opy_=bstack1ll111l_opy_ (u"ࠫࠬધ")):
  global bstack111ll11l_opy_
  self.platform_index = platform_index
  self.bstack11l11l11_opy_ = bstack11l11111_opy_
  bstack111ll11l_opy_(self, datasources, outs_dir, options,
                      execution_item, command, verbose, argfile, hive, processes)
def bstack1l1l1ll1l_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack1ll1lllll1_opy_
  global bstack1l1l1ll1_opy_
  if not bstack1ll111l_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧન") in item.options:
    item.options[bstack1ll111l_opy_ (u"࠭ࡶࡢࡴ࡬ࡥࡧࡲࡥࠨ઩")] = []
  for v in item.options[bstack1ll111l_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠩપ")]:
    if bstack1ll111l_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡑࡎࡄࡘࡋࡕࡒࡎࡋࡑࡈࡊ࡞ࠧફ") in v:
      item.options[bstack1ll111l_opy_ (u"ࠩࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠫબ")].remove(v)
    if bstack1ll111l_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡆࡐࡎࡇࡒࡈࡕࠪભ") in v:
      item.options[bstack1ll111l_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭મ")].remove(v)
  item.options[bstack1ll111l_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧય")].insert(0, bstack1ll111l_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡖࡌࡂࡖࡉࡓࡗࡓࡉࡏࡆࡈ࡜࠿ࢁࡽࠨર").format(item.platform_index))
  item.options[bstack1ll111l_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠩ઱")].insert(0, bstack1ll111l_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡅࡇࡉࡐࡔࡉࡁࡍࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖ࠿ࢁࡽࠨલ").format(item.bstack11l11l11_opy_))
  if bstack1l1l1ll1_opy_:
    item.options[bstack1ll111l_opy_ (u"ࠩࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠫળ")].insert(0, bstack1ll111l_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡆࡐࡎࡇࡒࡈࡕ࠽ࡿࢂ࠭઴").format(bstack1l1l1ll1_opy_))
  return bstack1ll1lllll1_opy_(caller_id, datasources, is_last, item, outs_dir)
def bstack11lll1l11_opy_(command, item_index):
  global bstack1l1l1ll1_opy_
  if bstack1l1l1ll1_opy_:
    command[0] = command[0].replace(bstack1ll111l_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪવ"), bstack1ll111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠱ࡸࡪ࡫ࠡࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠢ࠰࠱ࡧࡹࡴࡢࡥ࡮ࡣ࡮ࡺࡥ࡮ࡡ࡬ࡲࡩ࡫ࡸࠡࠩશ") + str(
      item_index) + bstack1ll111l_opy_ (u"࠭ࠠࠨષ") + bstack1l1l1ll1_opy_, 1)
  else:
    command[0] = command[0].replace(bstack1ll111l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭સ"),
                                    bstack1ll111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠭ࡴࡦ࡮ࠤࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠥ࠳࠭ࡣࡵࡷࡥࡨࡱ࡟ࡪࡶࡨࡱࡤ࡯࡮ࡥࡧࡻࠤࠬહ") + str(item_index), 1)
def bstack1ll11111l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack111ll1l11_opy_
  bstack11lll1l11_opy_(command, item_index)
  return bstack111ll1l11_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
def bstack111ll11ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir):
  global bstack111ll1l11_opy_
  bstack11lll1l11_opy_(command, item_index)
  return bstack111ll1l11_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
def bstack1l1l111l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout):
  global bstack111ll1l11_opy_
  bstack11lll1l11_opy_(command, item_index)
  return bstack111ll1l11_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
def bstack1lllll1111_opy_(self, runner, quiet=False, capture=True):
  global bstack111ll111_opy_
  bstack1llll11111_opy_ = bstack111ll111_opy_(self, runner, quiet=False, capture=True)
  if self.exception:
    if not hasattr(runner, bstack1ll111l_opy_ (u"ࠩࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࡤࡧࡲࡳࠩ઺")):
      runner.exception_arr = []
    if not hasattr(runner, bstack1ll111l_opy_ (u"ࠪࡩࡽࡩ࡟ࡵࡴࡤࡧࡪࡨࡡࡤ࡭ࡢࡥࡷࡸࠧ઻")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack1llll11111_opy_
def bstack1ll1l111_opy_(self, name, context, *args):
  global bstack1111lll1l_opy_
  if name == bstack1ll111l_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࡣ࡫࡫ࡡࡵࡷࡵࡩ઼ࠬ"):
    bstack1111lll1l_opy_(self, name, context, *args)
    try:
      if not bstack11l1111l1_opy_:
        bstack1l11ll111_opy_ = threading.current_thread().bstackSessionDriver if bstack1l1lll111_opy_(bstack1ll111l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫઽ")) else context.browser
        bstack1l1l11l1_opy_ = str(self.feature.name)
        bstack11l1lll1_opy_(context, bstack1l1l11l1_opy_)
        bstack1l11ll111_opy_.execute_script(bstack1ll111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠣࠫા") + json.dumps(bstack1l1l11l1_opy_) + bstack1ll111l_opy_ (u"ࠧࡾࡿࠪિ"))
      self.driver_before_scenario = False
    except Exception as e:
      logger.debug(bstack1ll111l_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠠࡪࡰࠣࡦࡪ࡬࡯ࡳࡧࠣࡪࡪࡧࡴࡶࡴࡨ࠾ࠥࢁࡽࠨી").format(str(e)))
  elif name == bstack1ll111l_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠫુ"):
    bstack1111lll1l_opy_(self, name, context, *args)
    try:
      if not hasattr(self, bstack1ll111l_opy_ (u"ࠪࡨࡷ࡯ࡶࡦࡴࡢࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬૂ")):
        self.driver_before_scenario = True
      if (not bstack11l1111l1_opy_):
        scenario_name = args[0].name
        feature_name = bstack1l1l11l1_opy_ = str(self.feature.name)
        bstack1l1l11l1_opy_ = feature_name + bstack1ll111l_opy_ (u"ࠫࠥ࠳ࠠࠨૃ") + scenario_name
        bstack1l11ll111_opy_ = threading.current_thread().bstackSessionDriver if bstack1l1lll111_opy_(bstack1ll111l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫૄ")) else context.browser
        if self.driver_before_scenario:
          bstack11l1lll1_opy_(context, bstack1l1l11l1_opy_)
          bstack1l11ll111_opy_.execute_script(bstack1ll111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠣࠫૅ") + json.dumps(bstack1l1l11l1_opy_) + bstack1ll111l_opy_ (u"ࠧࡾࡿࠪ૆"))
    except Exception as e:
      logger.debug(bstack1ll111l_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠠࡪࡰࠣࡦࡪ࡬࡯ࡳࡧࠣࡷࡨ࡫࡮ࡢࡴ࡬ࡳ࠿ࠦࡻࡾࠩે").format(str(e)))
  elif name == bstack1ll111l_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪૈ"):
    try:
      bstack1l1l1ll11_opy_ = args[0].status.name
      bstack1l11ll111_opy_ = threading.current_thread().bstackSessionDriver if bstack1ll111l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩૉ") in threading.current_thread().__dict__.keys() else context.browser
      if str(bstack1l1l1ll11_opy_).lower() == bstack1ll111l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ૊"):
        bstack11l111lll_opy_ = bstack1ll111l_opy_ (u"ࠬ࠭ો")
        bstack1l1l11l1l_opy_ = bstack1ll111l_opy_ (u"࠭ࠧૌ")
        bstack11l1ll11l_opy_ = bstack1ll111l_opy_ (u"ࠧࠨ્")
        try:
          import traceback
          bstack11l111lll_opy_ = self.exception.__class__.__name__
          bstack1l1lll1l_opy_ = traceback.format_tb(self.exc_traceback)
          bstack1l1l11l1l_opy_ = bstack1ll111l_opy_ (u"ࠨࠢࠪ૎").join(bstack1l1lll1l_opy_)
          bstack11l1ll11l_opy_ = bstack1l1lll1l_opy_[-1]
        except Exception as e:
          logger.debug(bstack1lll11l111_opy_.format(str(e)))
        bstack11l111lll_opy_ += bstack11l1ll11l_opy_
        bstack1ll1ll1l1l_opy_(context, json.dumps(str(args[0].name) + bstack1ll111l_opy_ (u"ࠤࠣ࠱ࠥࡌࡡࡪ࡮ࡨࡨࠦࡢ࡮ࠣ૏") + str(bstack1l1l11l1l_opy_)),
                            bstack1ll111l_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠤૐ"))
        if self.driver_before_scenario:
          bstack1l1l1l11_opy_(context, bstack1ll111l_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦ૑"), bstack11l111lll_opy_)
          bstack1l11ll111_opy_.execute_script(bstack1ll111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡨࡦࡺࡡࠣ࠼ࠪ૒") + json.dumps(str(args[0].name) + bstack1ll111l_opy_ (u"ࠨࠠ࠮ࠢࡉࡥ࡮ࡲࡥࡥࠣ࡟ࡲࠧ૓") + str(bstack1l1l11l1l_opy_)) + bstack1ll111l_opy_ (u"ࠧ࠭ࠢࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠤࠧ࡫ࡲࡳࡱࡵࠦࢂࢃࠧ૔"))
        if self.driver_before_scenario:
          bstack1l11ll111_opy_.execute_script(bstack1ll111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡴࡶࡤࡸࡺࡹࠢ࠻ࠤࡩࡥ࡮ࡲࡥࡥࠤ࠯ࠤࠧࡸࡥࡢࡵࡲࡲࠧࡀࠠࠨ૕") + json.dumps(bstack1ll111l_opy_ (u"ࠤࡖࡧࡪࡴࡡࡳ࡫ࡲࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡼ࡯ࡴࡩ࠼ࠣࡠࡳࠨ૖") + str(bstack11l111lll_opy_)) + bstack1ll111l_opy_ (u"ࠪࢁࢂ࠭૗"))
      else:
        bstack1ll1ll1l1l_opy_(context, bstack1ll111l_opy_ (u"ࠦࡕࡧࡳࡴࡧࡧࠥࠧ૘"), bstack1ll111l_opy_ (u"ࠧ࡯࡮ࡧࡱࠥ૙"))
        if self.driver_before_scenario:
          bstack1l1l1l11_opy_(context, bstack1ll111l_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨ૚"))
        bstack1l11ll111_opy_.execute_script(bstack1ll111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡪࡡࡵࡣࠥ࠾ࠬ૛") + json.dumps(str(args[0].name) + bstack1ll111l_opy_ (u"ࠣࠢ࠰ࠤࡕࡧࡳࡴࡧࡧࠥࠧ૜")) + bstack1ll111l_opy_ (u"ࠩ࠯ࠤࠧࡲࡥࡷࡧ࡯ࠦ࠿ࠦࠢࡪࡰࡩࡳࠧࢃࡽࠨ૝"))
        if self.driver_before_scenario:
          bstack1l11ll111_opy_.execute_script(bstack1ll111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡶࡸࡦࡺࡵࡴࠤ࠽ࠦࡵࡧࡳࡴࡧࡧࠦࢂࢃࠧ૞"))
    except Exception as e:
      logger.debug(bstack1ll111l_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠ࡮ࡣࡵ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡳࡵࡣࡷࡹࡸࠦࡩ࡯ࠢࡤࡪࡹ࡫ࡲࠡࡨࡨࡥࡹࡻࡲࡦ࠼ࠣࡿࢂ࠭૟").format(str(e)))
  elif name == bstack1ll111l_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣ࡫࡫ࡡࡵࡷࡵࡩࠬૠ"):
    try:
      bstack1l11ll111_opy_ = threading.current_thread().bstackSessionDriver if bstack1l1lll111_opy_(bstack1ll111l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬૡ")) else context.browser
      if context.failed is True:
        bstack111111ll_opy_ = []
        bstack1l1lllll1_opy_ = []
        bstack1l1ll11l_opy_ = []
        bstack1ll1ll11l1_opy_ = bstack1ll111l_opy_ (u"ࠧࠨૢ")
        try:
          import traceback
          for exc in self.exception_arr:
            bstack111111ll_opy_.append(exc.__class__.__name__)
          for exc_tb in self.exc_traceback_arr:
            bstack1l1lll1l_opy_ = traceback.format_tb(exc_tb)
            bstack1llll11l1l_opy_ = bstack1ll111l_opy_ (u"ࠨࠢࠪૣ").join(bstack1l1lll1l_opy_)
            bstack1l1lllll1_opy_.append(bstack1llll11l1l_opy_)
            bstack1l1ll11l_opy_.append(bstack1l1lll1l_opy_[-1])
        except Exception as e:
          logger.debug(bstack1lll11l111_opy_.format(str(e)))
        bstack11l111lll_opy_ = bstack1ll111l_opy_ (u"ࠩࠪ૤")
        for i in range(len(bstack111111ll_opy_)):
          bstack11l111lll_opy_ += bstack111111ll_opy_[i] + bstack1l1ll11l_opy_[i] + bstack1ll111l_opy_ (u"ࠪࡠࡳ࠭૥")
        bstack1ll1ll11l1_opy_ = bstack1ll111l_opy_ (u"ࠫࠥ࠭૦").join(bstack1l1lllll1_opy_)
        if not self.driver_before_scenario:
          bstack1ll1ll1l1l_opy_(context, bstack1ll1ll11l1_opy_, bstack1ll111l_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠦ૧"))
          bstack1l1l1l11_opy_(context, bstack1ll111l_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨ૨"), bstack11l111lll_opy_)
          bstack1l11ll111_opy_.execute_script(bstack1ll111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡪࡡࡵࡣࠥ࠾ࠬ૩") + json.dumps(bstack1ll1ll11l1_opy_) + bstack1ll111l_opy_ (u"ࠨ࠮ࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡥࡳࡴࡲࡶࠧࢃࡽࠨ૪"))
          bstack1l11ll111_opy_.execute_script(bstack1ll111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡵࡷࡥࡹࡻࡳࠣ࠼ࠥࡪࡦ࡯࡬ࡦࡦࠥ࠰ࠥࠨࡲࡦࡣࡶࡳࡳࠨ࠺ࠡࠩ૫") + json.dumps(bstack1ll111l_opy_ (u"ࠥࡗࡴࡳࡥࠡࡵࡦࡩࡳࡧࡲࡪࡱࡶࠤ࡫ࡧࡩ࡭ࡧࡧ࠾ࠥࡢ࡮ࠣ૬") + str(bstack11l111lll_opy_)) + bstack1ll111l_opy_ (u"ࠫࢂࢃࠧ૭"))
      else:
        if not self.driver_before_scenario:
          bstack1ll1ll1l1l_opy_(context, bstack1ll111l_opy_ (u"ࠧࡌࡥࡢࡶࡸࡶࡪࡀࠠࠣ૮") + str(self.feature.name) + bstack1ll111l_opy_ (u"ࠨࠠࡱࡣࡶࡷࡪࡪࠡࠣ૯"), bstack1ll111l_opy_ (u"ࠢࡪࡰࡩࡳࠧ૰"))
          bstack1l1l1l11_opy_(context, bstack1ll111l_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣ૱"))
          bstack1l11ll111_opy_.execute_script(bstack1ll111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧ૲") + json.dumps(bstack1ll111l_opy_ (u"ࠥࡊࡪࡧࡴࡶࡴࡨ࠾ࠥࠨ૳") + str(self.feature.name) + bstack1ll111l_opy_ (u"ࠦࠥࡶࡡࡴࡵࡨࡨࠦࠨ૴")) + bstack1ll111l_opy_ (u"ࠬ࠲ࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥ࡭ࡳ࡬࡯ࠣࡿࢀࠫ૵"))
          bstack1l11ll111_opy_.execute_script(bstack1ll111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡹࡴࡢࡶࡸࡷࠧࡀࠢࡱࡣࡶࡷࡪࡪࠢࡾࡿࠪ૶"))
    except Exception as e:
      logger.debug(bstack1ll111l_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡱࡦࡸ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡶࡸࡦࡺࡵࡴࠢ࡬ࡲࠥࡧࡦࡵࡧࡵࠤ࡫࡫ࡡࡵࡷࡵࡩ࠿ࠦࡻࡾࠩ૷").format(str(e)))
  else:
    bstack1111lll1l_opy_(self, name, context, *args)
  if name in [bstack1ll111l_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡧࡧࡤࡸࡺࡸࡥࠨ૸"), bstack1ll111l_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪૹ")]:
    bstack1111lll1l_opy_(self, name, context, *args)
    if (name == bstack1ll111l_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠫૺ") and self.driver_before_scenario) or (
            name == bstack1ll111l_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡪࡪࡧࡴࡶࡴࡨࠫૻ") and not self.driver_before_scenario):
      try:
        bstack1l11ll111_opy_ = threading.current_thread().bstackSessionDriver if bstack1l1lll111_opy_(bstack1ll111l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫૼ")) else context.browser
        bstack1l11ll111_opy_.quit()
      except Exception:
        pass
def bstack11l11ll1_opy_(config, startdir):
  return bstack1ll111l_opy_ (u"ࠨࡤࡳ࡫ࡹࡩࡷࡀࠠࡼ࠲ࢀࠦ૽").format(bstack1ll111l_opy_ (u"ࠢࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠨ૾"))
notset = Notset()
def bstack1l1l1111l_opy_(self, name: str, default=notset, skip: bool = False):
  global bstack1ll11lll11_opy_
  if str(name).lower() == bstack1ll111l_opy_ (u"ࠨࡦࡵ࡭ࡻ࡫ࡲࠨ૿"):
    return bstack1ll111l_opy_ (u"ࠤࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠣ଀")
  else:
    return bstack1ll11lll11_opy_(self, name, default, skip)
def bstack11111lll_opy_(item, when):
  global bstack1lll11l11_opy_
  try:
    bstack1lll11l11_opy_(item, when)
  except Exception as e:
    pass
def bstack1l11l1l11_opy_():
  return
def bstack1l11ll1l1_opy_(type, name, status, reason, bstack1llll11ll_opy_, bstack1ll111l1l_opy_):
  bstack1ll111ll1_opy_ = {
    bstack1ll111l_opy_ (u"ࠪࡥࡨࡺࡩࡰࡰࠪଁ"): type,
    bstack1ll111l_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧଂ"): {}
  }
  if type == bstack1ll111l_opy_ (u"ࠬࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠧଃ"):
    bstack1ll111ll1_opy_[bstack1ll111l_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩ଄")][bstack1ll111l_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ଅ")] = bstack1llll11ll_opy_
    bstack1ll111ll1_opy_[bstack1ll111l_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫଆ")][bstack1ll111l_opy_ (u"ࠩࡧࡥࡹࡧࠧଇ")] = json.dumps(str(bstack1ll111l1l_opy_))
  if type == bstack1ll111l_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫଈ"):
    bstack1ll111ll1_opy_[bstack1ll111l_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧଉ")][bstack1ll111l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪଊ")] = name
  if type == bstack1ll111l_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩଋ"):
    bstack1ll111ll1_opy_[bstack1ll111l_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪଌ")][bstack1ll111l_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ଍")] = status
    if status == bstack1ll111l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ଎"):
      bstack1ll111ll1_opy_[bstack1ll111l_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ଏ")][bstack1ll111l_opy_ (u"ࠫࡷ࡫ࡡࡴࡱࡱࠫଐ")] = json.dumps(str(reason))
  bstack11l111l1l_opy_ = bstack1ll111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠪ଑").format(json.dumps(bstack1ll111ll1_opy_))
  return bstack11l111l1l_opy_
def bstack1llll11ll1_opy_(item, call, rep):
  global bstack1lllll11ll_opy_
  global bstack1l11lllll_opy_
  global bstack11l1111l1_opy_
  name = bstack1ll111l_opy_ (u"࠭ࠧ଒")
  try:
    if rep.when == bstack1ll111l_opy_ (u"ࠧࡤࡣ࡯ࡰࠬଓ"):
      bstack1ll1l1l111_opy_ = threading.current_thread().bstack11llll111_opy_
      try:
        if not bstack11l1111l1_opy_:
          name = str(rep.nodeid)
          bstack1llll111l_opy_ = bstack1l11ll1l1_opy_(bstack1ll111l_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩଔ"), name, bstack1ll111l_opy_ (u"ࠩࠪକ"), bstack1ll111l_opy_ (u"ࠪࠫଖ"), bstack1ll111l_opy_ (u"ࠫࠬଗ"), bstack1ll111l_opy_ (u"ࠬ࠭ଘ"))
          for driver in bstack1l11lllll_opy_:
            if bstack1ll1l1l111_opy_ == driver.session_id:
              driver.execute_script(bstack1llll111l_opy_)
      except Exception as e:
        logger.debug(bstack1ll111l_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠠࡧࡱࡵࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡵࡨࡷࡸ࡯࡯࡯࠼ࠣࡿࢂ࠭ଙ").format(str(e)))
      try:
        bstack111ll1lll_opy_(rep.outcome.lower())
        if rep.outcome.lower() != bstack1ll111l_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨଚ"):
          status = bstack1ll111l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨଛ") if rep.outcome.lower() == bstack1ll111l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩଜ") else bstack1ll111l_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪଝ")
          reason = bstack1ll111l_opy_ (u"ࠫࠬଞ")
          if (reason != bstack1ll111l_opy_ (u"ࠧࠨଟ")):
            try:
              if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
            except Exception as e:
              threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(str(reason))
          if status == bstack1ll111l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ଠ"):
            reason = rep.longrepr.reprcrash.message
            if (not threading.current_thread().bstackTestErrorMessages):
              threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(reason)
          level = bstack1ll111l_opy_ (u"ࠧࡪࡰࡩࡳࠬଡ") if status == bstack1ll111l_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨଢ") else bstack1ll111l_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨଣ")
          data = name + bstack1ll111l_opy_ (u"ࠪࠤࡵࡧࡳࡴࡧࡧࠥࠬତ") if status == bstack1ll111l_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫଥ") else name + bstack1ll111l_opy_ (u"ࠬࠦࡦࡢ࡫࡯ࡩࡩࠧࠠࠨଦ") + reason
          bstack111lll1l_opy_ = bstack1l11ll1l1_opy_(bstack1ll111l_opy_ (u"࠭ࡡ࡯ࡰࡲࡸࡦࡺࡥࠨଧ"), bstack1ll111l_opy_ (u"ࠧࠨନ"), bstack1ll111l_opy_ (u"ࠨࠩ଩"), bstack1ll111l_opy_ (u"ࠩࠪପ"), level, data)
          for driver in bstack1l11lllll_opy_:
            if bstack1ll1l1l111_opy_ == driver.session_id:
              driver.execute_script(bstack111lll1l_opy_)
      except Exception as e:
        logger.debug(bstack1ll111l_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡤࡱࡱࡸࡪࡾࡴࠡࡨࡲࡶࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡶࡩࡸࡹࡩࡰࡰ࠽ࠤࢀࢃࠧଫ").format(str(e)))
  except Exception as e:
    logger.debug(bstack1ll111l_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡶࡤࡸࡪࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡴࡦࡵࡷࠤࡸࡺࡡࡵࡷࡶ࠾ࠥࢁࡽࠨବ").format(str(e)))
  bstack1lllll11ll_opy_(item, call, rep)
def bstack11l11l1ll_opy_(framework_name):
  global bstack1l1ll1lll_opy_
  global bstack11lll1ll_opy_
  global bstack1llll1111_opy_
  bstack1l1ll1lll_opy_ = framework_name
  logger.info(bstack1l1lllll_opy_.format(bstack1l1ll1lll_opy_.split(bstack1ll111l_opy_ (u"ࠬ࠳ࠧଭ"))[0]))
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
    if bstack1ll1llllll_opy_:
      Service.start = bstack1ll11llll1_opy_
      Service.stop = bstack111111l1l_opy_
      webdriver.Remote.get = bstack1lllll1l1_opy_
      WebDriver.close = bstack111llll1_opy_
      WebDriver.quit = bstack1111ll11_opy_
      webdriver.Remote.__init__ = bstack11l111ll1_opy_
    if not bstack1ll1llllll_opy_ and bstack11llllll1_opy_.on():
      webdriver.Remote.__init__ = bstack1lll11111l_opy_
    bstack11lll1ll_opy_ = True
  except Exception as e:
    pass
  bstack111l1l1l1_opy_()
  if not bstack11lll1ll_opy_:
    bstack1l1lll1l1_opy_(bstack1ll111l_opy_ (u"ࠨࡐࡢࡥ࡮ࡥ࡬࡫ࡳࠡࡰࡲࡸࠥ࡯࡮ࡴࡶࡤࡰࡱ࡫ࡤࠣମ"), bstack1l1ll1l1l_opy_)
  if bstack1llllll1l_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      RemoteConnection._get_proxy_url = bstack1ll1l11ll1_opy_
    except Exception as e:
      logger.error(bstack1ll1l1ll_opy_.format(str(e)))
  if (bstack1ll111l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ଯ") in str(framework_name).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        WebDriverCreator._get_ff_profile = bstack1lll1111l_opy_
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCache.close = bstack1ll1l11l1l_opy_
      except Exception as e:
        logger.warn(bstack1111lll11_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        ApplicationCache.close = bstack1lll1l1111_opy_
      except Exception as e:
        logger.debug(bstack1lll11llll_opy_ + str(e))
    except Exception as e:
      bstack1l1lll1l1_opy_(e, bstack1111lll11_opy_)
    Output.end_test = bstack11l11lll1_opy_
    TestStatus.__init__ = bstack1llll1l1l1_opy_
    QueueItem.__init__ = bstack1ll1l11l_opy_
    pabot._create_items = bstack1ll1ll1ll_opy_
    try:
      from pabot import __version__ as bstack11l1l1l11_opy_
      if version.parse(bstack11l1l1l11_opy_) >= version.parse(bstack1ll111l_opy_ (u"ࠨ࠴࠱࠵࠺࠴࠰ࠨର")):
        pabot._run = bstack1l1l111l_opy_
      elif version.parse(bstack11l1l1l11_opy_) >= version.parse(bstack1ll111l_opy_ (u"ࠩ࠵࠲࠶࠹࠮࠱ࠩ଱")):
        pabot._run = bstack111ll11ll_opy_
      else:
        pabot._run = bstack1ll11111l_opy_
    except Exception as e:
      pabot._run = bstack1ll11111l_opy_
    pabot._create_command_for_execution = bstack1l1l1ll1l_opy_
    pabot._report_results = bstack1llll11lll_opy_
  if bstack1ll111l_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪଲ") in str(framework_name).lower():
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1l1lll1l1_opy_(e, bstack1l11111ll_opy_)
    Runner.run_hook = bstack1ll1l111_opy_
    Step.run = bstack1lllll1111_opy_
  if bstack1ll111l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫଳ") in str(framework_name).lower():
    if not bstack1ll1llllll_opy_:
      return
    try:
      from pytest_selenium import pytest_selenium
      from _pytest.config import Config
      pytest_selenium.pytest_report_header = bstack11l11ll1_opy_
      from pytest_selenium.drivers import browserstack
      browserstack.pytest_selenium_runtest_makereport = bstack1l11l1l11_opy_
      Config.getoption = bstack1l1l1111l_opy_
    except Exception as e:
      pass
    try:
      from pytest_bdd import reporting
      reporting.runtest_makereport = bstack1llll11ll1_opy_
    except Exception as e:
      pass
def bstack1ll11l1lll_opy_():
  global CONFIG
  if bstack1ll111l_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ଴") in CONFIG and int(CONFIG[bstack1ll111l_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭ଵ")]) > 1:
    logger.warn(bstack1lll11ll11_opy_)
def bstack1l111l11l_opy_(arg, bstack1ll1ll11_opy_):
  global CONFIG
  global bstack1llll11l_opy_
  global bstack1lll11l1l1_opy_
  global bstack1ll1llllll_opy_
  global bstack1ll1ll111_opy_
  bstack1llll11l1_opy_ = bstack1ll111l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧଶ")
  if bstack1ll1ll11_opy_ and isinstance(bstack1ll1ll11_opy_, str):
    bstack1ll1ll11_opy_ = eval(bstack1ll1ll11_opy_)
  CONFIG = bstack1ll1ll11_opy_[bstack1ll111l_opy_ (u"ࠨࡅࡒࡒࡋࡏࡇࠨଷ")]
  bstack1llll11l_opy_ = bstack1ll1ll11_opy_[bstack1ll111l_opy_ (u"ࠩࡋ࡙ࡇࡥࡕࡓࡎࠪସ")]
  bstack1lll11l1l1_opy_ = bstack1ll1ll11_opy_[bstack1ll111l_opy_ (u"ࠪࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬହ")]
  bstack1ll1llllll_opy_ = bstack1ll1ll11_opy_[bstack1ll111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠧ଺")]
  bstack1ll1ll111_opy_.bstack1ll11ll1ll_opy_(bstack1ll111l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳ࠭଻"), bstack1ll1llllll_opy_)
  os.environ[bstack1ll111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠨ଼")] = bstack1llll11l1_opy_
  os.environ[bstack1ll111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡐࡐࡉࡍࡌ࠭ଽ")] = json.dumps(CONFIG)
  os.environ[bstack1ll111l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡉࡗࡅࡣ࡚ࡘࡌࠨା")] = bstack1llll11l_opy_
  os.environ[bstack1ll111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪି")] = str(bstack1lll11l1l1_opy_)
  os.environ[bstack1ll111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓ࡝࡙ࡋࡓࡕࡡࡓࡐ࡚ࡍࡉࡏࠩୀ")] = str(True)
  if bstack1ll1ll111l_opy_(arg, [bstack1ll111l_opy_ (u"ࠫ࠲ࡴࠧୁ"), bstack1ll111l_opy_ (u"ࠬ࠳࠭࡯ࡷࡰࡴࡷࡵࡣࡦࡵࡶࡩࡸ࠭ୂ")]) != -1:
    os.environ[bstack1ll111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖ࡙ࡕࡇࡖࡘࡤࡖࡁࡓࡃࡏࡐࡊࡒࠧୃ")] = str(True)
  if len(sys.argv) <= 1:
    logger.critical(bstack1ll1llll1_opy_)
    return
  bstack1l1l1lll1_opy_()
  global bstack1lll1ll11_opy_
  global bstack1llllll111_opy_
  global bstack11lll1lll_opy_
  global bstack1l1l1ll1_opy_
  global bstack1ll111l11_opy_
  global bstack1llll1111_opy_
  global bstack11l1111l_opy_
  arg.append(bstack1ll111l_opy_ (u"ࠢ࠮࡙ࠥୄ"))
  arg.append(bstack1ll111l_opy_ (u"ࠣ࡫ࡪࡲࡴࡸࡥ࠻ࡏࡲࡨࡺࡲࡥࠡࡣ࡯ࡶࡪࡧࡤࡺࠢ࡬ࡱࡵࡵࡲࡵࡧࡧ࠾ࡵࡿࡴࡦࡵࡷ࠲ࡕࡿࡴࡦࡵࡷ࡛ࡦࡸ࡮ࡪࡰࡪࠦ୅"))
  arg.append(bstack1ll111l_opy_ (u"ࠤ࠰࡛ࠧ୆"))
  arg.append(bstack1ll111l_opy_ (u"ࠥ࡭࡬ࡴ࡯ࡳࡧ࠽ࡘ࡭࡫ࠠࡩࡱࡲ࡯࡮ࡳࡰ࡭ࠤେ"))
  global bstack11l1l1ll1_opy_
  global bstack1ll11lll_opy_
  global bstack1llll1l1ll_opy_
  global bstack11ll11111_opy_
  global bstack111ll11l_opy_
  global bstack1ll1lllll1_opy_
  global bstack111ll111l_opy_
  global bstack11l1l11l1_opy_
  global bstack11l1llll_opy_
  global bstack1ll11lll11_opy_
  global bstack1lll11l11_opy_
  global bstack1lllll11ll_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack11l1l1ll1_opy_ = webdriver.Remote.__init__
    bstack1ll11lll_opy_ = WebDriver.quit
    bstack111ll111l_opy_ = WebDriver.close
    bstack11l1l11l1_opy_ = WebDriver.get
  except Exception as e:
    pass
  if bstack1ll1l1l1ll_opy_(CONFIG):
    if bstack1l1111lll_opy_() < version.parse(bstack1ll1lll1ll_opy_):
      logger.error(bstack1ll11lllll_opy_.format(bstack1l1111lll_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack11l1llll_opy_ = RemoteConnection._get_proxy_url
      except Exception as e:
        logger.error(bstack1ll1l1ll_opy_.format(str(e)))
  try:
    from _pytest.config import Config
    bstack1ll11lll11_opy_ = Config.getoption
    from _pytest import runner
    bstack1lll11l11_opy_ = runner._update_current_test_var
  except Exception as e:
    logger.warn(e, bstack1l1111l1_opy_)
  try:
    from pytest_bdd import reporting
    bstack1lllll11ll_opy_ = reporting.runtest_makereport
  except Exception as e:
    logger.debug(bstack1ll111l_opy_ (u"ࠫࡕࡲࡥࡢࡵࡨࠤ࡮ࡴࡳࡵࡣ࡯ࡰࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡳࠥࡸࡵ࡯ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡴࡦࡵࡷࡷࠬୈ"))
  bstack11lll1lll_opy_ = CONFIG.get(bstack1ll111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ୉"), {}).get(bstack1ll111l_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ୊"))
  bstack11l1111l_opy_ = True
  bstack11l11l1ll_opy_(bstack111l11l11_opy_)
  os.environ[bstack1ll111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡕࡔࡇࡕࡒࡆࡓࡅࠨୋ")] = CONFIG[bstack1ll111l_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪୌ")]
  os.environ[bstack1ll111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡆࡇࡊ࡙ࡓࡠࡍࡈ࡝୍ࠬ")] = CONFIG[bstack1ll111l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭୎")]
  os.environ[bstack1ll111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠧ୏")] = bstack1ll1llllll_opy_.__str__()
  from _pytest.config import main as bstack111lllll_opy_
  bstack111lllll_opy_(arg)
def bstack11ll11l11_opy_(arg):
  bstack11l11l1ll_opy_(bstack11111l111_opy_)
  from behave.__main__ import main as bstack1lll1lll11_opy_
  bstack1lll1lll11_opy_(arg)
def bstack11ll11l1l_opy_():
  logger.info(bstack1lllll1ll_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack1ll111l_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫ୐"), help=bstack1ll111l_opy_ (u"࠭ࡇࡦࡰࡨࡶࡦࡺࡥࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡤࡱࡱࡪ࡮࡭ࠧ୑"))
  parser.add_argument(bstack1ll111l_opy_ (u"ࠧ࠮ࡷࠪ୒"), bstack1ll111l_opy_ (u"ࠨ࠯࠰ࡹࡸ࡫ࡲ࡯ࡣࡰࡩࠬ୓"), help=bstack1ll111l_opy_ (u"ࠩ࡜ࡳࡺࡸࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡵࡴࡧࡵࡲࡦࡳࡥࠨ୔"))
  parser.add_argument(bstack1ll111l_opy_ (u"ࠪ࠱ࡰ࠭୕"), bstack1ll111l_opy_ (u"ࠫ࠲࠳࡫ࡦࡻࠪୖ"), help=bstack1ll111l_opy_ (u"ࠬ࡟࡯ࡶࡴࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡤࡧࡨ࡫ࡳࡴࠢ࡮ࡩࡾ࠭ୗ"))
  parser.add_argument(bstack1ll111l_opy_ (u"࠭࠭ࡧࠩ୘"), bstack1ll111l_opy_ (u"ࠧ࠮࠯ࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ୙"), help=bstack1ll111l_opy_ (u"ࠨ࡛ࡲࡹࡷࠦࡴࡦࡵࡷࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧ୚"))
  bstack1lll1ll1ll_opy_ = parser.parse_args()
  try:
    bstack1llll1ll11_opy_ = bstack1ll111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡩࡨࡲࡪࡸࡩࡤ࠰ࡼࡱࡱ࠴ࡳࡢ࡯ࡳࡰࡪ࠭୛")
    if bstack1lll1ll1ll_opy_.framework and bstack1lll1ll1ll_opy_.framework not in (bstack1ll111l_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪଡ଼"), bstack1ll111l_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠷ࠬଢ଼")):
      bstack1llll1ll11_opy_ = bstack1ll111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࠮ࡺ࡯࡯࠲ࡸࡧ࡭ࡱ࡮ࡨࠫ୞")
    bstack1ll1l1l11_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1llll1ll11_opy_)
    bstack1llll1lll_opy_ = open(bstack1ll1l1l11_opy_, bstack1ll111l_opy_ (u"࠭ࡲࠨୟ"))
    bstack11lll11ll_opy_ = bstack1llll1lll_opy_.read()
    bstack1llll1lll_opy_.close()
    if bstack1lll1ll1ll_opy_.username:
      bstack11lll11ll_opy_ = bstack11lll11ll_opy_.replace(bstack1ll111l_opy_ (u"࡚ࠧࡑࡘࡖࡤ࡛ࡓࡆࡔࡑࡅࡒࡋࠧୠ"), bstack1lll1ll1ll_opy_.username)
    if bstack1lll1ll1ll_opy_.key:
      bstack11lll11ll_opy_ = bstack11lll11ll_opy_.replace(bstack1ll111l_opy_ (u"ࠨ࡛ࡒ࡙ࡗࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪୡ"), bstack1lll1ll1ll_opy_.key)
    if bstack1lll1ll1ll_opy_.framework:
      bstack11lll11ll_opy_ = bstack11lll11ll_opy_.replace(bstack1ll111l_opy_ (u"ࠩ࡜ࡓ࡚ࡘ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠪୢ"), bstack1lll1ll1ll_opy_.framework)
    file_name = bstack1ll111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱ࠭ୣ")
    file_path = os.path.abspath(file_name)
    bstack1ll11l11l_opy_ = open(file_path, bstack1ll111l_opy_ (u"ࠫࡼ࠭୤"))
    bstack1ll11l11l_opy_.write(bstack11lll11ll_opy_)
    bstack1ll11l11l_opy_.close()
    logger.info(bstack1l11l1ll1_opy_)
    try:
      os.environ[bstack1ll111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧ୥")] = bstack1lll1ll1ll_opy_.framework if bstack1lll1ll1ll_opy_.framework != None else bstack1ll111l_opy_ (u"ࠨࠢ୦")
      config = yaml.safe_load(bstack11lll11ll_opy_)
      config[bstack1ll111l_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧ୧")] = bstack1ll111l_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠮ࡵࡨࡸࡺࡶࠧ୨")
      bstack1ll11llll_opy_(bstack1ll111ll_opy_, config)
    except Exception as e:
      logger.debug(bstack1lll1l111_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack11l1l1111_opy_.format(str(e)))
def bstack1ll11llll_opy_(bstack1ll11l1l_opy_, config, bstack1l1l1l11l_opy_={}):
  global bstack1ll1llllll_opy_
  if not config:
    return
  bstack11ll11lll_opy_ = bstack11ll111l_opy_ if not bstack1ll1llllll_opy_ else (
    bstack11ll1l111_opy_ if bstack1ll111l_opy_ (u"ࠩࡤࡴࡵ࠭୩") in config else bstack1llll11l11_opy_)
  data = {
    bstack1ll111l_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬ୪"): config[bstack1ll111l_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭୫")],
    bstack1ll111l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ୬"): config[bstack1ll111l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ୭")],
    bstack1ll111l_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫ୮"): bstack1ll11l1l_opy_,
    bstack1ll111l_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡱࡴࡲࡴࡪࡸࡴࡪࡧࡶࠫ୯"): {
      bstack1ll111l_opy_ (u"ࠩ࡯ࡥࡳ࡭ࡵࡢࡩࡨࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧ୰"): str(config[bstack1ll111l_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪୱ")]) if bstack1ll111l_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫ୲") in config else bstack1ll111l_opy_ (u"ࠧࡻ࡮࡬ࡰࡲࡻࡳࠨ୳"),
      bstack1ll111l_opy_ (u"࠭ࡲࡦࡨࡨࡶࡷ࡫ࡲࠨ୴"): bstack11111l1ll_opy_(os.getenv(bstack1ll111l_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠤ୵"), bstack1ll111l_opy_ (u"ࠣࠤ୶"))),
      bstack1ll111l_opy_ (u"ࠩ࡯ࡥࡳ࡭ࡵࡢࡩࡨࠫ୷"): bstack1ll111l_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪ୸"),
      bstack1ll111l_opy_ (u"ࠫࡵࡸ࡯ࡥࡷࡦࡸࠬ୹"): bstack11ll11lll_opy_,
      bstack1ll111l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ୺"): config[bstack1ll111l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ୻")] if config[bstack1ll111l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ୼")] else bstack1ll111l_opy_ (u"ࠣࡷࡱ࡯ࡳࡵࡷ࡯ࠤ୽"),
      bstack1ll111l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ୾"): str(config[bstack1ll111l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ୿")]) if bstack1ll111l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭஀") in config else bstack1ll111l_opy_ (u"ࠧࡻ࡮࡬ࡰࡲࡻࡳࠨ஁"),
      bstack1ll111l_opy_ (u"࠭࡯ࡴࠩஂ"): sys.platform,
      bstack1ll111l_opy_ (u"ࠧࡩࡱࡶࡸࡳࡧ࡭ࡦࠩஃ"): socket.gethostname()
    }
  }
  update(data[bstack1ll111l_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡱࡴࡲࡴࡪࡸࡴࡪࡧࡶࠫ஄")], bstack1l1l1l11l_opy_)
  try:
    response = bstack1l1l11l11_opy_(bstack1ll111l_opy_ (u"ࠩࡓࡓࡘ࡚ࠧஅ"), bstack1ll1ll1111_opy_(bstack1lll1l11_opy_), data, {
      bstack1ll111l_opy_ (u"ࠪࡥࡺࡺࡨࠨஆ"): (config[bstack1ll111l_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭இ")], config[bstack1ll111l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨஈ")])
    })
    if response:
      logger.debug(bstack1ll1l11ll_opy_.format(bstack1ll11l1l_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack11111ll1_opy_.format(str(e)))
def bstack11111l1ll_opy_(framework):
  return bstack1ll111l_opy_ (u"ࠨࡻࡾ࠯ࡳࡽࡹ࡮࡯࡯ࡣࡪࡩࡳࡺ࠯ࡼࡿࠥஉ").format(str(framework), __version__) if framework else bstack1ll111l_opy_ (u"ࠢࡱࡻࡷ࡬ࡴࡴࡡࡨࡧࡱࡸ࠴ࢁࡽࠣஊ").format(
    __version__)
def bstack1l1l1lll1_opy_():
  global CONFIG
  if bool(CONFIG):
    return
  try:
    bstack1111l11l1_opy_()
    logger.debug(bstack11llll1ll_opy_.format(str(CONFIG)))
    bstack1ll1l1l1l_opy_()
    bstack1ll1l1l1l1_opy_()
  except Exception as e:
    logger.error(bstack1ll111l_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࡶࡲ࠯ࠤࡪࡸࡲࡰࡴ࠽ࠤࠧ஋") + str(e))
    sys.exit(1)
  sys.excepthook = bstack1ll1111ll_opy_
  atexit.register(bstack1l11l11l_opy_)
  signal.signal(signal.SIGINT, bstack1ll1111l1_opy_)
  signal.signal(signal.SIGTERM, bstack1ll1111l1_opy_)
def bstack1ll1111ll_opy_(exctype, value, traceback):
  global bstack1l11lllll_opy_
  try:
    for driver in bstack1l11lllll_opy_:
      driver.execute_script(
        bstack1ll111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡵࡷࡥࡹࡻࡳࠣ࠼ࠥࡪࡦ࡯࡬ࡦࡦࠥ࠰ࠥࠨࡲࡦࡣࡶࡳࡳࠨ࠺ࠡࠩ஌") + json.dumps(
          bstack1ll111l_opy_ (u"ࠥࡗࡪࡹࡳࡪࡱࡱࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡼ࡯ࡴࡩ࠼ࠣࡠࡳࠨ஍") + str(value)) + bstack1ll111l_opy_ (u"ࠫࢂࢃࠧஎ"))
  except Exception:
    pass
  bstack11ll1l1ll_opy_(value)
  sys.__excepthook__(exctype, value, traceback)
  sys.exit(1)
def bstack11ll1l1ll_opy_(message=bstack1ll111l_opy_ (u"ࠬ࠭ஏ")):
  global CONFIG
  try:
    if message:
      bstack1l1l1l11l_opy_ = {
        bstack1ll111l_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬஐ"): str(message)
      }
      bstack1ll11llll_opy_(bstack1l11l1l1l_opy_, CONFIG, bstack1l1l1l11l_opy_)
    else:
      bstack1ll11llll_opy_(bstack1l11l1l1l_opy_, CONFIG)
  except Exception as e:
    logger.debug(bstack1l1lll11_opy_.format(str(e)))
def bstack1llllllll_opy_(bstack1lll11ll1_opy_, size):
  bstack11lll111_opy_ = []
  while len(bstack1lll11ll1_opy_) > size:
    bstack11l111l1_opy_ = bstack1lll11ll1_opy_[:size]
    bstack11lll111_opy_.append(bstack11l111l1_opy_)
    bstack1lll11ll1_opy_ = bstack1lll11ll1_opy_[size:]
  bstack11lll111_opy_.append(bstack1lll11ll1_opy_)
  return bstack11lll111_opy_
def bstack111111lll_opy_(args):
  if bstack1ll111l_opy_ (u"ࠧ࠮࡯ࠪ஑") in args and bstack1ll111l_opy_ (u"ࠨࡲࡧࡦࠬஒ") in args:
    return True
  return False
def run_on_browserstack(bstack11ll11ll1_opy_=None, bstack1lllllll11_opy_=None, bstack11l1ll1l_opy_=False):
  global CONFIG
  global bstack1llll11l_opy_
  global bstack1lll11l1l1_opy_
  bstack1llll11l1_opy_ = bstack1ll111l_opy_ (u"ࠩࠪஓ")
  bstack11111lll1_opy_(bstack1111l1l1_opy_, logger)
  if bstack11ll11ll1_opy_ and isinstance(bstack11ll11ll1_opy_, str):
    bstack11ll11ll1_opy_ = eval(bstack11ll11ll1_opy_)
  if bstack11ll11ll1_opy_:
    CONFIG = bstack11ll11ll1_opy_[bstack1ll111l_opy_ (u"ࠪࡇࡔࡔࡆࡊࡉࠪஔ")]
    bstack1llll11l_opy_ = bstack11ll11ll1_opy_[bstack1ll111l_opy_ (u"ࠫࡍ࡛ࡂࡠࡗࡕࡐࠬக")]
    bstack1lll11l1l1_opy_ = bstack11ll11ll1_opy_[bstack1ll111l_opy_ (u"ࠬࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧ஖")]
    bstack1ll1ll111_opy_.bstack1ll11ll1ll_opy_(bstack1ll111l_opy_ (u"࠭ࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨ஗"), bstack1lll11l1l1_opy_)
    bstack1llll11l1_opy_ = bstack1ll111l_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧ஘")
  if not bstack11l1ll1l_opy_:
    if len(sys.argv) <= 1:
      logger.critical(bstack1ll1llll1_opy_)
      return
    if sys.argv[1] == bstack1ll111l_opy_ (u"ࠨ࠯࠰ࡺࡪࡸࡳࡪࡱࡱࠫங") or sys.argv[1] == bstack1ll111l_opy_ (u"ࠩ࠰ࡺࠬச"):
      logger.info(bstack1ll111l_opy_ (u"ࠪࡆࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡓࡽࡹ࡮࡯࡯ࠢࡖࡈࡐࠦࡶࡼࡿࠪ஛").format(__version__))
      return
    if sys.argv[1] == bstack1ll111l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪஜ"):
      bstack11ll11l1l_opy_()
      return
  args = sys.argv
  bstack1l1l1lll1_opy_()
  global bstack1lll1ll11_opy_
  global bstack11l1111l_opy_
  global bstack11l11ll1l_opy_
  global bstack1llllll111_opy_
  global bstack11lll1lll_opy_
  global bstack1l1l1ll1_opy_
  global bstack11ll1111_opy_
  global bstack1ll111l11_opy_
  global bstack1llll1111_opy_
  if not bstack1llll11l1_opy_:
    if args[1] == bstack1ll111l_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ஝") or args[1] == bstack1ll111l_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠹ࠧஞ"):
      bstack1llll11l1_opy_ = bstack1ll111l_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧட")
      args = args[2:]
    elif args[1] == bstack1ll111l_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ஠"):
      bstack1llll11l1_opy_ = bstack1ll111l_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ஡")
      args = args[2:]
    elif args[1] == bstack1ll111l_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩ஢"):
      bstack1llll11l1_opy_ = bstack1ll111l_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪண")
      args = args[2:]
    elif args[1] == bstack1ll111l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭த"):
      bstack1llll11l1_opy_ = bstack1ll111l_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧ஥")
      args = args[2:]
    elif args[1] == bstack1ll111l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ஦"):
      bstack1llll11l1_opy_ = bstack1ll111l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ஧")
      args = args[2:]
    elif args[1] == bstack1ll111l_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩந"):
      bstack1llll11l1_opy_ = bstack1ll111l_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪன")
      args = args[2:]
    else:
      if not bstack1ll111l_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧப") in CONFIG or str(CONFIG[bstack1ll111l_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ஫")]).lower() in [bstack1ll111l_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭஬"), bstack1ll111l_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴ࠳ࠨ஭")]:
        bstack1llll11l1_opy_ = bstack1ll111l_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨம")
        args = args[1:]
      elif str(CONFIG[bstack1ll111l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬய")]).lower() == bstack1ll111l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩர"):
        bstack1llll11l1_opy_ = bstack1ll111l_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪற")
        args = args[1:]
      elif str(CONFIG[bstack1ll111l_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨல")]).lower() == bstack1ll111l_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬள"):
        bstack1llll11l1_opy_ = bstack1ll111l_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭ழ")
        args = args[1:]
      elif str(CONFIG[bstack1ll111l_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫவ")]).lower() == bstack1ll111l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩஶ"):
        bstack1llll11l1_opy_ = bstack1ll111l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪஷ")
        args = args[1:]
      elif str(CONFIG[bstack1ll111l_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧஸ")]).lower() == bstack1ll111l_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬஹ"):
        bstack1llll11l1_opy_ = bstack1ll111l_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭஺")
        args = args[1:]
      else:
        os.environ[bstack1ll111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠩ஻")] = bstack1llll11l1_opy_
        bstack1llllll11l_opy_(bstack1lll1l1ll1_opy_)
  global bstack1ll1ll11l_opy_
  if bstack11ll11ll1_opy_:
    try:
      os.environ[bstack1ll111l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠪ஼")] = bstack1llll11l1_opy_
      bstack1ll11llll_opy_(bstack111l1lll1_opy_, CONFIG)
    except Exception as e:
      logger.debug(bstack1l1lll11_opy_.format(str(e)))
  global bstack11l1l1ll1_opy_
  global bstack1ll11lll_opy_
  global bstack1ll111l1_opy_
  global bstack111lllll1_opy_
  global bstack1llll1111l_opy_
  global bstack1llll1l1ll_opy_
  global bstack11ll11111_opy_
  global bstack111ll1l11_opy_
  global bstack111ll11l_opy_
  global bstack1ll1lllll1_opy_
  global bstack111ll111l_opy_
  global bstack1111lll1l_opy_
  global bstack111ll111_opy_
  global bstack11l1l11l1_opy_
  global bstack11l1llll_opy_
  global bstack1ll11lll11_opy_
  global bstack1lll11l11_opy_
  global bstack1lllllll1_opy_
  global bstack1lllll11ll_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack11l1l1ll1_opy_ = webdriver.Remote.__init__
    bstack1ll11lll_opy_ = WebDriver.quit
    bstack111ll111l_opy_ = WebDriver.close
    bstack11l1l11l1_opy_ = WebDriver.get
  except Exception as e:
    pass
  try:
    import Browser
    from subprocess import Popen
    bstack1ll1ll11l_opy_ = Popen.__init__
  except Exception as e:
    pass
  if bstack1ll1l1l1ll_opy_(CONFIG):
    if bstack1l1111lll_opy_() < version.parse(bstack1ll1lll1ll_opy_):
      logger.error(bstack1ll11lllll_opy_.format(bstack1l1111lll_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack11l1llll_opy_ = RemoteConnection._get_proxy_url
      except Exception as e:
        logger.error(bstack1ll1l1ll_opy_.format(str(e)))
  if bstack1llll11l1_opy_ != bstack1ll111l_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩ஽") or (bstack1llll11l1_opy_ == bstack1ll111l_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪா") and not bstack11ll11ll1_opy_):
    bstack1ll1ll1lll_opy_()
  if (bstack1llll11l1_opy_ in [bstack1ll111l_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪி"), bstack1ll111l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫீ"), bstack1ll111l_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧு")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCreator._get_ff_profile = bstack1lll1111l_opy_
        bstack1llll1111l_opy_ = WebDriverCache.close
      except Exception as e:
        logger.warn(bstack1111lll11_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        bstack111lllll1_opy_ = ApplicationCache.close
      except Exception as e:
        logger.debug(bstack1lll11llll_opy_ + str(e))
    except Exception as e:
      bstack1l1lll1l1_opy_(e, bstack1111lll11_opy_)
    if bstack1llll11l1_opy_ != bstack1ll111l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨூ"):
      bstack11111l1l_opy_()
    bstack1ll111l1_opy_ = Output.end_test
    bstack1llll1l1ll_opy_ = TestStatus.__init__
    bstack111ll1l11_opy_ = pabot._run
    bstack111ll11l_opy_ = QueueItem.__init__
    bstack1ll1lllll1_opy_ = pabot._create_command_for_execution
    bstack1lllllll1_opy_ = pabot._report_results
  if bstack1llll11l1_opy_ == bstack1ll111l_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨ௃"):
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1l1lll1l1_opy_(e, bstack1l11111ll_opy_)
    bstack1111lll1l_opy_ = Runner.run_hook
    bstack111ll111_opy_ = Step.run
  if bstack1ll111l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ௄") in CONFIG and CONFIG[bstack1ll111l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ௅")] == True:
    os.environ[bstack1ll111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠ࡛ࡐࡐࠬெ")] = bstack1ll111l_opy_ (u"ࠬࡺࡲࡶࡧࠪே")
  if bstack1ll111l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ை") in CONFIG:
    os.environ[bstack1ll111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨ௉")] = json.dumps(CONFIG[bstack1ll111l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨொ")])
  os.environ[bstack1ll111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡐࡍࡃࡗࡊࡔࡘࡍࠨோ")] = bstack1ll111l_opy_ (u"ࠪࡸࡷࡻࡥࠨௌ") if any([p.get(bstack1ll111l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼ்ࠫ"), False) == True for p in CONFIG[bstack1ll111l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ௎")]]) else bstack1ll111l_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬ௏")
  if bstack1llll11l1_opy_ == bstack1ll111l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧௐ"):
    try:
      bstack11llllll1_opy_.launch(CONFIG, {
        bstack1ll111l_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦࠩ௑"): bstack1ll111l_opy_ (u"ࠩࡓࡽࡹ࡫ࡳࡵ࠯ࡦࡹࡨࡻ࡭ࡣࡧࡵࠫ௒") if bstack111l1ll1_opy_() else bstack1ll111l_opy_ (u"ࠪࡔࡾࡺࡥࡴࡶࠪ௓"),
        bstack1ll111l_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ௔"): bstack1111ll1l_opy_.version(),
        bstack1ll111l_opy_ (u"ࠬࡹࡤ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪ௕"): __version__
      })
      if bstack1ll1llllll_opy_ and bstack1ll111l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭௖") in CONFIG and CONFIG[bstack1ll111l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧௗ")] == True:
        bstack1lll11l1ll_opy_, bstack1l1lll11l_opy_ = bstack111l111l1_opy_(CONFIG, bstack1llll11l1_opy_, bstack1111ll1l_opy_.version());
        if not bstack1lll11l1ll_opy_ is None:
          os.environ[bstack1ll111l_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭௘")] = bstack1lll11l1ll_opy_;
          os.environ[bstack1ll111l_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡘࡊ࡙ࡔࡠࡔࡘࡒࡤࡏࡄࠨ௙")] = str(bstack1l1lll11l_opy_);
      from _pytest.config import Config
      bstack1ll11lll11_opy_ = Config.getoption
      from _pytest import runner
      bstack1lll11l11_opy_ = runner._update_current_test_var
    except Exception as e:
      logger.warn(e, bstack1l1111l1_opy_)
    try:
      from pytest_bdd import reporting
      bstack1lllll11ll_opy_ = reporting.runtest_makereport
    except Exception as e:
      logger.debug(bstack1ll111l_opy_ (u"ࠪࡔࡱ࡫ࡡࡴࡧࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡲࠤࡷࡻ࡮ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺࡥࡴࡶࡶࠫ௚"))
  if bstack1llll11l1_opy_ == bstack1ll111l_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫ௛"):
    bstack11l1111l_opy_ = True
    if bstack11ll11ll1_opy_ and bstack11l1ll1l_opy_:
      bstack11lll1lll_opy_ = CONFIG.get(bstack1ll111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ௜"), {}).get(bstack1ll111l_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ௝"))
      bstack11l11l1ll_opy_(bstack11llll1l1_opy_)
    elif bstack11ll11ll1_opy_:
      bstack11lll1lll_opy_ = CONFIG.get(bstack1ll111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫ௞"), {}).get(bstack1ll111l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ௟"))
      global bstack1l11lllll_opy_
      try:
        if bstack111111lll_opy_(bstack11ll11ll1_opy_[bstack1ll111l_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ௠")]) and multiprocessing.current_process().name == bstack1ll111l_opy_ (u"ࠪ࠴ࠬ௡"):
          bstack11ll11ll1_opy_[bstack1ll111l_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧ௢")].remove(bstack1ll111l_opy_ (u"ࠬ࠳࡭ࠨ௣"))
          bstack11ll11ll1_opy_[bstack1ll111l_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ௤")].remove(bstack1ll111l_opy_ (u"ࠧࡱࡦࡥࠫ௥"))
          bstack11ll11ll1_opy_[bstack1ll111l_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ௦")] = bstack11ll11ll1_opy_[bstack1ll111l_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ௧")][0]
          with open(bstack11ll11ll1_opy_[bstack1ll111l_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭௨")], bstack1ll111l_opy_ (u"ࠫࡷ࠭௩")) as f:
            bstack1lll1llll_opy_ = f.read()
          bstack11l111l11_opy_ = bstack1ll111l_opy_ (u"ࠧࠨࠢࡧࡴࡲࡱࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡸࡪ࡫ࠡ࡫ࡰࡴࡴࡸࡴࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡪࡰ࡬ࡸ࡮ࡧ࡬ࡪࡼࡨ࠿ࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣ࡮ࡴࡩࡵ࡫ࡤࡰ࡮ࢀࡥࠩࡽࢀ࠭ࡀࠦࡦࡳࡱࡰࠤࡵࡪࡢࠡ࡫ࡰࡴࡴࡸࡴࠡࡒࡧࡦࡀࠦ࡯ࡨࡡࡧࡦࠥࡃࠠࡑࡦࡥ࠲ࡩࡵ࡟ࡣࡴࡨࡥࡰࡁࠊࡥࡧࡩࠤࡲࡵࡤࡠࡤࡵࡩࡦࡱࠨࡴࡧ࡯ࡪ࠱ࠦࡡࡳࡩ࠯ࠤࡹ࡫࡭ࡱࡱࡵࡥࡷࡿࠠ࠾ࠢ࠳࠭࠿ࠐࠠࠡࡶࡵࡽ࠿ࠐࠠࠡࠢࠣࡥࡷ࡭ࠠ࠾ࠢࡶࡸࡷ࠮ࡩ࡯ࡶࠫࡥࡷ࡭ࠩࠬ࠳࠳࠭ࠏࠦࠠࡦࡺࡦࡩࡵࡺࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡥࡸࠦࡥ࠻ࠌࠣࠤࠥࠦࡰࡢࡵࡶࠎࠥࠦ࡯ࡨࡡࡧࡦ࠭ࡹࡥ࡭ࡨ࠯ࡥࡷ࡭ࠬࡵࡧࡰࡴࡴࡸࡡࡳࡻࠬࠎࡕࡪࡢ࠯ࡦࡲࡣࡧࠦ࠽ࠡ࡯ࡲࡨࡤࡨࡲࡦࡣ࡮ࠎࡕࡪࡢ࠯ࡦࡲࡣࡧࡸࡥࡢ࡭ࠣࡁࠥࡳ࡯ࡥࡡࡥࡶࡪࡧ࡫ࠋࡒࡧࡦ࠭࠯࠮ࡴࡧࡷࡣࡹࡸࡡࡤࡧࠫ࠭ࡡࡴࠢࠣࠤ௪").format(str(bstack11ll11ll1_opy_))
          bstack11111ll1l_opy_ = bstack11l111l11_opy_ + bstack1lll1llll_opy_
          bstack11l1lll11_opy_ = bstack11ll11ll1_opy_[bstack1ll111l_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ௫")] + bstack1ll111l_opy_ (u"ࠧࡠࡤࡶࡸࡦࡩ࡫ࡠࡶࡨࡱࡵ࠴ࡰࡺࠩ௬")
          with open(bstack11l1lll11_opy_, bstack1ll111l_opy_ (u"ࠨࡹࠪ௭")):
            pass
          with open(bstack11l1lll11_opy_, bstack1ll111l_opy_ (u"ࠤࡺ࠯ࠧ௮")) as f:
            f.write(bstack11111ll1l_opy_)
          import subprocess
          bstack1l1l1l1ll_opy_ = subprocess.run([bstack1ll111l_opy_ (u"ࠥࡴࡾࡺࡨࡰࡰࠥ௯"), bstack11l1lll11_opy_])
          if os.path.exists(bstack11l1lll11_opy_):
            os.unlink(bstack11l1lll11_opy_)
          os._exit(bstack1l1l1l1ll_opy_.returncode)
        else:
          if bstack111111lll_opy_(bstack11ll11ll1_opy_[bstack1ll111l_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧ௰")]):
            bstack11ll11ll1_opy_[bstack1ll111l_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ௱")].remove(bstack1ll111l_opy_ (u"࠭࠭࡮ࠩ௲"))
            bstack11ll11ll1_opy_[bstack1ll111l_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪ௳")].remove(bstack1ll111l_opy_ (u"ࠨࡲࡧࡦࠬ௴"))
            bstack11ll11ll1_opy_[bstack1ll111l_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ௵")] = bstack11ll11ll1_opy_[bstack1ll111l_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭௶")][0]
          bstack11l11l1ll_opy_(bstack11llll1l1_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(bstack11ll11ll1_opy_[bstack1ll111l_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧ௷")])))
          sys.argv = sys.argv[2:]
          mod_globals = globals()
          mod_globals[bstack1ll111l_opy_ (u"ࠬࡥ࡟࡯ࡣࡰࡩࡤࡥࠧ௸")] = bstack1ll111l_opy_ (u"࠭࡟ࡠ࡯ࡤ࡭ࡳࡥ࡟ࠨ௹")
          mod_globals[bstack1ll111l_opy_ (u"ࠧࡠࡡࡩ࡭ࡱ࡫࡟ࡠࠩ௺")] = os.path.abspath(bstack11ll11ll1_opy_[bstack1ll111l_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ௻")])
          exec(open(bstack11ll11ll1_opy_[bstack1ll111l_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ௼")]).read(), mod_globals)
      except BaseException as e:
        try:
          traceback.print_exc()
          logger.error(bstack1ll111l_opy_ (u"ࠪࡇࡦࡻࡧࡩࡶࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࡀࠠࡼࡿࠪ௽").format(str(e)))
          for driver in bstack1l11lllll_opy_:
            bstack1lllllll11_opy_.append({
              bstack1ll111l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ௾"): bstack11ll11ll1_opy_[bstack1ll111l_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ௿")],
              bstack1ll111l_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬఀ"): str(e),
              bstack1ll111l_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭ఁ"): multiprocessing.current_process().name
            })
            driver.execute_script(
              bstack1ll111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡴࡶࡤࡸࡺࡹࠢ࠻ࠤࡩࡥ࡮ࡲࡥࡥࠤ࠯ࠤࠧࡸࡥࡢࡵࡲࡲࠧࡀࠠࠨం") + json.dumps(
                bstack1ll111l_opy_ (u"ࠤࡖࡩࡸࡹࡩࡰࡰࠣࡪࡦ࡯࡬ࡦࡦࠣࡻ࡮ࡺࡨ࠻ࠢ࡟ࡲࠧః") + str(e)) + bstack1ll111l_opy_ (u"ࠪࢁࢂ࠭ఄ"))
        except Exception:
          pass
      finally:
        try:
          for driver in bstack1l11lllll_opy_:
            driver.quit()
        except Exception as e:
          pass
    else:
      percy.init(bstack1lll11l1l1_opy_, CONFIG, logger)
      bstack1ll1l111l_opy_()
      bstack1ll11l1lll_opy_()
      bstack1ll1ll11_opy_ = {
        bstack1ll111l_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧఅ"): args[0],
        bstack1ll111l_opy_ (u"ࠬࡉࡏࡏࡈࡌࡋࠬఆ"): CONFIG,
        bstack1ll111l_opy_ (u"࠭ࡈࡖࡄࡢ࡙ࡗࡒࠧఇ"): bstack1llll11l_opy_,
        bstack1ll111l_opy_ (u"ࠧࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩఈ"): bstack1lll11l1l1_opy_
      }
      percy.bstack1lllll11l1_opy_()
      if bstack1ll111l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫఉ") in CONFIG:
        bstack11111l11_opy_ = []
        manager = multiprocessing.Manager()
        bstack111l1l11_opy_ = manager.list()
        if bstack111111lll_opy_(args):
          for index, platform in enumerate(CONFIG[bstack1ll111l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬఊ")]):
            if index == 0:
              bstack1ll1ll11_opy_[bstack1ll111l_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ఋ")] = args
            bstack11111l11_opy_.append(multiprocessing.Process(name=str(index),
                                                       target=run_on_browserstack,
                                                       args=(bstack1ll1ll11_opy_, bstack111l1l11_opy_)))
        else:
          for index, platform in enumerate(CONFIG[bstack1ll111l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧఌ")]):
            bstack11111l11_opy_.append(multiprocessing.Process(name=str(index),
                                                       target=run_on_browserstack,
                                                       args=(bstack1ll1ll11_opy_, bstack111l1l11_opy_)))
        for t in bstack11111l11_opy_:
          t.start()
        for t in bstack11111l11_opy_:
          t.join()
        bstack11ll1111_opy_ = list(bstack111l1l11_opy_)
      else:
        if bstack111111lll_opy_(args):
          bstack1ll1ll11_opy_[bstack1ll111l_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ఍")] = args
          test = multiprocessing.Process(name=str(0),
                                         target=run_on_browserstack, args=(bstack1ll1ll11_opy_,))
          test.start()
          test.join()
        else:
          bstack11l11l1ll_opy_(bstack11llll1l1_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(args[0])))
          mod_globals = globals()
          mod_globals[bstack1ll111l_opy_ (u"࠭࡟ࡠࡰࡤࡱࡪࡥ࡟ࠨఎ")] = bstack1ll111l_opy_ (u"ࠧࡠࡡࡰࡥ࡮ࡴ࡟ࡠࠩఏ")
          mod_globals[bstack1ll111l_opy_ (u"ࠨࡡࡢࡪ࡮ࡲࡥࡠࡡࠪఐ")] = os.path.abspath(args[0])
          sys.argv = sys.argv[2:]
          exec(open(args[0]).read(), mod_globals)
  elif bstack1llll11l1_opy_ == bstack1ll111l_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨ఑") or bstack1llll11l1_opy_ == bstack1ll111l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩఒ"):
    try:
      from pabot import pabot
    except Exception as e:
      bstack1l1lll1l1_opy_(e, bstack1111lll11_opy_)
    bstack1ll1l111l_opy_()
    bstack11l11l1ll_opy_(bstack1lll1lll_opy_)
    if bstack1ll111l_opy_ (u"ࠫ࠲࠳ࡰࡳࡱࡦࡩࡸࡹࡥࡴࠩఓ") in args:
      i = args.index(bstack1ll111l_opy_ (u"ࠬ࠳࠭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪఔ"))
      args.pop(i)
      args.pop(i)
    args.insert(0, str(bstack1lll1ll11_opy_))
    args.insert(0, str(bstack1ll111l_opy_ (u"࠭࠭࠮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫక")))
    pabot.main(args)
  elif bstack1llll11l1_opy_ == bstack1ll111l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨఖ"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack1l1lll1l1_opy_(e, bstack1111lll11_opy_)
    for a in args:
      if bstack1ll111l_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡑࡎࡄࡘࡋࡕࡒࡎࡋࡑࡈࡊ࡞ࠧగ") in a:
        bstack1llllll111_opy_ = int(a.split(bstack1ll111l_opy_ (u"ࠩ࠽ࠫఘ"))[1])
      if bstack1ll111l_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡇࡉࡋࡒࡏࡄࡃࡏࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧఙ") in a:
        bstack11lll1lll_opy_ = str(a.split(bstack1ll111l_opy_ (u"ࠫ࠿࠭చ"))[1])
      if bstack1ll111l_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡈࡒࡉࡂࡔࡊࡗࠬఛ") in a:
        bstack1l1l1ll1_opy_ = str(a.split(bstack1ll111l_opy_ (u"࠭࠺ࠨజ"))[1])
    bstack1lll1l1l1_opy_ = None
    if bstack1ll111l_opy_ (u"ࠧ࠮࠯ࡥࡷࡹࡧࡣ࡬ࡡ࡬ࡸࡪࡳ࡟ࡪࡰࡧࡩࡽ࠭ఝ") in args:
      i = args.index(bstack1ll111l_opy_ (u"ࠨ࠯࠰ࡦࡸࡺࡡࡤ࡭ࡢ࡭ࡹ࡫࡭ࡠ࡫ࡱࡨࡪࡾࠧఞ"))
      args.pop(i)
      bstack1lll1l1l1_opy_ = args.pop(i)
    if bstack1lll1l1l1_opy_ is not None:
      global bstack11l1ll1l1_opy_
      bstack11l1ll1l1_opy_ = bstack1lll1l1l1_opy_
    bstack11l11l1ll_opy_(bstack1lll1lll_opy_)
    run_cli(args)
  elif bstack1llll11l1_opy_ == bstack1ll111l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩట"):
    bstack1lllll11l_opy_ = bstack1111ll1l_opy_(args, logger, CONFIG, bstack1ll1llllll_opy_)
    bstack1lllll11l_opy_.bstack11111111l_opy_()
    bstack1ll1l111l_opy_()
    bstack11l11ll1l_opy_ = True
    bstack1llll1111_opy_ = bstack1lllll11l_opy_.bstack1l1llll1_opy_()
    bstack1lllll11l_opy_.bstack1ll1ll11_opy_(bstack11l1111l1_opy_)
    bstack1ll111l11_opy_ = bstack1lllll11l_opy_.bstack111l111ll_opy_(bstack1l111l11l_opy_, {
      bstack1ll111l_opy_ (u"ࠪࡌ࡚ࡈ࡟ࡖࡔࡏࠫఠ"): bstack1llll11l_opy_,
      bstack1ll111l_opy_ (u"ࠫࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭డ"): bstack1lll11l1l1_opy_,
      bstack1ll111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨఢ"): bstack1ll1llllll_opy_
    })
  elif bstack1llll11l1_opy_ == bstack1ll111l_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭ణ"):
    try:
      from behave.__main__ import main as bstack1lll1lll11_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack1l1lll1l1_opy_(e, bstack1l11111ll_opy_)
    bstack1ll1l111l_opy_()
    bstack11l11ll1l_opy_ = True
    bstack1l1l111ll_opy_ = 1
    if bstack1ll111l_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧత") in CONFIG:
      bstack1l1l111ll_opy_ = CONFIG[bstack1ll111l_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨథ")]
    bstack1l1111ll_opy_ = int(bstack1l1l111ll_opy_) * int(len(CONFIG[bstack1ll111l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬద")]))
    config = Configuration(args)
    bstack11l1ll11_opy_ = config.paths
    if len(bstack11l1ll11_opy_) == 0:
      import glob
      pattern = bstack1ll111l_opy_ (u"ࠪ࠮࠯࠵ࠪ࠯ࡨࡨࡥࡹࡻࡲࡦࠩధ")
      bstack111lll11_opy_ = glob.glob(pattern, recursive=True)
      args.extend(bstack111lll11_opy_)
      config = Configuration(args)
      bstack11l1ll11_opy_ = config.paths
    bstack111l1l1ll_opy_ = [os.path.normpath(item) for item in bstack11l1ll11_opy_]
    bstack1l111lll1_opy_ = [os.path.normpath(item) for item in args]
    bstack1l111l11_opy_ = [item for item in bstack1l111lll1_opy_ if item not in bstack111l1l1ll_opy_]
    import platform as pf
    if pf.system().lower() == bstack1ll111l_opy_ (u"ࠫࡼ࡯࡮ࡥࡱࡺࡷࠬన"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack111l1l1ll_opy_ = [str(PurePosixPath(PureWindowsPath(bstack11l1111ll_opy_)))
                    for bstack11l1111ll_opy_ in bstack111l1l1ll_opy_]
    bstack1ll1l1lll1_opy_ = []
    for spec in bstack111l1l1ll_opy_:
      bstack1l1llll11_opy_ = []
      bstack1l1llll11_opy_ += bstack1l111l11_opy_
      bstack1l1llll11_opy_.append(spec)
      bstack1ll1l1lll1_opy_.append(bstack1l1llll11_opy_)
    execution_items = []
    for bstack1l1llll11_opy_ in bstack1ll1l1lll1_opy_:
      for index, _ in enumerate(CONFIG[bstack1ll111l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ఩")]):
        item = {}
        item[bstack1ll111l_opy_ (u"࠭ࡡࡳࡩࠪప")] = bstack1ll111l_opy_ (u"ࠧࠡࠩఫ").join(bstack1l1llll11_opy_)
        item[bstack1ll111l_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧబ")] = index
        execution_items.append(item)
    bstack11llllll_opy_ = bstack1llllllll_opy_(execution_items, bstack1l1111ll_opy_)
    for execution_item in bstack11llllll_opy_:
      bstack11111l11_opy_ = []
      for item in execution_item:
        bstack11111l11_opy_.append(bstack111lll111_opy_(name=str(item[bstack1ll111l_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨభ")]),
                                             target=bstack11ll11l11_opy_,
                                             args=(item[bstack1ll111l_opy_ (u"ࠪࡥࡷ࡭ࠧమ")],)))
      for t in bstack11111l11_opy_:
        t.start()
      for t in bstack11111l11_opy_:
        t.join()
  else:
    bstack1llllll11l_opy_(bstack1lll1l1ll1_opy_)
  if not bstack11ll11ll1_opy_:
    bstack1l11l11l1_opy_()
def browserstack_initialize(bstack1111l1l1l_opy_=None):
  run_on_browserstack(bstack1111l1l1l_opy_, None, True)
def bstack1l11l11l1_opy_():
  global CONFIG
  bstack11llllll1_opy_.stop()
  bstack11llllll1_opy_.bstack1llll111_opy_()
  if bstack1111l1ll_opy_(CONFIG):
    bstack1lll111ll_opy_()
  [bstack1lll1ll1l1_opy_, bstack1ll11l1ll_opy_] = bstack11111llll_opy_()
  if bstack1lll1ll1l1_opy_ is not None and bstack11l1ll111_opy_() != -1:
    sessions = bstack1ll1lll111_opy_(bstack1lll1ll1l1_opy_)
    bstack1lll1ll11l_opy_(sessions, bstack1ll11l1ll_opy_)
def bstack11lll111l_opy_(bstack11ll11ll_opy_):
  if bstack11ll11ll_opy_:
    return bstack11ll11ll_opy_.capitalize()
  else:
    return bstack11ll11ll_opy_
def bstack11ll1l11_opy_(bstack1lllll11_opy_):
  if bstack1ll111l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩయ") in bstack1lllll11_opy_ and bstack1lllll11_opy_[bstack1ll111l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪర")] != bstack1ll111l_opy_ (u"࠭ࠧఱ"):
    return bstack1lllll11_opy_[bstack1ll111l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬల")]
  else:
    bstack1111l111_opy_ = bstack1ll111l_opy_ (u"ࠣࠤళ")
    if bstack1ll111l_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࠩఴ") in bstack1lllll11_opy_ and bstack1lllll11_opy_[bstack1ll111l_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࠪవ")] != None:
      bstack1111l111_opy_ += bstack1lllll11_opy_[bstack1ll111l_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࠫశ")] + bstack1ll111l_opy_ (u"ࠧ࠲ࠠࠣష")
      if bstack1lllll11_opy_[bstack1ll111l_opy_ (u"࠭࡯ࡴࠩస")] == bstack1ll111l_opy_ (u"ࠢࡪࡱࡶࠦహ"):
        bstack1111l111_opy_ += bstack1ll111l_opy_ (u"ࠣ࡫ࡒࡗࠥࠨ఺")
      bstack1111l111_opy_ += (bstack1lllll11_opy_[bstack1ll111l_opy_ (u"ࠩࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭఻")] or bstack1ll111l_opy_ (u"఼ࠪࠫ"))
      return bstack1111l111_opy_
    else:
      bstack1111l111_opy_ += bstack11lll111l_opy_(bstack1lllll11_opy_[bstack1ll111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬఽ")]) + bstack1ll111l_opy_ (u"ࠧࠦࠢా") + (
              bstack1lllll11_opy_[bstack1ll111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨి")] or bstack1ll111l_opy_ (u"ࠧࠨీ")) + bstack1ll111l_opy_ (u"ࠣ࠮ࠣࠦు")
      if bstack1lllll11_opy_[bstack1ll111l_opy_ (u"ࠩࡲࡷࠬూ")] == bstack1ll111l_opy_ (u"࡛ࠥ࡮ࡴࡤࡰࡹࡶࠦృ"):
        bstack1111l111_opy_ += bstack1ll111l_opy_ (u"ࠦ࡜࡯࡮ࠡࠤౄ")
      bstack1111l111_opy_ += bstack1lllll11_opy_[bstack1ll111l_opy_ (u"ࠬࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ౅")] or bstack1ll111l_opy_ (u"࠭ࠧె")
      return bstack1111l111_opy_
def bstack1llllllll1_opy_(bstack1ll1l1lll_opy_):
  if bstack1ll1l1lll_opy_ == bstack1ll111l_opy_ (u"ࠢࡥࡱࡱࡩࠧే"):
    return bstack1ll111l_opy_ (u"ࠨ࠾ࡷࡨࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࠤࡸࡺࡹ࡭ࡧࡀࠦࡨࡵ࡬ࡰࡴ࠽࡫ࡷ࡫ࡥ࡯࠽ࠥࡂࡁ࡬࡯࡯ࡶࠣࡧࡴࡲ࡯ࡳ࠿ࠥ࡫ࡷ࡫ࡥ࡯ࠤࡁࡇࡴࡳࡰ࡭ࡧࡷࡩࡩࡂ࠯ࡧࡱࡱࡸࡃࡂ࠯ࡵࡦࡁࠫై")
  elif bstack1ll1l1lll_opy_ == bstack1ll111l_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤ౉"):
    return bstack1ll111l_opy_ (u"ࠪࡀࡹࡪࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࠦࡳࡵࡻ࡯ࡩࡂࠨࡣࡰ࡮ࡲࡶ࠿ࡸࡥࡥ࠽ࠥࡂࡁ࡬࡯࡯ࡶࠣࡧࡴࡲ࡯ࡳ࠿ࠥࡶࡪࡪࠢ࠿ࡈࡤ࡭ࡱ࡫ࡤ࠽࠱ࡩࡳࡳࡺ࠾࠽࠱ࡷࡨࡃ࠭ొ")
  elif bstack1ll1l1lll_opy_ == bstack1ll111l_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦో"):
    return bstack1ll111l_opy_ (u"ࠬࡂࡴࡥࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢࠡࡵࡷࡽࡱ࡫࠽ࠣࡥࡲࡰࡴࡸ࠺ࡨࡴࡨࡩࡳࡁࠢ࠿࠾ࡩࡳࡳࡺࠠࡤࡱ࡯ࡳࡷࡃࠢࡨࡴࡨࡩࡳࠨ࠾ࡑࡣࡶࡷࡪࡪ࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂࠬౌ")
  elif bstack1ll1l1lll_opy_ == bstack1ll111l_opy_ (u"ࠨࡥࡳࡴࡲࡶ్ࠧ"):
    return bstack1ll111l_opy_ (u"ࠧ࠽ࡶࡧࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࠣࡷࡹࡿ࡬ࡦ࠿ࠥࡧࡴࡲ࡯ࡳ࠼ࡵࡩࡩࡁࠢ࠿࠾ࡩࡳࡳࡺࠠࡤࡱ࡯ࡳࡷࡃࠢࡳࡧࡧࠦࡃࡋࡲࡳࡱࡵࡀ࠴࡬࡯࡯ࡶࡁࡀ࠴ࡺࡤ࠿ࠩ౎")
  elif bstack1ll1l1lll_opy_ == bstack1ll111l_opy_ (u"ࠣࡶ࡬ࡱࡪࡵࡵࡵࠤ౏"):
    return bstack1ll111l_opy_ (u"ࠩ࠿ࡸࡩࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࠥࡹࡴࡺ࡮ࡨࡁࠧࡩ࡯࡭ࡱࡵ࠾ࠨ࡫ࡥࡢ࠵࠵࠺ࡀࠨ࠾࠽ࡨࡲࡲࡹࠦࡣࡰ࡮ࡲࡶࡂࠨࠣࡦࡧࡤ࠷࠷࠼ࠢ࠿ࡖ࡬ࡱࡪࡵࡵࡵ࠾࠲ࡪࡴࡴࡴ࠿࠾࠲ࡸࡩࡄࠧ౐")
  elif bstack1ll1l1lll_opy_ == bstack1ll111l_opy_ (u"ࠥࡶࡺࡴ࡮ࡪࡰࡪࠦ౑"):
    return bstack1ll111l_opy_ (u"ࠫࡁࡺࡤࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨࠠࡴࡶࡼࡰࡪࡃࠢࡤࡱ࡯ࡳࡷࡀࡢ࡭ࡣࡦ࡯ࡀࠨ࠾࠽ࡨࡲࡲࡹࠦࡣࡰ࡮ࡲࡶࡂࠨࡢ࡭ࡣࡦ࡯ࠧࡄࡒࡶࡰࡱ࡭ࡳ࡭࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂࠬ౒")
  else:
    return bstack1ll111l_opy_ (u"ࠬࡂࡴࡥࠢࡤࡰ࡮࡭࡮࠾ࠤࡦࡩࡳࡺࡥࡳࠤࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࠢࡶࡸࡾࡲࡥ࠾ࠤࡦࡳࡱࡵࡲ࠻ࡤ࡯ࡥࡨࡱ࠻ࠣࡀ࠿ࡪࡴࡴࡴࠡࡥࡲࡰࡴࡸ࠽ࠣࡤ࡯ࡥࡨࡱࠢ࠿ࠩ౓") + bstack11lll111l_opy_(
      bstack1ll1l1lll_opy_) + bstack1ll111l_opy_ (u"࠭࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂࠬ౔")
def bstack1ll11ll11l_opy_(session):
  return bstack1ll111l_opy_ (u"ࠧ࠽ࡶࡵࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡷࡵࡷࠣࡀ࠿ࡸࡩࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠲ࡴࡡ࡮ࡧࠥࡂࡁࡧࠠࡩࡴࡨࡪࡂࠨࡻࡾࠤࠣࡸࡦࡸࡧࡦࡶࡀࠦࡤࡨ࡬ࡢࡰ࡮ࠦࡃࢁࡽ࠽࠱ࡤࡂࡁ࠵ࡴࡥࡀࡾࢁࢀࢃ࠼ࡵࡦࠣࡥࡱ࡯ࡧ࡯࠿ࠥࡧࡪࡴࡴࡦࡴࠥࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࡁࡿࢂࡂ࠯ࡵࡦࡁࡀࡹࡪࠠࡢ࡮࡬࡫ࡳࡃࠢࡤࡧࡱࡸࡪࡸࠢࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨ࠾ࡼࡿ࠿࠳ࡹࡪ࠾࠽ࡶࡧࠤࡦࡲࡩࡨࡰࡀࠦࡨ࡫࡮ࡵࡧࡵࠦࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࡂࢀࢃ࠼࠰ࡶࡧࡂࡁࡺࡤࠡࡣ࡯࡭࡬ࡴ࠽ࠣࡥࡨࡲࡹ࡫ࡲࠣࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢ࠿ࡽࢀࡀ࠴ࡺࡤ࠿࠾࠲ࡸࡷࡄౕࠧ").format(
    session[bstack1ll111l_opy_ (u"ࠨࡲࡸࡦࡱ࡯ࡣࡠࡷࡵࡰౖࠬ")], bstack11ll1l11_opy_(session), bstack1llllllll1_opy_(session[bstack1ll111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡵࡷࡥࡹࡻࡳࠨ౗")]),
    bstack1llllllll1_opy_(session[bstack1ll111l_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪౘ")]),
    bstack11lll111l_opy_(session[bstack1ll111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬౙ")] or session[bstack1ll111l_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࠬౚ")] or bstack1ll111l_opy_ (u"࠭ࠧ౛")) + bstack1ll111l_opy_ (u"ࠢࠡࠤ౜") + (session[bstack1ll111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪౝ")] or bstack1ll111l_opy_ (u"ࠩࠪ౞")),
    session[bstack1ll111l_opy_ (u"ࠪࡳࡸ࠭౟")] + bstack1ll111l_opy_ (u"ࠦࠥࠨౠ") + session[bstack1ll111l_opy_ (u"ࠬࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠩౡ")], session[bstack1ll111l_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࠨౢ")] or bstack1ll111l_opy_ (u"ࠧࠨౣ"),
    session[bstack1ll111l_opy_ (u"ࠨࡥࡵࡩࡦࡺࡥࡥࡡࡤࡸࠬ౤")] if session[bstack1ll111l_opy_ (u"ࠩࡦࡶࡪࡧࡴࡦࡦࡢࡥࡹ࠭౥")] else bstack1ll111l_opy_ (u"ࠪࠫ౦"))
def bstack1lll1ll11l_opy_(sessions, bstack1ll11l1ll_opy_):
  try:
    bstack11ll111ll_opy_ = bstack1ll111l_opy_ (u"ࠦࠧ౧")
    if not os.path.exists(bstack11lllll1l_opy_):
      os.mkdir(bstack11lllll1l_opy_)
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1ll111l_opy_ (u"ࠬࡧࡳࡴࡧࡷࡷ࠴ࡸࡥࡱࡱࡵࡸ࠳࡮ࡴ࡮࡮ࠪ౨")), bstack1ll111l_opy_ (u"࠭ࡲࠨ౩")) as f:
      bstack11ll111ll_opy_ = f.read()
    bstack11ll111ll_opy_ = bstack11ll111ll_opy_.replace(bstack1ll111l_opy_ (u"ࠧࡼࠧࡕࡉࡘ࡛ࡌࡕࡕࡢࡇࡔ࡛ࡎࡕࠧࢀࠫ౪"), str(len(sessions)))
    bstack11ll111ll_opy_ = bstack11ll111ll_opy_.replace(bstack1ll111l_opy_ (u"ࠨࡽࠨࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠫࡽࠨ౫"), bstack1ll11l1ll_opy_)
    bstack11ll111ll_opy_ = bstack11ll111ll_opy_.replace(bstack1ll111l_opy_ (u"ࠩࡾࠩࡇ࡛ࡉࡍࡆࡢࡒࡆࡓࡅࠦࡿࠪ౬"),
                                              sessions[0].get(bstack1ll111l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡࡱࡥࡲ࡫ࠧ౭")) if sessions[0] else bstack1ll111l_opy_ (u"ࠫࠬ౮"))
    with open(os.path.join(bstack11lllll1l_opy_, bstack1ll111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠱ࡷ࡫ࡰࡰࡴࡷ࠲࡭ࡺ࡭࡭ࠩ౯")), bstack1ll111l_opy_ (u"࠭ࡷࠨ౰")) as stream:
      stream.write(bstack11ll111ll_opy_.split(bstack1ll111l_opy_ (u"ࠧࡼࠧࡖࡉࡘ࡙ࡉࡐࡐࡖࡣࡉࡇࡔࡂࠧࢀࠫ౱"))[0])
      for session in sessions:
        stream.write(bstack1ll11ll11l_opy_(session))
      stream.write(bstack11ll111ll_opy_.split(bstack1ll111l_opy_ (u"ࠨࡽࠨࡗࡊ࡙ࡓࡊࡑࡑࡗࡤࡊࡁࡕࡃࠨࢁࠬ౲"))[1])
    logger.info(bstack1ll111l_opy_ (u"ࠩࡊࡩࡳ࡫ࡲࡢࡶࡨࡨࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡧࡻࡩ࡭ࡦࠣࡥࡷࡺࡩࡧࡣࡦࡸࡸࠦࡡࡵࠢࡾࢁࠬ౳").format(bstack11lllll1l_opy_));
  except Exception as e:
    logger.debug(bstack11l111111_opy_.format(str(e)))
def bstack1ll1lll111_opy_(bstack1lll1ll1l1_opy_):
  global CONFIG
  try:
    host = bstack1ll111l_opy_ (u"ࠪࡥࡵ࡯࠭ࡤ࡮ࡲࡹࡩ࠭౴") if bstack1ll111l_opy_ (u"ࠫࡦࡶࡰࠨ౵") in CONFIG else bstack1ll111l_opy_ (u"ࠬࡧࡰࡪࠩ౶")
    user = CONFIG[bstack1ll111l_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨ౷")]
    key = CONFIG[bstack1ll111l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ౸")]
    bstack1l1l11lll_opy_ = bstack1ll111l_opy_ (u"ࠨࡣࡳࡴ࠲ࡧࡵࡵࡱࡰࡥࡹ࡫ࠧ౹") if bstack1ll111l_opy_ (u"ࠩࡤࡴࡵ࠭౺") in CONFIG else bstack1ll111l_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷࡩࠬ౻")
    url = bstack1ll111l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࢁࡽ࠻ࡽࢀࡄࢀࢃ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡿࢂ࠵ࡢࡶ࡫࡯ࡨࡸ࠵ࡻࡾ࠱ࡶࡩࡸࡹࡩࡰࡰࡶ࠲࡯ࡹ࡯࡯ࠩ౼").format(user, key, host, bstack1l1l11lll_opy_,
                                                                                bstack1lll1ll1l1_opy_)
    headers = {
      bstack1ll111l_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡴࡺࡲࡨࠫ౽"): bstack1ll111l_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩ౾"),
    }
    proxies = bstack11ll11l1_opy_(CONFIG, url)
    response = requests.get(url, headers=headers, proxies=proxies)
    if response.json():
      return list(map(lambda session: session[bstack1ll111l_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠬ౿")], response.json()))
  except Exception as e:
    logger.debug(bstack11l11l111_opy_.format(str(e)))
def bstack11111llll_opy_():
  global CONFIG
  try:
    if bstack1ll111l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫಀ") in CONFIG:
      host = bstack1ll111l_opy_ (u"ࠩࡤࡴ࡮࠳ࡣ࡭ࡱࡸࡨࠬಁ") if bstack1ll111l_opy_ (u"ࠪࡥࡵࡶࠧಂ") in CONFIG else bstack1ll111l_opy_ (u"ࠫࡦࡶࡩࠨಃ")
      user = CONFIG[bstack1ll111l_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧ಄")]
      key = CONFIG[bstack1ll111l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩಅ")]
      bstack1l1l11lll_opy_ = bstack1ll111l_opy_ (u"ࠧࡢࡲࡳ࠱ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭ಆ") if bstack1ll111l_opy_ (u"ࠨࡣࡳࡴࠬಇ") in CONFIG else bstack1ll111l_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨࠫಈ")
      url = bstack1ll111l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳ࢀࢃ࠺ࡼࡿࡃࡿࢂ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡾࢁ࠴ࡨࡵࡪ࡮ࡧࡷ࠳ࡰࡳࡰࡰࠪಉ").format(user, key, host, bstack1l1l11lll_opy_)
      headers = {
        bstack1ll111l_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲ࡺࡹࡱࡧࠪಊ"): bstack1ll111l_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨಋ"),
      }
      if bstack1ll111l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨಌ") in CONFIG:
        params = {bstack1ll111l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ಍"): CONFIG[bstack1ll111l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫಎ")], bstack1ll111l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠ࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬಏ"): CONFIG[bstack1ll111l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬಐ")]}
      else:
        params = {bstack1ll111l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ಑"): CONFIG[bstack1ll111l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨಒ")]}
      proxies = bstack11ll11l1_opy_(CONFIG, url)
      response = requests.get(url, params=params, headers=headers, proxies=proxies)
      if response.json():
        bstack111l11ll1_opy_ = response.json()[0][bstack1ll111l_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡦࡺ࡯࡬ࡥࠩಓ")]
        if bstack111l11ll1_opy_:
          bstack1ll11l1ll_opy_ = bstack111l11ll1_opy_[bstack1ll111l_opy_ (u"ࠧࡱࡷࡥࡰ࡮ࡩ࡟ࡶࡴ࡯ࠫಔ")].split(bstack1ll111l_opy_ (u"ࠨࡲࡸࡦࡱ࡯ࡣ࠮ࡤࡸ࡭ࡱࡪࠧಕ"))[0] + bstack1ll111l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡴ࠱ࠪಖ") + bstack111l11ll1_opy_[
            bstack1ll111l_opy_ (u"ࠪ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ಗ")]
          logger.info(bstack1l11l1l1_opy_.format(bstack1ll11l1ll_opy_))
          bstack1l11ll11l_opy_ = CONFIG[bstack1ll111l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧಘ")]
          if bstack1ll111l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧಙ") in CONFIG:
            bstack1l11ll11l_opy_ += bstack1ll111l_opy_ (u"࠭ࠠࠨಚ") + CONFIG[bstack1ll111l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩಛ")]
          if bstack1l11ll11l_opy_ != bstack111l11ll1_opy_[bstack1ll111l_opy_ (u"ࠨࡰࡤࡱࡪ࠭ಜ")]:
            logger.debug(bstack1ll11111_opy_.format(bstack111l11ll1_opy_[bstack1ll111l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧಝ")], bstack1l11ll11l_opy_))
          return [bstack111l11ll1_opy_[bstack1ll111l_opy_ (u"ࠪ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ಞ")], bstack1ll11l1ll_opy_]
    else:
      logger.warn(bstack1l1ll1l11_opy_)
  except Exception as e:
    logger.debug(bstack11l1l11l_opy_.format(str(e)))
  return [None, None]
def bstack1lllll111_opy_(url, bstack11l1llll1_opy_=False):
  global CONFIG
  global bstack1l1l11111_opy_
  if not bstack1l1l11111_opy_:
    hostname = bstack1llll1ll1l_opy_(url)
    is_private = bstack1lll1l11l1_opy_(hostname)
    if (bstack1ll111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨಟ") in CONFIG and not CONFIG[bstack1ll111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩಠ")]) and (is_private or bstack11l1llll1_opy_):
      bstack1l1l11111_opy_ = hostname
def bstack1llll1ll1l_opy_(url):
  return urlparse(url).hostname
def bstack1lll1l11l1_opy_(hostname):
  for bstack1ll11lll1l_opy_ in bstack1lll111l11_opy_:
    regex = re.compile(bstack1ll11lll1l_opy_)
    if regex.match(hostname):
      return True
  return False
def bstack1l1lll111_opy_(key_name):
  return True if key_name in threading.current_thread().__dict__.keys() else False
def bstack1llll1l11l_opy_(driver):
  global CONFIG
  if not bstack1111l1ll_opy_(CONFIG):
    logger.warning(bstack1ll111l_opy_ (u"ࠨࡎࡰࡶࠣࡥࡳࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡷࡪࡹࡳࡪࡱࡱ࠰ࠥࡩࡡ࡯ࡰࡲࡸࠥࡸࡥࡵࡴ࡬ࡩࡻ࡫ࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡳࡧࡶࡹࡱࡺࡳ࠯ࠤಡ"))
    return {}
  try:
    results = driver.execute_script(bstack1ll111l_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡷ࡫ࡴࡶࡴࡱࠤࡳ࡫ࡷࠡࡒࡵࡳࡲ࡯ࡳࡦࠪࡩࡹࡳࡩࡴࡪࡱࡱࠤ࠭ࡸࡥࡴࡱ࡯ࡺࡪ࠲ࠠࡳࡧ࡭ࡩࡨࡺࠩࠡࡽࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡶࡵࡽࠥࢁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡦࡳࡳࡹࡴࠡࡧࡹࡩࡳࡺࠠ࠾ࠢࡱࡩࡼࠦࡃࡶࡵࡷࡳࡲࡋࡶࡦࡰࡷࠬࠬࡇ࠱࠲࡛ࡢࡘࡆࡖ࡟ࡈࡇࡗࡣࡗࡋࡓࡖࡎࡗࡗࠬ࠯࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡧࡴࡴࡳࡵࠢࡩࡲࠥࡃࠠࡧࡷࡱࡧࡹ࡯࡯࡯ࠢࠫࡩࡻ࡫࡮ࡵࠫࠣࡿࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡼ࡯࡮ࡥࡱࡺ࠲ࡷ࡫࡭ࡰࡸࡨࡉࡻ࡫࡮ࡵࡎ࡬ࡷࡹ࡫࡮ࡦࡴࠫࠫࡆ࠷࠱࡚ࡡࡕࡉࡘ࡛ࡌࡕࡕࡢࡖࡊ࡙ࡐࡐࡐࡖࡉࠬ࠲ࠠࡧࡰࠬ࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡷ࡫ࡳࡰ࡮ࡹࡩ࠭࡫ࡶࡦࡰࡷ࠲ࡩ࡫ࡴࡢ࡫࡯࠲ࡩࡧࡴࡢࠫ࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽ࠼ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡼ࡯࡮ࡥࡱࡺ࠲ࡦࡪࡤࡆࡸࡨࡲࡹࡒࡩࡴࡶࡨࡲࡪࡸࠨࠨࡃ࠴࠵࡞ࡥࡒࡆࡕࡘࡐ࡙࡙࡟ࡓࡇࡖࡔࡔࡔࡓࡆࠩ࠯ࠤ࡫ࡴࠩ࠼ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡼ࡯࡮ࡥࡱࡺ࠲ࡩ࡯ࡳࡱࡣࡷࡧ࡭ࡋࡶࡦࡰࡷࠬࡪࡼࡥ࡯ࡶࠬ࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࢁࠥࡩࡡࡵࡥ࡫ࠤࢀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡴࡨ࡮ࡪࡩࡴࠩࠫ࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࢀࠎࠥࠦࠠࠡࠢࠣࠤࠥࢃࠩ࠼ࠌࠣࠤࠥࠦࠢࠣࠤಢ"))
    return results
  except Exception:
    logger.error(bstack1ll111l_opy_ (u"ࠣࡐࡲࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠥࡽࡥࡳࡧࠣࡪࡴࡻ࡮ࡥ࠰ࠥಣ"))
    return {}
def bstack1llll1l1l_opy_(driver):
  global CONFIG
  if not bstack1111l1ll_opy_(CONFIG):
    logger.warning(bstack1ll111l_opy_ (u"ࠤࡑࡳࡹࠦࡡ࡯ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡳࡦࡵࡶ࡭ࡴࡴࠬࠡࡥࡤࡲࡳࡵࡴࠡࡴࡨࡸࡷ࡯ࡥࡷࡧࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡶࡪࡹࡵ࡭ࡶࡶࠤࡸࡻ࡭࡮ࡣࡵࡽ࠳ࠨತ"))
    return {}
  try:
    bstack11lll1l1_opy_ = driver.execute_script(bstack1ll111l_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡳࡧࡷࡹࡷࡴࠠ࡯ࡧࡺࠤࡕࡸ࡯࡮࡫ࡶࡩ࠭࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠠࠩࡴࡨࡷࡴࡲࡶࡦ࠮ࠣࡶࡪࡰࡥࡤࡶࠬࠤࢀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡹࡸࡹࠡࡽࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡩ࡯࡯ࡵࡷࠤࡪࡼࡥ࡯ࡶࠣࡁࠥࡴࡥࡸࠢࡆࡹࡸࡺ࡯࡮ࡇࡹࡩࡳࡺࠨࠨࡃ࠴࠵࡞ࡥࡔࡂࡒࡢࡋࡊ࡚࡟ࡓࡇࡖ࡙ࡑ࡚ࡓࡠࡕࡘࡑࡒࡇࡒ࡚ࠩࠬ࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡤࡱࡱࡷࡹࠦࡦ࡯ࠢࡀࠤ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠦࠨࡦࡸࡨࡲࡹ࠯ࠠࡼࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡹ࡬ࡲࡩࡵࡷ࠯ࡴࡨࡱࡴࡼࡥࡆࡸࡨࡲࡹࡒࡩࡴࡶࡨࡲࡪࡸࠨࠨࡃ࠴࠵࡞ࡥࡒࡆࡕࡘࡐ࡙࡙࡟ࡔࡗࡐࡑࡆࡘ࡙ࡠࡔࡈࡗࡕࡕࡎࡔࡇࠪ࠰ࠥ࡬࡮ࠪ࠽ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡵࡩࡸࡵ࡬ࡷࡧࠫࡩࡻ࡫࡮ࡵ࠰ࡧࡩࡹࡧࡩ࡭࠰ࡶࡹࡲࡳࡡࡳࡻࠬ࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡾ࠽ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡽࡩ࡯ࡦࡲࡻ࠳ࡧࡤࡥࡇࡹࡩࡳࡺࡌࡪࡵࡷࡩࡳ࡫ࡲࠩࠩࡄ࠵࠶࡟࡟ࡓࡇࡖ࡙ࡑ࡚ࡓࡠࡕࡘࡑࡒࡇࡒ࡚ࡡࡕࡉࡘࡖࡏࡏࡕࡈࠫ࠱ࠦࡦ࡯ࠫ࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡷࡪࡰࡧࡳࡼ࠴ࡤࡪࡵࡳࡥࡹࡩࡨࡆࡸࡨࡲࡹ࠮ࡥࡷࡧࡱࡸ࠮ࡁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃࠠࡤࡣࡷࡧ࡭ࠦࡻࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡶࡪࡰࡥࡤࡶࠫ࠭ࡀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢂࠐࠠࠡࠢࠣࠤࠥࠦࠠࡾࠫ࠾ࠎࠥࠦࠠࠡࠤࠥࠦಥ"))
    return bstack11lll1l1_opy_
  except Exception:
    logger.error(bstack1ll111l_opy_ (u"ࠦࡓࡵࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡴࡷࡰࡱࡦࡸࡹࠡࡹࡤࡷࠥ࡬࡯ࡶࡰࡧ࠲ࠧದ"))
    return {}