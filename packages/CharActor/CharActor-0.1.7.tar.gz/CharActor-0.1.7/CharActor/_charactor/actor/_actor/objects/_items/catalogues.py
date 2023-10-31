from typing import Optional as _Optional, Union as _Union, List as _List
from .item import _ItemFactory, _GENERAL_ITEMS_DICT, _TRADE_ITEMS_DICT
from ._weapon import _WeaponFactory, _WEAPONS_DICT
from ._clothing import _ClothingFactory, _CLOTHING_DICT
from ._armor import ArmorFactory, _ARMOR_DICT
from pyglet.event import EventDispatcher
from CharActor._grid_object import GridItem

MANIFESTS = ['weapons', 'clothing', 'armor', 'general', 'trade']
DICTS = [_WEAPONS_DICT, _CLOTHING_DICT, _ARMOR_DICT, _GENERAL_ITEMS_DICT, _TRADE_ITEMS_DICT]

class QuietDict:
    def __init__(self, manifest_names: _Optional[_Union[list[str, ], str]], *args, **kwargs):
        self.items = {}
        self._manidict1 = None
        self._manidict2 = None
        self._manidict3 = None
        if isinstance(manifest_names, list):
            for i in range(len(manifest_names)):
                name = manifest_names[i]
                setattr(self, f'{name}_manifest', [])
                setattr(self, f'_manidict{i}', DICTS[MANIFESTS.index(name)])
        else:
            setattr(self, f'{manifest_names}_manifest', [])

    def __getitem__(self, key):
        key = key.replace(" ", "")
        return self.items[key]()
    
    def __setitem__(self, key, value):
        self.items[key] = value

    def __delitem__(self, key):
        del self.items[key]

    def __iter__(self):
        return iter(self.items)
    
    def __contains__(self, key):
        return key in self.items
    
    def __repr__(self):
        return repr(self.items)
    
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


class _Armory(QuietDict):
    def __init__(self):
        super(_Armory, self).__init__(['armor', 'weapons'])
        self.weapons_manifest = []
        self.armor_manifest = []
        self._weapon_classes = {}
        self._armor_classes = {}
        self._grid_instances = {}
        self._create_armor_classes()
        self._create_weapon_classes()


    def _create_armor(self, armor_name: str):
        _armor_class = ArmorFactory.create_armor(armor_name)
        if _armor_class is not None:
            return _armor_class

    def _create_armor_classes(self):
        for _armor_name, _armor_attr in _ARMOR_DICT.items():
            _armor_class = self._create_armor(_armor_name)
            if _armor_class is not None:
                setattr(_armor_class, '_entry', _armor_attr)
                self._armor_classes[_armor_name.replace(" ", "").replace(",", "_").replace("-","")] = _armor_class
                setattr(self, _armor_name.replace(" ", "").replace(",", "_").replace("-","").lower(), _armor_class)
                self.armor_manifest.append(_ARMOR_DICT[_armor_name]['name'])
        self.update(self._armor_classes)

    def _create_weapon(self, weapon_name: str):
        _weapon_class = _WeaponFactory.create_weapon(weapon_name)
        if _weapon_class is not None:
            return _weapon_class
        
    def _create_weapon_classes(self):
        for _weapon_name, _weapon_attr in _WEAPONS_DICT.items():
            _weapon_class = self._create_weapon(_weapon_name)
            if _weapon_class is not None:
                setattr(_weapon_class, '_entry', _weapon_attr)
                # _weapon_instance = _weapon_class(**_WEAPONS_DICT[_weapon_name])
                # _weapon_instances[_weapon_instance.name] = _weapon_instance
                self._weapon_classes[_weapon_name.replace(" ", "").replace(",", "_").replace("-","")] = _weapon_class
                setattr(self, _weapon_name.replace(" ", "").replace(",", "_").replace("-","").lower(), _weapon_class)
                self.weapons_manifest.append(_WEAPONS_DICT[_weapon_name]['name'])
        self.update(self._weapon_classes)

    def _get_class(self, item_name: str):
        if item_name in self.items:
            return self.items[item_name]
            
    def _combine(self, item_name, item_class):
        return type(item_name.replace(" ", "").replace(",", "_").replace("-",""), (GridItem, item_class), {'dispatcher': EventDispatcher()})
        
    def get(self, item_name: str, grid: object = None, cell: object = None):
        item_name = item_name.title()
        if grid or cell:
            item = self._create_griditem(item_name, grid, cell)
            setattr(item, 'tile_color', (255, 0, 0, 255))
            cell=grid[cell]
            cell.add_object(item)
            return item
        item_class = self._get_class(item_name)
        return item_class()

    # TODO Rename this here and in `get`
    def _create_griditem(self, item_name, grid, cell):
        item_class = self._get_class(item_name)
        combined_class = self._combine(item_name, item_class)
        cell = grid[cell] if cell is not None else cell
        griditem_instance = combined_class(grid, item_name, cell)
        if self._grid_instances.get(item_name, None) is not None:
            item_count = 1 + sum(bool(key.startswith(item_name))
                             for key in list(self._grid_instances.keys()))
            self._grid_instances[f'{item_name}{item_count}'] = griditem_instance
        else:
            self._grid_instances[item_name] = griditem_instance
        return griditem_instance

class _Goods(QuietDict):
    def __init__(self):
        super(_Goods, self).__init__(['general', 'trade'])
        self._goods_classes = {}
        self._grid_instances = {}
        self.general_manifest = []
        self.trade_manifest = []
        self._create_item_classes()
        

    def _create_item(self, item_name: str):
        if item_name in list(_GENERAL_ITEMS_DICT.keys()):
            _item_class = _ItemFactory.create_general_item(item_name)
        elif item_name in list(_TRADE_ITEMS_DICT.keys()):
            _item_class = _ItemFactory.create_trade_item(item_name)
        return _item_class

    def _get_class(self, item_name: str):
       if item_name in self.items and (
                        item_name in self.general_manifest
                        or item_name in self.trade_manifest
                    ):
            return self.items[item_name]

    def _combine(self, item_name, item_class):
        return type(item_name.replace(" ", "").replace(",", "_").replace("-",""), (GridItem, item_class), {'dispatcher': EventDispatcher()})
        
    def _create_item_classes(self):
        for _item_name, _item_attr in _GENERAL_ITEMS_DICT.items():
            _item_class = self._create_item(_item_name)
            if _item_class is not None:
                setattr(_item_class, '_entry', _item_attr)
                # _item_instance = _item_class(**_GENERAL_ITEMS_DICT[_item_name])
                # _goods_instances[_item_instance.name] = _item_instance
                self._goods_classes[_item_name.replace(" ", "").replace(",", "_").replace("-","")] = _item_class
                setattr(self, _item_name.replace(" ", "").replace(",", "_").replace("-","").replace("'",'').lower(), _item_class)
                self.general_manifest.append(_item_name)
        for _item_name, _item_attr in _TRADE_ITEMS_DICT.items():
            _item_class = self._create_item(_item_name)
            if _item_class is not None:
                setattr(_item_class, '_entry', _item_attr)
                # _item_instance = _item_class(**_TRADE_ITEMS_DICT[_item_name])
                # _goods_instances[_item_instance.name] = _item_instance
                self._goods_classes[_item_name.replace(" ", "").replace(",", "_").replace("-","")] = _item_class
                setattr(self, _item_name.replace(" ", "").replace(",", "_").replace("-","").replace("'",'').lower(), _item_class)
                self.trade_manifest.append(_item_name)
        self.update(self._goods_classes)

    def get(self, item_name: str, grid: object = None, cell: object = None):
        item_name = item_name.title()
        if grid or cell:
            item = self._create_griditem(item_name, grid, cell)
            setattr(item, 'tile_color', (0, 255, 255, 255))
            cell = grid[cell]
            cell.add_object(item)
            return item
        item_class = self._get_class(item_name)
        return item_class()

    # TODO Rename this here and in `get`
    def _create_griditem(self, item_name, grid, cell):
        item_class = self._get_class(item_name)
        combined_class = self._combine(item_name, item_class)
        cell = grid[cell] if cell is not None else cell
        griditem_instance = combined_class(grid, item_name, cell)
        if self._grid_instances.get(item_name, None) is not None:
            item_count = 1 + sum(bool(key.startswith(item_name))
                             for key in list(self._grid_instances.keys()))
            self._grid_instances[f'{item_name}{item_count}'] = griditem_instance
        else:
            self._grid_instances[item_name] = griditem_instance
        return griditem_instance

        

Armory = _Armory()
# _weapon_classes = {}

# for _weapon_name, _weapon_attr in _WEAPONS_DICT.items():
#     _weapon_class = _WeaponFactory.create_weapon(_weapon_name)
#     if _weapon_class is not None:
#         # _weapon_instance = _weapon_class(**_WEAPONS_DICT[_weapon_name])
#         # _weapon_instances[_weapon_instance.name] = _weapon_instance
#         _weapon_classes[_weapon_name.replace(" ", "").replace(",", "_").replace("-","")] = _weapon_class
#         setattr(Armory, _weapon_name.replace(" ", "").replace(",", "_").replace("-","").lower(), _weapon_class)
#         Armory.weapons_manifest.append(_WEAPONS_DICT[_weapon_name]['name'])
# Armory.update(_weapon_classes)

# _armor_classes = {}
# for _armor_name, _armor_attr in _ARMOR_DICT.items():
#     _armor_class = ArmorFactory.create_armor(_armor_name)
#     if _armor_class is not None:
#         # _armor_instance = _armor_class(**_ARMOR_DICT[_armor_name])
#         # _armor_instances[_armor_instance.name] = _armor_instance
#         _armor_classes[_armor_name.replace(" ", "").replace(",", "_").replace("-","")] = _armor_class
#         setattr(Armory, _armor_name.replace(" ", "").replace(",", "_").replace("-","").lower(), _armor_class)
#         Armory.armor_manifest.append(_armor_name)
# Armory.update(_armor_classes)

Goods = _Goods()

# _goods_classes = {}

# for _item_name, _item_attr in _GENERAL_ITEMS_DICT.items():
#     _item_class = _ItemFactory.create_general_item(_item_name)
#     if _item_class is not None:
#         # _item_instance = _item_class(**_GENERAL_ITEMS_DICT[_item_name])
#         # _goods_instances[_item_instance.name] = _item_instance
#         _goods_classes[_item_name.replace(" ", "").replace(",", "_").replace("-","")] = _item_class
#         setattr(Goods, _item_name.replace(" ", "").replace(",", "_").replace("-","").replace("'",'').lower(), _item_class)
#         Goods.general_manifest.append(_item_name)
# for _item_name, _item_attr in _TRADE_ITEMS_DICT.items():
#     _item_class = _ItemFactory.create_trade_item(_item_name)
#     if _item_class is not None:
#         # _item_instance = _item_class(**_TRADE_ITEMS_DICT[_item_name])
#         # _goods_instances[_item_instance.name] = _item_instance
#         _goods_classes[_item_name.replace(" ", "").replace(",", "_").replace("-","")] = _item_class
#         setattr(Goods, _item_name.replace(" ", "").replace(",", "_").replace("-","").replace("'",'').lower(), _item_class)
#         Goods.trade_manifest.append(_item_name)
# Goods.update(_goods_classes)