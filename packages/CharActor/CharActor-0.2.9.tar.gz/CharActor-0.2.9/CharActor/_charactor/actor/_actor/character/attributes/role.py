import json as _json
from typing import Union as _Union
from .ability import _ABC, SPECIAL_ABILITIES as _SPECIAL_ABILITIES, \
    SpecialAbilityFactory as _SpecialAbilityFactory
    
from dicepy import Die as _Die

from CharActor._charactor.dicts import load_dict

Die = _Die.Die

def _load_json(path):
    with open(path, 'r') as f:
        return _json.load(f)
    
ROLE_ATTRIBUTES = load_dict('role_attributes')

role_instances = {}


class AbstractRole:
    def __new__(cls, *args, **kwargs):
        if kwargs.get('title', None) is not None:
            title = kwargs.get('title').capitalize()
        elif isinstance(args[0], str):
            title = args[0].capitalize()
        attributes = ROLE_ATTRIBUTES[title]
        if attributes is not None:
            for attr in attributes:
                setattr(cls, f'_{attr}', attributes[attr])
            return super().__new__(cls)
    
    @property
    def title(self):
        return self._title
    
    @title.setter
    def title(self, value):
        self._title = value
    
    @property
    def class_description(self):
        return self._class_description
    
    @class_description.setter
    def class_description(self, value):
        self._class_description = value
    
    @property
    def hit_die(self):
        if isinstance(self._hit_die, Die):
            return self._hit_die
        elif isinstance(self._hit_die, str):
            return Die(int(self._hit_die.removeprefix('d')))
        
    @hit_die.setter
    def hit_die(self, value):
        self._hit_die = value
        
    @property
    def skill_points(self):
        return self._skill_points
    
    @skill_points.setter
    def skill_points(self, value):
        self._skill_points = value

    @property
    def proficiencies(self):
        return self._proficiencies
    
    @proficiencies.setter
    def proficiencies(self, value):
        self._proficiencies = value
    
    @property
    def special_abilities(self):
        return self._special_abilities
    
    @special_abilities.setter
    def special_abilities(self, value):
        self._special_abilities = value
    
    def __str__(self):
        return self.title

    def __repr__(self):
        return f'{self.class_description}'

class BaseRole(AbstractRole):
    def __init__(self, title: str, class_description: str, hit_die: _Union[str, Die], skill_points: int, proficiencies: list[str]):
        self.title = title
        self.class_description = class_description
        self.hit_die = Die(int(hit_die.removeprefix('d'))) if isinstance(hit_die, str) else hit_die
        self.skill_points = skill_points
        self.proficiencies = proficiencies
        self.special_abilities = {}


class Role(BaseRole):
    def __init__(self, title):
        attributes = ROLE_ATTRIBUTES.get(title)
        super(Role, self).__init__(attributes['title'], attributes['_class_description'], attributes['hit_die'], attributes['skill_points'],
                                   attributes['proficiencies'])

    def _add_special_ability(self):
        ability_name = _SPECIAL_ABILITIES[self.title]["name"]
        if ability_name is not None:
            ability_instance = _SpecialAbilityFactory.create_special_ability(self.title)
            self._special_abilities[ability_name.replace(" ", "_").lower()] = ability_instance
            setattr(self, ability_name.replace(" ", "_").lower(), ability_instance)


class RoleFactory:
    @staticmethod
    def create_role(role_name):
        if role_instances.get(role_name) is not None:
            return role_instances[role_name]
        role_attr = ROLE_ATTRIBUTES.get(role_name)
        if role_attr is None:
            return None
        role_instances[role_name] = type(role_name, (Role,), {'title': role_attr['title']})
        # Create a new class based on the role attributes
        setattr(Role, role_name, role_instances[role_name])
        globals().update(role_instances)
        return globals()[role_name]


# for role_name, role_attributes in ROLE_ATTRIBUTES.items():
#     role_class = RoleFactory.create_role(role_name)
#     if role_class is not None:
#         role_instance = role_class(role_name)
#         role_instances[role_name] = role_instance
#         role_instance.add_special_ability()
#         role_instance.hit_die = role_instance._hit_die
# globals().update(role_instances)
