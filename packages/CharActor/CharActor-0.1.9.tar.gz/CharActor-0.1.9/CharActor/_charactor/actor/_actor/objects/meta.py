from begingine.components.map.grid_object import GridObject
from ._items import Item, Weapon, Armor

class GridItemMeta(type):
    def __new__(cls, name, bases, attrs):
        new_class = super().__new__(cls, name, bases, attrs)
        if issubclass(bases[1], Item):
            new_class._object_type = "item"
        return new_class
    
    def __call__(self, *args, **kwargs):
        obj = super().__call__(*args, **kwargs)
        if kwargs.get('grid', None) and kwargs.get('cell', None):
            cell = kwargs['grid'].get_cell_by_name(kwargs['cell'])
            cell.add_object(obj)
        return obj
            