import re
import pymunk
import json as _json
from pyglet.event import EventDispatcher as _EventDispatcher
from typing import Optional as _Optional, Union as _Union

from CharActor._charactor.dicts import load_dict

def _load_json(path):
    with open(path, 'r') as f:
        return _json.load(f)

_WEIGHTS = ['mg', 'g', 'kg']

_CURRENCY = ['cp', 'sp', 'gp', 'pp']

_ITEM_EVENTS = ['on_pickup', 'on_drop', 'on_equip', 'on_unequip', 'on_use', 'on_destroy', 'on_sell', 'on_buy',
                'on_trade', 'on_identify',
                'on_consume', 'on_eat', 'on_drink', 'on_read', 'on_wear', 'on_wield', 'on_hold', 'on_throw', 'on_shoot',
                'on_cast', 'on_activate',
                'on_repair', 'on_recharge']

_ITEM_CATEGORIES = ['FOOD', 'CLOTHING', 'TOYS', 'TOOLS', 'EQUIPMENT', 'WEAPONS', 'ARMOR', 'JEWELRY', 'GEMS', 'ORE',
                    'MATERIALS', 'POTIONS', 'SCROLLS', 'BOOKS', 'RELICS', 'MISC']

_ITEM_SLOT = ['HEAD', 'NECK', 'LEFT_SHOULDER', 'RIGHT_SHOULDER', 'CHEST', 'BACK', 'LEFT_WRIST', 'RIGHT_WRIST',
              'LEFT_HAND', 'RIGHT_HAND', 'WAIST', 'LEGS', 'FEET', 'FINGER_A', 'FINGER_B', 'TRINKET_A', 'TRINKET_B',
              'MAIN_HAND', 'OFF_HAND', 'RANGED', 'AMMO', 'MOUNT', 'TOY', 'CLOAK', 'BAG', 'TABARD', 'ROBE', 'QUIVER',
              'RELIC', 'SHIELD', 'HOLDABLE', 'THROWN', 'SHIRT', 'TROUSERS']

_MATERIAL_TYPES = ['WOOD', 'LEATHER', 'CLOTH', 'BURLAP', 'IRON', 'BRONZE', 'STEEL', 'SILVER', 'GOLD', 'STONE', 'GLASS',
                   'FUR', 'SILK', 'BONE', 'SHELL', 'CERAMIC', 'PAPER', 'FABRIC', 'ORGANIC', 'MISC']

_QUALITY_TYPES = ['COMMON', 'UNCOMMON', 'RARE', 'EPIC', 'LEGENDARY', 'ARTIFACT', 'MYTHIC']

_BINDINGS = ['BOUND', 'UNBOUND']

_GENERAL_ITEMS_DICT = load_dict('general_items')

_TRADE_ITEMS_DICT = load_dict('trade_items')


class AbstractItem:
    _item_id = None 
    _name = None
    _category = None
    _slot = None
    _weight = None
    _material = None
    _consumable = None
    _mundane = None
    _description = None
    _quality = None
    _value = None
    _binding = None
    _quest_item = None
    _relic = None
    _stackable = None
    def __init__(self):
        super(AbstractItem, self).__init__()
        self._grid = None
        self._cell = None
        self._identified = None
        self._equipped = None
        self._owner = None

    @property
    def item_id(self) -> int:
        return self._item_id
    
    @item_id.setter
    def item_id(self, item_id: int) -> None:
        self._item_id = item_id

    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, name: str) -> None:
        self._name = name

    @property
    def category(self) -> str:
        return self._category
    
    @category.setter
    def category(self, category: str) -> None:
        self._category = category

    @property
    def slot(self) -> _Union[str, tuple[str, str], list[str, str]]:
        return self._slot
    
    @slot.setter
    def slot(self, slot: _Union[str, tuple[str, str], list[str, str]]) -> None:
        self._slot = slot

    @property
    def weight(self) -> _Union[list[float, str], tuple[float, str]]:
        return self._weight
    
    @weight.setter
    def weight(self, weight: _Union[list[float, str], tuple[float, str]]) -> None:
        self._weight = weight
        
    @property
    def material(self) -> str:
        return self._material
    
    @material.setter
    def material(self, material: str) -> None:
        self._material = material

    @property
    def consumable(self) -> bool:
        return self._consumable
    
    @consumable.setter
    def consumable(self, consumable: bool) -> None:
        self._consumable = consumable

    @property
    def mundane(self) -> bool:
        return self._mundane
    
    @mundane.setter
    def mundane(self, mundane: bool) -> None:
        self._mundane = mundane

    @property
    def description(self) -> str:
        return self._description
    
    @description.setter
    def description(self, description: str) -> None:
        self._description = description

    @property
    def quality(self) -> str:
        return self._quality
    
    @quality.setter
    def quality(self, quality: str) -> None:
        self._quality = quality

    @property
    def value(self) -> _Union[list[int, str], tuple[int, str]]:
        return self._value
    
    @value.setter
    def value(self, value: _Union[list[int, str], tuple[int, str]]) -> None:
        self._value = value

    @property
    def binding(self) -> str:
        return self._binding
    
    @binding.setter
    def binding(self, binding: str) -> None:
        self._binding = binding

    @property
    def quest_item(self) -> bool:
        return self._quest_item
    
    @quest_item.setter
    def quest_item(self, quest_item: bool) -> None:
        self._quest_item = quest_item

    @property
    def relic(self) -> bool:
        return self._relic
    
    @relic.setter
    def relic(self, relic: bool) -> None:
        self._relic = relic

    @property
    def stackable(self) -> bool:
        return self._stackable
    
    @stackable.setter
    def stackable(self, stackable: bool) -> None:
        self._stackable = stackable

    @property
    def identified(self) -> bool:
        return self._identified
    
    @identified.setter
    def identified(self, identified: bool) -> None:
        self._identified = identified

    @property
    def equipped(self) -> bool:
        return self._equipped
    
    @equipped.setter
    def equipped(self, equipped: bool) -> None:
        self._equipped = equipped

    @property
    def owner(self) -> _Optional[object]:
        return self._owner
    
    @owner.setter
    def owner(self, owner: _Optional[object]) -> None:
        self._owner = owner

    @property
    def grid(self):
        return self._grid

    @property
    def cell(self):
        return self._cell
    
    @property
    def position(self):
        return pymunk.Vec2d(*self.cell.coordinates)

    def _dispatch_event(self, event: str, *args, **kwargs):
        self.dispatcher.dispatch_event(event, *args, **kwargs)

    def _pickup(self, owner):
        self.owner = owner
        self._dispatch_event('on_pickup', self)

    def _drop(self):
        self._dispatch_event('on_drop', self)

    def _use(self):
        self._dispatch_event('on_use', self)

    def _destroy(self):
        self._dispatch_event('on_destroy', self)

    def _sell(self):
        self._dispatch_event('on_sell', self)

    def _buy(self):
        self._dispatch_event('on_buy', self)

    def _trade(self):
        self._dispatch_event('on_trade', self)

    def _identify(self):
        self._dispatch_event('on_identify', self)

    def _consume(self):
        self._dispatch_event('on_consume', self)

    def _spawn(self, grid, cell = None):
        self._grid = grid
        cell = cell if cell is not None else grid.random_cell()
        while not cell.passable:
            cell = grid.random_cell()
        self._cell = cell

class _Item(AbstractItem):
    dispatcher = _EventDispatcher()
    for event in _ITEM_EVENTS:
        dispatcher.register_event_type(event)
    
    def __repr__(self):
        return self.name
    
    def __init__(
            self,
            item_id: _Optional[int] = None,
            name: _Optional[str] = None,
            category: _Optional[str] = None,
            slot: _Optional[_Union[str, tuple[str, str]]] = None,
            weight: _Optional[tuple[float, str]] = None,
            material: _Optional[str] = None,
            consumable: _Optional[bool] = None,
            mundane: _Optional[bool] = None,
            description: _Optional[str] = None,
            quality: _Optional[str] = None,
            value: _Optional[tuple[int, str]] = None,
            binding: _Optional[str] = None,
            quest_item: _Optional[bool] = None,
            relic: _Optional[bool] = None,
            stackable: _Optional[bool] = None,
            *args, **kwargs
    ):
        super(_Item, self).__init__()
        self.item_id = item_id
        self.name = name
        self.category = category if category in _ITEM_CATEGORIES else None
        self.slot = slot if isinstance(slot, tuple) and slot[0] in _ITEM_SLOT and slot[1] in _ITEM_SLOT or \
            isinstance(slot, str) and slot in _ITEM_SLOT or isinstance(slot, list) and slot[0] in _ITEM_SLOT and slot[1] in _ITEM_SLOT else None
        self.weight = weight if isinstance(weight[0], (float, int)) and weight[1] in _WEIGHTS else None
        self.material = material if material in _MATERIAL_TYPES else None
        self.consumable = consumable if consumable is not None else False
        self.mundane = mundane if mundane is not None else True
        self.description = description if description is not None else ""
        self.quality = quality if quality in _QUALITY_TYPES else None
        self.value = value if isinstance(value[0], int) and value[1] in _CURRENCY else None
        self.binding = binding if binding in _BINDINGS else None
        self.quest_item = quest_item if quest_item is not None else False
        self.relic = relic
        self.stackable = stackable if stackable is not None else False
        self.identified = False
        self.equipped = False
        self.owner = None

    def __repr__(self):
        return self.name

    def identify(self):
        if self.identified:
            return
        self.identified = True
        self._dispatch_event('on_identify', self)

class GeneralItemByClass(_Item):
    def __init__(self):
        item_name = re.sub(r'([a-z])([A-Z])', r'\1 \2', self.__class__.__name__)
        super(GeneralItemByClass, self).__init__(**_GENERAL_ITEMS_DICT[item_name])

class TradeItemByClass(_Item):
    def __init__(self):
        item_name = re.sub(r'([a-z])([A-Z])', r'\1 \2', self.__class__.__name__)
        super(TradeItemByClass, self).__init__(**_TRADE_ITEMS_DICT[item_name])


class _ItemStack:
    def __init__(self, item: _Item, quantity: int):
        self.name = item.name
        self.item = item
        self.quantity = quantity
        self.weight = [item.weight[0] * quantity, item.weight[1]]

    def __repr__(self):
        return f"{self.item} x{self.quantity}"
    
    def update_weight(self):
        self.weight = [self.item.weight[0] * self.quantity, self.item.weight[1]]
        

    def add(self, quantity: int):
        self.quantity += quantity
        self.update_weight()

    def remove(self, quantity: int):
        self.quantity -= quantity
        self.update_weight()

        
class _ItemFactory:
    @staticmethod
    def create_general_item(item_name: str) -> _Item:
        item_class = type(item_name.replace(' ', '').replace("'", ''), (GeneralItemByClass,), {})
        return None if item_class is None else item_class

    @staticmethod
    def create_trade_item(item_name: str) -> _Item:
        item_class = type(item_name.replace(' ', '').replace("'", ''), (TradeItemByClass,), {})
        return None if item_class is None else item_class
