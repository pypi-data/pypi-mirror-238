from .base_actor import BaseActor
from .character import task_list, ALIGNMENTS as _ALIGNMENTS, BACKGROUNDS as _BACKGROUNDS
from .objects import Armory, Goods, Weapon, Armor, Item, _Armory, _Goods
from . import _base_race_actors as build_actor_by_race
from . import _base_class_actors as build_actor_by_class
from . import _base_character as _character_list

_base_characters = _character_list._base_characters

#     from .base_class_actors import BaseBarbarian, BaseBard, BaseCleric, BaseDruid, BaseFighter, BaseMonk, BasePaladin, BaseRanger, BaseRogue, BaseSorcerer, BaseWarlock, BaseWizard
