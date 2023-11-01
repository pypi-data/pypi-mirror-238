import logging
from typing import Union

from .model import ShopModel, ShopType
from .common.parser import CommonShopParser
from .staples.parser import StaplesShopParser

common_shop_parser = CommonShopParser()
staples_shop_parser = StaplesShopParser()

LOGGER = logging.getLogger(__name__)


def common_shop7(plat_code: str, shop_name: str, brand_name: str = None) -> Union[ShopModel, None]:
    """
    通用7类分类
    """
    result = common_shop_parser.parse_shop7(plat_code=plat_code, shop_name=shop_name, brand_name=brand_name)

    return result


def staples_shop3(plat_code: str, shop_name: str, brand_name: str = None) -> Union[ShopModel, None]:
    """
    史泰博3类分类
    """
    result = staples_shop_parser.parse_shop3(plat_code=plat_code, shop_name=shop_name, brand_name=brand_name)

    return result


def staples_shop7(plat_code: str, shop_name: str, brand_name: str = None) -> Union[ShopModel, None]:
    """
    史泰博7类分类
    """
    result = staples_shop_parser.parse_shop7(plat_code=plat_code, shop_name=shop_name, brand_name=brand_name)

    return result
