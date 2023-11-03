from typing import Optional as _Optional

from .base_actor import *


class _BaseBarbarian(BaseActor):
    def __init__(
            self,
            actor_type: _Optional[str] = None,
            name: _Optional[str] = None,
            race: _Optional[str] = None,
            age: _Optional[int] = None,
            *args, **kwargs
    ) -> None:
        super(_BaseBarbarian, self).__init__(actor_type, name, 'Barbarian', race, age, *args, **kwargs)


class _BaseBard(BaseActor):
    def __init__(
            self,
            actor_type: _Optional[str] = None,
            name: _Optional[str] = None,
            race: _Optional[str] = None,
            age: _Optional[int] = None,
            *args, **kwargs
    ) -> None:
        super(_BaseBard, self).__init__(actor_type, name, 'Bard', race, age, *args, **kwargs)


class _BaseCleric(BaseActor):
    def __init__(
            self,
            actor_type: _Optional[str] = None,
            name: _Optional[str] = None,
            race: _Optional[str] = None,
            age: _Optional[int] = None,
            *args, **kwargs
    ) -> None:
        super(_BaseCleric, self).__init__(actor_type, name, 'Cleric', race, age, *args, **kwargs)


class _BaseDruid(BaseActor):
    def __init__(
            self,
            actor_type: _Optional[str] = None,
            name: _Optional[str] = None,
            race: _Optional[str] = None,
            age: _Optional[int] = None,
            *args, **kwargs
    ) -> None:
        super(_BaseDruid, self).__init__(actor_type, name, 'Druid', race, age, *args, **kwargs)


class _BaseFighter(BaseActor):
    def __init__(
            self,
            actor_type: _Optional[str] = None,
            name: _Optional[str] = None,
            race: _Optional[str] = None,
            age: _Optional[int] = None,
            *args, **kwargs
    ) -> None:
        super(_BaseFighter, self).__init__(actor_type, name, 'Fighter', race, age, *args, **kwargs)


class _BaseMonk(BaseActor):
    def __init__(
            self,
            actor_type: _Optional[str] = None,
            name: _Optional[str] = None,
            race: _Optional[str] = None,
            age: _Optional[int] = None,
            *args, **kwargs
    ) -> None:
        super(_BaseMonk, self).__init__(actor_type, name, 'Monk', race, age, *args, **kwargs)


class _BasePaladin(BaseActor):
    def __init__(
            self,
            actor_type: _Optional[str] = None,
            name: _Optional[str] = None,
            race: _Optional[str] = None,
            age: _Optional[int] = None,
            *args, **kwargs
    ) -> None:
        super(_BasePaladin, self).__init__(actor_type, name, 'Paladin', race, age, *args, **kwargs)


class _BaseRanger(BaseActor):
    def __init__(
            self,
            actor_type: _Optional[str] = None,
            name: _Optional[str] = None,
            race: _Optional[str] = None,
            age: _Optional[int] = None,
            *args, **kwargs
    ) -> None:
        super(_BaseRanger, self).__init__(actor_type, name, 'Ranger', race, age, *args, **kwargs)


class _BaseRogue(BaseActor):
    def __init__(
            self,
            actor_type: _Optional[str] = None,
            name: _Optional[str] = None,
            race: _Optional[str] = None,
            age: _Optional[int] = None,
            *args, **kwargs
    ) -> None:
        super(_BaseRogue, self).__init__(actor_type, name, 'Rogue', race, age, *args, **kwargs)


class _BaseSorcerer(BaseActor):
    def __init__(
            self,
            actor_type: _Optional[str] = None,
            name: _Optional[str] = None,
            race: _Optional[str] = None,
            age: _Optional[int] = None,
            *args, **kwargs
    ) -> None:
        super(_BaseSorcerer, self).__init__(actor_type, name, 'Sorcerer', race, age, *args, **kwargs)


class _BaseWarlock(BaseActor):
    def __init__(
            self,
            actor_type: _Optional[str] = None,
            name: _Optional[str] = None,
            race: _Optional[str] = None,
            age: _Optional[int] = None,
            *args, **kwargs
    ) -> None:
        super(_BaseWarlock, self).__init__(actor_type, name, 'Warlock', race, age, *args, **kwargs)


class _BaseWizard(BaseActor):
    def __init__(
            self,
            actor_type: _Optional[str] = None,
            name: _Optional[str] = None,
            race: _Optional[str] = None,
            age: _Optional[int] = None,
            *args, **kwargs
    ) -> None:
        super(_BaseWizard, self).__init__(actor_type, name, 'Wizard', race, age, *args, **kwargs)
