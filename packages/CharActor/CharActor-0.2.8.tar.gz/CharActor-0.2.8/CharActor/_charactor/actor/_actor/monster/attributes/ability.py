from abc import ABC as _ABC
from begingine.utility import ability_roll as _ability_roll, check
from typing import Optional as _Optional

ABILITIES = {
    'Strength': {"Save": None},
    'Dexterity': {"Save": "Reflex"},
    'Constitution': {"Save": "Fortitude"},
    'Intelligence': {"Save": None},
    'Wisdom': {"Save": "Will"},
    'Charisma': {"Save": None}
}

SAVING_THROWS = {
    'Fortitude': {'ability': 'Constitution'},
    'Reflex': {'ability': 'Dexterity'},
    'Will': {'ability': 'Wisdom'}
}


# Path: begingine/Ability.py

# begingine an Ability class which can be attached to a actor

# The class should have a constructor that takes a actor object, the ability name and score as an argument.

# The class should have a method to calculate the modifier from the score.

# The class should have a method to permanently alter the score.

# The class should have a method to temporarily alter the score.

# The class should have a method that returns the ability score.

# The class should have a method that returns the ability modifier.

# The class should have a method which performs an ability check and returns the result.

# The class should have a method which can determine if the ability is a primary ability.
# The method should have a constructor that takes a character_class as an argument
# The method should return True if the ability is a primary ability for the character_class.

class AbstractAbility:
    def __init__(
            self,
            parent: _Optional[object] = None,
            name: _Optional[str] = None,
            score: _Optional[int] = None,
    ) -> None:
        """
        Abstract class representing an ability.
        :param parent: The object that has this ability.
        :param name: The name of the ability.
        :param score: The score associated with the ability.
        """
        self.parent = parent
        self.name = name
        self.primary = self.is_primary(self.parent._role.title)
        self.short = name[0:3].upper()
        self.score = score if score is not None else _ability_roll()
        self.modifier = (self.score - 10) // 2
        self.temp_mod = 0
        self.temp_mod_duration = 0

    def _get_score(self):
        """
        Gets the score associated with the ability.
        """

        return self.score

    def _get_modifier(self):
        """
        Gets the modifier associated with the ability.
        """

        return self.modifier

    def _set_score(self, score: int):
        """
        Sets the score associated with this ability.
        """

        self.score = score
        self.modifier = (self.score - 10) // 2

    def _increase_score(self, amount: int):
        """
        Inceases the score associated with this ability
        """

        self._set_score(self.score + amount)

    def _decrease_score(self, amount: int):
        """
        Decreases the score associated with this ability
        """

        self._set_score(self.score - amount)

    def _plus_one(self):
        """
        Increases the ability score by a single point.
        """

        self._increase_score(1)

    def _minus_one(self):
        """
        Decreases the ability score by a single point.
        """

        self._decrease_score(1)

    def ability_check(self, dc: int):
        """
        Checks if the ability passes a DC check.
        :param dc: The DC value to check against.
        :return: True if the check passes, False otherwise.
        """

        mod = self.modifier + self.temp_mod
        return check(mod, dc)

    def is_primary(self, role: _Optional[str] = None):
        """
        Checks if the ability is a primary ability for a given role.
        :param role: The role to check against.
        :return: True if the ability is a primary ability for the given role, False otherwise.
        """

        if role is None:
            role = self.parent._role.title
        return role in ABILITIES[self.name]['Primary']

    def __str__(self):
        """
        Gets a string representation of the ability.
        :return: A string representation of the ability.
        """

        return f'{self.short}: {self.score} ({"+" if self.modifier > 0 else ""}{self.modifier})'

    def __repr__(self):
        return f'{self.short}: {self.score} ({"+" if self.modifier > 0 else ""}{self.modifier})'


class Ability(AbstractAbility):
    """A class representing an ability score for a character, such as strength or dexterity.

    Attributes:
    - name (str): The name of the ability score.
    - _init_score (_Optional[int]): The initial score of the ability, if it is provided in the parent object.
    """

    def __init__(
            self,
            parent: _Optional[object] = None,
    ):
        """Initialize a new Ability object.

        Args:
        - parent (_Optional[object]): The parent object that the ability belongs to, usually a BaseActor object.
        """
        self.name = self.__class__.__name__.capitalize()
        self._init_score = parent._initial_ability_scores[
            self.name] if parent._initial_ability_scores is not None else None
        if self.name in parent._race.racial_bonuses.keys():
            self._racial_bonus = parent._race.racial_bonuses[self.name]
            self._init_score += self._racial_bonus
        super(Ability, self).__init__(parent, self.name, self._init_score)
        if ABILITIES[self.name]["Save"] is not None:
            setattr(self, f'{ABILITIES[self.name]["Save"].lower()}_save', self.ability_check)


class AbilityFactory:
    """A factory class for creating Ability objects.

    Methods:
    - create_ability(parent, ability_name): Create a new Ability object with the given parent object and ability name.
    """

    @staticmethod
    def create_ability(parent, ability_name):
        """Create a new Ability object with the given parent object and ability name.

        Args:
        - parent (object): The parent object that the ability belongs to.
        - ability_name (str): The name of the ability to create.

        Returns:
        - Ability: The newly created Ability object.
        """

        if ability_name is not None:
            return type(ability_name, (Ability,), {})(parent)
        return None


class AbstractSpecialAbility(_ABC):
    """An abstract base class for special abilities that a character can have.

    Attributes:
    - name (str): The name of the special ability.
    - description (str): A description of the special ability.
    """

    def __init__(
            self,
            name: str,
            description: str
    ) -> None:
        """Initialize a new AbstractSpecialAbility object.

        Args:
        - name (str): The name of the special ability.
        - description (str): A description of the special ability.
        """
        self.name = name
        self.description = description


class SpecialAbility(AbstractSpecialAbility):
    """A class representing a special ability that a character can have.

    Attributes:
    - _role_title (_Optional[str]): The role title of the special ability, if it is provided in the parent object.
    """

    def __init__(
            self,
            role_title: _Optional[str] = None
    ) -> None:
        self._role_title = role_title
        attributes = SPECIAL_ABILITIES[self._role_title]
        super(SpecialAbility, self).__init__(attributes["name"], attributes["description"])

    def __repr__(self):
        """Return a string representation of the SpecialAbility object.

        Returns:
        - str: A string representation of the SpecialAbility object.
        """

        return self.description

    def __str__(self):
        """Return a string representation of the SpecialAbility object.

        Returns:
        - str: A string representation of the SpecialAbility object.
        """
        return f'{self.name}: {self.description}'


class SpecialAbilityFactory:
    @staticmethod
    def create_special_ability(role_title):
        """
        A static method that creates an instance of the SpecialAbility class based on the attributes
        defined in the SPECIAL_ABILITIES dictionary for the given role title.

        Args:
        - role_title: A string representing the role title for which a special ability needs to be created.

        Returns:
        - An instance of the SpecialAbility class or None if the role title is not found in SPECIAL_ABILITIES.
        """

        special_ability_attr = SPECIAL_ABILITIES[role_title]
        if special_ability_attr is None:
            return None
        return type(special_ability_attr["name"], (SpecialAbility,), dict(special_ability_attr))


if __name__ == '__main__':
    specialability_instances = {}

    for role_title, special_ability_attr in SPECIAL_ABILITIES.items():
        specialability_class = SpecialAbilityFactory.create_special_ability(role_title)
        if specialability_class is not None:
            specialability_instance = specialability_class(role_title)
            specialability_instances[special_ability_attr["name"].replace(" ", "_").lower()] = specialability_instance
    globals().update(specialability_instances)
