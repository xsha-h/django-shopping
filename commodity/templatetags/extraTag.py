from django import template

from commodity.models import CommodityType

register = template.Library()


# 自定义模板标签
@register.simple_tag
def TypeTag():
    typelist = CommodityType.objects.all()
    all_types = []
    for one in typelist:
        if one.level == 1:
            one_type = {}
            one_type["id"] = one.id
            one_type["name"] = one.name
            one_type["two"] = []
            for two in typelist:
                if two.level == 2 and two.uper_type_id == one.id:
                    two_type = {}
                    two_type["id"] = two.id
                    two_type["name"] = two.name
                    two_type["three"] = []
                    for three in typelist:
                        if three.level == 3 and three.uper_type_id == two.id:
                            three_type = {}
                            three_type["id"] = three.id
                            three_type["name"] = three.name
                            two_type["three"].append(three_type)
                    one_type["two"].append(two_type)
            all_types.append(one_type)
    return all_types

