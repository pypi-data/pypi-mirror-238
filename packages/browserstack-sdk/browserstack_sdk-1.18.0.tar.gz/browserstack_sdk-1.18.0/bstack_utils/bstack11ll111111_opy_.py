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
from uuid import uuid4
from bstack_utils.helper import bstack1lll111l1l_opy_, bstack1l1ll111ll_opy_
from bstack_utils.bstack11111ll11_opy_ import bstack11lll1ll11_opy_
class bstack11ll111l11_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, bstack11l1lll1ll_opy_=None, framework=None, tags=[], scope=[], bstack11l1llll11_opy_=None, bstack11ll111lll_opy_=True, bstack11l1lll11l_opy_=None, bstack1ll11l1l_opy_=None, result=None, duration=None, meta={}):
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack11ll111lll_opy_:
            self.uuid = uuid4().__str__()
        self.bstack11l1lll1ll_opy_ = bstack11l1lll1ll_opy_
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack11l1llll11_opy_ = bstack11l1llll11_opy_
        self.bstack11l1lll11l_opy_ = bstack11l1lll11l_opy_
        self.bstack1ll11l1l_opy_ = bstack1ll11l1l_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
    def bstack11l1lll111_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack11l1lll1l1_opy_(self):
        bstack11ll111l1l_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack1ll111l_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫሢ"): bstack11ll111l1l_opy_,
            bstack1ll111l_opy_ (u"ࠩ࡯ࡳࡨࡧࡴࡪࡱࡱࠫሣ"): bstack11ll111l1l_opy_,
            bstack1ll111l_opy_ (u"ࠪࡺࡨࡥࡦࡪ࡮ࡨࡴࡦࡺࡨࠨሤ"): bstack11ll111l1l_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack1ll111l_opy_ (u"࡚ࠦࡴࡥࡹࡲࡨࡧࡹ࡫ࡤࠡࡣࡵ࡫ࡺࡳࡥ࡯ࡶ࠽ࠤࠧሥ") + key)
            setattr(self, key, val)
    def bstack11ll111ll1_opy_(self):
        return {
            bstack1ll111l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪሦ"): self.name,
            bstack1ll111l_opy_ (u"࠭ࡢࡰࡦࡼࠫሧ"): {
                bstack1ll111l_opy_ (u"ࠧ࡭ࡣࡱ࡫ࠬረ"): bstack1ll111l_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨሩ"),
                bstack1ll111l_opy_ (u"ࠩࡦࡳࡩ࡫ࠧሪ"): self.code
            },
            bstack1ll111l_opy_ (u"ࠪࡷࡨࡵࡰࡦࡵࠪራ"): self.scope,
            bstack1ll111l_opy_ (u"ࠫࡹࡧࡧࡴࠩሬ"): self.tags,
            bstack1ll111l_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨር"): self.framework,
            bstack1ll111l_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪሮ"): self.bstack11l1lll1ll_opy_
        }
    def bstack11ll11l11l_opy_(self):
        return {
         bstack1ll111l_opy_ (u"ࠧ࡮ࡧࡷࡥࠬሯ"): self.meta
        }
    def bstack11ll11l1ll_opy_(self):
        return {
            bstack1ll111l_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡓࡧࡵࡹࡳࡖࡡࡳࡣࡰࠫሰ"): {
                bstack1ll111l_opy_ (u"ࠩࡵࡩࡷࡻ࡮ࡠࡰࡤࡱࡪ࠭ሱ"): self.bstack11l1llll11_opy_
            }
        }
    def bstack11ll11l111_opy_(self, bstack11ll1111l1_opy_, details):
        step = next(filter(lambda st: st[bstack1ll111l_opy_ (u"ࠪ࡭ࡩ࠭ሲ")] == bstack11ll1111l1_opy_, self.meta[bstack1ll111l_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪሳ")]), None)
        step.update(details)
    def bstack11l1llllll_opy_(self, bstack11ll1111l1_opy_):
        step = next(filter(lambda st: st[bstack1ll111l_opy_ (u"ࠬ࡯ࡤࠨሴ")] == bstack11ll1111l1_opy_, self.meta[bstack1ll111l_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬስ")]), None)
        step.update({
            bstack1ll111l_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫሶ"): bstack1lll111l1l_opy_()
        })
    def bstack11ll1111ll_opy_(self, bstack11ll1111l1_opy_, result):
        bstack11l1lll11l_opy_ = bstack1lll111l1l_opy_()
        step = next(filter(lambda st: st[bstack1ll111l_opy_ (u"ࠨ࡫ࡧࠫሷ")] == bstack11ll1111l1_opy_, self.meta[bstack1ll111l_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨሸ")]), None)
        step.update({
            bstack1ll111l_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨሹ"): bstack11l1lll11l_opy_,
            bstack1ll111l_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳ࠭ሺ"): bstack1l1ll111ll_opy_(step[bstack1ll111l_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩሻ")], bstack11l1lll11l_opy_),
            bstack1ll111l_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ሼ"): result.result,
            bstack1ll111l_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨሽ"): str(result.exception) if result.exception else None
        })
    def bstack11l1llll1l_opy_(self):
        return {
            bstack1ll111l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ሾ"): self.bstack11l1lll111_opy_(),
            **self.bstack11ll111ll1_opy_(),
            **self.bstack11l1lll1l1_opy_(),
            **self.bstack11ll11l11l_opy_()
        }
    def bstack11l1ll1lll_opy_(self):
        data = {
            bstack1ll111l_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧሿ"): self.bstack11l1lll11l_opy_,
            bstack1ll111l_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࡤ࡯࡮ࡠ࡯ࡶࠫቀ"): self.duration,
            bstack1ll111l_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫቁ"): self.result.result
        }
        if data[bstack1ll111l_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬቂ")] == bstack1ll111l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ቃ"):
            data[bstack1ll111l_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࡠࡶࡼࡴࡪ࠭ቄ")] = self.result.bstack1l1ll11111_opy_()
            data[bstack1ll111l_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࠩቅ")] = [{bstack1ll111l_opy_ (u"ࠩࡥࡥࡨࡱࡴࡳࡣࡦࡩࠬቆ"): self.result.bstack1l1l111lll_opy_()}]
        return data
    def bstack11l1lllll1_opy_(self):
        return {
            bstack1ll111l_opy_ (u"ࠪࡹࡺ࡯ࡤࠨቇ"): self.bstack11l1lll111_opy_(),
            **self.bstack11ll111ll1_opy_(),
            **self.bstack11l1lll1l1_opy_(),
            **self.bstack11l1ll1lll_opy_(),
            **self.bstack11ll11l11l_opy_()
        }
    def bstack11ll11ll11_opy_(self, event, result=None):
        if result:
            self.result = result
        if event == bstack1ll111l_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬቈ"):
            return self.bstack11l1llll1l_opy_()
        elif event == bstack1ll111l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ቉"):
            return self.bstack11l1lllll1_opy_()
    def bstack11ll11lll1_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack11l1lll11l_opy_ = time if time else bstack1lll111l1l_opy_()
        self.duration = duration if duration else bstack1l1ll111ll_opy_(self.bstack11l1lll1ll_opy_, self.bstack11l1lll11l_opy_)
        if result:
            self.result = result
class bstack11ll11111l_opy_(bstack11ll111l11_opy_):
    def __init__(self, *args, hooks=[], **kwargs):
        self.hooks = hooks
        super().__init__(*args, **kwargs, bstack1ll11l1l_opy_=bstack1ll111l_opy_ (u"࠭ࡴࡦࡵࡷࠫቊ"))
    @classmethod
    def bstack11ll11l1l1_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack1ll111l_opy_ (u"ࠧࡪࡦࠪቋ"): id(step),
                bstack1ll111l_opy_ (u"ࠨࡶࡨࡼࡹ࠭ቌ"): step.name,
                bstack1ll111l_opy_ (u"ࠩ࡮ࡩࡾࡽ࡯ࡳࡦࠪቍ"): step.keyword,
            })
        return bstack11ll11111l_opy_(
            **kwargs,
            meta={
                bstack1ll111l_opy_ (u"ࠪࡪࡪࡧࡴࡶࡴࡨࠫ቎"): {
                    bstack1ll111l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ቏"): feature.name,
                    bstack1ll111l_opy_ (u"ࠬࡶࡡࡵࡪࠪቐ"): feature.filename,
                    bstack1ll111l_opy_ (u"࠭ࡤࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫቑ"): feature.description
                },
                bstack1ll111l_opy_ (u"ࠧࡴࡥࡨࡲࡦࡸࡩࡰࠩቒ"): {
                    bstack1ll111l_opy_ (u"ࠨࡰࡤࡱࡪ࠭ቓ"): scenario.name
                },
                bstack1ll111l_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨቔ"): steps,
                bstack1ll111l_opy_ (u"ࠪࡩࡽࡧ࡭ࡱ࡮ࡨࡷࠬቕ"): bstack11lll1ll11_opy_(test)
            }
        )
    def bstack11ll11ll1l_opy_(self):
        return {
            bstack1ll111l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪቖ"): self.hooks
        }
    def bstack11l1lllll1_opy_(self):
        return {
            **super().bstack11l1lllll1_opy_(),
            **self.bstack11ll11ll1l_opy_()
        }
    def bstack11ll11lll1_opy_(self):
        return bstack1ll111l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧ቗")