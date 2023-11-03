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
from _pytest import fixtures
from _pytest.python import _call_with_optional_argument
from pytest import Module, Class
from bstack_utils.helper import Result
def _1l1l111l1l_opy_(method, this, arg):
    arg_count = method.__code__.co_argcount
    if arg_count > 1:
        method(this, arg)
    else:
        method(this)
class bstack1l1l111l11_opy_:
    def __init__(self, handler):
        self._1l11lll11l_opy_ = {}
        self._1l11llll1l_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        self._1l11lll11l_opy_[bstack1ll111l_opy_ (u"ࠫ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧნ")] = Module._inject_setup_function_fixture
        self._1l11lll11l_opy_[bstack1ll111l_opy_ (u"ࠬࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ო")] = Module._inject_setup_module_fixture
        self._1l11lll11l_opy_[bstack1ll111l_opy_ (u"࠭ࡣ࡭ࡣࡶࡷࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭პ")] = Class._inject_setup_class_fixture
        self._1l11lll11l_opy_[bstack1ll111l_opy_ (u"ࠧ࡮ࡧࡷ࡬ࡴࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨჟ")] = Class._inject_setup_method_fixture
        Module._inject_setup_function_fixture = self.bstack1l1l11111l_opy_(bstack1ll111l_opy_ (u"ࠨࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫრ"))
        Module._inject_setup_module_fixture = self.bstack1l1l11111l_opy_(bstack1ll111l_opy_ (u"ࠩࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪს"))
        Class._inject_setup_class_fixture = self.bstack1l1l11111l_opy_(bstack1ll111l_opy_ (u"ࠪࡧࡱࡧࡳࡴࡡࡩ࡭ࡽࡺࡵࡳࡧࠪტ"))
        Class._inject_setup_method_fixture = self.bstack1l1l11111l_opy_(bstack1ll111l_opy_ (u"ࠫࡲ࡫ࡴࡩࡱࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࠬუ"))
    def bstack1l1l1111ll_opy_(self, bstack1l11ll1lll_opy_, hook_type):
        meth = getattr(bstack1l11ll1lll_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._1l11llll1l_opy_[hook_type] = meth
            setattr(bstack1l11ll1lll_opy_, hook_type, self.bstack1l11llll11_opy_(hook_type))
    def bstack1l11lllll1_opy_(self, instance, bstack1l11lll1ll_opy_):
        if bstack1l11lll1ll_opy_ == bstack1ll111l_opy_ (u"ࠧ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠣფ"):
            self.bstack1l1l1111ll_opy_(instance.obj, bstack1ll111l_opy_ (u"ࠨࡳࡦࡶࡸࡴࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠢქ"))
            self.bstack1l1l1111ll_opy_(instance.obj, bstack1ll111l_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡩࡹࡳࡩࡴࡪࡱࡱࠦღ"))
        if bstack1l11lll1ll_opy_ == bstack1ll111l_opy_ (u"ࠣ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠤყ"):
            self.bstack1l1l1111ll_opy_(instance.obj, bstack1ll111l_opy_ (u"ࠤࡶࡩࡹࡻࡰࡠ࡯ࡲࡨࡺࡲࡥࠣშ"))
            self.bstack1l1l1111ll_opy_(instance.obj, bstack1ll111l_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳ࡯ࡥࡷ࡯ࡩࠧჩ"))
        if bstack1l11lll1ll_opy_ == bstack1ll111l_opy_ (u"ࠦࡨࡲࡡࡴࡵࡢࡪ࡮ࡾࡴࡶࡴࡨࠦც"):
            self.bstack1l1l1111ll_opy_(instance.obj, bstack1ll111l_opy_ (u"ࠧࡹࡥࡵࡷࡳࡣࡨࡲࡡࡴࡵࠥძ"))
            self.bstack1l1l1111ll_opy_(instance.obj, bstack1ll111l_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡥ࡯ࡥࡸࡹࠢწ"))
        if bstack1l11lll1ll_opy_ == bstack1ll111l_opy_ (u"ࠢ࡮ࡧࡷ࡬ࡴࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠣჭ"):
            self.bstack1l1l1111ll_opy_(instance.obj, bstack1ll111l_opy_ (u"ࠣࡵࡨࡸࡺࡶ࡟࡮ࡧࡷ࡬ࡴࡪࠢხ"))
            self.bstack1l1l1111ll_opy_(instance.obj, bstack1ll111l_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲ࡫ࡴࡩࡱࡧࠦჯ"))
    @staticmethod
    def bstack1l1l111111_opy_(hook_type, func, args):
        if hook_type in [bstack1ll111l_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡩࡹ࡮࡯ࡥࠩჰ"), bstack1ll111l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡦࡶ࡫ࡳࡩ࠭ჱ")]:
            _1l1l111l1l_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack1l11llll11_opy_(self, hook_type):
        def bstack1l11lll1l1_opy_(arg=None):
            self.handler(hook_type, bstack1ll111l_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࠬჲ"))
            result = None
            exception = None
            try:
                self.bstack1l1l111111_opy_(hook_type, self._1l11llll1l_opy_[hook_type], (arg,))
                result = Result(result=bstack1ll111l_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ჳ"))
            except Exception as e:
                result = Result(result=bstack1ll111l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧჴ"), exception=e)
                self.handler(hook_type, bstack1ll111l_opy_ (u"ࠨࡣࡩࡸࡪࡸࠧჵ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1ll111l_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࠨჶ"), result)
        def bstack1l1l1111l1_opy_(this, arg=None):
            self.handler(hook_type, bstack1ll111l_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࠪჷ"))
            result = None
            exception = None
            try:
                self.bstack1l1l111111_opy_(hook_type, self._1l11llll1l_opy_[hook_type], (this, arg))
                result = Result(result=bstack1ll111l_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫჸ"))
            except Exception as e:
                result = Result(result=bstack1ll111l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬჹ"), exception=e)
                self.handler(hook_type, bstack1ll111l_opy_ (u"࠭ࡡࡧࡶࡨࡶࠬჺ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1ll111l_opy_ (u"ࠧࡢࡨࡷࡩࡷ࠭჻"), result)
        if hook_type in [bstack1ll111l_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡧࡷ࡬ࡴࡪࠧჼ"), bstack1ll111l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲ࡫ࡴࡩࡱࡧࠫჽ")]:
            return bstack1l1l1111l1_opy_
        return bstack1l11lll1l1_opy_
    def bstack1l1l11111l_opy_(self, bstack1l11lll1ll_opy_):
        def bstack1l11lll111_opy_(this, *args, **kwargs):
            self.bstack1l11lllll1_opy_(this, bstack1l11lll1ll_opy_)
            self._1l11lll11l_opy_[bstack1l11lll1ll_opy_](this, *args, **kwargs)
        return bstack1l11lll111_opy_