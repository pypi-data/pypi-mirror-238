from typing import Optional as _Optional
import json as _json
from CharActor._charactor.dicts import load_dict

def _load_json(path):
    with open(path, 'r') as f:
        return _json.load(f)

BACKGROUNDS = load_dict('backgrounds')

BACKGROUND_INSTANCES = {}


class AbstractBackground:
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

class BaseBackground(AbstractBackground):
    def __init__(
        self, 
        name: str = None,
        description: str = None,
        skills: list = None,
        tools: list = None,
        languages: list = None,
        equipment: list = None,
        special: str = None
    ) -> None:
        self.name = name
        self.description = description
        self.skills = skills
        self.tools = tools
        self.languages = languages
        self.equipment = equipment
        self.special = special
        
class Background(BaseBackground):
    def __init__(self) -> None:
        name = self.__class__.__name__
        attrs = BACKGROUNDS[name]
        super(Background, self).__init__(
            attrs['name'],
            attrs['description'],
            attrs['skills'],
            attrs['tools'],
            attrs['languages'],
            attrs['equipment'],
            attrs['special']
        )

class BackgroundFactory:
    background_instances = {}
    @staticmethod
    def create_background(name: str) -> type(Background):
        attrs = BACKGROUNDS[name]
        if attrs is not None:
            background_class = type(name, (Background, ), {})
            background_instance = background_class()
            BackgroundFactory.background_instances[name] = background_instance
            globals().update(BackgroundFactory.background_instances)
            return background_instance
        
    @staticmethod
    def create_backgrounds() -> dict:
        return [BackgroundFactory.create_background(name) for name in BACKGROUNDS]
    
BackgroundFactory.create_backgrounds()


