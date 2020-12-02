from ..base import get_suite
from ...api.attribute import ATTRIBUTE_TYPES


def suite(api, check_all=False):
    for attribute_type in ATTRIBUTE_TYPES:
        namespace = api.attribute(attribute_type)
        suite = get_suite(namespace)
        yield suite
        if not check_all:
            return
