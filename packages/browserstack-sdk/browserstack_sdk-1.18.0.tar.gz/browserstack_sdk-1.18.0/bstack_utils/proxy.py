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
from urllib.parse import urlparse
from bstack_utils.messages import bstack1l11ll1l1l_opy_
def bstack11lllll1ll_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack11llll1lll_opy_(bstack11llll1ll1_opy_, bstack11lllll11l_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack11llll1ll1_opy_):
        with open(bstack11llll1ll1_opy_) as f:
            pac = PACFile(f.read())
    elif bstack11lllll1ll_opy_(bstack11llll1ll1_opy_):
        pac = get_pac(url=bstack11llll1ll1_opy_)
    else:
        raise Exception(bstack1ll111l_opy_ (u"࠭ࡐࡢࡥࠣࡪ࡮ࡲࡥࠡࡦࡲࡩࡸࠦ࡮ࡰࡶࠣࡩࡽ࡯ࡳࡵ࠼ࠣࡿࢂ࠭ᆢ").format(bstack11llll1ll1_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack1ll111l_opy_ (u"ࠢ࠹࠰࠻࠲࠽࠴࠸ࠣᆣ"), 80))
        bstack11lllll111_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack11lllll111_opy_ = bstack1ll111l_opy_ (u"ࠨ࠲࠱࠴࠳࠶࠮࠱ࠩᆤ")
    proxy_url = session.get_pac().find_proxy_for_url(bstack11lllll11l_opy_, bstack11lllll111_opy_)
    return proxy_url
def bstack1ll1l1l1ll_opy_(config):
    return bstack1ll111l_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬᆥ") in config or bstack1ll111l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧᆦ") in config
def bstack111llll11_opy_(config):
    if not bstack1ll1l1l1ll_opy_(config):
        return
    if config.get(bstack1ll111l_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧᆧ")):
        return config.get(bstack1ll111l_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨᆨ"))
    if config.get(bstack1ll111l_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪᆩ")):
        return config.get(bstack1ll111l_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫᆪ"))
def bstack11ll11l1_opy_(config, bstack11lllll11l_opy_):
    proxy = bstack111llll11_opy_(config)
    proxies = {}
    if config.get(bstack1ll111l_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫᆫ")) or config.get(bstack1ll111l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ᆬ")):
        if proxy.endswith(bstack1ll111l_opy_ (u"ࠪ࠲ࡵࡧࡣࠨᆭ")):
            proxies = bstack11l1l1l1l_opy_(proxy, bstack11lllll11l_opy_)
        else:
            proxies = {
                bstack1ll111l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࠪᆮ"): proxy
            }
    return proxies
def bstack11l1l1l1l_opy_(bstack11llll1ll1_opy_, bstack11lllll11l_opy_):
    proxies = {}
    global bstack11lllll1l1_opy_
    if bstack1ll111l_opy_ (u"ࠬࡖࡁࡄࡡࡓࡖࡔ࡞࡙ࠨᆯ") in globals():
        return bstack11lllll1l1_opy_
    try:
        proxy = bstack11llll1lll_opy_(bstack11llll1ll1_opy_, bstack11lllll11l_opy_)
        if bstack1ll111l_opy_ (u"ࠨࡄࡊࡔࡈࡇ࡙ࠨᆰ") in proxy:
            proxies = {}
        elif bstack1ll111l_opy_ (u"ࠢࡉࡖࡗࡔࠧᆱ") in proxy or bstack1ll111l_opy_ (u"ࠣࡊࡗࡘࡕ࡙ࠢᆲ") in proxy or bstack1ll111l_opy_ (u"ࠤࡖࡓࡈࡑࡓࠣᆳ") in proxy:
            bstack11llllll11_opy_ = proxy.split(bstack1ll111l_opy_ (u"ࠥࠤࠧᆴ"))
            if bstack1ll111l_opy_ (u"ࠦ࠿࠵࠯ࠣᆵ") in bstack1ll111l_opy_ (u"ࠧࠨᆶ").join(bstack11llllll11_opy_[1:]):
                proxies = {
                    bstack1ll111l_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬᆷ"): bstack1ll111l_opy_ (u"ࠢࠣᆸ").join(bstack11llllll11_opy_[1:])
                }
            else:
                proxies = {
                    bstack1ll111l_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧᆹ"): str(bstack11llllll11_opy_[0]).lower() + bstack1ll111l_opy_ (u"ࠤ࠽࠳࠴ࠨᆺ") + bstack1ll111l_opy_ (u"ࠥࠦᆻ").join(bstack11llllll11_opy_[1:])
                }
        elif bstack1ll111l_opy_ (u"ࠦࡕࡘࡏ࡙࡛ࠥᆼ") in proxy:
            bstack11llllll11_opy_ = proxy.split(bstack1ll111l_opy_ (u"ࠧࠦࠢᆽ"))
            if bstack1ll111l_opy_ (u"ࠨ࠺࠰࠱ࠥᆾ") in bstack1ll111l_opy_ (u"ࠢࠣᆿ").join(bstack11llllll11_opy_[1:]):
                proxies = {
                    bstack1ll111l_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧᇀ"): bstack1ll111l_opy_ (u"ࠤࠥᇁ").join(bstack11llllll11_opy_[1:])
                }
            else:
                proxies = {
                    bstack1ll111l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩᇂ"): bstack1ll111l_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧᇃ") + bstack1ll111l_opy_ (u"ࠧࠨᇄ").join(bstack11llllll11_opy_[1:])
                }
        else:
            proxies = {
                bstack1ll111l_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬᇅ"): proxy
            }
    except Exception as e:
        print(bstack1ll111l_opy_ (u"ࠢࡴࡱࡰࡩࠥ࡫ࡲࡳࡱࡵࠦᇆ"), bstack1l11ll1l1l_opy_.format(bstack11llll1ll1_opy_, str(e)))
    bstack11lllll1l1_opy_ = proxies
    return proxies