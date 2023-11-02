from typing import Union as _Union, Optional as _Optional
from dicepy import Die
from ..item import _Item

_Die = Die.Die

import re
import json as _json

from CharActor._charactor.dicts import load_dict

def _load_json(path):
    with open(path, 'r') as f:
        return _json.load(f)

_ARMOR_DICT = load_dict('armor')


class _Armor(_Item):
    def __init__(
            self,
            item_id: _Optional[int] = None,
            name: _Optional[str] = None,
            slot: _Optional[_Union[str, tuple[str, str]]] = None,
            weight: _Optional[tuple[float, str]] = None,
            material: _Optional[str] = None,
            mundane: _Optional[bool] = None,
            description: _Optional[str] = None,
            quality: _Optional[str] = None,
            value: _Optional[tuple[int, str]] = None,
            binding: _Optional[str] = None,
            relic: _Optional[bool] = None,
            armor_class: _Optional[_Union[_Die, int]] = None,
            set_name: _Optional[str] = None,
            *args, **kwargs
    ):
        super(_Armor, self).__init__(
            item_id=item_id,
            name=name,
            category='ARMOR',
            slot=slot,
            weight=weight,
            material=material,
            consumable=False,
            mundane=mundane,
            description=description,
            quality=quality,
            value=value,
            binding=binding,
            quest_item=False,
            relic=relic,
            *args, **kwargs
        )
        self.armor_class = armor_class
        self.set_name = set_name

    def __repr__(self):
        return f'{super(_Armor, self).__repr__()}[ac {self.armor_class}]'

    def _equip(self):
        self._dispatch_event('on_equip', self)

    def _unequip(self):
        self._dispatch_event('on_unequip', self)


class ArmorByClass(_Armor):
    def __init__(self):
        armor_name = re.sub(r'([a-z])([A-Z])',r'\1 \2', self.__class__.__name__)
        super(ArmorByClass, self).__init__(**_ARMOR_DICT[armor_name])


class ArmorFactory:
    @staticmethod
    def create_armor(armor_name):
        _armor_class = type(armor_name.replace(" ", ""), (ArmorByClass, ), {})
        return None if _armor_class is None else _armor_class
