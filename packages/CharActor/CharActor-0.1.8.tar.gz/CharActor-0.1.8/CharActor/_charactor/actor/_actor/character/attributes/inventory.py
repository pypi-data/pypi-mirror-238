from pyglet.event import EventDispatcher as _EventDispatcher
from abc import ABC as _ABC
from typing import Optional as _Optional
from ...objects import ItemStack, Armory, Goods

EQUIPMENT_SLOTS = {
    'HEAD': None,
    'NECK': None,
    'LEFT_SHOULDER': None,
    'RIGHT_SHOULDER': None,
    'CHEST': None,
    'BACK': None,
    'LEFT_WRIST': None,
    'RIGHT_WRIST': None,
    'LEFT_HAND': None,
    'RIGHT_HAND': None,
    'WAIST': None,
    'LEGS': None,
    'FEET': None,
    'FINGER_A': None,
    'FINGER_B': None,
    'TRINKET_A': None,
    'TRINKET_B': None,
    'MAIN_HAND': None,
    'OFF_HAND': None,
    'RANGED': None,
    'AMMO': None,
    'MOUNT': None,
    'TOY': None,
    'CLOAK': None,
    'BAG': None,
    'TABARD': None,
    'ROBE': None,
    'QUIVER': None,
    'RELIC': None,
    'SHIELD': None,
    'HOLDABLE': None,
    'THROWN': None,
    'SHIRT': None,
    'TROUSERS': None
}



class Equipment:
    def __init__(self, _parent):
        self._parent = _parent
        self._slots = EQUIPMENT_SLOTS.copy()
        # self.register_event_type('on_equip_item')
        # self.register_event_type('on_unequip_item')

    def __repr__(self):
        return repr({list(self._slots.keys())[i]: list(self._slots.values())[i] for i in range(len(self._slots)) if
                     list(self._slots.values())[i] is not None})

    def __getitem__(self, key):
        return self._slots[key]

    def __setitem__(self, key, value):
        self._slots[key] = value

    def __delitem__(self, key):
        del self._slots[key]

    def __iter__(self):
        return iter(self._slots)

    def __contains__(self, key):
        return key in self._slots
    
    def __getstate__(self):
        return self._slots

    def update(self, other=None, **kwargs):
        if other:
            if hasattr(other, "keys"):
                for key in other.keys():
                    self[key] = other[key]
            else:
                for key, value in other:
                    self[key] = value
        for key, value in kwargs.items():
            self[key] = value

    def equip_item(self, item):
        if isinstance(item.slot, list):
            for slot in item.slot:
                if slot in self._slots:
                    if self._slots[slot] is not None:
                        continue
                    self._slots[slot] = item
                    # self.dispatch_event('on_equip_item', item)
        elif item.slot in self._slots:
            self._slots[item.slot] = item
                # self.dispatch_event('on_unequip_item', item)

            # self.dispatch_event('on_equip_item', item)

    def unequip_item(self, item):
        if item.slot in self._slots and self._slots[item.slot] is not None:
            self._slots[item.slot] = None
            # self._dispatch_event('on_unequip_item', item)

    def get_equipped_item(self, slot):
        if slot in self._slots:
            return self._slots[slot]

class InventoryMeta(type):
    _dispatcher = _EventDispatcher()

    def __new__(cls, name, bases, attrs):
        attrs['_dispatcher'] = cls._dispatcher
        return super().__new__(cls, name, bases, attrs)

class Inventory:
    # InventoryMeta._dispatcher.register_event_type('on_add_item')
    # InventoryMeta._dispatcher.register_event_type('on_remove_item')
    # InventoryMeta._dispatcher.register_event_type('on_equip_item')
    # InventoryMeta._dispatcher.register_event_type('on_unequip_item')

    def __init__(self, parent):
        self._parent = parent
        self.carry_limit = self.calc_carry_limit()
        self.carry_weight = 0
        self.items = []
        self._full_contains = None
        self.equipment = Equipment(self._parent)

    def __repr__(self):
        return repr(self.items)

    def __iter__(self):
        return iter([item.name for item in self.items])
    
    def __contains__(self, item_name):
        if item_name is not None:
            iterable = iter(self)
            return item_name in iterable
        
    def __getitem__(self, item_name):
        if item_name is not None:
            for item in self.items:
                if item.name == item_name:
                    return item
    
    def __getstate__(self):
        state = self.__dict__.copy()
        for item in state['items']:
            state['items'][state['items'].index(item)] = item.name
        state['equipment'] = self.equipment.__getstate__()
        return state

    def calc_carry_limit(self):
        return self._parent.Strength.score * 10

    def calc_carry_weight(self):
        kilos = sum(item.weight[0] for item in self.items if item.weight[1] == 'kg')
        grams = sum(item.weight[0] for item in self.items if item.weight[1] == 'g')
        if grams > 999:
            kilos += grams // 1000
            grams = grams % 1000
        return kilos + (grams / 1000)

    def pick_up(self, item):
        if self.calc_carry_weight() + item.weight[0] > self.carry_limit:
            return False
        if item.stackable and item.name in self:
            for i in self.items:
                if i.name == item.name and isinstance(i, ItemStack):
                    i.add(1)
                elif not isinstance(i, ItemStack):
                    self.items.remove(i)
                    item = ItemStack(item, 2)
            return self.update_carry_weight(item)
        self.acquire_possession(item)

    def add_item(self, item_name, quantity=1):
        item_name = item_name.replace(" ", "")
        if quantity > 1:
            for _ in range(quantity):
                self.add_item(item_name)
            return
        if item_name in Goods:
            item = Goods[item_name]
        elif item_name in Armory:
            item = Armory[item_name]
        else:
            raise KeyError(f'Item {item_name} not found in Goods or Armory')
        if self.calc_carry_weight() + item.weight[0] > self.carry_limit:
            return False
        if item.stackable and item.name in self:
            for i in self.items:
                if i.name == item.name and isinstance(i, ItemStack):
                    i.add(1)
                    self.calc_carry_weight()
                    return
        elif item.stackable:
            item = ItemStack(item, 1)
        self.acquire_possession(item)

    # TODO Rename this here and in `pick_up` and `add_item`
    def update_carry_weight(self, item):
        self.carry_weight = self.calc_carry_weight()
        self._dispatcher.dispatch_event('on_add_item', item)
        return

    # TODO Rename this here and in `pick_up` and `add_item`
    def acquire_possession(self, item):
        self.items.append(item)
        if hasattr(item, 'on_pick_up'):
            item.on_pick_up(self._parent)
        item.owner = self._parent
        self.carry_weight = self.calc_carry_weight()
        # self._dispatcher.dispatch_event('on_add_item', item)        

    def remove_item(self, item_name: str = None):
        if item_name not in self:
            return
        for item in self.items:
            if item.name == item_name:
                if isinstance(item, ItemStack):
                    if item.quantity > 1:
                        item.remove(1)
                    else:
                        self.items.remove(item)
                elif isinstance(item.slot, list):
                    for slot in item.slot:
                        if self.equipment[slot] == item:
                            self.equipment.unequip_item(item)
                self.carry_weight = self.calc_carry_weight()
                # self._dispatcher.dispatch_event('on_remove_item', item)
                return item
            
    def drop_item(self, item_name: str = None):
        self.remove_item(item_name)
        if hasattr(self, 'on_drop'):
            self.on_drop() 


    def equip_item(self, item):
        if not item.identified:
            item.identify()
        self.equipment.equip_item(item)
        item.equipped = True
        # self._dispatcher.dispatch_event('on_equip_item', item)

    def unequip_item(self, item):
        self.equipment[item.slot] = None
        item.equipped = False
        # self._dispatcher.dispatch_event('on_unequip_item', item)
