from enum import Enum  # noqa


class ShopTypeSeven(str, Enum):
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
        for tuple_item in ShopTypeSeven.__members__.items():
            enum_list.append({'id': tuple_item[0], 'name': tuple_item[1].value})
        return enum_list
