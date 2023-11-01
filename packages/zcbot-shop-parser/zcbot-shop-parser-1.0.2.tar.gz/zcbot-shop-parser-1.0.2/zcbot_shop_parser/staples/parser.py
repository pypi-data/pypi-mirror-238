import logging

from typing import Union, List
from ..core.model import ShopModel
from ..staples.model import ShopTypeThree, ShopTypeSeven

LOGGER = logging.getLogger(__name__)


class StaplesShopParser(object):
    def __init__(self):
        pass

    def parse_shop7(self, plat_code: str, shop_name: str, brand_name: str = None) -> Union[ShopModel, None]:
        """
        根据平台编码和店铺名称解析店铺类型
        有效链接返回ShopModel，无效链接返回None
        """
        _shop_type = ""

        if plat_code == "jd":
            if not shop_name:
                _shop_type = "其他"
            if "自营" in shop_name and "企业购" in shop_name:
                _shop_type = "自营企业购"
            if "旗舰店" in shop_name and "自营" not in shop_name:
                _shop_type = "非自营旗舰店"
            if "专营店" in shop_name:
                _shop_type = "专营店"

            if not brand_name:
                _shop_type = "其他"

            if "自营" in shop_name:
                if brand_name and brand_name in shop_name:
                    _shop_type = "自营品牌旗舰店"
                elif "旗舰" in shop_name:
                    _shop_type = "自营旗舰店"
                else:
                    _shop_type = "自营非旗舰店"
            shop_types = ShopTypeSeven.to_list()
            shop_model = self.build_model(shop_types=shop_types, plat_code=plat_code, shop_name=shop_name, shop_type=_shop_type)

            if shop_model.shop_type_code:
                return shop_model

        return None

    def parse_shop3(self, plat_code: str, shop_name: str, brand_name: str = None) -> Union[ShopModel, None]:
        """
        根据平台编码和店铺名称解析店铺类型
        有效链接返回ShopModel，无效链接返回None
        """
        _shop_type = ""
        # 京东、苏宁逻辑一样
        if plat_code == "jd" or plat_code == "suning":
            if "自营" in shop_name:
                _shop_type = "自营"

            elif "自营" not in shop_name and "旗舰店" in shop_name:
                _shop_type = "旗舰店"

            else:
                _shop_type = "专营店"
        # 天猫
        elif plat_code == "tmall":
            if "旗舰店" in shop_name:
                _shop_type = "旗舰店"
            else:
                _shop_type = "专营店"

        else:
            _shop_type = "其他"

        shop_types = ShopTypeThree.to_list()
        shop_model = self.build_model(shop_types=shop_types, plat_code=plat_code, shop_name=shop_name, shop_type=_shop_type)
        if shop_model.shop_type_code:
            return shop_model

        return None

    @staticmethod
    def build_model(shop_types: List[dict] = [], plat_code: str = None, shop_name: str = None, shop_type: str = None) -> Union[ShopModel, None]:

        shop_type_code = None
        shop_type_name = None

        for _shop_type in shop_types:  # noqa
            code = _shop_type.get("id", "")
            name = _shop_type.get("name", "")
            if shop_type == name:
                shop_type_name = name
                shop_type_code = code

        if "自营" in shop_name:
            is_self = "是"
        else:
            is_self = "否"

        shop_model = ShopModel()
        shop_model.plat_code = plat_code
        shop_model.shop_name = shop_name
        shop_model.shop_type_code = shop_type_code
        shop_model.shop_type_name = shop_type_name
        shop_model.is_self = is_self

        return shop_model
