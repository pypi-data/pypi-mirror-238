from abc import ABC as _ABC
from typing import Optional as _Optional

from begingine.utility.saved_objects import save_json as _save_json, load_json as _load_json

KIND_ATTRIBUTES = _load_json('begingine/dicts/kinds.json')

class AbstractMonster(_ABC):
    def __init__(self):
        super(AbstractMonster, self).__init__()
        self._name = None
        self._type = None
        self._size = None
        self._alignment = None
        self._armor_class = None
        self._hit_points = None
        self._speed = None
        self._abilities = None
        self._skills = None
        self._senses = None
        self._languages = None
        self._challenge_rating = None
        self._special_abilities = None
        self._actions = None

    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, name: _Optional[str] = None) -> None:
        self._name = name

    @property
    def type(self) -> str:
        return self._type
    
    @type.setter
    def type(self, type: _Optional[str] = None) -> None:
        self._type = type

    @property
    def size(self) -> str:
        return self._size
    
    @property
    def alignment(self) -> str:
        return self._alignment
