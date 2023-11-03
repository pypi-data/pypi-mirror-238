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
import datetime
import inspect
import logging
import os
import sys
import threading
from uuid import uuid4
import pytest
from packaging import version
from browserstack_sdk.__init__ import (bstack1ll1l11111_opy_, bstack11l11l11l_opy_, update, bstack11l11l1l1_opy_,
                                       bstack11l11ll1_opy_, bstack1l11l1l11_opy_, bstack1ll11llll1_opy_, bstack111111l1l_opy_,
                                       bstack111llll1_opy_, bstack1l1ll1ll_opy_, bstack1l1lll1l1_opy_, bstack1l1l1lll_opy_,
                                       bstack1l1lll1ll_opy_)
from browserstack_sdk._version import __version__
from bstack_utils.capture import bstack1l1lll11ll_opy_
from bstack_utils.constants import bstack11l11111l_opy_, bstack1ll1lll1_opy_, bstack1ll1lll1ll_opy_, bstack1l1111l1l_opy_, \
    bstack111l11l11_opy_
from bstack_utils.helper import bstack1lll1111_opy_, bstack1l1ll11ll1_opy_, bstack1l1l11llll_opy_, bstack1lll111l1l_opy_, bstack1l1l11l111_opy_, \
    bstack1l1l111ll1_opy_, bstack1l1111lll_opy_, bstack1lll1lll1_opy_, bstack1l1l1l11l1_opy_, bstack111l1ll1_opy_, Notset, \
    bstack1111l11l_opy_, bstack1l1ll111ll_opy_, bstack1l1l11l1l1_opy_, Result, bstack1l1l11lll1_opy_, bstack1l1l1ll111_opy_, bstack1l1l1l1l1l_opy_
from bstack_utils.bstack1l11llllll_opy_ import bstack1l1l111l11_opy_
from bstack_utils.messages import bstack111l1111_opy_, bstack11l1ll1ll_opy_, bstack11l1lll1l_opy_, bstack1l111llll_opy_, bstack1l1111l1_opy_, \
    bstack1ll1l1ll_opy_, bstack1ll11lllll_opy_, bstack1llllll1ll_opy_, bstack111ll1l1l_opy_, bstack1l1l1111_opy_, \
    bstack1l1ll1l1l_opy_, bstack1l1lllll_opy_
from bstack_utils.proxy import bstack111llll11_opy_, bstack11l1l1l1l_opy_
from bstack_utils.bstack11111ll11_opy_ import bstack11llll1111_opy_, bstack11lll1lll1_opy_, bstack11llll11l1_opy_, bstack11llll1l1l_opy_, \
    bstack11lll1l1l1_opy_, bstack11lll1l11l_opy_, bstack11lll1l1ll_opy_, bstack111ll1lll_opy_, bstack11llll1l11_opy_
from bstack_utils.bstack11ll1l1l1l_opy_ import bstack11ll1l1lll_opy_
from bstack_utils.bstack11llll11ll_opy_ import bstack1l11ll1l1_opy_, bstack1lllll111_opy_, bstack11l1l1ll_opy_
from bstack_utils.bstack11ll111111_opy_ import bstack11ll11111l_opy_
from bstack_utils.bstack11lllll1_opy_ import bstack11llllll1_opy_
bstack11l1l1ll1_opy_ = None
bstack1ll11lll_opy_ = None
bstack1llll1l1ll_opy_ = None
bstack11ll11111_opy_ = None
bstack111ll11l_opy_ = None
bstack1ll1lllll1_opy_ = None
bstack11l1llll_opy_ = None
bstack111ll111l_opy_ = None
bstack11l1l11l1_opy_ = None
bstack1ll1ll11l_opy_ = None
bstack1ll11lll11_opy_ = None
bstack1lll11l11_opy_ = None
bstack1lllll11ll_opy_ = None
bstack1l1ll1lll_opy_ = bstack1ll111l_opy_ (u"ࠫࠬጡ")
CONFIG = {}
bstack1lll11l1l1_opy_ = False
bstack1llll11l_opy_ = bstack1ll111l_opy_ (u"ࠬ࠭ጢ")
bstack11lll1lll_opy_ = bstack1ll111l_opy_ (u"࠭ࠧጣ")
bstack11l1111l_opy_ = False
bstack1l11lllll_opy_ = []
bstack1ll1l1111_opy_ = bstack1ll1lll1_opy_
bstack111lllllll_opy_ = bstack1ll111l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧጤ")
logger = logging.getLogger(__name__)
logging.basicConfig(level=bstack1ll1l1111_opy_,
                    format=bstack1ll111l_opy_ (u"ࠨ࡞ࡱࠩ࠭ࡧࡳࡤࡶ࡬ࡱࡪ࠯ࡳࠡ࡝ࠨࠬࡳࡧ࡭ࡦࠫࡶࡡࡠࠫࠨ࡭ࡧࡹࡩࡱࡴࡡ࡮ࡧࠬࡷࡢࠦ࠭ࠡࠧࠫࡱࡪࡹࡳࡢࡩࡨ࠭ࡸ࠭ጥ"),
                    datefmt=bstack1ll111l_opy_ (u"ࠩࠨࡌ࠿ࠫࡍ࠻ࠧࡖࠫጦ"),
                    stream=sys.stdout)
store = {
    bstack1ll111l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧጧ"): []
}
def bstack1ll1l1l1l_opy_():
    global CONFIG
    global bstack1ll1l1111_opy_
    if bstack1ll111l_opy_ (u"ࠫࡱࡵࡧࡍࡧࡹࡩࡱ࠭ጨ") in CONFIG:
        bstack1ll1l1111_opy_ = bstack11l11111l_opy_[CONFIG[bstack1ll111l_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧጩ")]]
        logging.getLogger().setLevel(bstack1ll1l1111_opy_)
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
_11l11l111l_opy_ = {}
current_test_uuid = None
def bstack11l1lll1_opy_(page, bstack1l1l11l1_opy_):
    try:
        page.evaluate(bstack1ll111l_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢጪ"),
                      bstack1ll111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡳࡧ࡭ࡦࠤ࠽ࠫጫ") + json.dumps(
                          bstack1l1l11l1_opy_) + bstack1ll111l_opy_ (u"ࠣࡿࢀࠦጬ"))
    except Exception as e:
        print(bstack1ll111l_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨࠤࢀࢃࠢጭ"), e)
def bstack1ll1ll1l1l_opy_(page, message, level):
    try:
        page.evaluate(bstack1ll111l_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦጮ"), bstack1ll111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩጯ") + json.dumps(
            message) + bstack1ll111l_opy_ (u"ࠬ࠲ࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠨጰ") + json.dumps(level) + bstack1ll111l_opy_ (u"࠭ࡽࡾࠩጱ"))
    except Exception as e:
        print(bstack1ll111l_opy_ (u"ࠢࡦࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡥࡳࡴ࡯ࡵࡣࡷ࡭ࡴࡴࠠࡼࡿࠥጲ"), e)
def bstack1l1l1l11_opy_(page, status, message=bstack1ll111l_opy_ (u"ࠣࠤጳ")):
    try:
        if (status == bstack1ll111l_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤጴ")):
            page.evaluate(bstack1ll111l_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦጵ"),
                          bstack1ll111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡶࡪࡧࡳࡰࡰࠥ࠾ࠬጶ") + json.dumps(
                              bstack1ll111l_opy_ (u"࡙ࠧࡣࡦࡰࡤࡶ࡮ࡵࠠࡧࡣ࡬ࡰࡪࡪࠠࡸ࡫ࡷ࡬࠿ࠦࠢጷ") + str(message)) + bstack1ll111l_opy_ (u"࠭ࠬࠣࡵࡷࡥࡹࡻࡳࠣ࠼ࠪጸ") + json.dumps(status) + bstack1ll111l_opy_ (u"ࠢࡾࡿࠥጹ"))
        else:
            page.evaluate(bstack1ll111l_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤጺ"),
                          bstack1ll111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡵࡷࡥࡹࡻࡳࠣ࠼ࠪጻ") + json.dumps(
                              status) + bstack1ll111l_opy_ (u"ࠥࢁࢂࠨጼ"))
    except Exception as e:
        print(bstack1ll111l_opy_ (u"ࠦࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡴࡧࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡹࡴࡢࡶࡸࡷࠥࢁࡽࠣጽ"), e)
def pytest_configure(config):
    config.args = bstack11llllll1_opy_.bstack11l1l1l111_opy_(config.args)
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    bstack11l11l11ll_opy_ = item.config.getoption(bstack1ll111l_opy_ (u"ࠬࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧጾ"))
    plugins = item.config.getoption(bstack1ll111l_opy_ (u"ࠨࡰ࡭ࡷࡪ࡭ࡳࡹࠢጿ"))
    report = outcome.get_result()
    bstack111lllll1l_opy_(item, call, report)
    if bstack1ll111l_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࡟ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡶ࡬ࡶࡩ࡬ࡲࠧፀ") not in plugins or bstack111l1ll1_opy_():
        return
    summary = []
    driver = getattr(item, bstack1ll111l_opy_ (u"ࠣࡡࡧࡶ࡮ࡼࡥࡳࠤፁ"), None)
    page = getattr(item, bstack1ll111l_opy_ (u"ࠤࡢࡴࡦ࡭ࡥࠣፂ"), None)
    try:
        if (driver == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None):
        bstack111lll1lll_opy_(item, report, summary, bstack11l11l11ll_opy_)
    if (page is not None):
        bstack11l111111l_opy_(item, report, summary, bstack11l11l11ll_opy_)
def bstack111lll1lll_opy_(item, report, summary, bstack11l11l11ll_opy_):
    if report.when in [bstack1ll111l_opy_ (u"ࠥࡷࡪࡺࡵࡱࠤፃ"), bstack1ll111l_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࠨፄ")]:
        return
    if not bstack1l1l11llll_opy_():
        return
    try:
        if (str(bstack11l11l11ll_opy_).lower() != bstack1ll111l_opy_ (u"ࠬࡺࡲࡶࡧࠪፅ")):
            item._driver.execute_script(
                bstack1ll111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠣࠫፆ") + json.dumps(
                    report.nodeid) + bstack1ll111l_opy_ (u"ࠧࡾࡿࠪፇ"))
    except Exception as e:
        summary.append(
            bstack1ll111l_opy_ (u"࡙ࠣࡄࡖࡓࡏࡎࡈ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦ࡭ࡢࡴ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧ࠽ࠤࢀ࠶ࡽࠣፈ").format(e)
        )
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1ll111l_opy_ (u"ࠤࡺࡥࡸࡾࡦࡢ࡫࡯ࠦፉ")))
    bstack11l111lll_opy_ = bstack1ll111l_opy_ (u"ࠥࠦፊ")
    if not passed:
        try:
            bstack11l111lll_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack1ll111l_opy_ (u"ࠦ࡜ࡇࡒࡏࡋࡑࡋ࠿ࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡧࡩࡹ࡫ࡲ࡮࡫ࡱࡩࠥ࡬ࡡࡪ࡮ࡸࡶࡪࠦࡲࡦࡣࡶࡳࡳࡀࠠࡼ࠲ࢀࠦፋ").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack11l111lll_opy_))
    if not report.skipped:
        passed = report.passed or (report.failed and hasattr(report, bstack1ll111l_opy_ (u"ࠧࡽࡡࡴࡺࡩࡥ࡮ࡲࠢፌ")))
        bstack11l111lll_opy_ = bstack1ll111l_opy_ (u"ࠨࠢፍ")
        if not passed:
            try:
                bstack11l111lll_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1ll111l_opy_ (u"ࠢࡘࡃࡕࡒࡎࡔࡇ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡪࡥࡵࡧࡵࡱ࡮ࡴࡥࠡࡨࡤ࡭ࡱࡻࡲࡦࠢࡵࡩࡦࡹ࡯࡯࠼ࠣࡿ࠵ࢃࠢፎ").format(e)
                )
            try:
                if (threading.current_thread().bstackTestErrorMessages == None):
                    threading.current_thread().bstackTestErrorMessages = []
            except Exception as e:
                threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(str(bstack11l111lll_opy_))
        try:
            if passed:
                item._driver.execute_script(
                    bstack1ll111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦ࡮ࡴࡦࡰࠤ࠯ࠤࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡩࡧࡴࡢࠤ࠽ࠤࠬፏ")
                    + json.dumps(bstack1ll111l_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠣࠥፐ"))
                    + bstack1ll111l_opy_ (u"ࠥࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢂࠨፑ")
                )
            else:
                item._driver.execute_script(
                    bstack1ll111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡲࡥࡷࡧ࡯ࠦ࠿ࠦࠢࡦࡴࡵࡳࡷࠨࠬࠡ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡦࡤࡸࡦࠨ࠺ࠡࠩፒ")
                    + json.dumps(str(bstack11l111lll_opy_))
                    + bstack1ll111l_opy_ (u"ࠧࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡾ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽࠣፓ")
                )
        except Exception as e:
            summary.append(bstack1ll111l_opy_ (u"ࠨࡗࡂࡔࡑࡍࡓࡍ࠺ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡦࡴ࡮ࡰࡶࡤࡸࡪࡀࠠࡼ࠲ࢀࠦፔ").format(e))
def bstack11l111111l_opy_(item, report, summary, bstack11l11l11ll_opy_):
    if report.when in [bstack1ll111l_opy_ (u"ࠢࡴࡧࡷࡹࡵࠨፕ"), bstack1ll111l_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࠥፖ")]:
        return
    if (str(bstack11l11l11ll_opy_).lower() != bstack1ll111l_opy_ (u"ࠩࡷࡶࡺ࡫ࠧፗ")):
        bstack11l1lll1_opy_(item._page, report.nodeid)
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1ll111l_opy_ (u"ࠥࡻࡦࡹࡸࡧࡣ࡬ࡰࠧፘ")))
    bstack11l111lll_opy_ = bstack1ll111l_opy_ (u"ࠦࠧፙ")
    bstack11llll1l11_opy_(report)
    if not report.skipped:
        if not passed:
            try:
                bstack11l111lll_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1ll111l_opy_ (u"ࠧ࡝ࡁࡓࡐࡌࡒࡌࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡨࡪࡺࡥࡳ࡯࡬ࡲࡪࠦࡦࡢ࡫࡯ࡹࡷ࡫ࠠࡳࡧࡤࡷࡴࡴ࠺ࠡࡽ࠳ࢁࠧፚ").format(e)
                )
        try:
            if passed:
                bstack1l1l1l11_opy_(item._page, bstack1ll111l_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨ፛"))
            else:
                if bstack11l111lll_opy_:
                    bstack1ll1ll1l1l_opy_(item._page, str(bstack11l111lll_opy_), bstack1ll111l_opy_ (u"ࠢࡦࡴࡵࡳࡷࠨ፜"))
                    bstack1l1l1l11_opy_(item._page, bstack1ll111l_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣ፝"), str(bstack11l111lll_opy_))
                else:
                    bstack1l1l1l11_opy_(item._page, bstack1ll111l_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤ፞"))
        except Exception as e:
            summary.append(bstack1ll111l_opy_ (u"࡛ࠥࡆࡘࡎࡊࡐࡊ࠾ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡷࡳࡨࡦࡺࡥࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡶࡸࡦࡺࡵࡴ࠼ࠣࡿ࠵ࢃࠢ፟").format(e))
try:
    from typing import Generator
    import pytest_playwright.pytest_playwright as p
    @pytest.fixture
    def page(context: BrowserContext, request: pytest.FixtureRequest) -> Generator[Page, None, None]:
        page = context.new_page()
        request.node._page = page
        yield page
except:
    pass
def pytest_addoption(parser):
    parser.addoption(bstack1ll111l_opy_ (u"ࠦ࠲࠳ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ፠"), default=bstack1ll111l_opy_ (u"ࠧࡌࡡ࡭ࡵࡨࠦ፡"), help=bstack1ll111l_opy_ (u"ࠨࡁࡶࡶࡲࡱࡦࡺࡩࡤࠢࡶࡩࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠧ።"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack1ll111l_opy_ (u"ࠢ࠮࠯ࡧࡶ࡮ࡼࡥࡳࠤ፣"), action=bstack1ll111l_opy_ (u"ࠣࡵࡷࡳࡷ࡫ࠢ፤"), default=bstack1ll111l_opy_ (u"ࠤࡦ࡬ࡷࡵ࡭ࡦࠤ፥"),
                         help=bstack1ll111l_opy_ (u"ࠥࡈࡷ࡯ࡶࡦࡴࠣࡸࡴࠦࡲࡶࡰࠣࡸࡪࡹࡴࡴࠤ፦"))
def bstack11l11111ll_opy_(log):
    if not (log[bstack1ll111l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ፧")] and log[bstack1ll111l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭፨")].strip()):
        return
    active = bstack11l111l1l1_opy_()
    log = {
        bstack1ll111l_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ፩"): log[bstack1ll111l_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭፪")],
        bstack1ll111l_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫ፫"): datetime.datetime.utcnow().isoformat() + bstack1ll111l_opy_ (u"ࠩ࡝ࠫ፬"),
        bstack1ll111l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ፭"): log[bstack1ll111l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ፮")],
    }
    if active:
        if active[bstack1ll111l_opy_ (u"ࠬࡺࡹࡱࡧࠪ፯")] == bstack1ll111l_opy_ (u"࠭ࡨࡰࡱ࡮ࠫ፰"):
            log[bstack1ll111l_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ፱")] = active[bstack1ll111l_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ፲")]
        elif active[bstack1ll111l_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ፳")] == bstack1ll111l_opy_ (u"ࠪࡸࡪࡹࡴࠨ፴"):
            log[bstack1ll111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ፵")] = active[bstack1ll111l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ፶")]
    bstack11llllll1_opy_.bstack11l1ll11ll_opy_([log])
def bstack11l111l1l1_opy_():
    if len(store[bstack1ll111l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪ፷")]) > 0 and store[bstack1ll111l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫ፸")][-1]:
        return {
            bstack1ll111l_opy_ (u"ࠨࡶࡼࡴࡪ࠭፹"): bstack1ll111l_opy_ (u"ࠩ࡫ࡳࡴࡱࠧ፺"),
            bstack1ll111l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ፻"): store[bstack1ll111l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨ፼")][-1]
        }
    if store.get(bstack1ll111l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩ፽"), None):
        return {
            bstack1ll111l_opy_ (u"࠭ࡴࡺࡲࡨࠫ፾"): bstack1ll111l_opy_ (u"ࠧࡵࡧࡶࡸࠬ፿"),
            bstack1ll111l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᎀ"): store[bstack1ll111l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭ᎁ")]
        }
    return None
bstack111llll1l1_opy_ = bstack1l1lll11ll_opy_(bstack11l11111ll_opy_)
def pytest_runtest_call(item):
    try:
        if not bstack11llllll1_opy_.on() or bstack111lllllll_opy_ != bstack1ll111l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪᎂ"):
            return
        global current_test_uuid, bstack111llll1l1_opy_
        bstack111llll1l1_opy_.start()
        bstack11l1111l1l_opy_ = {
            bstack1ll111l_opy_ (u"ࠫࡺࡻࡩࡥࠩᎃ"): uuid4().__str__(),
            bstack1ll111l_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩᎄ"): datetime.datetime.utcnow().isoformat() + bstack1ll111l_opy_ (u"࡚࠭ࠨᎅ")
        }
        current_test_uuid = bstack11l1111l1l_opy_[bstack1ll111l_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᎆ")]
        store[bstack1ll111l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬᎇ")] = bstack11l1111l1l_opy_[bstack1ll111l_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᎈ")]
        threading.current_thread().current_test_uuid = current_test_uuid
        _11l11l111l_opy_[item.nodeid] = {**_11l11l111l_opy_[item.nodeid], **bstack11l1111l1l_opy_}
        bstack11l111l1ll_opy_(item, _11l11l111l_opy_[item.nodeid], bstack1ll111l_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫᎉ"))
    except Exception as err:
        print(bstack1ll111l_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡶࡺࡴࡴࡦࡵࡷࡣࡨࡧ࡬࡭࠼ࠣࡿࢂ࠭ᎊ"), str(err))
def pytest_runtest_setup(item):
    if bstack1l1l1l11l1_opy_():
        atexit.register(bstack1l11l11l_opy_)
        try:
            item.config.hook.pytest_selenium_runtest_makereport = bstack11llll1111_opy_
        except Exception as err:
            threading.current_thread().bstack11ll1l11ll_opy_ = bstack1ll111l_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᎋ")
    try:
        if not bstack11llllll1_opy_.on():
            return
        bstack111llll1l1_opy_.start()
        uuid = uuid4().__str__()
        bstack11l1111l1l_opy_ = {
            bstack1ll111l_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᎌ"): uuid,
            bstack1ll111l_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫᎍ"): datetime.datetime.utcnow().isoformat() + bstack1ll111l_opy_ (u"ࠨ࡜ࠪᎎ"),
            bstack1ll111l_opy_ (u"ࠩࡷࡽࡵ࡫ࠧᎏ"): bstack1ll111l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨ᎐"),
            bstack1ll111l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡷࡽࡵ࡫ࠧ᎑"): bstack1ll111l_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪ᎒"),
            bstack1ll111l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡳࡧ࡭ࡦࠩ᎓"): bstack1ll111l_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭᎔")
        }
        threading.current_thread().bstack11l1111l11_opy_ = uuid
        store[bstack1ll111l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡶࡨࡱࠬ᎕")] = item
        store[bstack1ll111l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭᎖")] = [uuid]
        if not _11l11l111l_opy_.get(item.nodeid, None):
            _11l11l111l_opy_[item.nodeid] = {bstack1ll111l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩ᎗"): [], bstack1ll111l_opy_ (u"ࠫ࡫࡯ࡸࡵࡷࡵࡩࡸ࠭᎘"): []}
        _11l11l111l_opy_[item.nodeid][bstack1ll111l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫ᎙")].append(bstack11l1111l1l_opy_[bstack1ll111l_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ᎚")])
        _11l11l111l_opy_[item.nodeid + bstack1ll111l_opy_ (u"ࠧ࠮ࡵࡨࡸࡺࡶࠧ᎛")] = bstack11l1111l1l_opy_
        bstack11l11l1l11_opy_(item, bstack11l1111l1l_opy_, bstack1ll111l_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩ᎜"))
    except Exception as err:
        print(bstack1ll111l_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡴࡸࡲࡹ࡫ࡳࡵࡡࡶࡩࡹࡻࡰ࠻ࠢࡾࢁࠬ᎝"), str(err))
def pytest_runtest_teardown(item):
    try:
        if not bstack11llllll1_opy_.on():
            return
        bstack11l1111l1l_opy_ = {
            bstack1ll111l_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ᎞"): uuid4().__str__(),
            bstack1ll111l_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ᎟"): datetime.datetime.utcnow().isoformat() + bstack1ll111l_opy_ (u"ࠬࡠࠧᎠ"),
            bstack1ll111l_opy_ (u"࠭ࡴࡺࡲࡨࠫᎡ"): bstack1ll111l_opy_ (u"ࠧࡩࡱࡲ࡯ࠬᎢ"),
            bstack1ll111l_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨࠫᎣ"): bstack1ll111l_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡇࡄࡇࡍ࠭Ꭴ"),
            bstack1ll111l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡰࡤࡱࡪ࠭Ꭵ"): bstack1ll111l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭Ꭶ")
        }
        _11l11l111l_opy_[item.nodeid + bstack1ll111l_opy_ (u"ࠬ࠳ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨᎧ")] = bstack11l1111l1l_opy_
        bstack11l11l1l11_opy_(item, bstack11l1111l1l_opy_, bstack1ll111l_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧᎨ"))
    except Exception as err:
        print(bstack1ll111l_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡲࡶࡰࡷࡩࡸࡺ࡟ࡵࡧࡤࡶࡩࡵࡷ࡯࠼ࠣࡿࢂ࠭Ꭹ"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if not bstack11llllll1_opy_.on():
        yield
        return
    start_time = datetime.datetime.now()
    if bstack11llll1l1l_opy_(fixturedef.argname):
        store[bstack1ll111l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡰࡳࡩࡻ࡬ࡦࡡ࡬ࡸࡪࡳࠧᎪ")] = request.node
    elif bstack11lll1l1l1_opy_(fixturedef.argname):
        store[bstack1ll111l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡧࡱࡧࡳࡴࡡ࡬ࡸࡪࡳࠧᎫ")] = request.node
    outcome = yield
    try:
        fixture = {
            bstack1ll111l_opy_ (u"ࠪࡲࡦࡳࡥࠨᎬ"): fixturedef.argname,
            bstack1ll111l_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᎭ"): bstack1l1l11l111_opy_(outcome),
            bstack1ll111l_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴࠧᎮ"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        bstack111lll1ll1_opy_ = store[bstack1ll111l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡴࡦ࡯ࠪᎯ")]
        if not _11l11l111l_opy_.get(bstack111lll1ll1_opy_.nodeid, None):
            _11l11l111l_opy_[bstack111lll1ll1_opy_.nodeid] = {bstack1ll111l_opy_ (u"ࠧࡧ࡫ࡻࡸࡺࡸࡥࡴࠩᎰ"): []}
        _11l11l111l_opy_[bstack111lll1ll1_opy_.nodeid][bstack1ll111l_opy_ (u"ࠨࡨ࡬ࡼࡹࡻࡲࡦࡵࠪᎱ")].append(fixture)
    except Exception as err:
        logger.debug(bstack1ll111l_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡨ࡬ࡼࡹࡻࡲࡦࡡࡶࡩࡹࡻࡰ࠻ࠢࡾࢁࠬᎲ"), str(err))
if bstack111l1ll1_opy_() and bstack11llllll1_opy_.on():
    def pytest_bdd_before_step(request, step):
        try:
            _11l11l111l_opy_[request.node.nodeid][bstack1ll111l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭Ꮃ")].bstack11l1llllll_opy_(id(step))
        except Exception as err:
            print(bstack1ll111l_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡦࡩࡪ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡴࡶࡨࡴ࠿ࠦࡻࡾࠩᎴ"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        try:
            _11l11l111l_opy_[request.node.nodeid][bstack1ll111l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨᎵ")].bstack11ll1111ll_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstack1ll111l_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡨࡤࡥࡡࡶࡸࡪࡶ࡟ࡦࡴࡵࡳࡷࡀࠠࡼࡿࠪᎶ"), str(err))
    def pytest_bdd_after_step(request, step):
        try:
            bstack11ll111111_opy_: bstack11ll11111l_opy_ = _11l11l111l_opy_[request.node.nodeid][bstack1ll111l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪᎷ")]
            bstack11ll111111_opy_.bstack11ll1111ll_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstack1ll111l_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡣࡦࡧࡣࡸࡺࡥࡱࡡࡨࡶࡷࡵࡲ࠻ࠢࡾࢁࠬᎸ"), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack111lllllll_opy_
        try:
            if not bstack11llllll1_opy_.on() or bstack111lllllll_opy_ != bstack1ll111l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩ࠭Ꮉ"):
                return
            global bstack111llll1l1_opy_
            bstack111llll1l1_opy_.start()
            if not _11l11l111l_opy_.get(request.node.nodeid, None):
                _11l11l111l_opy_[request.node.nodeid] = {}
            bstack11ll111111_opy_ = bstack11ll11111l_opy_.bstack11ll11l1l1_opy_(
                scenario, feature, request.node,
                name=bstack11lll1l11l_opy_(request.node, scenario),
                bstack11l1lll1ll_opy_=bstack1lll111l1l_opy_(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstack1ll111l_opy_ (u"ࠪࡔࡾࡺࡥࡴࡶ࠰ࡧࡺࡩࡵ࡮ࡤࡨࡶࠬᎺ"),
                tags=bstack11lll1l1ll_opy_(feature, scenario)
            )
            _11l11l111l_opy_[request.node.nodeid][bstack1ll111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧᎻ")] = bstack11ll111111_opy_
            bstack11l111llll_opy_(bstack11ll111111_opy_.uuid)
            bstack11llllll1_opy_.bstack11l1l11l1l_opy_(bstack1ll111l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭Ꮌ"), bstack11ll111111_opy_)
        except Exception as err:
            print(bstack1ll111l_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡨࡤࡥࡡࡥࡩ࡫ࡵࡲࡦࡡࡶࡧࡪࡴࡡࡳ࡫ࡲ࠾ࠥࢁࡽࠨᎽ"), str(err))
def bstack11l11ll111_opy_(bstack11l1111111_opy_):
    if bstack11l1111111_opy_ in store[bstack1ll111l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫᎾ")]:
        store[bstack1ll111l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬᎿ")].remove(bstack11l1111111_opy_)
def bstack11l111llll_opy_(bstack11l1111lll_opy_):
    store[bstack1ll111l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭Ꮐ")] = bstack11l1111lll_opy_
    threading.current_thread().current_test_uuid = bstack11l1111lll_opy_
@bstack11llllll1_opy_.bstack11l1l1111l_opy_
def bstack111lllll1l_opy_(item, call, report):
    global bstack111lllllll_opy_
    try:
        if report.when == bstack1ll111l_opy_ (u"ࠪࡧࡦࡲ࡬ࠨᏁ"):
            bstack111llll1l1_opy_.reset()
        if report.when == bstack1ll111l_opy_ (u"ࠫࡨࡧ࡬࡭ࠩᏂ"):
            if bstack111lllllll_opy_ == bstack1ll111l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬᏃ"):
                _11l11l111l_opy_[item.nodeid][bstack1ll111l_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᏄ")] = bstack1l1l11lll1_opy_(report.stop)
                bstack11l111l1ll_opy_(item, _11l11l111l_opy_[item.nodeid], bstack1ll111l_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩᏅ"), report, call)
                store[bstack1ll111l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬᏆ")] = None
            elif bstack111lllllll_opy_ == bstack1ll111l_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠨᏇ"):
                bstack11ll111111_opy_ = _11l11l111l_opy_[item.nodeid][bstack1ll111l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭Ꮘ")]
                bstack11ll111111_opy_.set(hooks=_11l11l111l_opy_[item.nodeid].get(bstack1ll111l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪᏉ"), []))
                exception, bstack1l1l11l1ll_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack1l1l11l1ll_opy_ = [call.excinfo.exconly(), report.longreprtext]
                bstack11ll111111_opy_.stop(time=bstack1l1l11lll1_opy_(report.stop), result=Result(result=report.outcome, exception=exception, bstack1l1l11l1ll_opy_=bstack1l1l11l1ll_opy_))
                bstack11llllll1_opy_.bstack11l1l11l1l_opy_(bstack1ll111l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧᏊ"), _11l11l111l_opy_[item.nodeid][bstack1ll111l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩᏋ")])
        elif report.when in [bstack1ll111l_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭Ꮜ"), bstack1ll111l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪᏍ")]:
            bstack11l111l111_opy_ = item.nodeid + bstack1ll111l_opy_ (u"ࠩ࠰ࠫᏎ") + report.when
            if report.skipped:
                hook_type = bstack1ll111l_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡉࡆࡉࡈࠨᏏ") if report.when == bstack1ll111l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪᏐ") else bstack1ll111l_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡊࡇࡃࡉࠩᏑ")
                _11l11l111l_opy_[bstack11l111l111_opy_] = {
                    bstack1ll111l_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᏒ"): uuid4().__str__(),
                    bstack1ll111l_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫᏓ"): datetime.datetime.utcfromtimestamp(report.start).isoformat() + bstack1ll111l_opy_ (u"ࠨ࡜ࠪᏔ"),
                    bstack1ll111l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬᏕ"): hook_type
                }
            _11l11l111l_opy_[bstack11l111l111_opy_][bstack1ll111l_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᏖ")] = datetime.datetime.utcfromtimestamp(report.stop).isoformat() + bstack1ll111l_opy_ (u"ࠫ࡟࠭Ꮧ")
            bstack11l11ll111_opy_(_11l11l111l_opy_[bstack11l111l111_opy_][bstack1ll111l_opy_ (u"ࠬࡻࡵࡪࡦࠪᏘ")])
            bstack11l11l1l11_opy_(item, _11l11l111l_opy_[bstack11l111l111_opy_], bstack1ll111l_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨᏙ"), report, call)
            if report.when == bstack1ll111l_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭Ꮪ"):
                if report.outcome == bstack1ll111l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᏛ"):
                    bstack11l1111l1l_opy_ = {
                        bstack1ll111l_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᏜ"): uuid4().__str__(),
                        bstack1ll111l_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᏝ"): bstack1lll111l1l_opy_(),
                        bstack1ll111l_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᏞ"): bstack1lll111l1l_opy_()
                    }
                    _11l11l111l_opy_[item.nodeid] = {**_11l11l111l_opy_[item.nodeid], **bstack11l1111l1l_opy_}
                    bstack11l111l1ll_opy_(item, _11l11l111l_opy_[item.nodeid], bstack1ll111l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭Ꮯ"))
                    bstack11l111l1ll_opy_(item, _11l11l111l_opy_[item.nodeid], bstack1ll111l_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨᏠ"), report, call)
    except Exception as err:
        print(bstack1ll111l_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡨࡢࡰࡧࡰࡪࡥ࡯࠲࠳ࡼࡣࡹ࡫ࡳࡵࡡࡨࡺࡪࡴࡴ࠻ࠢࡾࢁࠬᏡ"), str(err))
def bstack111llll11l_opy_(test, bstack11l1111l1l_opy_, result=None, call=None, bstack1ll11l1l_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    bstack11ll111111_opy_ = {
        bstack1ll111l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭Ꮲ"): bstack11l1111l1l_opy_[bstack1ll111l_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᏣ")],
        bstack1ll111l_opy_ (u"ࠪࡸࡾࡶࡥࠨᏤ"): bstack1ll111l_opy_ (u"ࠫࡹ࡫ࡳࡵࠩᏥ"),
        bstack1ll111l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᏦ"): test.name,
        bstack1ll111l_opy_ (u"࠭ࡢࡰࡦࡼࠫᏧ"): {
            bstack1ll111l_opy_ (u"ࠧ࡭ࡣࡱ࡫ࠬᏨ"): bstack1ll111l_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨᏩ"),
            bstack1ll111l_opy_ (u"ࠩࡦࡳࡩ࡫ࠧᏪ"): inspect.getsource(test.obj)
        },
        bstack1ll111l_opy_ (u"ࠪ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧᏫ"): test.name,
        bstack1ll111l_opy_ (u"ࠫࡸࡩ࡯ࡱࡧࠪᏬ"): test.name,
        bstack1ll111l_opy_ (u"ࠬࡹࡣࡰࡲࡨࡷࠬᏭ"): bstack11llllll1_opy_.bstack11l1l11lll_opy_(test),
        bstack1ll111l_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩᏮ"): file_path,
        bstack1ll111l_opy_ (u"ࠧ࡭ࡱࡦࡥࡹ࡯࡯࡯ࠩᏯ"): file_path,
        bstack1ll111l_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᏰ"): bstack1ll111l_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪᏱ"),
        bstack1ll111l_opy_ (u"ࠪࡺࡨࡥࡦࡪ࡮ࡨࡴࡦࡺࡨࠨᏲ"): file_path,
        bstack1ll111l_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᏳ"): bstack11l1111l1l_opy_[bstack1ll111l_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩᏴ")],
        bstack1ll111l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩᏵ"): bstack1ll111l_opy_ (u"ࠧࡑࡻࡷࡩࡸࡺࠧ᏶"),
        bstack1ll111l_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡓࡧࡵࡹࡳࡖࡡࡳࡣࡰࠫ᏷"): {
            bstack1ll111l_opy_ (u"ࠩࡵࡩࡷࡻ࡮ࡠࡰࡤࡱࡪ࠭ᏸ"): test.nodeid
        },
        bstack1ll111l_opy_ (u"ࠪࡸࡦ࡭ࡳࠨᏹ"): bstack1l1l111ll1_opy_(test.own_markers)
    }
    if bstack1ll11l1l_opy_ in [bstack1ll111l_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡱࡩࡱࡲࡨࡨࠬᏺ"), bstack1ll111l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧᏻ")]:
        bstack11ll111111_opy_[bstack1ll111l_opy_ (u"࠭࡭ࡦࡶࡤࠫᏼ")] = {
            bstack1ll111l_opy_ (u"ࠧࡧ࡫ࡻࡸࡺࡸࡥࡴࠩᏽ"): bstack11l1111l1l_opy_.get(bstack1ll111l_opy_ (u"ࠨࡨ࡬ࡼࡹࡻࡲࡦࡵࠪ᏾"), [])
        }
    if bstack1ll11l1l_opy_ == bstack1ll111l_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖ࡯࡮ࡶࡰࡦࡦࠪ᏿"):
        bstack11ll111111_opy_[bstack1ll111l_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ᐀")] = bstack1ll111l_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬᐁ")
        bstack11ll111111_opy_[bstack1ll111l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫᐂ")] = bstack11l1111l1l_opy_[bstack1ll111l_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬᐃ")]
        bstack11ll111111_opy_[bstack1ll111l_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᐄ")] = bstack11l1111l1l_opy_[bstack1ll111l_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᐅ")]
    if result:
        bstack11ll111111_opy_[bstack1ll111l_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᐆ")] = result.outcome
        bstack11ll111111_opy_[bstack1ll111l_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࡤ࡯࡮ࡠ࡯ࡶࠫᐇ")] = result.duration * 1000
        bstack11ll111111_opy_[bstack1ll111l_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᐈ")] = bstack11l1111l1l_opy_[bstack1ll111l_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᐉ")]
        if result.failed:
            bstack11ll111111_opy_[bstack1ll111l_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩࠬᐊ")] = bstack11llllll1_opy_.bstack1l1ll11111_opy_(call.excinfo.typename)
            bstack11ll111111_opy_[bstack1ll111l_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨᐋ")] = bstack11llllll1_opy_.bstack11l1l111l1_opy_(call.excinfo, result)
        bstack11ll111111_opy_[bstack1ll111l_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧᐌ")] = bstack11l1111l1l_opy_[bstack1ll111l_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨᐍ")]
    if outcome:
        bstack11ll111111_opy_[bstack1ll111l_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᐎ")] = bstack1l1l11l111_opy_(outcome)
        bstack11ll111111_opy_[bstack1ll111l_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳࡥࡩ࡯ࡡࡰࡷࠬᐏ")] = 0
        bstack11ll111111_opy_[bstack1ll111l_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᐐ")] = bstack11l1111l1l_opy_[bstack1ll111l_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᐑ")]
        if bstack11ll111111_opy_[bstack1ll111l_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᐒ")] == bstack1ll111l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᐓ"):
            bstack11ll111111_opy_[bstack1ll111l_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠨᐔ")] = bstack1ll111l_opy_ (u"࡙ࠪࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠫᐕ")  # bstack11l11l11l1_opy_
            bstack11ll111111_opy_[bstack1ll111l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬᐖ")] = [{bstack1ll111l_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨᐗ"): [bstack1ll111l_opy_ (u"࠭ࡳࡰ࡯ࡨࠤࡪࡸࡲࡰࡴࠪᐘ")]}]
        bstack11ll111111_opy_[bstack1ll111l_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭ᐙ")] = bstack11l1111l1l_opy_[bstack1ll111l_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧᐚ")]
    return bstack11ll111111_opy_
def bstack111lll1l1l_opy_(test, bstack111lllll11_opy_, bstack1ll11l1l_opy_, result, call, outcome, bstack111llllll1_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack111lllll11_opy_[bstack1ll111l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬᐛ")]
    hook_name = bstack111lllll11_opy_[bstack1ll111l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡰࡤࡱࡪ࠭ᐜ")]
    hook_data = {
        bstack1ll111l_opy_ (u"ࠫࡺࡻࡩࡥࠩᐝ"): bstack111lllll11_opy_[bstack1ll111l_opy_ (u"ࠬࡻࡵࡪࡦࠪᐞ")],
        bstack1ll111l_opy_ (u"࠭ࡴࡺࡲࡨࠫᐟ"): bstack1ll111l_opy_ (u"ࠧࡩࡱࡲ࡯ࠬᐠ"),
        bstack1ll111l_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᐡ"): bstack1ll111l_opy_ (u"ࠩࡾࢁࠬᐢ").format(bstack11lll1lll1_opy_(hook_name)),
        bstack1ll111l_opy_ (u"ࠪࡦࡴࡪࡹࠨᐣ"): {
            bstack1ll111l_opy_ (u"ࠫࡱࡧ࡮ࡨࠩᐤ"): bstack1ll111l_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬᐥ"),
            bstack1ll111l_opy_ (u"࠭ࡣࡰࡦࡨࠫᐦ"): None
        },
        bstack1ll111l_opy_ (u"ࠧࡴࡥࡲࡴࡪ࠭ᐧ"): test.name,
        bstack1ll111l_opy_ (u"ࠨࡵࡦࡳࡵ࡫ࡳࠨᐨ"): bstack11llllll1_opy_.bstack11l1l11lll_opy_(test, hook_name),
        bstack1ll111l_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬᐩ"): file_path,
        bstack1ll111l_opy_ (u"ࠪࡰࡴࡩࡡࡵ࡫ࡲࡲࠬᐪ"): file_path,
        bstack1ll111l_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᐫ"): bstack1ll111l_opy_ (u"ࠬࡶࡥ࡯ࡦ࡬ࡲ࡬࠭ᐬ"),
        bstack1ll111l_opy_ (u"࠭ࡶࡤࡡࡩ࡭ࡱ࡫ࡰࡢࡶ࡫ࠫᐭ"): file_path,
        bstack1ll111l_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫᐮ"): bstack111lllll11_opy_[bstack1ll111l_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᐯ")],
        bstack1ll111l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬᐰ"): bstack1ll111l_opy_ (u"ࠪࡔࡾࡺࡥࡴࡶ࠰ࡧࡺࡩࡵ࡮ࡤࡨࡶࠬᐱ") if bstack111lllllll_opy_ == bstack1ll111l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠨᐲ") else bstack1ll111l_opy_ (u"ࠬࡖࡹࡵࡧࡶࡸࠬᐳ"),
        bstack1ll111l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩᐴ"): hook_type
    }
    bstack11l111ll11_opy_ = bstack11l11l1ll1_opy_(_11l11l111l_opy_.get(test.nodeid, None))
    if bstack11l111ll11_opy_:
        hook_data[bstack1ll111l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡ࡬ࡨࠬᐵ")] = bstack11l111ll11_opy_
    if result:
        hook_data[bstack1ll111l_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᐶ")] = result.outcome
        hook_data[bstack1ll111l_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࡣ࡮ࡴ࡟࡮ࡵࠪᐷ")] = result.duration * 1000
        hook_data[bstack1ll111l_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᐸ")] = bstack111lllll11_opy_[bstack1ll111l_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᐹ")]
        if result.failed:
            hook_data[bstack1ll111l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠫᐺ")] = bstack11llllll1_opy_.bstack1l1ll11111_opy_(call.excinfo.typename)
            hook_data[bstack1ll111l_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧᐻ")] = bstack11llllll1_opy_.bstack11l1l111l1_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstack1ll111l_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᐼ")] = bstack1l1l11l111_opy_(outcome)
        hook_data[bstack1ll111l_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࡢ࡭ࡳࡥ࡭ࡴࠩᐽ")] = 100
        hook_data[bstack1ll111l_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᐾ")] = bstack111lllll11_opy_[bstack1ll111l_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᐿ")]
        if hook_data[bstack1ll111l_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᑀ")] == bstack1ll111l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᑁ"):
            hook_data[bstack1ll111l_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩࠬᑂ")] = bstack1ll111l_opy_ (u"ࠧࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠨᑃ")  # bstack11l11l11l1_opy_
            hook_data[bstack1ll111l_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࠩᑄ")] = [{bstack1ll111l_opy_ (u"ࠩࡥࡥࡨࡱࡴࡳࡣࡦࡩࠬᑅ"): [bstack1ll111l_opy_ (u"ࠪࡷࡴࡳࡥࠡࡧࡵࡶࡴࡸࠧᑆ")]}]
    if bstack111llllll1_opy_:
        hook_data[bstack1ll111l_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᑇ")] = bstack111llllll1_opy_.result
        hook_data[bstack1ll111l_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴ࡟ࡪࡰࡢࡱࡸ࠭ᑈ")] = bstack1l1ll111ll_opy_(bstack111lllll11_opy_[bstack1ll111l_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪᑉ")], bstack111lllll11_opy_[bstack1ll111l_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᑊ")])
        hook_data[bstack1ll111l_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᑋ")] = bstack111lllll11_opy_[bstack1ll111l_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᑌ")]
        if hook_data[bstack1ll111l_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᑍ")] == bstack1ll111l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᑎ"):
            hook_data[bstack1ll111l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠫᑏ")] = bstack11llllll1_opy_.bstack1l1ll11111_opy_(bstack111llllll1_opy_.exception_type)
            hook_data[bstack1ll111l_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧᑐ")] = [{bstack1ll111l_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪᑑ"): bstack1l1l11l1l1_opy_(bstack111llllll1_opy_.exception)}]
    return hook_data
def bstack11l111l1ll_opy_(test, bstack11l1111l1l_opy_, bstack1ll11l1l_opy_, result=None, call=None, outcome=None):
    bstack11ll111111_opy_ = bstack111llll11l_opy_(test, bstack11l1111l1l_opy_, result, call, bstack1ll11l1l_opy_, outcome)
    driver = getattr(test, bstack1ll111l_opy_ (u"ࠨࡡࡧࡶ࡮ࡼࡥࡳࠩᑒ"), None)
    if bstack1ll11l1l_opy_ == bstack1ll111l_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪᑓ") and driver:
        bstack11ll111111_opy_[bstack1ll111l_opy_ (u"ࠪ࡭ࡳࡺࡥࡨࡴࡤࡸ࡮ࡵ࡮ࡴࠩᑔ")] = bstack11llllll1_opy_.bstack11l11lll1l_opy_(driver)
    if bstack1ll11l1l_opy_ == bstack1ll111l_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡱࡩࡱࡲࡨࡨࠬᑕ"):
        bstack1ll11l1l_opy_ = bstack1ll111l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧᑖ")
    bstack11l1ll1l1l_opy_ = {
        bstack1ll111l_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪᑗ"): bstack1ll11l1l_opy_,
        bstack1ll111l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࠩᑘ"): bstack11ll111111_opy_
    }
    bstack11llllll1_opy_.bstack11l1l1l1ll_opy_(bstack11l1ll1l1l_opy_)
def bstack11l11l1l11_opy_(test, bstack11l1111l1l_opy_, bstack1ll11l1l_opy_, result=None, call=None, outcome=None, bstack111llllll1_opy_=None):
    hook_data = bstack111lll1l1l_opy_(test, bstack11l1111l1l_opy_, bstack1ll11l1l_opy_, result, call, outcome, bstack111llllll1_opy_)
    bstack11l1ll1l1l_opy_ = {
        bstack1ll111l_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬᑙ"): bstack1ll11l1l_opy_,
        bstack1ll111l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࠫᑚ"): hook_data
    }
    bstack11llllll1_opy_.bstack11l1l1l1ll_opy_(bstack11l1ll1l1l_opy_)
def bstack11l11l1ll1_opy_(bstack11l1111l1l_opy_):
    if not bstack11l1111l1l_opy_:
        return None
    if bstack11l1111l1l_opy_.get(bstack1ll111l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ᑛ"), None):
        return getattr(bstack11l1111l1l_opy_[bstack1ll111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧᑜ")], bstack1ll111l_opy_ (u"ࠬࡻࡵࡪࡦࠪᑝ"), None)
    return bstack11l1111l1l_opy_.get(bstack1ll111l_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᑞ"), None)
@pytest.fixture(autouse=True)
def second_fixture(caplog, request):
    yield
    try:
        if not bstack11llllll1_opy_.on():
            return
        places = [bstack1ll111l_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭ᑟ"), bstack1ll111l_opy_ (u"ࠨࡥࡤࡰࡱ࠭ᑠ"), bstack1ll111l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫᑡ")]
        bstack11l1ll1111_opy_ = []
        for bstack11l11111l1_opy_ in places:
            records = caplog.get_records(bstack11l11111l1_opy_)
            bstack111llll1ll_opy_ = bstack1ll111l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᑢ") if bstack11l11111l1_opy_ == bstack1ll111l_opy_ (u"ࠫࡨࡧ࡬࡭ࠩᑣ") else bstack1ll111l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᑤ")
            bstack11l111ll1l_opy_ = request.node.nodeid + (bstack1ll111l_opy_ (u"࠭ࠧᑥ") if bstack11l11111l1_opy_ == bstack1ll111l_opy_ (u"ࠧࡤࡣ࡯ࡰࠬᑦ") else bstack1ll111l_opy_ (u"ࠨ࠯ࠪᑧ") + bstack11l11111l1_opy_)
            bstack11l1111lll_opy_ = bstack11l11l1ll1_opy_(_11l11l111l_opy_.get(bstack11l111ll1l_opy_, None))
            if not bstack11l1111lll_opy_:
                continue
            for record in records:
                if bstack1l1l1ll111_opy_(record.message):
                    continue
                bstack11l1ll1111_opy_.append({
                    bstack1ll111l_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬᑨ"): datetime.datetime.utcfromtimestamp(record.created).isoformat() + bstack1ll111l_opy_ (u"ࠪ࡞ࠬᑩ"),
                    bstack1ll111l_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪᑪ"): record.levelname,
                    bstack1ll111l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᑫ"): record.message,
                    bstack111llll1ll_opy_: bstack11l1111lll_opy_
                })
        if len(bstack11l1ll1111_opy_) > 0:
            bstack11llllll1_opy_.bstack11l1ll11ll_opy_(bstack11l1ll1111_opy_)
    except Exception as err:
        print(bstack1ll111l_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡥࡤࡱࡱࡨࡤ࡬ࡩࡹࡶࡸࡶࡪࡀࠠࡼࡿࠪᑬ"), str(err))
def bstack111llll111_opy_(driver_command, response):
    if driver_command == bstack1ll111l_opy_ (u"ࠧࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠫᑭ"):
        bstack11llllll1_opy_.bstack11l1l1l11l_opy_({
            bstack1ll111l_opy_ (u"ࠨ࡫ࡰࡥ࡬࡫ࠧᑮ"): response[bstack1ll111l_opy_ (u"ࠩࡹࡥࡱࡻࡥࠨᑯ")],
            bstack1ll111l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᑰ"): store[bstack1ll111l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨᑱ")]
        })
def bstack1l11l11l_opy_():
    global bstack1l11lllll_opy_
    bstack11llllll1_opy_.bstack11l1l1llll_opy_()
    for driver in bstack1l11lllll_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1lll11111l_opy_(self, *args, **kwargs):
    bstack1111111l1_opy_ = bstack11l1l1ll1_opy_(self, *args, **kwargs)
    bstack11llllll1_opy_.bstack1l111ll1l_opy_(self)
    return bstack1111111l1_opy_
def bstack11l11l1ll_opy_(framework_name):
    global bstack1l1ll1lll_opy_
    global bstack11lll1ll_opy_
    bstack1l1ll1lll_opy_ = framework_name
    logger.info(bstack1l1lllll_opy_.format(bstack1l1ll1lll_opy_.split(bstack1ll111l_opy_ (u"ࠬ࠳ࠧᑲ"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack1l1l11llll_opy_():
            Service.start = bstack1ll11llll1_opy_
            Service.stop = bstack111111l1l_opy_
            webdriver.Remote.__init__ = bstack11l111ll1_opy_
            webdriver.Remote.get = bstack1lllll1l1_opy_
            if not isinstance(os.getenv(bstack1ll111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖ࡙ࡕࡇࡖࡘࡤࡖࡁࡓࡃࡏࡐࡊࡒࠧᑳ")), str):
                return
            WebDriver.close = bstack111llll1_opy_
            WebDriver.quit = bstack1111ll11_opy_
        if not bstack1l1l11llll_opy_() and bstack11llllll1_opy_.on():
            webdriver.Remote.__init__ = bstack1lll11111l_opy_
        bstack11lll1ll_opy_ = True
    except Exception as e:
        pass
    bstack111l1l1l1_opy_()
    if os.environ.get(bstack1ll111l_opy_ (u"ࠧࡔࡇࡏࡉࡓࡏࡕࡎࡡࡒࡖࡤࡖࡌࡂ࡛࡚ࡖࡎࡍࡈࡕࡡࡌࡒࡘ࡚ࡁࡍࡎࡈࡈࠬᑴ")):
        bstack11lll1ll_opy_ = eval(os.environ.get(bstack1ll111l_opy_ (u"ࠨࡕࡈࡐࡊࡔࡉࡖࡏࡢࡓࡗࡥࡐࡍࡃ࡜࡛ࡗࡏࡇࡉࡖࡢࡍࡓ࡙ࡔࡂࡎࡏࡉࡉ࠭ᑵ")))
    if not bstack11lll1ll_opy_:
        bstack1l1lll1l1_opy_(bstack1ll111l_opy_ (u"ࠤࡓࡥࡨࡱࡡࡨࡧࡶࠤࡳࡵࡴࠡ࡫ࡱࡷࡹࡧ࡬࡭ࡧࡧࠦᑶ"), bstack1l1ll1l1l_opy_)
    if bstack1llllll1l_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            RemoteConnection._get_proxy_url = bstack1ll1l11ll1_opy_
        except Exception as e:
            logger.error(bstack1ll1l1ll_opy_.format(str(e)))
    if bstack1ll111l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪᑷ") in str(framework_name).lower():
        if not bstack1l1l11llll_opy_():
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
def bstack1111ll11_opy_(self):
    global bstack1l1ll1lll_opy_
    global bstack1ll1l1l111_opy_
    global bstack1ll11lll_opy_
    try:
        if bstack1ll111l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫᑸ") in bstack1l1ll1lll_opy_ and self.session_id != None and bstack1lll1111_opy_(threading.current_thread(), bstack1ll111l_opy_ (u"ࠬࡺࡥࡴࡶࡖࡸࡦࡺࡵࡴࠩᑹ"), bstack1ll111l_opy_ (u"࠭ࠧᑺ")) != bstack1ll111l_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨᑻ"):
            bstack1l11l11ll_opy_ = bstack1ll111l_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨᑼ") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack1ll111l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᑽ")
            bstack1llll111l_opy_ = bstack1l11ll1l1_opy_(bstack1ll111l_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭ᑾ"), bstack1ll111l_opy_ (u"ࠫࠬᑿ"), bstack1l11l11ll_opy_, bstack1ll111l_opy_ (u"ࠬ࠲ࠠࠨᒀ").join(
                threading.current_thread().bstackTestErrorMessages), bstack1ll111l_opy_ (u"࠭ࠧᒁ"), bstack1ll111l_opy_ (u"ࠧࠨᒂ"))
            if self != None:
                self.execute_script(bstack1llll111l_opy_)
    except Exception as e:
        logger.debug(bstack1ll111l_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦ࡭ࡢࡴ࡮࡭ࡳ࡭ࠠࡴࡶࡤࡸࡺࡹ࠺ࠡࠤᒃ") + str(e))
    bstack1ll11lll_opy_(self)
    self.session_id = None
def bstack11l111ll1_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack1ll1l1l111_opy_
    global bstack1ll11ll111_opy_
    global bstack11l1111l_opy_
    global bstack1l1ll1lll_opy_
    global bstack11l1l1ll1_opy_
    global bstack1l11lllll_opy_
    global bstack1llll11l_opy_
    global bstack11lll1lll_opy_
    CONFIG[bstack1ll111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫᒄ")] = str(bstack1l1ll1lll_opy_) + str(__version__)
    command_executor = bstack1lll1lll1_opy_(bstack1llll11l_opy_)
    logger.debug(bstack1l111llll_opy_.format(command_executor))
    proxy = bstack1l1lll1ll_opy_(CONFIG, proxy)
    bstack11lll1ll1_opy_ = 0
    try:
        if bstack11l1111l_opy_ is True:
            bstack11lll1ll1_opy_ = int(os.environ.get(bstack1ll111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪᒅ")))
    except:
        bstack11lll1ll1_opy_ = 0
    bstack1lllll1l1l_opy_ = bstack1ll1l11111_opy_(CONFIG, bstack11lll1ll1_opy_)
    logger.debug(bstack1llllll1ll_opy_.format(str(bstack1lllll1l1l_opy_)))
    if bstack1ll111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨᒆ") in CONFIG and CONFIG[bstack1ll111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩᒇ")]:
        bstack11l1l1ll_opy_(bstack1lllll1l1l_opy_, bstack11lll1lll_opy_)
    if desired_capabilities:
        bstack11llll11l_opy_ = bstack11l11l11l_opy_(desired_capabilities)
        bstack11llll11l_opy_[bstack1ll111l_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭ᒈ")] = bstack1111l11l_opy_(CONFIG)
        bstack11lll11l_opy_ = bstack1ll1l11111_opy_(bstack11llll11l_opy_)
        if bstack11lll11l_opy_:
            bstack1lllll1l1l_opy_ = update(bstack11lll11l_opy_, bstack1lllll1l1l_opy_)
        desired_capabilities = None
    if options:
        bstack1l1ll1ll_opy_(options, bstack1lllll1l1l_opy_)
    if not options:
        options = bstack11l11l1l1_opy_(bstack1lllll1l1l_opy_)
    if proxy and bstack1l1111lll_opy_() >= version.parse(bstack1ll111l_opy_ (u"ࠧ࠵࠰࠴࠴࠳࠶ࠧᒉ")):
        options.proxy(proxy)
    if options and bstack1l1111lll_opy_() >= version.parse(bstack1ll111l_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧᒊ")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack1l1111lll_opy_() < version.parse(bstack1ll111l_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨᒋ")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack1lllll1l1l_opy_)
    logger.info(bstack11l1lll1l_opy_)
    if bstack1l1111lll_opy_() >= version.parse(bstack1ll111l_opy_ (u"ࠪ࠸࠳࠷࠰࠯࠲ࠪᒌ")):
        bstack11l1l1ll1_opy_(self, command_executor=command_executor,
                  options=options, keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1l1111lll_opy_() >= version.parse(bstack1ll111l_opy_ (u"ࠫ࠸࠴࠸࠯࠲ࠪᒍ")):
        bstack11l1l1ll1_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities, options=options,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1l1111lll_opy_() >= version.parse(bstack1ll111l_opy_ (u"ࠬ࠸࠮࠶࠵࠱࠴ࠬᒎ")):
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
        bstack111l1l1l_opy_ = bstack1ll111l_opy_ (u"࠭ࠧᒏ")
        if bstack1l1111lll_opy_() >= version.parse(bstack1ll111l_opy_ (u"ࠧ࠵࠰࠳࠲࠵ࡨ࠱ࠨᒐ")):
            bstack111l1l1l_opy_ = self.caps.get(bstack1ll111l_opy_ (u"ࠣࡱࡳࡸ࡮ࡳࡡ࡭ࡊࡸࡦ࡚ࡸ࡬ࠣᒑ"))
        else:
            bstack111l1l1l_opy_ = self.capabilities.get(bstack1ll111l_opy_ (u"ࠤࡲࡴࡹ࡯࡭ࡢ࡮ࡋࡹࡧ࡛ࡲ࡭ࠤᒒ"))
        if bstack111l1l1l_opy_:
            if bstack1l1111lll_opy_() <= version.parse(bstack1ll111l_opy_ (u"ࠪ࠷࠳࠷࠳࠯࠲ࠪᒓ")):
                self.command_executor._url = bstack1ll111l_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧᒔ") + bstack1llll11l_opy_ + bstack1ll111l_opy_ (u"ࠧࡀ࠸࠱࠱ࡺࡨ࠴࡮ࡵࡣࠤᒕ")
            else:
                self.command_executor._url = bstack1ll111l_opy_ (u"ࠨࡨࡵࡶࡳࡷ࠿࠵࠯ࠣᒖ") + bstack111l1l1l_opy_ + bstack1ll111l_opy_ (u"ࠢ࠰ࡹࡧ࠳࡭ࡻࡢࠣᒗ")
            logger.debug(bstack11l1ll1ll_opy_.format(bstack111l1l1l_opy_))
        else:
            logger.debug(bstack111l1111_opy_.format(bstack1ll111l_opy_ (u"ࠣࡑࡳࡸ࡮ࡳࡡ࡭ࠢࡋࡹࡧࠦ࡮ࡰࡶࠣࡪࡴࡻ࡮ࡥࠤᒘ")))
    except Exception as e:
        logger.debug(bstack111l1111_opy_.format(e))
    bstack1ll1l1l111_opy_ = self.session_id
    if bstack1ll111l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩᒙ") in bstack1l1ll1lll_opy_:
        threading.current_thread().bstack11llll111_opy_ = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        bstack11llllll1_opy_.bstack1l111ll1l_opy_(self)
    bstack1l11lllll_opy_.append(self)
    if bstack1ll111l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ᒚ") in CONFIG and bstack1ll111l_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩᒛ") in CONFIG[bstack1ll111l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨᒜ")][bstack11lll1ll1_opy_]:
        bstack1ll11ll111_opy_ = CONFIG[bstack1ll111l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩᒝ")][bstack11lll1ll1_opy_][bstack1ll111l_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬᒞ")]
    logger.debug(bstack1l1l1111_opy_.format(bstack1ll1l1l111_opy_))
def bstack1lllll1l1_opy_(self, url):
    global bstack11l1l11l1_opy_
    global CONFIG
    try:
        bstack1lllll111_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack111ll1l1l_opy_.format(str(err)))
    try:
        bstack11l1l11l1_opy_(self, url)
    except Exception as e:
        try:
            bstack1l1ll11ll_opy_ = str(e)
            if any(err_msg in bstack1l1ll11ll_opy_ for err_msg in bstack1l1111l1l_opy_):
                bstack1lllll111_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack111ll1l1l_opy_.format(str(err)))
        raise e
def bstack11111lll_opy_(item, when):
    global bstack1lll11l11_opy_
    try:
        bstack1lll11l11_opy_(item, when)
    except Exception as e:
        pass
def bstack1llll11ll1_opy_(item, call, rep):
    global bstack1lllll11ll_opy_
    global bstack1l11lllll_opy_
    name = bstack1ll111l_opy_ (u"ࠨࠩᒟ")
    try:
        if rep.when == bstack1ll111l_opy_ (u"ࠩࡦࡥࡱࡲࠧᒠ"):
            bstack1ll1l1l111_opy_ = threading.current_thread().bstack11llll111_opy_
            bstack11l11l11ll_opy_ = item.config.getoption(bstack1ll111l_opy_ (u"ࠪࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬᒡ"))
            try:
                if (str(bstack11l11l11ll_opy_).lower() != bstack1ll111l_opy_ (u"ࠫࡹࡸࡵࡦࠩᒢ")):
                    name = str(rep.nodeid)
                    bstack1llll111l_opy_ = bstack1l11ll1l1_opy_(bstack1ll111l_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ᒣ"), name, bstack1ll111l_opy_ (u"࠭ࠧᒤ"), bstack1ll111l_opy_ (u"ࠧࠨᒥ"), bstack1ll111l_opy_ (u"ࠨࠩᒦ"), bstack1ll111l_opy_ (u"ࠩࠪᒧ"))
                    for driver in bstack1l11lllll_opy_:
                        if bstack1ll1l1l111_opy_ == driver.session_id:
                            driver.execute_script(bstack1llll111l_opy_)
            except Exception as e:
                logger.debug(bstack1ll111l_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠤ࡫ࡵࡲࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡹࡥࡴࡵ࡬ࡳࡳࡀࠠࡼࡿࠪᒨ").format(str(e)))
            try:
                bstack111ll1lll_opy_(rep.outcome.lower())
                if rep.outcome.lower() != bstack1ll111l_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬᒩ"):
                    status = bstack1ll111l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᒪ") if rep.outcome.lower() == bstack1ll111l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᒫ") else bstack1ll111l_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᒬ")
                    reason = bstack1ll111l_opy_ (u"ࠨࠩᒭ")
                    if (reason != bstack1ll111l_opy_ (u"ࠤࠥᒮ")):
                        try:
                            if (threading.current_thread().bstackTestErrorMessages == None):
                                threading.current_thread().bstackTestErrorMessages = []
                        except Exception as e:
                            threading.current_thread().bstackTestErrorMessages = []
                        threading.current_thread().bstackTestErrorMessages.append(str(reason))
                    if status == bstack1ll111l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᒯ"):
                        reason = rep.longrepr.reprcrash.message
                        if (not threading.current_thread().bstackTestErrorMessages):
                            threading.current_thread().bstackTestErrorMessages = []
                        threading.current_thread().bstackTestErrorMessages.append(reason)
                    level = bstack1ll111l_opy_ (u"ࠫ࡮ࡴࡦࡰࠩᒰ") if status == bstack1ll111l_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᒱ") else bstack1ll111l_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬᒲ")
                    data = name + bstack1ll111l_opy_ (u"ࠧࠡࡲࡤࡷࡸ࡫ࡤࠢࠩᒳ") if status == bstack1ll111l_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨᒴ") else name + bstack1ll111l_opy_ (u"ࠩࠣࡪࡦ࡯࡬ࡦࡦࠤࠤࠬᒵ") + reason
                    bstack111lll1l_opy_ = bstack1l11ll1l1_opy_(bstack1ll111l_opy_ (u"ࠪࡥࡳࡴ࡯ࡵࡣࡷࡩࠬᒶ"), bstack1ll111l_opy_ (u"ࠫࠬᒷ"), bstack1ll111l_opy_ (u"ࠬ࠭ᒸ"), bstack1ll111l_opy_ (u"࠭ࠧᒹ"), level, data)
                    for driver in bstack1l11lllll_opy_:
                        if bstack1ll1l1l111_opy_ == driver.session_id:
                            driver.execute_script(bstack111lll1l_opy_)
            except Exception as e:
                logger.debug(bstack1ll111l_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࠤࡨࡵ࡮ࡵࡧࡻࡸࠥ࡬࡯ࡳࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡳࡦࡵࡶ࡭ࡴࡴ࠺ࠡࡽࢀࠫᒺ").format(str(e)))
    except Exception as e:
        logger.debug(bstack1ll111l_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡸࡺࡡࡵࡧࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡸࡪࡹࡴࠡࡵࡷࡥࡹࡻࡳ࠻ࠢࡾࢁࠬᒻ").format(str(e)))
    bstack1lllll11ll_opy_(item, call, rep)
notset = Notset()
def bstack1l1l1111l_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack1ll11lll11_opy_
    if str(name).lower() == bstack1ll111l_opy_ (u"ࠩࡧࡶ࡮ࡼࡥࡳࠩᒼ"):
        return bstack1ll111l_opy_ (u"ࠥࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠤᒽ")
    else:
        return bstack1ll11lll11_opy_(self, name, default, skip)
def bstack1ll1l11ll1_opy_(self):
    global CONFIG
    global bstack11l1llll_opy_
    try:
        proxy = bstack111llll11_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack1ll111l_opy_ (u"ࠫ࠳ࡶࡡࡤࠩᒾ")):
                proxies = bstack11l1l1l1l_opy_(proxy, bstack1lll1lll1_opy_())
                if len(proxies) > 0:
                    protocol, bstack11ll1ll11_opy_ = proxies.popitem()
                    if bstack1ll111l_opy_ (u"ࠧࡀ࠯࠰ࠤᒿ") in bstack11ll1ll11_opy_:
                        return bstack11ll1ll11_opy_
                    else:
                        return bstack1ll111l_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢᓀ") + bstack11ll1ll11_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack1ll111l_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡴࡷࡵࡸࡺࠢࡸࡶࡱࠦ࠺ࠡࡽࢀࠦᓁ").format(str(e)))
    return bstack11l1llll_opy_(self)
def bstack1llllll1l_opy_():
    return bstack1ll111l_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫᓂ") in CONFIG or bstack1ll111l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ᓃ") in CONFIG and bstack1l1111lll_opy_() >= version.parse(
        bstack1ll1lll1ll_opy_)
def bstack1l111l1l_opy_(self,
               executablePath=None,
               channel=None,
               args=None,
               ignoreDefaultArgs=None,
               handleSIGINT=None,
               handleSIGTERM=None,
               handleSIGHUP=None,
               timeout=None,
               env=None,
               headless=None,
               devtools=None,
               proxy=None,
               downloadsPath=None,
               slowMo=None,
               tracesDir=None,
               chromiumSandbox=None,
               firefoxUserPrefs=None
               ):
    global CONFIG
    global bstack1ll11ll111_opy_
    global bstack11l1111l_opy_
    global bstack1l1ll1lll_opy_
    CONFIG[bstack1ll111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬᓄ")] = str(bstack1l1ll1lll_opy_) + str(__version__)
    bstack11lll1ll1_opy_ = 0
    try:
        if bstack11l1111l_opy_ is True:
            bstack11lll1ll1_opy_ = int(os.environ.get(bstack1ll111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫᓅ")))
    except:
        bstack11lll1ll1_opy_ = 0
    CONFIG[bstack1ll111l_opy_ (u"ࠧ࡯ࡳࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦᓆ")] = True
    bstack1lllll1l1l_opy_ = bstack1ll1l11111_opy_(CONFIG, bstack11lll1ll1_opy_)
    logger.debug(bstack1llllll1ll_opy_.format(str(bstack1lllll1l1l_opy_)))
    if CONFIG.get(bstack1ll111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪᓇ")):
        bstack11l1l1ll_opy_(bstack1lllll1l1l_opy_, bstack11lll1lll_opy_)
    if bstack1ll111l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᓈ") in CONFIG and bstack1ll111l_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ᓉ") in CONFIG[bstack1ll111l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬᓊ")][bstack11lll1ll1_opy_]:
        bstack1ll11ll111_opy_ = CONFIG[bstack1ll111l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ᓋ")][bstack11lll1ll1_opy_][bstack1ll111l_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩᓌ")]
    import urllib
    import json
    bstack1lll11111_opy_ = bstack1ll111l_opy_ (u"ࠬࡽࡳࡴ࠼࠲࠳ࡨࡪࡰ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡀࡥࡤࡴࡸࡃࠧᓍ") + urllib.parse.quote(json.dumps(bstack1lllll1l1l_opy_))
    browser = self.connect(bstack1lll11111_opy_)
    return browser
def bstack111l1l1l1_opy_():
    global bstack11lll1ll_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        BrowserType.launch = bstack1l111l1l_opy_
        bstack11lll1ll_opy_ = True
    except Exception as e:
        pass
def bstack11l111lll1_opy_():
    global CONFIG
    global bstack1lll11l1l1_opy_
    global bstack1llll11l_opy_
    global bstack11lll1lll_opy_
    global bstack11l1111l_opy_
    CONFIG = json.loads(os.environ.get(bstack1ll111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡏࡏࡈࡌࡋࠬᓎ")))
    bstack1lll11l1l1_opy_ = eval(os.environ.get(bstack1ll111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨᓏ")))
    bstack1llll11l_opy_ = os.environ.get(bstack1ll111l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡉࡗࡅࡣ࡚ࡘࡌࠨᓐ"))
    bstack1l1l1lll_opy_(CONFIG, bstack1lll11l1l1_opy_)
    bstack1ll1l1l1l_opy_()
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
    if bstack1ll111l_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬᓑ") in CONFIG or bstack1ll111l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧᓒ") in CONFIG:
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
        logger.debug(bstack1ll111l_opy_ (u"ࠫࡕࡲࡥࡢࡵࡨࠤ࡮ࡴࡳࡵࡣ࡯ࡰࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡳࠥࡸࡵ࡯ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡴࡦࡵࡷࡷࠬᓓ"))
    bstack11lll1lll_opy_ = CONFIG.get(bstack1ll111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩᓔ"), {}).get(bstack1ll111l_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨᓕ"))
    bstack11l1111l_opy_ = True
    bstack11l11l1ll_opy_(bstack111l11l11_opy_)
if (bstack1l1l1l11l1_opy_()):
    bstack11l111lll1_opy_()
@bstack1l1l1l1l1l_opy_(class_method=False)
def bstack11l111l11l_opy_(hook_name, event, bstack11l11l1l1l_opy_=None):
    if hook_name not in [bstack1ll111l_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨᓖ"), bstack1ll111l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠬᓗ"), bstack1ll111l_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡲࡨࡺࡲࡥࠨᓘ"), bstack1ll111l_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳ࡯ࡥࡷ࡯ࡩࠬᓙ"), bstack1ll111l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡧࡱࡧࡳࡴࠩᓚ"), bstack1ll111l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡤ࡮ࡤࡷࡸ࠭ᓛ"), bstack1ll111l_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳࡥࡵࡪࡲࡨࠬᓜ"), bstack1ll111l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡩࡹ࡮࡯ࡥࠩᓝ")]:
        return
    node = store[bstack1ll111l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡶࡨࡱࠬᓞ")]
    if hook_name in [bstack1ll111l_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡲࡨࡺࡲࡥࠨᓟ"), bstack1ll111l_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳ࡯ࡥࡷ࡯ࡩࠬᓠ")]:
        node = store[bstack1ll111l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡳ࡯ࡥࡷ࡯ࡩࡤ࡯ࡴࡦ࡯ࠪᓡ")]
    elif hook_name in [bstack1ll111l_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡨࡲࡡࡴࡵࠪᓢ"), bstack1ll111l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡥ࡯ࡥࡸࡹࠧᓣ")]:
        node = store[bstack1ll111l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡥ࡯ࡥࡸࡹ࡟ࡪࡶࡨࡱࠬᓤ")]
    if event == bstack1ll111l_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࠨᓥ"):
        hook_type = bstack11llll11l1_opy_(hook_name)
        uuid = uuid4().__str__()
        bstack111lllll11_opy_ = {
            bstack1ll111l_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᓦ"): uuid,
            bstack1ll111l_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᓧ"): bstack1lll111l1l_opy_(),
            bstack1ll111l_opy_ (u"ࠫࡹࡿࡰࡦࠩᓨ"): bstack1ll111l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪᓩ"),
            bstack1ll111l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩᓪ"): hook_type,
            bstack1ll111l_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡴࡡ࡮ࡧࠪᓫ"): hook_name
        }
        store[bstack1ll111l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬᓬ")].append(uuid)
        bstack11l11l1lll_opy_ = node.nodeid
        if hook_type == bstack1ll111l_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧᓭ"):
            if not _11l11l111l_opy_.get(bstack11l11l1lll_opy_, None):
                _11l11l111l_opy_[bstack11l11l1lll_opy_] = {bstack1ll111l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩᓮ"): []}
            _11l11l111l_opy_[bstack11l11l1lll_opy_][bstack1ll111l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪᓯ")].append(bstack111lllll11_opy_[bstack1ll111l_opy_ (u"ࠬࡻࡵࡪࡦࠪᓰ")])
        _11l11l111l_opy_[bstack11l11l1lll_opy_ + bstack1ll111l_opy_ (u"࠭࠭ࠨᓱ") + hook_name] = bstack111lllll11_opy_
        bstack11l11l1l11_opy_(node, bstack111lllll11_opy_, bstack1ll111l_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨᓲ"))
    elif event == bstack1ll111l_opy_ (u"ࠨࡣࡩࡸࡪࡸࠧᓳ"):
        bstack11l111l111_opy_ = node.nodeid + bstack1ll111l_opy_ (u"ࠩ࠰ࠫᓴ") + hook_name
        _11l11l111l_opy_[bstack11l111l111_opy_][bstack1ll111l_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᓵ")] = bstack1lll111l1l_opy_()
        bstack11l11ll111_opy_(_11l11l111l_opy_[bstack11l111l111_opy_][bstack1ll111l_opy_ (u"ࠫࡺࡻࡩࡥࠩᓶ")])
        bstack11l11l1l11_opy_(node, _11l11l111l_opy_[bstack11l111l111_opy_], bstack1ll111l_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧᓷ"), bstack111llllll1_opy_=bstack11l11l1l1l_opy_)
def bstack11l1111ll1_opy_():
    global bstack111lllllll_opy_
    if bstack111l1ll1_opy_():
        bstack111lllllll_opy_ = bstack1ll111l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠪᓸ")
    else:
        bstack111lllllll_opy_ = bstack1ll111l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧᓹ")
@bstack11llllll1_opy_.bstack11l1l1111l_opy_
def bstack11l11l1111_opy_():
    bstack11l1111ll1_opy_()
    if bstack1l1ll11ll1_opy_():
        bstack11ll1l1lll_opy_(bstack111llll111_opy_)
    bstack1l11llllll_opy_ = bstack1l1l111l11_opy_(bstack11l111l11l_opy_)
bstack11l11l1111_opy_()