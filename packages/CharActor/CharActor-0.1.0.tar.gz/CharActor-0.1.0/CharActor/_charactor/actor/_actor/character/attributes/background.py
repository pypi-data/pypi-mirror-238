from abc import ABC as _ABC
from typing import Optional as _Optional
import json as _json


def _load_json(path):
    with open(path, 'r') as f:
        return _json.load(f)

BACKGROUNDS = _load_json('CharActor/_charactor/dicts/backgrounds.json')


class AbstractBackground(_ABC):
    _name = None
    _title = None
    _description = None
    _skills = None
    _tools = None
    _languages = None
    _equipment = None
    _special = None
    
    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, name: _Optional[str] = None) -> None:
        self._name = name
        
    @property
    def title(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description
    
    @description.setter
    def description(self, description: _Optional[str] = None) -> None:
        self._description = description
        
    @property
    def skills(self) -> list:
        return self._skills
    
    @skills.setter
    def skills(self, skills: _Optional[list] = None) -> None:
        self._skills = skills
        
    @property
    def tools(self) -> list:
        return self._tools
    
    @tools.setter
    def tools(self, tools: _Optional[list] = None) -> None:
        self._tools = tools
        
    @property
    def languages(self) -> list:
        return self._languages
    
    @languages.setter
    def languages(self, languages: _Optional[list] = None) -> None:
        self._languages = languages
        
    @property
    def equipment(self) -> list:
        return self._equipment
    
    @equipment.setter
    def equipment(self, equipment: _Optional[list] = None) -> None:
        self._equipment = equipment
        
    @property
    def special(self) -> list:
        return self._special
    
    @special.setter
    def special(self, special: _Optional[list] = None) -> None:
        self._special = special
        
    def __repr__(self) -> str:
        return f'{self.name.replace("_", " ").title()}'


class Background(AbstractBackground):
    def __init__(self, name: str) -> None:
        attrs = BACKGROUNDS[name]
        self.name = name
        self.description = attrs['description']
        self.skills = attrs['skills']
        self.tools = attrs['tools']
        self.languages = attrs['languages']
        self.equipment = attrs['equipment']
        self.special = attrs['special']


class BackgroundFactory:
    @staticmethod
    def create_background(name: str) -> type(Background):
        attrs = BACKGROUNDS[name]
        if attrs is not None:
            return type(name, (Background, ), {})


BACKGROUND_INSTANCES = {name: BackgroundFactory.create_background(name) for name in BACKGROUNDS}
