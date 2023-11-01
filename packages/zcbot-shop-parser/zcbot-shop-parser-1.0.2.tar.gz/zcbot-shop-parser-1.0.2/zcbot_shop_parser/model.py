from enum import Enum
from pydantic import BaseModel
from typing import Union


class ShopType(str, Enum):
    """
    任务类型枚举
    """
    # 自营企业购 --> 有自营标识，且店铺名称包含“企业购”
    TYPE_1 = '自营企业购'
    # 非自营旗舰店 --> 无自营标识，店铺名称含“旗舰店”
    TYPE_2 = '非自营旗舰店'
    # 专营店 --> 无自营标识，店铺名称含“专营店”
    TYPE_3 = '专营店'
    # 其它 --> 无自营标识，其它
    TYPE_4 = '无自营标识，其它'
    # 自营品牌旗舰店  --> 有自营标识，店铺名称包含商品品牌和“旗舰店”
    TYPE_5 = '自营品牌旗舰店'
    # 自营旗舰店  --> 有自营标识，店铺名称含“旗舰店”
    TYPE_6 = '自营旗舰店'
    # 自营非旗舰店  --> 有自营标识，店铺名称不含旗舰店
    TYPE_7 = '自营非旗舰店'

    @staticmethod
    def to_list():
        enum_list = list()
        for tuple_item in ShopType.__members__.items():
            enum_list.append({'id': tuple_item[0], 'name': tuple_item[1].value})
        return enum_list


class PartnerShopType(str, Enum):
    """
    1、自营
    a 有自营标识，店铺名称含企业购
    b 有自营标识，店铺名称里含SKU在PCS的品牌，完全一致，店铺名称含旗舰店
    c 有自营标识，店铺名称含旗舰店
    d 有自营标识，店铺名称不含旗舰店

    2、旗舰店
    无自营标识，店铺名称里含旗舰店 就是旗舰店

    3、专营店
    其他都算专营店

    4、其他
    除了京东、天猫、苏宁，其他平台都显示其他
    """

    TYPE_1 = "自营"

    TYPE_2 = "旗舰店"

    TYPE_3 = "专营店"

    TYPE_4 = "其他"

    @staticmethod
    def to_list():
        enum_list = list()
        for tuple_item in PartnerShopType.__members__.items():
            enum_list.append({'id': tuple_item[0], 'name': tuple_item[1].value})
        return enum_list


class ShopModel(BaseModel):
    """
    通用店铺类型数据模型
    """
    # 店铺名称
    shop_name: str = None
    # 平台编码  如：jd
    plat_code: str = None
    # 店铺类型编码
    shop_type_code: str = None
    # 店铺类型名称
    shop_type_name: str = None
    # 是否自营
    is_self: str = None
