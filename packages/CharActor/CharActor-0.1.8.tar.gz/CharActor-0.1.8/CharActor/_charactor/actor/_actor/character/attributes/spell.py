from abc import abstractmethod
import json as _json
from pyglet.event import EventDispatcher as _EventDispatcher

from CharActor._charactor.dicts import load_dict

def _load_json(path):
    with open(path, 'r') as f:
        return _json.load(f)

_SCHOOLS = ['DESTRUCTION', 'ILLUSION', 'ENCHANTMENT', 'DIVINATION', 'ABJURATION', 'TRANSMUTATION', 'CONJURATION', 'NECROMANCY', 'RESTORATION', 'ALTERATION', 'EVOCATION', 'CREATION', 'SPIRITUAL', 'ELEMENTAL', 'ARCANE', 'MYSTIC', 'PSIONIC', 'TELEPATHY', 'TELEKINESIS', 'TELEPORTATION']

_COMPONENTS = ['VERBAL', 'SOMATIC', 'MATERIAL', 'FOCUS', 'DIVINE_FOCUS', 'EXPERIENCE', 'BLOOD', 'SOUL', 'SHADOW', 'SONIC', 'MIND', 'BODY', 'LIFE', 'DEATH', 'LIGHT', 'DARKNESS', 'FIRE', 'WATER', 'EARTH', 'AIR', 'ICE', 'ELECTRICITY', 'ACID', 'FORCE', 'POSITIVE', 'NEGATIVE', 'CHAOS', 'LAW', 'GOOD', 'EVIL', 'ORDER', 'CHAOS', 'LAWFUL', 'CHAOTIC', 'NEUTRAL', 'ARCANE', 'DIVINE', 'NATURE', 'TECHNOLOGY', 'SONIC', 'MIND', 'BODY', 'LIFE', 'DEATH', 'LIGHT', 'DARKNESS', 'FIRE', 'WATER', 'EARTH', 'AIR', 'ICE', 'ELECTRICITY', 'ACID', 'FORCE', 'POSITIVE', 'NEGATIVE', 'CHAOS', 'LAW', 'GOOD', 'EVIL', 'ORDER', 'CHAOS', 'LAWFUL', 'CHAOTIC', 'NEUTRAL', 'ARCANE', 'DIVINE', 'NATURE', 'TECHNOLOGY']

_RESISTANCE = ['NONE', 'HALF', 'NULL']

_SPELL_DICT = load_dict('spells')

class SpellMeta(type):
    def __new__(cls, name, bases, attrs):
        attrs['_dispatcher'] = _EventDispatcher()
        return super().__new__(cls, name, bases, attrs)
    
class AbstractSpell(metaclass=SpellMeta):
    def __init__(self):
        self._parent = None
        self._name = None
        self._spell_id = None
        self._description = None
        self._spell_level = None
        self._school = None
        self._casting_time = None
        self._range = None
        self._touch = None
        self._saving_throw = None
        self._resist = None
        self._damage = None
        self._components = None
        self._duration = None
        self._ritual = None
        self._concentration = None
        self._classes = None
        self._archetype = None
    
    @property
    def parent(self):
        return self._parent
    
    @parent.setter
    def parent(self, parent):
        self._parent = parent

    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, name: str):
        if name is not None:
            self._name = name

    @property
    def description(self) -> str:
        return self._description
    
    @description.setter
    def description(self, description: str):
        if description is not None:
            self._description = description

    @property
    def spell_level(self) -> int:
        return self._spell_level
    
    @spell_level.setter
    def spell_level(self, spell_level: int):
        if spell_level is not None:
            self._spell_level = spell_level

    @property
    def school(self) -> str:
        return self._school
    
    @school.setter
    def school(self, school: str):
        if school is not None:
            self._school = school

    @property
    def casting_time(self) -> str:
        return self._casting_time
    
    @casting_time.setter
    def casting_time(self, casting_time: str):
        if casting_time is not None:
            self._casting_time = casting_time

    @property
    def range(self) -> str:
        return self._range
    
    @range.setter
    def range(self, range: str):
        if range is not None:
            self._range = range

    @property
    def touch(self):
        return self._touch
    
    @touch.setter
    def touch(self, touch):
        if touch is not None:
            self._touch = touch

    @property
    def saving_throw(self):
        return self._saving_throw
    
    @saving_throw.setter
    def saving_throw(self, saving_throw):
        if saving_throw is not None:
            self._saving_throw = saving_throw

    @property
    def resist(self):
        return self._resist
    
    @resist.setter
    def resist(self, resist):
        if resist is not None:
            self._resist = resist

    @property
    def damage(self):
        return self._damage
    
    @damage.setter
    def damage(self, damage):
        if damage is not None:
            self._damage = damage

    @property
    def components(self):
        return self._components
    
    @components.setter
    def components(self, components):
        if components is not None:
            self._components = components

    @property
    def duration(self):
        return self._duration
    
    @duration.setter
    def duration(self, duration):
        if duration is not None:
            self._duration = duration

    @property
    def ritual(self):
        return self._ritual
    
    @ritual.setter
    def ritual(self, ritual):
        if ritual is not None:
            self._ritual = ritual

    @property
    def concentration(self):
        return self._concentration
    
    @concentration.setter
    def concentration(self, concentration):
        if concentration is not None:
            self._concentration = concentration

    @property
    def classes(self):
        return self._classes
    
    @classes.setter
    def classes(self, classes):
        if classes is not None:
            self._classes = classes

    @property
    def archetype(self):
        return self._archetype
    
    @archetype.setter
    def archetype(self, archetype):
        if archetype is not None:
            self._archetype = archetype

    @abstractmethod
    def cast(self):
        pass

    @abstractmethod
    def cast_at(self, target):
        pass

    @abstractmethod
    def prepare(self):
        pass

    @abstractmethod
    def concentrate(self):
        pass

    @abstractmethod
    def dismiss(self):
        pass

    @abstractmethod
    def dispel(self):
        pass

    @abstractmethod
    def counterspell(self):
        pass

class Spell(AbstractSpell):
    def __init__(self, spell_id, name, description, spell_level, school, casting_time, range_, touch, saving_throw, resist, components, duration, ritual, concentration, classes, source, page, archetype):
        super().__init__()
        self.spell_id = spell_id
        self.name = name
        self.description = description
        self.spell_level = spell_level
        self.school = school
        self.casting_time = casting_time
        self.range = range_
        self.touch = touch
        self.saving_throw = saving_throw
        self.resist = resist
        self.components = components
        self.duration = duration
        self.ritual = ritual
        self.concentration = concentration
        self.classes = classes
        self.source = source
        self.page = page
        self.archetype = archetype
