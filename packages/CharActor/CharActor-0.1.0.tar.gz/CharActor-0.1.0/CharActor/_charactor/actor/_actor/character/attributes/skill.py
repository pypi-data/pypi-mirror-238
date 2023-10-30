from abc import ABC as _ABC

import pyglet.event as _event

import json as _json

from dicepy import Roll as _Roll

from CharActor._quiet_dict import QuietDict as _QuietDict

check = _Roll.check

def _load_json(path):
    with open(path, 'r') as f:
        return _json.load(f)
    
SKILLS = _load_json('CharActor/_charactor/dicts/skills.json')


class SkillMeta(type):
    def __new__(cls, name, bases, attrs):
        attrs['_dispatcher'] = _event.EventDispatcher()
        attrs['_dispatcher'].register_event_type('on_level_up')
        return super().__new__(cls, name, bases, attrs)

class AbstractSkill(metaclass=SkillMeta):
    """Abstract class for skills.

    :param parent: The parent entity
    :type parent: :class:`entity.BaseActor`"""
    
    def __init__(self, parent, name, description, ability, proficient):
        self._parent = parent
        self.name = name
        self.description = description
        self.ability = ability
        self.proficient = proficient
        self.level = 0

    @property
    def parent(self):
        return self._parent

    def __repr__(self):
        return repr(self.level)
    
    def dispatch_event(self, event, *args, **kwargs):
        self._dispatcher.dispatch_event(event, *args, **kwargs)


class Skill(AbstractSkill):
    """A skill

    :param parent: The parent entity
    :type parent: :class:`entity.actor.Actor`"""

    def __init__(self, parent):
        self.name = self.__class__.__name__.replace("_", " ").replace("O", "o")

        super(Skill, self).__init__(parent, self.name, SKILLS[self.name]["description"], SKILLS[self.name]["ability"],
                                    SKILLS[self.name]["proficient"])

    def level_up(self):
        self.dispatch_event('on_level_up', self)

    def check(self, dc):
        """Perform a skill check"""
        ability = getattr(self.parent, self.ability)
        modifier = getattr(ability, 'modifier')
        return check(self.level + modifier, dc)


class SkillFactory:
    """A factory for creating skills"""

    @staticmethod
    def create_skill(parent, skill_name):
        if skill_name is not None:
            return type(skill_name, (Skill,), SKILLS[skill_name])(parent)


class SkillbookMeta(type):
    def __new__(cls, name, bases, attrs):
        attrs['_dispatcher'] = _event.EventDispatcher()
        return super().__new__(cls, name, bases, attrs)

class Skillbook(_QuietDict, metaclass=SkillbookMeta):
    def __init__(self, parent):
        self._parent = parent
        super(Skillbook, self).__init__()
