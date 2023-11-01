from abc import ABC as _ABC
from typing import Optional as _Optional
import json as _json
from CharActor._charactor.dicts import load_dict

def _load_json(path):
    with open(path, 'r') as f:
        return _json.load(f)
    
RACE_ATTRIBUTES = load_dict('race_attributes')

SUBRACE_ATTRIBUTES = load_dict('subrace_attributes')

RACE_INSTANCES = {}


class AbstractRace:
    title = None
    description = None
    racial_bonuses = None
    age = None
    size = None
    speed = None
    languages = None
    traits = None
    subraces = None
    parent_race = None
    
    def __repr__(self) -> str:
        return self.description


class BaseRace(AbstractRace):
    def __init__(
            self,
            title: _Optional[str] = None,
            description: _Optional[str] = None,
            _ability_score_increase: _Optional[dict] = None,
            age: _Optional[dict] = None,
            size: _Optional[str] = None,
            speed: _Optional[int] = None,
            languages: _Optional[list] = None,
            traits: _Optional[list] = None,
            subraces: _Optional[list] = None,
            parent_race: _Optional[str] = None,
    ) -> None:
        self.title = title
        self.description = description
        self.racial_bonuses = _ability_score_increase
        self.age = age
        self.size = size
        self.speed = speed
        self.languages = languages
        self.traits = traits
        self.subraces = subraces
        self.parent_race = parent_race
    
class Race(BaseRace): 
    def __init__(self, title):
        attributes = RACE_ATTRIBUTES.get(title)
        super(Race, self).__init__(attributes['title'], attributes['description'],
                                   attributes['_ability_score_increase'], attributes['_age'], attributes['size'],
                                   attributes['speed'], attributes['languages'], attributes['traits'],
                                   attributes['subraces'])


class SubRace(BaseRace):
    def __init__(self, title):
        attributes = SUBRACE_ATTRIBUTES.get(title)
        super(SubRace, self).__init__(attributes['title'], attributes['description'],
                                      attributes['_ability_score_increase'], attributes['_age'], attributes['size'],
                                      attributes['speed'], attributes['languages'], attributes['traits'],
                                      attributes['subraces'], attributes['parent_race'])


class RaceFactory:
    @staticmethod
    def create_race(race_name):
        if RACE_INSTANCES.get(race_name) is not None:
            return RACE_INSTANCES[race_name]
        race_attr = RACE_ATTRIBUTES.get(race_name)
        if race_attr is None:
            return None
        type_instance = type(race_name, (Race, ), RACE_ATTRIBUTES[race_name])
        RACE_INSTANCES[race_name] = type_instance
        globals().update(RACE_INSTANCES)
        return RACE_INSTANCES[race_name]
