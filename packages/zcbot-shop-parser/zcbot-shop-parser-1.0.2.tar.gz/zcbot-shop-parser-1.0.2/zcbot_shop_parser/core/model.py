# encoding: utf-8

from pydantic import BaseModel


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

