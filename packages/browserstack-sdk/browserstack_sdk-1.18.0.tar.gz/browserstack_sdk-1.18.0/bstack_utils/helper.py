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
import os
import re
import subprocess
import traceback
from urllib.parse import urlparse
import git
import requests
from packaging import version
from bstack_utils.config import Config
from bstack_utils.constants import bstack1l1lll1111_opy_, bstack1lll111l11_opy_, bstack11111l1l1_opy_, bstack1l111111l_opy_
from bstack_utils.messages import bstack1ll1ll1l_opy_
from bstack_utils.proxy import bstack11ll11l1_opy_
bstack1ll1ll111_opy_ = Config.get_instance()
def bstack1ll1111l11_opy_(config):
    return config[bstack1ll111l_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ཭")]
def bstack1ll11111l1_opy_(config):
    return config[bstack1ll111l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬ཮")]
def bstack1l1l1llll1_opy_(obj):
    values = []
    bstack1l1ll111l1_opy_ = re.compile(bstack1ll111l_opy_ (u"ࡵࠦࡣࡉࡕࡔࡖࡒࡑࡤ࡚ࡁࡈࡡ࡟ࡨ࠰ࠪࠢ཯"), re.I)
    for key in obj.keys():
        if bstack1l1ll111l1_opy_.match(key):
            values.append(obj[key])
    return values
def bstack1l1l1lllll_opy_(config):
    tags = []
    tags.extend(bstack1l1l1llll1_opy_(os.environ))
    tags.extend(bstack1l1l1llll1_opy_(config))
    return tags
def bstack1l1l111ll1_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack1l1ll1l11l_opy_(bstack1l1l11ll1l_opy_):
    if not bstack1l1l11ll1l_opy_:
        return bstack1ll111l_opy_ (u"ࠫࠬ཰")
    return bstack1ll111l_opy_ (u"ࠧࢁࡽࠡࠪࡾࢁ࠮ࠨཱ").format(bstack1l1l11ll1l_opy_.name, bstack1l1l11ll1l_opy_.email)
def bstack1ll11111ll_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack1l1l1l1l11_opy_ = repo.common_dir
        info = {
            bstack1ll111l_opy_ (u"ࠨࡳࡩࡣིࠥ"): repo.head.commit.hexsha,
            bstack1ll111l_opy_ (u"ࠢࡴࡪࡲࡶࡹࡥࡳࡩࡣཱིࠥ"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack1ll111l_opy_ (u"ࠣࡤࡵࡥࡳࡩࡨུࠣ"): repo.active_branch.name,
            bstack1ll111l_opy_ (u"ࠤࡷࡥ࡬ࠨཱུ"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack1ll111l_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡷࡩࡷࠨྲྀ"): bstack1l1ll1l11l_opy_(repo.head.commit.committer),
            bstack1ll111l_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡸࡪࡸ࡟ࡥࡣࡷࡩࠧཷ"): repo.head.commit.committed_datetime.isoformat(),
            bstack1ll111l_opy_ (u"ࠧࡧࡵࡵࡪࡲࡶࠧླྀ"): bstack1l1ll1l11l_opy_(repo.head.commit.author),
            bstack1ll111l_opy_ (u"ࠨࡡࡶࡶ࡫ࡳࡷࡥࡤࡢࡶࡨࠦཹ"): repo.head.commit.authored_datetime.isoformat(),
            bstack1ll111l_opy_ (u"ࠢࡤࡱࡰࡱ࡮ࡺ࡟࡮ࡧࡶࡷࡦ࡭ࡥེࠣ"): repo.head.commit.message,
            bstack1ll111l_opy_ (u"ࠣࡴࡲࡳࡹࠨཻ"): repo.git.rev_parse(bstack1ll111l_opy_ (u"ࠤ࠰࠱ࡸ࡮࡯ࡸ࠯ࡷࡳࡵࡲࡥࡷࡧ࡯ོࠦ")),
            bstack1ll111l_opy_ (u"ࠥࡧࡴࡳ࡭ࡰࡰࡢ࡫࡮ࡺ࡟ࡥ࡫ࡵཽࠦ"): bstack1l1l1l1l11_opy_,
            bstack1ll111l_opy_ (u"ࠦࡼࡵࡲ࡬ࡶࡵࡩࡪࡥࡧࡪࡶࡢࡨ࡮ࡸࠢཾ"): subprocess.check_output([bstack1ll111l_opy_ (u"ࠧ࡭ࡩࡵࠤཿ"), bstack1ll111l_opy_ (u"ࠨࡲࡦࡸ࠰ࡴࡦࡸࡳࡦࠤྀ"), bstack1ll111l_opy_ (u"ࠢ࠮࠯ࡪ࡭ࡹ࠳ࡣࡰ࡯ࡰࡳࡳ࠳ࡤࡪࡴཱྀࠥ")]).strip().decode(
                bstack1ll111l_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧྂ")),
            bstack1ll111l_opy_ (u"ࠤ࡯ࡥࡸࡺ࡟ࡵࡣࡪࠦྃ"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack1ll111l_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡶࡣࡸ࡯࡮ࡤࡧࡢࡰࡦࡹࡴࡠࡶࡤ࡫྄ࠧ"): repo.git.rev_list(
                bstack1ll111l_opy_ (u"ࠦࢀࢃ࠮࠯ࡽࢀࠦ྅").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack1l1l1ll11l_opy_ = []
        for remote in remotes:
            bstack1l1l1l11ll_opy_ = {
                bstack1ll111l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ྆"): remote.name,
                bstack1ll111l_opy_ (u"ࠨࡵࡳ࡮ࠥ྇"): remote.url,
            }
            bstack1l1l1ll11l_opy_.append(bstack1l1l1l11ll_opy_)
        return {
            bstack1ll111l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧྈ"): bstack1ll111l_opy_ (u"ࠣࡩ࡬ࡸࠧྉ"),
            **info,
            bstack1ll111l_opy_ (u"ࠤࡵࡩࡲࡵࡴࡦࡵࠥྊ"): bstack1l1l1ll11l_opy_
        }
    except Exception as err:
        print(bstack1ll111l_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡳࡵࡻ࡬ࡢࡶ࡬ࡲ࡬ࠦࡇࡪࡶࠣࡱࡪࡺࡡࡥࡣࡷࡥࠥࡽࡩࡵࡪࠣࡩࡷࡸ࡯ࡳ࠼ࠣࡿࢂࠨྋ").format(err))
        return {}
def bstack1llll1ll1_opy_():
    env = os.environ
    if (bstack1ll111l_opy_ (u"ࠦࡏࡋࡎࡌࡋࡑࡗࡤ࡛ࡒࡍࠤྌ") in env and len(env[bstack1ll111l_opy_ (u"ࠧࡐࡅࡏࡍࡌࡒࡘࡥࡕࡓࡎࠥྍ")]) > 0) or (
            bstack1ll111l_opy_ (u"ࠨࡊࡆࡐࡎࡍࡓ࡙࡟ࡉࡑࡐࡉࠧྎ") in env and len(env[bstack1ll111l_opy_ (u"ࠢࡋࡇࡑࡏࡎࡔࡓࡠࡊࡒࡑࡊࠨྏ")]) > 0):
        return {
            bstack1ll111l_opy_ (u"ࠣࡰࡤࡱࡪࠨྐ"): bstack1ll111l_opy_ (u"ࠤࡍࡩࡳࡱࡩ࡯ࡵࠥྑ"),
            bstack1ll111l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨྒ"): env.get(bstack1ll111l_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢྒྷ")),
            bstack1ll111l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢྔ"): env.get(bstack1ll111l_opy_ (u"ࠨࡊࡐࡄࡢࡒࡆࡓࡅࠣྕ")),
            bstack1ll111l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨྖ"): env.get(bstack1ll111l_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢྗ"))
        }
    if env.get(bstack1ll111l_opy_ (u"ࠤࡆࡍࠧ྘")) == bstack1ll111l_opy_ (u"ࠥࡸࡷࡻࡥࠣྙ") and bstack1l1ll11l1l_opy_(env.get(bstack1ll111l_opy_ (u"ࠦࡈࡏࡒࡄࡎࡈࡇࡎࠨྚ"))):
        return {
            bstack1ll111l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥྛ"): bstack1ll111l_opy_ (u"ࠨࡃࡪࡴࡦࡰࡪࡉࡉࠣྜ"),
            bstack1ll111l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥྜྷ"): env.get(bstack1ll111l_opy_ (u"ࠣࡅࡌࡖࡈࡒࡅࡠࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦྞ")),
            bstack1ll111l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦྟ"): env.get(bstack1ll111l_opy_ (u"ࠥࡇࡎࡘࡃࡍࡇࡢࡎࡔࡈࠢྠ")),
            bstack1ll111l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥྡ"): env.get(bstack1ll111l_opy_ (u"ࠧࡉࡉࡓࡅࡏࡉࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࠣྡྷ"))
        }
    if env.get(bstack1ll111l_opy_ (u"ࠨࡃࡊࠤྣ")) == bstack1ll111l_opy_ (u"ࠢࡵࡴࡸࡩࠧྤ") and bstack1l1ll11l1l_opy_(env.get(bstack1ll111l_opy_ (u"ࠣࡖࡕࡅ࡛ࡏࡓࠣྥ"))):
        return {
            bstack1ll111l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢྦ"): bstack1ll111l_opy_ (u"ࠥࡘࡷࡧࡶࡪࡵࠣࡇࡎࠨྦྷ"),
            bstack1ll111l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢྨ"): env.get(bstack1ll111l_opy_ (u"࡚ࠧࡒࡂࡘࡌࡗࡤࡈࡕࡊࡎࡇࡣ࡜ࡋࡂࡠࡗࡕࡐࠧྩ")),
            bstack1ll111l_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣྪ"): env.get(bstack1ll111l_opy_ (u"ࠢࡕࡔࡄ࡚ࡎ࡙࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤྫ")),
            bstack1ll111l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢྫྷ"): env.get(bstack1ll111l_opy_ (u"ࠤࡗࡖࡆ࡜ࡉࡔࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣྭ"))
        }
    if env.get(bstack1ll111l_opy_ (u"ࠥࡇࡎࠨྮ")) == bstack1ll111l_opy_ (u"ࠦࡹࡸࡵࡦࠤྯ") and env.get(bstack1ll111l_opy_ (u"ࠧࡉࡉࡠࡐࡄࡑࡊࠨྰ")) == bstack1ll111l_opy_ (u"ࠨࡣࡰࡦࡨࡷ࡭࡯ࡰࠣྱ"):
        return {
            bstack1ll111l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧྲ"): bstack1ll111l_opy_ (u"ࠣࡅࡲࡨࡪࡹࡨࡪࡲࠥླ"),
            bstack1ll111l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧྴ"): None,
            bstack1ll111l_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧྵ"): None,
            bstack1ll111l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥྶ"): None
        }
    if env.get(bstack1ll111l_opy_ (u"ࠧࡈࡉࡕࡄࡘࡇࡐࡋࡔࡠࡄࡕࡅࡓࡉࡈࠣྷ")) and env.get(bstack1ll111l_opy_ (u"ࠨࡂࡊࡖࡅ࡙ࡈࡑࡅࡕࡡࡆࡓࡒࡓࡉࡕࠤྸ")):
        return {
            bstack1ll111l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧྐྵ"): bstack1ll111l_opy_ (u"ࠣࡄ࡬ࡸࡧࡻࡣ࡬ࡧࡷࠦྺ"),
            bstack1ll111l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧྻ"): env.get(bstack1ll111l_opy_ (u"ࠥࡆࡎ࡚ࡂࡖࡅࡎࡉ࡙ࡥࡇࡊࡖࡢࡌ࡙࡚ࡐࡠࡑࡕࡍࡌࡏࡎࠣྼ")),
            bstack1ll111l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ྽"): None,
            bstack1ll111l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ྾"): env.get(bstack1ll111l_opy_ (u"ࠨࡂࡊࡖࡅ࡙ࡈࡑࡅࡕࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣ྿"))
        }
    if env.get(bstack1ll111l_opy_ (u"ࠢࡄࡋࠥ࿀")) == bstack1ll111l_opy_ (u"ࠣࡶࡵࡹࡪࠨ࿁") and bstack1l1ll11l1l_opy_(env.get(bstack1ll111l_opy_ (u"ࠤࡇࡖࡔࡔࡅࠣ࿂"))):
        return {
            bstack1ll111l_opy_ (u"ࠥࡲࡦࡳࡥࠣ࿃"): bstack1ll111l_opy_ (u"ࠦࡉࡸ࡯࡯ࡧࠥ࿄"),
            bstack1ll111l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ࿅"): env.get(bstack1ll111l_opy_ (u"ࠨࡄࡓࡑࡑࡉࡤࡈࡕࡊࡎࡇࡣࡑࡏࡎࡌࠤ࿆")),
            bstack1ll111l_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ࿇"): None,
            bstack1ll111l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ࿈"): env.get(bstack1ll111l_opy_ (u"ࠤࡇࡖࡔࡔࡅࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢ࿉"))
        }
    if env.get(bstack1ll111l_opy_ (u"ࠥࡇࡎࠨ࿊")) == bstack1ll111l_opy_ (u"ࠦࡹࡸࡵࡦࠤ࿋") and bstack1l1ll11l1l_opy_(env.get(bstack1ll111l_opy_ (u"࡙ࠧࡅࡎࡃࡓࡌࡔࡘࡅࠣ࿌"))):
        return {
            bstack1ll111l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ࿍"): bstack1ll111l_opy_ (u"ࠢࡔࡧࡰࡥࡵ࡮࡯ࡳࡧࠥ࿎"),
            bstack1ll111l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ࿏"): env.get(bstack1ll111l_opy_ (u"ࠤࡖࡉࡒࡇࡐࡉࡑࡕࡉࡤࡕࡒࡈࡃࡑࡍ࡟ࡇࡔࡊࡑࡑࡣ࡚ࡘࡌࠣ࿐")),
            bstack1ll111l_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ࿑"): env.get(bstack1ll111l_opy_ (u"ࠦࡘࡋࡍࡂࡒࡋࡓࡗࡋ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤ࿒")),
            bstack1ll111l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ࿓"): env.get(bstack1ll111l_opy_ (u"ࠨࡓࡆࡏࡄࡔࡍࡕࡒࡆࡡࡍࡓࡇࡥࡉࡅࠤ࿔"))
        }
    if env.get(bstack1ll111l_opy_ (u"ࠢࡄࡋࠥ࿕")) == bstack1ll111l_opy_ (u"ࠣࡶࡵࡹࡪࠨ࿖") and bstack1l1ll11l1l_opy_(env.get(bstack1ll111l_opy_ (u"ࠤࡊࡍ࡙ࡒࡁࡃࡡࡆࡍࠧ࿗"))):
        return {
            bstack1ll111l_opy_ (u"ࠥࡲࡦࡳࡥࠣ࿘"): bstack1ll111l_opy_ (u"ࠦࡌ࡯ࡴࡍࡣࡥࠦ࿙"),
            bstack1ll111l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ࿚"): env.get(bstack1ll111l_opy_ (u"ࠨࡃࡊࡡࡍࡓࡇࡥࡕࡓࡎࠥ࿛")),
            bstack1ll111l_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ࿜"): env.get(bstack1ll111l_opy_ (u"ࠣࡅࡌࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨ࿝")),
            bstack1ll111l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ࿞"): env.get(bstack1ll111l_opy_ (u"ࠥࡇࡎࡥࡊࡐࡄࡢࡍࡉࠨ࿟"))
        }
    if env.get(bstack1ll111l_opy_ (u"ࠦࡈࡏࠢ࿠")) == bstack1ll111l_opy_ (u"ࠧࡺࡲࡶࡧࠥ࿡") and bstack1l1ll11l1l_opy_(env.get(bstack1ll111l_opy_ (u"ࠨࡂࡖࡋࡏࡈࡐࡏࡔࡆࠤ࿢"))):
        return {
            bstack1ll111l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ࿣"): bstack1ll111l_opy_ (u"ࠣࡄࡸ࡭ࡱࡪ࡫ࡪࡶࡨࠦ࿤"),
            bstack1ll111l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ࿥"): env.get(bstack1ll111l_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡍࡌࡘࡊࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤ࿦")),
            bstack1ll111l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ࿧"): env.get(bstack1ll111l_opy_ (u"ࠧࡈࡕࡊࡎࡇࡏࡎ࡚ࡅࡠࡎࡄࡆࡊࡒࠢ࿨")) or env.get(bstack1ll111l_opy_ (u"ࠨࡂࡖࡋࡏࡈࡐࡏࡔࡆࡡࡓࡍࡕࡋࡌࡊࡐࡈࡣࡓࡇࡍࡆࠤ࿩")),
            bstack1ll111l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ࿪"): env.get(bstack1ll111l_opy_ (u"ࠣࡄࡘࡍࡑࡊࡋࡊࡖࡈࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥ࿫"))
        }
    if bstack1l1ll11l1l_opy_(env.get(bstack1ll111l_opy_ (u"ࠤࡗࡊࡤࡈࡕࡊࡎࡇࠦ࿬"))):
        return {
            bstack1ll111l_opy_ (u"ࠥࡲࡦࡳࡥࠣ࿭"): bstack1ll111l_opy_ (u"࡛ࠦ࡯ࡳࡶࡣ࡯ࠤࡘࡺࡵࡥ࡫ࡲࠤ࡙࡫ࡡ࡮ࠢࡖࡩࡷࡼࡩࡤࡧࡶࠦ࿮"),
            bstack1ll111l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ࿯"): bstack1ll111l_opy_ (u"ࠨࡻࡾࡽࢀࠦ࿰").format(env.get(bstack1ll111l_opy_ (u"ࠧࡔ࡛ࡖࡘࡊࡓ࡟ࡕࡇࡄࡑࡋࡕࡕࡏࡆࡄࡘࡎࡕࡎࡔࡇࡕ࡚ࡊࡘࡕࡓࡋࠪ࿱")), env.get(bstack1ll111l_opy_ (u"ࠨࡕ࡜ࡗ࡙ࡋࡍࡠࡖࡈࡅࡒࡖࡒࡐࡌࡈࡇ࡙ࡏࡄࠨ࿲"))),
            bstack1ll111l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ࿳"): env.get(bstack1ll111l_opy_ (u"ࠥࡗ࡞࡙ࡔࡆࡏࡢࡈࡊࡌࡉࡏࡋࡗࡍࡔࡔࡉࡅࠤ࿴")),
            bstack1ll111l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ࿵"): env.get(bstack1ll111l_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡌࡈࠧ࿶"))
        }
    if bstack1l1ll11l1l_opy_(env.get(bstack1ll111l_opy_ (u"ࠨࡁࡑࡒ࡙ࡉ࡞ࡕࡒࠣ࿷"))):
        return {
            bstack1ll111l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ࿸"): bstack1ll111l_opy_ (u"ࠣࡃࡳࡴࡻ࡫ࡹࡰࡴࠥ࿹"),
            bstack1ll111l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ࿺"): bstack1ll111l_opy_ (u"ࠥࡿࢂ࠵ࡰࡳࡱ࡭ࡩࡨࡺ࠯ࡼࡿ࠲ࡿࢂ࠵ࡢࡶ࡫࡯ࡨࡸ࠵ࡻࡾࠤ࿻").format(env.get(bstack1ll111l_opy_ (u"ࠫࡆࡖࡐࡗࡇ࡜ࡓࡗࡥࡕࡓࡎࠪ࿼")), env.get(bstack1ll111l_opy_ (u"ࠬࡇࡐࡑࡘࡈ࡝ࡔࡘ࡟ࡂࡅࡆࡓ࡚ࡔࡔࡠࡐࡄࡑࡊ࠭࿽")), env.get(bstack1ll111l_opy_ (u"࠭ࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡒࡕࡓࡏࡋࡃࡕࡡࡖࡐ࡚ࡍࠧ࿾")), env.get(bstack1ll111l_opy_ (u"ࠧࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠫ࿿"))),
            bstack1ll111l_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥက"): env.get(bstack1ll111l_opy_ (u"ࠤࡄࡔࡕ࡜ࡅ࡚ࡑࡕࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨခ")),
            bstack1ll111l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤဂ"): env.get(bstack1ll111l_opy_ (u"ࠦࡆࡖࡐࡗࡇ࡜ࡓࡗࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧဃ"))
        }
    if env.get(bstack1ll111l_opy_ (u"ࠧࡇ࡚ࡖࡔࡈࡣࡍ࡚ࡔࡑࡡࡘࡗࡊࡘ࡟ࡂࡉࡈࡒ࡙ࠨင")) and env.get(bstack1ll111l_opy_ (u"ࠨࡔࡇࡡࡅ࡙ࡎࡒࡄࠣစ")):
        return {
            bstack1ll111l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧဆ"): bstack1ll111l_opy_ (u"ࠣࡃࡽࡹࡷ࡫ࠠࡄࡋࠥဇ"),
            bstack1ll111l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧဈ"): bstack1ll111l_opy_ (u"ࠥࡿࢂࢁࡽ࠰ࡡࡥࡹ࡮ࡲࡤ࠰ࡴࡨࡷࡺࡲࡴࡴࡁࡥࡹ࡮ࡲࡤࡊࡦࡀࡿࢂࠨဉ").format(env.get(bstack1ll111l_opy_ (u"ࠫࡘ࡟ࡓࡕࡇࡐࡣ࡙ࡋࡁࡎࡈࡒ࡙ࡓࡊࡁࡕࡋࡒࡒࡘࡋࡒࡗࡇࡕ࡙ࡗࡏࠧည")), env.get(bstack1ll111l_opy_ (u"࡙࡙ࠬࡔࡖࡈࡑࡤ࡚ࡅࡂࡏࡓࡖࡔࡐࡅࡄࡖࠪဋ")), env.get(bstack1ll111l_opy_ (u"࠭ࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡍࡉ࠭ဌ"))),
            bstack1ll111l_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤဍ"): env.get(bstack1ll111l_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡏࡄࠣဎ")),
            bstack1ll111l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣဏ"): env.get(bstack1ll111l_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡊࡆࠥတ"))
        }
    if any([env.get(bstack1ll111l_opy_ (u"ࠦࡈࡕࡄࡆࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠤထ")), env.get(bstack1ll111l_opy_ (u"ࠧࡉࡏࡅࡇࡅ࡙ࡎࡒࡄࡠࡔࡈࡗࡔࡒࡖࡆࡆࡢࡗࡔ࡛ࡒࡄࡇࡢ࡚ࡊࡘࡓࡊࡑࡑࠦဒ")), env.get(bstack1ll111l_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡖࡓ࡚ࡘࡃࡆࡡ࡙ࡉࡗ࡙ࡉࡐࡐࠥဓ"))]):
        return {
            bstack1ll111l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧန"): bstack1ll111l_opy_ (u"ࠣࡃ࡚ࡗࠥࡉ࡯ࡥࡧࡅࡹ࡮ࡲࡤࠣပ"),
            bstack1ll111l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧဖ"): env.get(bstack1ll111l_opy_ (u"ࠥࡇࡔࡊࡅࡃࡗࡌࡐࡉࡥࡐࡖࡄࡏࡍࡈࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤဗ")),
            bstack1ll111l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨဘ"): env.get(bstack1ll111l_opy_ (u"ࠧࡉࡏࡅࡇࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠥမ")),
            bstack1ll111l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧယ"): env.get(bstack1ll111l_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠧရ"))
        }
    if env.get(bstack1ll111l_opy_ (u"ࠣࡤࡤࡱࡧࡵ࡯ࡠࡤࡸ࡭ࡱࡪࡎࡶ࡯ࡥࡩࡷࠨလ")):
        return {
            bstack1ll111l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢဝ"): bstack1ll111l_opy_ (u"ࠥࡆࡦࡳࡢࡰࡱࠥသ"),
            bstack1ll111l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢဟ"): env.get(bstack1ll111l_opy_ (u"ࠧࡨࡡ࡮ࡤࡲࡳࡤࡨࡵࡪ࡮ࡧࡖࡪࡹࡵ࡭ࡶࡶ࡙ࡷࡲࠢဠ")),
            bstack1ll111l_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣအ"): env.get(bstack1ll111l_opy_ (u"ࠢࡣࡣࡰࡦࡴࡵ࡟ࡴࡪࡲࡶࡹࡐ࡯ࡣࡐࡤࡱࡪࠨဢ")),
            bstack1ll111l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢဣ"): env.get(bstack1ll111l_opy_ (u"ࠤࡥࡥࡲࡨ࡯ࡰࡡࡥࡹ࡮ࡲࡤࡏࡷࡰࡦࡪࡸࠢဤ"))
        }
    if env.get(bstack1ll111l_opy_ (u"࡛ࠥࡊࡘࡃࡌࡇࡕࠦဥ")) or env.get(bstack1ll111l_opy_ (u"ࠦ࡜ࡋࡒࡄࡍࡈࡖࡤࡓࡁࡊࡐࡢࡔࡎࡖࡅࡍࡋࡑࡉࡤ࡙ࡔࡂࡔࡗࡉࡉࠨဦ")):
        return {
            bstack1ll111l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥဧ"): bstack1ll111l_opy_ (u"ࠨࡗࡦࡴࡦ࡯ࡪࡸࠢဨ"),
            bstack1ll111l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥဩ"): env.get(bstack1ll111l_opy_ (u"࡙ࠣࡈࡖࡈࡑࡅࡓࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧဪ")),
            bstack1ll111l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦါ"): bstack1ll111l_opy_ (u"ࠥࡑࡦ࡯࡮ࠡࡒ࡬ࡴࡪࡲࡩ࡯ࡧࠥာ") if env.get(bstack1ll111l_opy_ (u"ࠦ࡜ࡋࡒࡄࡍࡈࡖࡤࡓࡁࡊࡐࡢࡔࡎࡖࡅࡍࡋࡑࡉࡤ࡙ࡔࡂࡔࡗࡉࡉࠨိ")) else None,
            bstack1ll111l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦီ"): env.get(bstack1ll111l_opy_ (u"ࠨࡗࡆࡔࡆࡏࡊࡘ࡟ࡈࡋࡗࡣࡈࡕࡍࡎࡋࡗࠦု"))
        }
    if any([env.get(bstack1ll111l_opy_ (u"ࠢࡈࡅࡓࡣࡕࡘࡏࡋࡇࡆࡘࠧူ")), env.get(bstack1ll111l_opy_ (u"ࠣࡉࡆࡐࡔ࡛ࡄࡠࡒࡕࡓࡏࡋࡃࡕࠤေ")), env.get(bstack1ll111l_opy_ (u"ࠤࡊࡓࡔࡍࡌࡆࡡࡆࡐࡔ࡛ࡄࡠࡒࡕࡓࡏࡋࡃࡕࠤဲ"))]):
        return {
            bstack1ll111l_opy_ (u"ࠥࡲࡦࡳࡥࠣဳ"): bstack1ll111l_opy_ (u"ࠦࡌࡵ࡯ࡨ࡮ࡨࠤࡈࡲ࡯ࡶࡦࠥဴ"),
            bstack1ll111l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣဵ"): None,
            bstack1ll111l_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣံ"): env.get(bstack1ll111l_opy_ (u"ࠢࡑࡔࡒࡎࡊࡉࡔࡠࡋࡇ့ࠦ")),
            bstack1ll111l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢး"): env.get(bstack1ll111l_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡋࡇ္ࠦ"))
        }
    if env.get(bstack1ll111l_opy_ (u"ࠥࡗࡍࡏࡐࡑࡃࡅࡐࡊࠨ်")):
        return {
            bstack1ll111l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤျ"): bstack1ll111l_opy_ (u"࡙ࠧࡨࡪࡲࡳࡥࡧࡲࡥࠣြ"),
            bstack1ll111l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤွ"): env.get(bstack1ll111l_opy_ (u"ࠢࡔࡊࡌࡔࡕࡇࡂࡍࡇࡢࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨှ")),
            bstack1ll111l_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥဿ"): bstack1ll111l_opy_ (u"ࠤࡍࡳࡧࠦࠣࡼࡿࠥ၀").format(env.get(bstack1ll111l_opy_ (u"ࠪࡗࡍࡏࡐࡑࡃࡅࡐࡊࡥࡊࡐࡄࡢࡍࡉ࠭၁"))) if env.get(bstack1ll111l_opy_ (u"ࠦࡘࡎࡉࡑࡒࡄࡆࡑࡋ࡟ࡋࡑࡅࡣࡎࡊࠢ၂")) else None,
            bstack1ll111l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ၃"): env.get(bstack1ll111l_opy_ (u"ࠨࡓࡉࡋࡓࡔࡆࡈࡌࡆࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣ၄"))
        }
    if bstack1l1ll11l1l_opy_(env.get(bstack1ll111l_opy_ (u"ࠢࡏࡇࡗࡐࡎࡌ࡙ࠣ၅"))):
        return {
            bstack1ll111l_opy_ (u"ࠣࡰࡤࡱࡪࠨ၆"): bstack1ll111l_opy_ (u"ࠤࡑࡩࡹࡲࡩࡧࡻࠥ၇"),
            bstack1ll111l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ၈"): env.get(bstack1ll111l_opy_ (u"ࠦࡉࡋࡐࡍࡑ࡜ࡣ࡚ࡘࡌࠣ၉")),
            bstack1ll111l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ၊"): env.get(bstack1ll111l_opy_ (u"ࠨࡓࡊࡖࡈࡣࡓࡇࡍࡆࠤ။")),
            bstack1ll111l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ၌"): env.get(bstack1ll111l_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡊࡆࠥ၍"))
        }
    if bstack1l1ll11l1l_opy_(env.get(bstack1ll111l_opy_ (u"ࠤࡊࡍ࡙ࡎࡕࡃࡡࡄࡇ࡙ࡏࡏࡏࡕࠥ၎"))):
        return {
            bstack1ll111l_opy_ (u"ࠥࡲࡦࡳࡥࠣ၏"): bstack1ll111l_opy_ (u"ࠦࡌ࡯ࡴࡉࡷࡥࠤࡆࡩࡴࡪࡱࡱࡷࠧၐ"),
            bstack1ll111l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣၑ"): bstack1ll111l_opy_ (u"ࠨࡻࡾ࠱ࡾࢁ࠴ࡧࡣࡵ࡫ࡲࡲࡸ࠵ࡲࡶࡰࡶ࠳ࢀࢃࠢၒ").format(env.get(bstack1ll111l_opy_ (u"ࠧࡈࡋࡗࡌ࡚ࡈ࡟ࡔࡇࡕ࡚ࡊࡘ࡟ࡖࡔࡏࠫၓ")), env.get(bstack1ll111l_opy_ (u"ࠨࡉࡌࡘࡍ࡛ࡂࡠࡔࡈࡔࡔ࡙ࡉࡕࡑࡕ࡝ࠬၔ")), env.get(bstack1ll111l_opy_ (u"ࠩࡊࡍ࡙ࡎࡕࡃࡡࡕ࡙ࡓࡥࡉࡅࠩၕ"))),
            bstack1ll111l_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧၖ"): env.get(bstack1ll111l_opy_ (u"ࠦࡌࡏࡔࡉࡗࡅࡣ࡜ࡕࡒࡌࡈࡏࡓ࡜ࠨၗ")),
            bstack1ll111l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦၘ"): env.get(bstack1ll111l_opy_ (u"ࠨࡇࡊࡖࡋ࡙ࡇࡥࡒࡖࡐࡢࡍࡉࠨၙ"))
        }
    if env.get(bstack1ll111l_opy_ (u"ࠢࡄࡋࠥၚ")) == bstack1ll111l_opy_ (u"ࠣࡶࡵࡹࡪࠨၛ") and env.get(bstack1ll111l_opy_ (u"ࠤ࡙ࡉࡗࡉࡅࡍࠤၜ")) == bstack1ll111l_opy_ (u"ࠥ࠵ࠧၝ"):
        return {
            bstack1ll111l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤၞ"): bstack1ll111l_opy_ (u"ࠧ࡜ࡥࡳࡥࡨࡰࠧၟ"),
            bstack1ll111l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤၠ"): bstack1ll111l_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࡼࡿࠥၡ").format(env.get(bstack1ll111l_opy_ (u"ࠨࡘࡈࡖࡈࡋࡌࡠࡗࡕࡐࠬၢ"))),
            bstack1ll111l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦၣ"): None,
            bstack1ll111l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤၤ"): None,
        }
    if env.get(bstack1ll111l_opy_ (u"࡙ࠦࡋࡁࡎࡅࡌࡘ࡞ࡥࡖࡆࡔࡖࡍࡔࡔࠢၥ")):
        return {
            bstack1ll111l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥၦ"): bstack1ll111l_opy_ (u"ࠨࡔࡦࡣࡰࡧ࡮ࡺࡹࠣၧ"),
            bstack1ll111l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥၨ"): None,
            bstack1ll111l_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥၩ"): env.get(bstack1ll111l_opy_ (u"ࠤࡗࡉࡆࡓࡃࡊࡖ࡜ࡣࡕࡘࡏࡋࡇࡆࡘࡤࡔࡁࡎࡇࠥၪ")),
            bstack1ll111l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤၫ"): env.get(bstack1ll111l_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥၬ"))
        }
    if any([env.get(bstack1ll111l_opy_ (u"ࠧࡉࡏࡏࡅࡒ࡙ࡗ࡙ࡅࠣၭ")), env.get(bstack1ll111l_opy_ (u"ࠨࡃࡐࡐࡆࡓ࡚ࡘࡓࡆࡡࡘࡖࡑࠨၮ")), env.get(bstack1ll111l_opy_ (u"ࠢࡄࡑࡑࡇࡔ࡛ࡒࡔࡇࡢ࡙ࡘࡋࡒࡏࡃࡐࡉࠧၯ")), env.get(bstack1ll111l_opy_ (u"ࠣࡅࡒࡒࡈࡕࡕࡓࡕࡈࡣ࡙ࡋࡁࡎࠤၰ"))]):
        return {
            bstack1ll111l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢၱ"): bstack1ll111l_opy_ (u"ࠥࡇࡴࡴࡣࡰࡷࡵࡷࡪࠨၲ"),
            bstack1ll111l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢၳ"): None,
            bstack1ll111l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢၴ"): env.get(bstack1ll111l_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡐࡏࡃࡡࡑࡅࡒࡋࠢၵ")) or None,
            bstack1ll111l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨၶ"): env.get(bstack1ll111l_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡊࡆࠥၷ"), 0)
        }
    if env.get(bstack1ll111l_opy_ (u"ࠤࡊࡓࡤࡐࡏࡃࡡࡑࡅࡒࡋࠢၸ")):
        return {
            bstack1ll111l_opy_ (u"ࠥࡲࡦࡳࡥࠣၹ"): bstack1ll111l_opy_ (u"ࠦࡌࡵࡃࡅࠤၺ"),
            bstack1ll111l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣၻ"): None,
            bstack1ll111l_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣၼ"): env.get(bstack1ll111l_opy_ (u"ࠢࡈࡑࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧၽ")),
            bstack1ll111l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢၾ"): env.get(bstack1ll111l_opy_ (u"ࠤࡊࡓࡤࡖࡉࡑࡇࡏࡍࡓࡋ࡟ࡄࡑࡘࡒ࡙ࡋࡒࠣၿ"))
        }
    if env.get(bstack1ll111l_opy_ (u"ࠥࡇࡋࡥࡂࡖࡋࡏࡈࡤࡏࡄࠣႀ")):
        return {
            bstack1ll111l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤႁ"): bstack1ll111l_opy_ (u"ࠧࡉ࡯ࡥࡧࡉࡶࡪࡹࡨࠣႂ"),
            bstack1ll111l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤႃ"): env.get(bstack1ll111l_opy_ (u"ࠢࡄࡈࡢࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨႄ")),
            bstack1ll111l_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥႅ"): env.get(bstack1ll111l_opy_ (u"ࠤࡆࡊࡤࡖࡉࡑࡇࡏࡍࡓࡋ࡟ࡏࡃࡐࡉࠧႆ")),
            bstack1ll111l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤႇ"): env.get(bstack1ll111l_opy_ (u"ࠦࡈࡌ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠤႈ"))
        }
    return {bstack1ll111l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦႉ"): None}
def get_host_info():
    uname = os.uname()
    return {
        bstack1ll111l_opy_ (u"ࠨࡨࡰࡵࡷࡲࡦࡳࡥࠣႊ"): uname.nodename,
        bstack1ll111l_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠤႋ"): uname.sysname,
        bstack1ll111l_opy_ (u"ࠣࡶࡼࡴࡪࠨႌ"): uname.machine,
        bstack1ll111l_opy_ (u"ࠤࡹࡩࡷࡹࡩࡰࡰႍࠥ"): uname.version,
        bstack1ll111l_opy_ (u"ࠥࡥࡷࡩࡨࠣႎ"): uname.machine
    }
def bstack1l1ll11ll1_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack1l1ll11lll_opy_():
    if bstack1ll1ll111_opy_.get_property(bstack1ll111l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠬႏ")):
        return bstack1ll111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ႐")
    return bstack1ll111l_opy_ (u"࠭ࡵ࡯࡭ࡱࡳࡼࡴ࡟ࡨࡴ࡬ࡨࠬ႑")
def bstack1l1l1l1ll1_opy_(driver):
    info = {
        bstack1ll111l_opy_ (u"ࠧࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭႒"): driver.capabilities,
        bstack1ll111l_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠬ႓"): driver.session_id,
        bstack1ll111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪ႔"): driver.capabilities.get(bstack1ll111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨ႕"), None),
        bstack1ll111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭႖"): driver.capabilities.get(bstack1ll111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭႗"), None),
        bstack1ll111l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠨ႘"): driver.capabilities.get(bstack1ll111l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪ࠭႙"), None),
    }
    if bstack1l1ll11lll_opy_() == bstack1ll111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧႚ"):
        info[bstack1ll111l_opy_ (u"ࠩࡳࡶࡴࡪࡵࡤࡶࠪႛ")] = bstack1ll111l_opy_ (u"ࠪࡥࡵࡶ࠭ࡢࡷࡷࡳࡲࡧࡴࡦࠩႜ") if bstack11111111_opy_() else bstack1ll111l_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭ႝ")
    return info
def bstack11111111_opy_():
    if bstack1ll1ll111_opy_.get_property(bstack1ll111l_opy_ (u"ࠬࡧࡰࡱࡡࡤࡹࡹࡵ࡭ࡢࡶࡨࠫ႞")):
        return True
    if bstack1l1ll11l1l_opy_(os.environ.get(bstack1ll111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧ႟"), None)):
        return True
    return False
def bstack1l1l11l11_opy_(bstack1l1l1ll1l1_opy_, url, data, config):
    headers = config.get(bstack1ll111l_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨႠ"), None)
    proxies = bstack11ll11l1_opy_(config, url)
    auth = config.get(bstack1ll111l_opy_ (u"ࠨࡣࡸࡸ࡭࠭Ⴁ"), None)
    response = requests.request(
            bstack1l1l1ll1l1_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    return response
def bstack1llllllll_opy_(bstack1lll11ll1_opy_, size):
    bstack11lll111_opy_ = []
    while len(bstack1lll11ll1_opy_) > size:
        bstack11l111l1_opy_ = bstack1lll11ll1_opy_[:size]
        bstack11lll111_opy_.append(bstack11l111l1_opy_)
        bstack1lll11ll1_opy_ = bstack1lll11ll1_opy_[size:]
    bstack11lll111_opy_.append(bstack1lll11ll1_opy_)
    return bstack11lll111_opy_
def bstack1l1ll11l11_opy_(message, bstack1l1l1lll1l_opy_=False):
    os.write(1, bytes(message, bstack1ll111l_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨႢ")))
    os.write(1, bytes(bstack1ll111l_opy_ (u"ࠪࡠࡳ࠭Ⴃ"), bstack1ll111l_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪႤ")))
    if bstack1l1l1lll1l_opy_:
        with open(bstack1ll111l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠲ࡵ࠱࠲ࡻ࠰ࠫႥ") + os.environ[bstack1ll111l_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡋࡅࡘࡎࡅࡅࡡࡌࡈࠬႦ")] + bstack1ll111l_opy_ (u"ࠧ࠯࡮ࡲ࡫ࠬႧ"), bstack1ll111l_opy_ (u"ࠨࡣࠪႨ")) as f:
            f.write(message + bstack1ll111l_opy_ (u"ࠩ࡟ࡲࠬႩ"))
def bstack1l1l11llll_opy_():
    return os.environ[bstack1ll111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄ࡙࡙ࡕࡍࡂࡖࡌࡓࡓ࠭Ⴊ")].lower() == bstack1ll111l_opy_ (u"ࠫࡹࡸࡵࡦࠩႫ")
def bstack1ll1ll1111_opy_(bstack1l1l11ll11_opy_):
    return bstack1ll111l_opy_ (u"ࠬࢁࡽ࠰ࡽࢀࠫႬ").format(bstack1l1lll1111_opy_, bstack1l1l11ll11_opy_)
def bstack1lll111l1l_opy_():
    return datetime.datetime.utcnow().isoformat() + bstack1ll111l_opy_ (u"࡚࠭ࠨႭ")
def bstack1l1ll111ll_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack1ll111l_opy_ (u"࡛ࠧࠩႮ"))) - datetime.datetime.fromisoformat(start.rstrip(bstack1ll111l_opy_ (u"ࠨ࡜ࠪႯ")))).total_seconds() * 1000
def bstack1l1l11lll1_opy_(timestamp):
    return datetime.datetime.utcfromtimestamp(timestamp).isoformat() + bstack1ll111l_opy_ (u"ࠩ࡝ࠫႰ")
def bstack1l1l11l111_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack1ll111l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪႱ")
    else:
        return bstack1ll111l_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫႲ")
def bstack1l1ll11l1l_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack1ll111l_opy_ (u"ࠬࡺࡲࡶࡧࠪႳ")
def bstack1l1l1l1lll_opy_(val):
    return val.__str__().lower() == bstack1ll111l_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬႴ")
def bstack1l1l1l1l1l_opy_(bstack1l1l1lll11_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack1l1l1lll11_opy_ as e:
                print(bstack1ll111l_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠡࡽࢀࠤ࠲ࡄࠠࡼࡿ࠽ࠤࢀࢃࠢႵ").format(func.__name__, bstack1l1l1lll11_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack1l1l1l1111_opy_(bstack1l1ll1l111_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack1l1ll1l111_opy_(cls, *args, **kwargs)
            except bstack1l1l1lll11_opy_ as e:
                print(bstack1ll111l_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡧࡷࡱࡧࡹ࡯࡯࡯ࠢࡾࢁࠥ࠳࠾ࠡࡽࢀ࠾ࠥࢁࡽࠣႶ").format(bstack1l1ll1l111_opy_.__name__, bstack1l1l1lll11_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack1l1l1l1111_opy_
    else:
        return decorator
def bstack111llllll_opy_(bstack1ll111l1l1_opy_):
    if bstack1ll111l_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭Ⴗ") in bstack1ll111l1l1_opy_ and bstack1l1l1l1lll_opy_(bstack1ll111l1l1_opy_[bstack1ll111l_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧႸ")]):
        return False
    if bstack1ll111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭Ⴙ") in bstack1ll111l1l1_opy_ and bstack1l1l1l1lll_opy_(bstack1ll111l1l1_opy_[bstack1ll111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧႺ")]):
        return False
    return True
def bstack111l1ll1_opy_():
    try:
        from pytest_bdd import reporting
        return True
    except Exception as e:
        return False
def bstack1lll1lll1_opy_(hub_url):
    if bstack1l1111lll_opy_() <= version.parse(bstack1ll111l_opy_ (u"࠭࠳࠯࠳࠶࠲࠵࠭Ⴛ")):
        if hub_url != bstack1ll111l_opy_ (u"ࠧࠨႼ"):
            return bstack1ll111l_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤႽ") + hub_url + bstack1ll111l_opy_ (u"ࠤ࠽࠼࠵࠵ࡷࡥ࠱࡫ࡹࡧࠨႾ")
        return bstack11111l1l1_opy_
    if hub_url != bstack1ll111l_opy_ (u"ࠪࠫႿ"):
        return bstack1ll111l_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࠨჀ") + hub_url + bstack1ll111l_opy_ (u"ࠧ࠵ࡷࡥ࠱࡫ࡹࡧࠨჁ")
    return bstack1l111111l_opy_
def bstack1l1l1l11l1_opy_():
    return isinstance(os.getenv(bstack1ll111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖ࡙ࡕࡇࡖࡘࡤࡖࡌࡖࡉࡌࡒࠬჂ")), str)
def bstack1llll1ll1l_opy_(url):
    return urlparse(url).hostname
def bstack1lll1l11l1_opy_(hostname):
    for bstack1ll11lll1l_opy_ in bstack1lll111l11_opy_:
        regex = re.compile(bstack1ll11lll1l_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack1l1ll1111l_opy_(bstack1l1l1ll1ll_opy_, file_name, logger):
    bstack1ll1ll11ll_opy_ = os.path.join(os.path.expanduser(bstack1ll111l_opy_ (u"ࠧࡿࠩჃ")), bstack1l1l1ll1ll_opy_)
    try:
        if not os.path.exists(bstack1ll1ll11ll_opy_):
            os.makedirs(bstack1ll1ll11ll_opy_)
        file_path = os.path.join(os.path.expanduser(bstack1ll111l_opy_ (u"ࠨࢀࠪჄ")), bstack1l1l1ll1ll_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack1ll111l_opy_ (u"ࠩࡺࠫჅ")):
                pass
            with open(file_path, bstack1ll111l_opy_ (u"ࠥࡻ࠰ࠨ჆")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack1ll1ll1l_opy_.format(str(e)))
def bstack1l1l11l11l_opy_(file_name, key, value, logger):
    file_path = bstack1l1ll1111l_opy_(bstack1ll111l_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫჇ"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack11l1lllll_opy_ = json.load(open(file_path, bstack1ll111l_opy_ (u"ࠬࡸࡢࠨ჈")))
        else:
            bstack11l1lllll_opy_ = {}
        bstack11l1lllll_opy_[key] = value
        with open(file_path, bstack1ll111l_opy_ (u"ࠨࡷࠬࠤ჉")) as outfile:
            json.dump(bstack11l1lllll_opy_, outfile)
def bstack111l1ll1l_opy_(file_name, logger):
    file_path = bstack1l1ll1111l_opy_(bstack1ll111l_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ჊"), file_name, logger)
    bstack11l1lllll_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack1ll111l_opy_ (u"ࠨࡴࠪ჋")) as bstack11ll1l1l1_opy_:
            bstack11l1lllll_opy_ = json.load(bstack11ll1l1l1_opy_)
    return bstack11l1lllll_opy_
def bstack11111lll1_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack1ll111l_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡩ࡫࡬ࡦࡶ࡬ࡲ࡬ࠦࡦࡪ࡮ࡨ࠾ࠥ࠭჌") + file_path + bstack1ll111l_opy_ (u"ࠪࠤࠬჍ") + str(e))
def bstack1l1111lll_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack1ll111l_opy_ (u"ࠦࡁࡔࡏࡕࡕࡈࡘࡃࠨ჎")
def bstack1111l11l_opy_(config):
    if bstack1ll111l_opy_ (u"ࠬ࡯ࡳࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫ჏") in config:
        del (config[bstack1ll111l_opy_ (u"࠭ࡩࡴࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬა")])
        return False
    if bstack1l1111lll_opy_() < version.parse(bstack1ll111l_opy_ (u"ࠧ࠴࠰࠷࠲࠵࠭ბ")):
        return False
    if bstack1l1111lll_opy_() >= version.parse(bstack1ll111l_opy_ (u"ࠨ࠶࠱࠵࠳࠻ࠧგ")):
        return True
    if bstack1ll111l_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩდ") in config and config[bstack1ll111l_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪე")] is False:
        return False
    else:
        return True
def bstack1ll1ll111l_opy_(args_list, bstack1l1l1l111l_opy_):
    index = -1
    for value in bstack1l1l1l111l_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack1l1l11l1ll_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack1l1l11l1ll_opy_ = bstack1l1l11l1ll_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack1ll111l_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫვ"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack1ll111l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬზ"), exception=exception)
    def bstack1l1ll11111_opy_(self):
        if self.result != bstack1ll111l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭თ"):
            return None
        if bstack1ll111l_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࠥი") in self.exception_type:
            return bstack1ll111l_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࡉࡷࡸ࡯ࡳࠤკ")
        return bstack1ll111l_opy_ (u"ࠤࡘࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࡊࡸࡲࡰࡴࠥლ")
    def bstack1l1l111lll_opy_(self):
        if self.result != bstack1ll111l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪმ"):
            return None
        if self.bstack1l1l11l1ll_opy_:
            return self.bstack1l1l11l1ll_opy_
        return bstack1l1l11l1l1_opy_(self.exception)
def bstack1l1l11l1l1_opy_(exc):
    return traceback.format_exception(exc)
def bstack1l1l1ll111_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack1lll1111_opy_(object, key, default_value):
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value