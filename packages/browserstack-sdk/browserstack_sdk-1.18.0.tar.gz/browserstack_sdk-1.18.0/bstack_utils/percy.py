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
import re
import sys
import json
import time
import shutil
import tempfile
import requests
import subprocess
from threading import Thread
from os.path import expanduser
from bstack_utils.constants import *
from requests.auth import HTTPBasicAuth
from bstack_utils.helper import bstack1ll1ll1111_opy_, bstack1l1l11l11_opy_
class bstack111lll11l_opy_:
  working_dir = os.getcwd()
  bstack11111111_opy_ = False
  config = {}
  binary_path = bstack1ll111l_opy_ (u"ࠩࠪᅃ")
  bstack1l111ll11l_opy_ = bstack1ll111l_opy_ (u"ࠪࠫᅄ")
  bstack1l11l11l11_opy_ = False
  bstack1l111ll111_opy_ = None
  bstack1l1111l1ll_opy_ = {}
  bstack1l1111l111_opy_ = 300
  bstack1l11111l11_opy_ = False
  logger = None
  bstack1l11l1111l_opy_ = False
  bstack1l11l11ll1_opy_ = bstack1ll111l_opy_ (u"ࠫࠬᅅ")
  bstack1l11l1llll_opy_ = {
    bstack1ll111l_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬᅆ") : 1,
    bstack1ll111l_opy_ (u"࠭ࡦࡪࡴࡨࡪࡴࡾࠧᅇ") : 2,
    bstack1ll111l_opy_ (u"ࠧࡦࡦࡪࡩࠬᅈ") : 3,
    bstack1ll111l_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࠨᅉ") : 4
  }
  def __init__(self) -> None: pass
  def bstack1l111llll1_opy_(self):
    bstack1l11l1l1l1_opy_ = bstack1ll111l_opy_ (u"ࠩࠪᅊ")
    bstack1l111l1111_opy_ = sys.platform
    bstack11lllllll1_opy_ = bstack1ll111l_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩᅋ")
    if re.match(bstack1ll111l_opy_ (u"ࠦࡩࡧࡲࡸ࡫ࡱࢀࡲࡧࡣࠡࡱࡶࠦᅌ"), bstack1l111l1111_opy_) != None:
      bstack1l11l1l1l1_opy_ = bstack1l1ll1lll1_opy_ + bstack1ll111l_opy_ (u"ࠧ࠵ࡰࡦࡴࡦࡽ࠲ࡵࡳࡹ࠰ࡽ࡭ࡵࠨᅍ")
      self.bstack1l11l11ll1_opy_ = bstack1ll111l_opy_ (u"࠭࡭ࡢࡥࠪᅎ")
    elif re.match(bstack1ll111l_opy_ (u"ࠢ࡮ࡵࡺ࡭ࡳࢂ࡭ࡴࡻࡶࢀࡲ࡯࡮ࡨࡹࡿࡧࡾ࡭ࡷࡪࡰࡿࡦࡨࡩࡷࡪࡰࡿࡻ࡮ࡴࡣࡦࡾࡨࡱࡨࢂࡷࡪࡰ࠶࠶ࠧᅏ"), bstack1l111l1111_opy_) != None:
      bstack1l11l1l1l1_opy_ = bstack1l1ll1lll1_opy_ + bstack1ll111l_opy_ (u"ࠣ࠱ࡳࡩࡷࡩࡹ࠮ࡹ࡬ࡲ࠳ࢀࡩࡱࠤᅐ")
      bstack11lllllll1_opy_ = bstack1ll111l_opy_ (u"ࠤࡳࡩࡷࡩࡹ࠯ࡧࡻࡩࠧᅑ")
      self.bstack1l11l11ll1_opy_ = bstack1ll111l_opy_ (u"ࠪࡻ࡮ࡴࠧᅒ")
    else:
      bstack1l11l1l1l1_opy_ = bstack1l1ll1lll1_opy_ + bstack1ll111l_opy_ (u"ࠦ࠴ࡶࡥࡳࡥࡼ࠱ࡱ࡯࡮ࡶࡺ࠱ࡾ࡮ࡶࠢᅓ")
      self.bstack1l11l11ll1_opy_ = bstack1ll111l_opy_ (u"ࠬࡲࡩ࡯ࡷࡻࠫᅔ")
    return bstack1l11l1l1l1_opy_, bstack11lllllll1_opy_
  def bstack1l111l1ll1_opy_(self):
    try:
      bstack1l11l1lll1_opy_ = [os.path.join(expanduser(bstack1ll111l_opy_ (u"ࠨࡾࠣᅕ")), bstack1ll111l_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧᅖ")), self.working_dir, tempfile.gettempdir()]
      for path in bstack1l11l1lll1_opy_:
        if(self.bstack1l1111ll1l_opy_(path)):
          return path
      raise bstack1ll111l_opy_ (u"ࠣࡗࡱࡥࡱࡨࡥࠡࡶࡲࠤࡩࡵࡷ࡯࡮ࡲࡥࡩࠦࡰࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽࠧᅗ")
    except Exception as e:
      self.logger.error(bstack1ll111l_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥ࡬ࡩ࡯ࡦࠣࡥࡻࡧࡩ࡭ࡣࡥࡰࡪࠦࡰࡢࡶ࡫ࠤ࡫ࡵࡲࠡࡲࡨࡶࡨࡿࠠࡥࡱࡺࡲࡱࡵࡡࡥ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦ࠭ࠡࡽࢀࠦᅘ").format(e))
  def bstack1l1111ll1l_opy_(self, path):
    try:
      if not os.path.exists(path):
        os.makedirs(path)
      return True
    except:
      return False
  def bstack1l1111llll_opy_(self, bstack1l11l1l1l1_opy_, bstack11lllllll1_opy_):
    try:
      bstack1l111ll1l1_opy_ = self.bstack1l111l1ll1_opy_()
      bstack1l11111lll_opy_ = os.path.join(bstack1l111ll1l1_opy_, bstack1ll111l_opy_ (u"ࠪࡴࡪࡸࡣࡺ࠰ࡽ࡭ࡵ࠭ᅙ"))
      bstack1l111l1l11_opy_ = os.path.join(bstack1l111ll1l1_opy_, bstack11lllllll1_opy_)
      if os.path.exists(bstack1l111l1l11_opy_):
        self.logger.info(bstack1ll111l_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠣࡪࡴࡻ࡮ࡥࠢ࡬ࡲࠥࢁࡽ࠭ࠢࡶ࡯࡮ࡶࡰࡪࡰࡪࠤࡩࡵࡷ࡯࡮ࡲࡥࡩࠨᅚ").format(bstack1l111l1l11_opy_))
        return bstack1l111l1l11_opy_
      if os.path.exists(bstack1l11111lll_opy_):
        self.logger.info(bstack1ll111l_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡿ࡯ࡰࠡࡨࡲࡹࡳࡪࠠࡪࡰࠣࡿࢂ࠲ࠠࡶࡰࡽ࡭ࡵࡶࡩ࡯ࡩࠥᅛ").format(bstack1l11111lll_opy_))
        return self.bstack1l1111111l_opy_(bstack1l11111lll_opy_, bstack11lllllll1_opy_)
      self.logger.info(bstack1ll111l_opy_ (u"ࠨࡄࡰࡹࡱࡰࡴࡧࡤࡪࡰࡪࠤࡵ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠣࡪࡷࡵ࡭ࠡࡽࢀࠦᅜ").format(bstack1l11l1l1l1_opy_))
      response = bstack1l1l11l11_opy_(bstack1ll111l_opy_ (u"ࠧࡈࡇࡗࠫᅝ"), bstack1l11l1l1l1_opy_, {}, {})
      if response.status_code == 200:
        with open(bstack1l11111lll_opy_, bstack1ll111l_opy_ (u"ࠨࡹࡥࠫᅞ")) as file:
          file.write(response.content)
        self.logger.info(bstack1l11l11111_opy_ (u"ࠤࡇࡳࡼࡴ࡬ࡰࡣࡧࡩࡩࠦࡰࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽࠥࡧ࡮ࡥࠢࡶࡥࡻ࡫ࡤࠡࡣࡷࠤࢀࡨࡩ࡯ࡣࡵࡽࡤࢀࡩࡱࡡࡳࡥࡹ࡮ࡽࠣᅟ"))
        return self.bstack1l1111111l_opy_(bstack1l11111lll_opy_, bstack11lllllll1_opy_)
      else:
        raise(bstack1l11l11111_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡤࡰࡹࡱࡰࡴࡧࡤࠡࡶ࡫ࡩࠥ࡬ࡩ࡭ࡧ࠱ࠤࡘࡺࡡࡵࡷࡶࠤࡨࡵࡤࡦ࠼ࠣࡿࡷ࡫ࡳࡱࡱࡱࡷࡪ࠴ࡳࡵࡣࡷࡹࡸࡥࡣࡰࡦࡨࢁࠧᅠ"))
    except:
      self.logger.error(bstack1ll111l_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡥࡱࡺࡲࡱࡵࡡࡥࠢࡳࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠣᅡ"))
  def bstack1l11l1l111_opy_(self, bstack1l11l1l1l1_opy_, bstack11lllllll1_opy_):
    try:
      bstack1l111l1l11_opy_ = self.bstack1l1111llll_opy_(bstack1l11l1l1l1_opy_, bstack11lllllll1_opy_)
      bstack11llllllll_opy_ = self.bstack1l11l111ll_opy_(bstack1l11l1l1l1_opy_, bstack11lllllll1_opy_, bstack1l111l1l11_opy_)
      return bstack1l111l1l11_opy_, bstack11llllllll_opy_
    except Exception as e:
      self.logger.error(bstack1ll111l_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡩࡨࡸࠥࡶࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠤࡵࡧࡴࡩࠤᅢ").format(e))
    return bstack1l111l1l11_opy_, False
  def bstack1l11l111ll_opy_(self, bstack1l11l1l1l1_opy_, bstack11lllllll1_opy_, bstack1l111l1l11_opy_, bstack1l11l111l1_opy_ = 0):
    if bstack1l11l111l1_opy_ > 1:
      return False
    if bstack1l111l1l11_opy_ == None or os.path.exists(bstack1l111l1l11_opy_) == False:
      self.logger.warn(bstack1ll111l_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࡶࡡࡵࡪࠣࡲࡴࡺࠠࡧࡱࡸࡲࡩ࠲ࠠࡳࡧࡷࡶࡾ࡯࡮ࡨࠢࡧࡳࡼࡴ࡬ࡰࡣࡧࠦᅣ"))
      bstack1l111l1l11_opy_ = self.bstack1l1111llll_opy_(bstack1l11l1l1l1_opy_, bstack11lllllll1_opy_)
      self.bstack1l11l111ll_opy_(bstack1l11l1l1l1_opy_, bstack11lllllll1_opy_, bstack1l111l1l11_opy_, bstack1l11l111l1_opy_+1)
    bstack1l111l111l_opy_ = bstack1ll111l_opy_ (u"ࠢ࡟࠰࠭ࡄࡵ࡫ࡲࡤࡻ࡟࠳ࡨࡲࡩࠡ࡞ࡧ࠲ࡡࡪࠫ࠯࡞ࡧ࠯ࠧᅤ")
    command = bstack1ll111l_opy_ (u"ࠨࡽࢀࠤ࠲࠳ࡶࡦࡴࡶ࡭ࡴࡴࠧᅥ").format(bstack1l111l1l11_opy_)
    bstack1l11l1ll11_opy_ = subprocess.check_output(command, shell=True, text=True)
    if re.match(bstack1l111l111l_opy_, bstack1l11l1ll11_opy_) != None:
      return True
    else:
      self.logger.error(bstack1ll111l_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡸࡨࡶࡸ࡯࡯࡯ࠢࡦ࡬ࡪࡩ࡫ࠡࡨࡤ࡭ࡱ࡫ࡤࠣᅦ"))
      bstack1l111l1l11_opy_ = self.bstack1l1111llll_opy_(bstack1l11l1l1l1_opy_, bstack11lllllll1_opy_)
      self.bstack1l11l111ll_opy_(bstack1l11l1l1l1_opy_, bstack11lllllll1_opy_, bstack1l111l1l11_opy_, bstack1l11l111l1_opy_+1)
  def bstack1l1111111l_opy_(self, bstack1l11111lll_opy_, bstack11lllllll1_opy_):
    try:
      working_dir = os.path.dirname(bstack1l11111lll_opy_)
      shutil.unpack_archive(bstack1l11111lll_opy_, working_dir)
      bstack1l111l1l11_opy_ = os.path.join(working_dir, bstack11lllllll1_opy_)
      os.chmod(bstack1l111l1l11_opy_, 0o755)
      return bstack1l111l1l11_opy_
    except Exception as e:
      self.logger.error(bstack1ll111l_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡵ࡯ࡼ࡬ࡴࠥࡶࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠦᅧ"))
  def bstack1l111ll1ll_opy_(self):
    try:
      percy = str(self.config.get(bstack1ll111l_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪᅨ"), bstack1ll111l_opy_ (u"ࠧ࡬ࡡ࡭ࡵࡨࠦᅩ"))).lower()
      if percy != bstack1ll111l_opy_ (u"ࠨࡴࡳࡷࡨࠦᅪ"):
        return False
      self.bstack1l11l11l11_opy_ = True
      return True
    except Exception as e:
      self.logger.error(bstack1ll111l_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡨࡪࡺࡥࡤࡶࠣࡴࡪࡸࡣࡺ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡻࡾࠤᅫ").format(e))
  def init(self, bstack11111111_opy_, config, logger):
    self.bstack11111111_opy_ = bstack11111111_opy_
    self.config = config
    self.logger = logger
    if not self.bstack1l111ll1ll_opy_():
      return
    self.bstack1l1111l1ll_opy_ = config.get(bstack1ll111l_opy_ (u"ࠨࡲࡨࡶࡨࡿࡏࡱࡶ࡬ࡳࡳࡹࠧᅬ"), {})
    try:
      bstack1l11l1l1l1_opy_, bstack11lllllll1_opy_ = self.bstack1l111llll1_opy_()
      bstack1l111l1l11_opy_, bstack11llllllll_opy_ = self.bstack1l11l1l111_opy_(bstack1l11l1l1l1_opy_, bstack11lllllll1_opy_)
      if bstack11llllllll_opy_:
        self.binary_path = bstack1l111l1l11_opy_
        thread = Thread(target=self.bstack1l111l1lll_opy_)
        thread.start()
      else:
        self.bstack1l11l1111l_opy_ = True
        self.logger.error(bstack1ll111l_opy_ (u"ࠤࡌࡲࡻࡧ࡬ࡪࡦࠣࡴࡪࡸࡣࡺࠢࡳࡥࡹ࡮ࠠࡧࡱࡸࡲࡩࠦ࠭ࠡࡽࢀ࠰࡛ࠥ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡷࡥࡷࡺࠠࡑࡧࡵࡧࡾࠨᅭ").format(bstack1l111l1l11_opy_))
    except Exception as e:
      self.logger.error(bstack1ll111l_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡵࡣࡵࡸࠥࡶࡥࡳࡥࡼ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦᅮ").format(e))
  def bstack1l11l1l11l_opy_(self):
    try:
      logfile = os.path.join(self.working_dir, bstack1ll111l_opy_ (u"ࠫࡱࡵࡧࠨᅯ"), bstack1ll111l_opy_ (u"ࠬࡶࡥࡳࡥࡼ࠲ࡱࡵࡧࠨᅰ"))
      os.makedirs(os.path.dirname(logfile)) if not os.path.exists(os.path.dirname(logfile)) else None
      self.logger.debug(bstack1ll111l_opy_ (u"ࠨࡐࡶࡵ࡫࡭ࡳ࡭ࠠࡱࡧࡵࡧࡾࠦ࡬ࡰࡩࡶࠤࡦࡺࠠࡼࡿࠥᅱ").format(logfile))
      self.bstack1l111ll11l_opy_ = logfile
    except Exception as e:
      self.logger.error(bstack1ll111l_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡪࡺࠠࡱࡧࡵࡧࡾࠦ࡬ࡰࡩࠣࡴࡦࡺࡨ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࢁࡽࠣᅲ").format(e))
  def bstack1l111l1lll_opy_(self):
    bstack1l11111ll1_opy_ = self.bstack1l111l1l1l_opy_()
    if bstack1l11111ll1_opy_ == None:
      self.bstack1l11l1111l_opy_ = True
      self.logger.error(bstack1ll111l_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡵࡱ࡮ࡩࡳࠦ࡮ࡰࡶࠣࡪࡴࡻ࡮ࡥ࠮ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡵࡣࡵࡸࠥࡶࡥࡳࡥࡼࠦᅳ"))
      return False
    command_args = [bstack1ll111l_opy_ (u"ࠤࡤࡴࡵࡀࡥࡹࡧࡦ࠾ࡸࡺࡡࡳࡶࠥᅴ") if self.bstack11111111_opy_ else bstack1ll111l_opy_ (u"ࠪࡩࡽ࡫ࡣ࠻ࡵࡷࡥࡷࡺࠧᅵ")]
    bstack1l111111l1_opy_ = self.bstack1l1111l1l1_opy_()
    if bstack1l111111l1_opy_ != None:
      command_args.append(bstack1ll111l_opy_ (u"ࠦ࠲ࡩࠠࡼࡿࠥᅶ").format(bstack1l111111l1_opy_))
    env = os.environ.copy()
    env[bstack1ll111l_opy_ (u"ࠧࡖࡅࡓࡅ࡜ࡣ࡙ࡕࡋࡆࡐࠥᅷ")] = bstack1l11111ll1_opy_
    bstack1l11l11lll_opy_ = [self.binary_path]
    self.bstack1l11l1l11l_opy_()
    self.bstack1l111ll111_opy_ = self.bstack11llllll1l_opy_(bstack1l11l11lll_opy_ + command_args, env)
    self.logger.debug(bstack1ll111l_opy_ (u"ࠨࡓࡵࡣࡵࡸ࡮ࡴࡧࠡࡊࡨࡥࡱࡺࡨࠡࡅ࡫ࡩࡨࡱࠢᅸ"))
    bstack1l11l111l1_opy_ = 0
    while self.bstack1l111ll111_opy_.poll() == None:
      bstack1l11l1l1ll_opy_ = self.bstack1l11111111_opy_()
      if bstack1l11l1l1ll_opy_:
        self.logger.debug(bstack1ll111l_opy_ (u"ࠢࡉࡧࡤࡰࡹ࡮ࠠࡄࡪࡨࡧࡰࠦࡳࡶࡥࡦࡩࡸࡹࡦࡶ࡮ࠥᅹ"))
        self.bstack1l11111l11_opy_ = True
        return True
      bstack1l11l111l1_opy_ += 1
      self.logger.debug(bstack1ll111l_opy_ (u"ࠣࡊࡨࡥࡱࡺࡨࠡࡅ࡫ࡩࡨࡱࠠࡓࡧࡷࡶࡾࠦ࠭ࠡࡽࢀࠦᅺ").format(bstack1l11l111l1_opy_))
      time.sleep(2)
    self.logger.error(bstack1ll111l_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡴࡢࡴࡷࠤࡵ࡫ࡲࡤࡻ࠯ࠤࡍ࡫ࡡ࡭ࡶ࡫ࠤࡈ࡮ࡥࡤ࡭ࠣࡊࡦ࡯࡬ࡦࡦࠣࡥ࡫ࡺࡥࡳࠢࡾࢁࠥࡧࡴࡵࡧࡰࡴࡹࡹࠢᅻ").format(bstack1l11l111l1_opy_))
    self.bstack1l11l1111l_opy_ = True
    return False
  def bstack1l11111111_opy_(self, bstack1l11l111l1_opy_ = 0):
    try:
      if bstack1l11l111l1_opy_ > 10:
        return False
      bstack1l111l11l1_opy_ = os.environ.get(bstack1ll111l_opy_ (u"ࠪࡔࡊࡘࡃ࡚ࡡࡖࡉࡗ࡜ࡅࡓࡡࡄࡈࡉࡘࡅࡔࡕࠪᅼ"), bstack1ll111l_opy_ (u"ࠫ࡭ࡺࡴࡱ࠼࠲࠳ࡱࡵࡣࡢ࡮࡫ࡳࡸࡺ࠺࠶࠵࠶࠼ࠬᅽ"))
      bstack1l11l11l1l_opy_ = bstack1l111l11l1_opy_ + bstack1l1ll1ll11_opy_
      response = requests.get(bstack1l11l11l1l_opy_)
      return True if response.json() else False
    except:
      return False
  def bstack1l111l1l1l_opy_(self):
    bstack1l11ll1111_opy_ = bstack1ll111l_opy_ (u"ࠬࡧࡰࡱࠩᅾ") if self.bstack11111111_opy_ else bstack1ll111l_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡥࠨᅿ")
    bstack1l1l11ll11_opy_ = bstack1ll111l_opy_ (u"ࠢࡢࡲ࡬࠳ࡦࡶࡰࡠࡲࡨࡶࡨࡿ࠯ࡨࡧࡷࡣࡵࡸ࡯࡫ࡧࡦࡸࡤࡺ࡯࡬ࡧࡱࡃࡳࡧ࡭ࡦ࠿ࡾࢁࠫࡺࡹࡱࡧࡀࡿࢂࠨᆀ").format(self.config[bstack1ll111l_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭ᆁ")], bstack1l11ll1111_opy_)
    uri = bstack1ll1ll1111_opy_(bstack1l1l11ll11_opy_)
    try:
      response = bstack1l1l11l11_opy_(bstack1ll111l_opy_ (u"ࠩࡊࡉ࡙࠭ᆂ"), uri, {}, {bstack1ll111l_opy_ (u"ࠪࡥࡺࡺࡨࠨᆃ"): (self.config[bstack1ll111l_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ᆄ")], self.config[bstack1ll111l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨᆅ")])})
      if response.status_code == 200:
        bstack1l111lll1l_opy_ = response.json()
        if bstack1ll111l_opy_ (u"ࠨࡴࡰ࡭ࡨࡲࠧᆆ") in bstack1l111lll1l_opy_:
          return bstack1l111lll1l_opy_[bstack1ll111l_opy_ (u"ࠢࡵࡱ࡮ࡩࡳࠨᆇ")]
        else:
          raise bstack1ll111l_opy_ (u"ࠨࡖࡲ࡯ࡪࡴࠠࡏࡱࡷࠤࡋࡵࡵ࡯ࡦࠣ࠱ࠥࢁࡽࠨᆈ").format(bstack1l111lll1l_opy_)
      else:
        raise bstack1ll111l_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥ࡬ࡥࡵࡥ࡫ࠤࡵ࡫ࡲࡤࡻࠣࡸࡴࡱࡥ࡯࠮ࠣࡖࡪࡹࡰࡰࡰࡶࡩࠥࡹࡴࡢࡶࡸࡷࠥ࠳ࠠࡼࡿ࠯ࠤࡗ࡫ࡳࡱࡱࡱࡷࡪࠦࡂࡰࡦࡼࠤ࠲ࠦࡻࡾࠤᆉ").format(response.status_code, response.json())
    except Exception as e:
      self.logger.error(bstack1ll111l_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡦࡶࡪࡧࡴࡪࡰࡪࠤࡵ࡫ࡲࡤࡻࠣࡴࡷࡵࡪࡦࡥࡷࠦᆊ").format(e))
  def bstack1l1111l1l1_opy_(self):
    bstack1l111l11ll_opy_ = os.path.join(tempfile.gettempdir(), bstack1ll111l_opy_ (u"ࠦࡵ࡫ࡲࡤࡻࡆࡳࡳ࡬ࡩࡨ࠰࡭ࡷࡴࡴࠢᆋ"))
    try:
      if bstack1ll111l_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳ࠭ᆌ") not in self.bstack1l1111l1ll_opy_:
        self.bstack1l1111l1ll_opy_[bstack1ll111l_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࠧᆍ")] = 2
      with open(bstack1l111l11ll_opy_, bstack1ll111l_opy_ (u"ࠧࡸࠩᆎ")) as fp:
        json.dump(self.bstack1l1111l1ll_opy_, fp)
      return bstack1l111l11ll_opy_
    except Exception as e:
      self.logger.error(bstack1ll111l_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡨࡸࡥࡢࡶࡨࠤࡵ࡫ࡲࡤࡻࠣࡧࡴࡴࡦ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࢁࡽࠣᆏ").format(e))
  def bstack11llllll1l_opy_(self, cmd, env = os.environ.copy()):
    try:
      if self.bstack1l11l11ll1_opy_ == bstack1ll111l_opy_ (u"ࠩࡺ࡭ࡳ࠭ᆐ"):
        bstack1l1111ll11_opy_ = [bstack1ll111l_opy_ (u"ࠪࡧࡲࡪ࠮ࡦࡺࡨࠫᆑ"), bstack1ll111l_opy_ (u"ࠫ࠴ࡩࠧᆒ")]
        cmd = bstack1l1111ll11_opy_ + cmd
      cmd = bstack1ll111l_opy_ (u"ࠬࠦࠧᆓ").join(cmd)
      self.logger.debug(bstack1ll111l_opy_ (u"ࠨࡒࡶࡰࡱ࡭ࡳ࡭ࠠࡼࡿࠥᆔ").format(cmd))
      with open(self.bstack1l111ll11l_opy_, bstack1ll111l_opy_ (u"ࠢࡢࠤᆕ")) as bstack1l1111l11l_opy_:
        process = subprocess.Popen(cmd, shell=True, stdout=bstack1l1111l11l_opy_, text=True, stderr=bstack1l1111l11l_opy_, env=env, universal_newlines=True)
      return process
    except Exception as e:
      self.bstack1l11l1111l_opy_ = True
      self.logger.error(bstack1ll111l_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸࡺࡡࡳࡶࠣࡴࡪࡸࡣࡺࠢࡺ࡭ࡹ࡮ࠠࡤ࡯ࡧࠤ࠲ࠦࡻࡾ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࡀࠠࡼࡿࠥᆖ").format(cmd, e))
  def shutdown(self):
    try:
      if self.bstack1l11111l11_opy_:
        self.logger.info(bstack1ll111l_opy_ (u"ࠤࡖࡸࡴࡶࡰࡪࡰࡪࠤࡕ࡫ࡲࡤࡻࠥᆗ"))
        cmd = [self.binary_path, bstack1ll111l_opy_ (u"ࠥࡩࡽ࡫ࡣ࠻ࡵࡷࡳࡵࠨᆘ")]
        self.bstack11llllll1l_opy_(cmd)
        self.bstack1l11111l11_opy_ = False
    except Exception as e:
      self.logger.error(bstack1ll111l_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡶࡲࡴࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡷࡪࡶ࡫ࠤࡨࡵ࡭࡮ࡣࡱࡨࠥ࠳ࠠࡼࡿ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴ࠺ࠡࡽࢀࠦᆙ").format(cmd, e))
  def bstack1lllll11l1_opy_(self):
    if not self.bstack1l11l11l11_opy_:
      return
    try:
      bstack1l111lllll_opy_ = 0
      while not self.bstack1l11111l11_opy_ and bstack1l111lllll_opy_ < self.bstack1l1111l111_opy_:
        if self.bstack1l11l1111l_opy_:
          self.logger.info(bstack1ll111l_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡸ࡫ࡴࡶࡲࠣࡪࡦ࡯࡬ࡦࡦࠥᆚ"))
          return
        time.sleep(1)
        bstack1l111lllll_opy_ += 1
      os.environ[bstack1ll111l_opy_ (u"࠭ࡐࡆࡔࡆ࡝ࡤࡈࡅࡔࡖࡢࡔࡑࡇࡔࡇࡑࡕࡑࠬᆛ")] = str(self.bstack1l1111lll1_opy_())
      self.logger.info(bstack1ll111l_opy_ (u"ࠢࡑࡧࡵࡧࡾࠦࡳࡦࡶࡸࡴࠥࡩ࡯࡮ࡲ࡯ࡩࡹ࡫ࡤࠣᆜ"))
    except Exception as e:
      self.logger.error(bstack1ll111l_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸ࡫ࡴࡶࡲࠣࡴࡪࡸࡣࡺ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡻࡾࠤᆝ").format(e))
  def bstack1l1111lll1_opy_(self):
    if self.bstack11111111_opy_:
      return
    try:
      bstack1l111111ll_opy_ = [platform[bstack1ll111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧᆞ")].lower() for platform in self.config.get(bstack1ll111l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ᆟ"), [])]
      bstack1l111lll11_opy_ = sys.maxsize
      bstack1l11l1ll1l_opy_ = bstack1ll111l_opy_ (u"ࠫࠬᆠ")
      for browser in bstack1l111111ll_opy_:
        if browser in self.bstack1l11l1llll_opy_:
          bstack1l11111l1l_opy_ = self.bstack1l11l1llll_opy_[browser]
        if bstack1l11111l1l_opy_ < bstack1l111lll11_opy_:
          bstack1l111lll11_opy_ = bstack1l11111l1l_opy_
          bstack1l11l1ll1l_opy_ = browser
      return bstack1l11l1ll1l_opy_
    except Exception as e:
      self.logger.error(bstack1ll111l_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡨ࡬ࡲࡩࠦࡢࡦࡵࡷࠤࡵࡲࡡࡵࡨࡲࡶࡲ࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡿࢂࠨᆡ").format(e))