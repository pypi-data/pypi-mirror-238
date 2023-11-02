from ..item import _Item, _ITEM_SLOT, _WEIGHTS, _QUALITY_TYPES, _MATERIAL_TYPES, _ITEM_EVENTS, _ITEM_CATEGORIES, \
    _CURRENCY, _Optional

_CLOTHING_DICT = {
    "Burlap Tunic": {
        'item_id': 193,
        'name': 'Burlap Tunic',
        'slot': 'SHIRT',
        'weight': (.2, 'kg'),
        'material': 'BURLAP',
        'mundane': True,
        'description': 'A basic burlap tunic.',
        'quality': 'COMMON',
        'value': (1, 'cp'),
        'color': 'BROWN',
        'appeal': 1
    },
    "Leather Tunic": {
        'item_id': 194,
        'name': 'Leather Tunic',
        'slot': 'SHIRT',
        'weight': (.5, 'kg'),
        'material': 'LEATHER',
        'mundane': True,
        'description': 'A basic leather tunic.',
        'quality': 'COMMON',
        'value': (5, 'cp'),
        'color': 'BROWN',
        'appeal': 2
    },
    "Burlap Trousers": {
        'item_id': 195,
        'name': 'Burlap Trousers',
        'slot': 'TROUSERS',
        'weight': (.4, 'kg'),
        'material': 'BURLAP',
        'mundane': True,
        'description': 'A basic pair of burlap trousers.',
        'quality': 'COMMON',
        'value': (1, 'cp'),
        'color': 'BROWN',
        'appeal': 1
    },
    "Leather Trousers": {
        'item_id': 196,
        'name': 'Leather Trousers',
        'slot': 'TROUSERS',
        'weight': (.6, 'kg'),
        'material': 'LEATHER',
        'mundane': True,
        'description': 'A basic pair of leather trousers.',
        'quality': 'COMMON',
        'value': (5, 'cp'),
        'color': 'BROWN',
        'appeal': 2
    },
    "Loincloth": {
        'item_id': 197,
        'name': 'Loincloth',
        'slot': 'TROUSERS',
        'weight': (.1, 'kg'),
        'material': 'CLOTH',
        'mundane': True,
        'description': 'A basic loincloth.',
        'quality': 'COMMON',
        'value': (1, 'cp'),
        'color': 'BROWN',
        'appeal': 1
    }

}


class _Clothing(_Item):
    def __init__(
            self,
            item_id: _Optional[int] = None,
            name: _Optional[str] = None,
            slot: _Optional[str] = None,
            weight: _Optional[tuple[float, str]] = None,
            material: _Optional[str] = None,
            mundane: _Optional[bool] = None,
            description: _Optional[str] = None,
            quality: _Optional[str] = None,
            value: _Optional[tuple[int, str]] = None,
            color: _Optional[str] = None,
            appeal: _Optional[int] = None
    ):
        self.color = color
        self.appeal = appeal
        super(_Clothing, self).__init__(
            item_id=item_id,
            name=name,
            category='CLOTHING',
            slot=slot,
            weight=weight,
            material=material,
            consumable=False,
            mundane=mundane,
            description=description,
            quality=quality,
            value=value,
            binding='UNBOUND',
            quest_item=False,
            relic=False
        )


class _ClothingByName(_Clothing):
    def __init__(self, clothing_name):
        super(_ClothingByName, self).__init__(**_CLOTHING_DICT[clothing_name])


class _ClothingFactory:
    @staticmethod
    def create_clothing(clothing_name: int) -> type | None:
        _clothing_class = type(clothing_name.replace(" ", "").replace(",", "_").lower(),
                               (_Clothing,),
                               {})
        return None if _clothing_class is None else _clothing_class
