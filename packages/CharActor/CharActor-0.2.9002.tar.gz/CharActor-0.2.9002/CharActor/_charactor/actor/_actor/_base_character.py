from ...._entity import _base_entity
from ._base_class_actors import *
from ._base_race_actors import *

_base_characters = {}
_char_list = []

for race in RACE_ATTRIBUTES.keys():
    _base_characters[race.replace('-','')] = {}
    for role in ROLE_ATTRIBUTES.keys():
        _base_characters[race.replace('-','')][role] = type(f'{race.replace("-","")}{role}', (BaseCharacter, ), {})


globals().update(_base_characters)

for k, v in _base_characters.items():
    _char_list.extend(f'{k}{K}' for K in v.keys())

for race in RACE_ATTRIBUTES:
    race = race.replace('-', '')
    for role in ROLE_ATTRIBUTES:
        setattr(_base_entity, f'{race}{role}', _base_characters[race][role])

