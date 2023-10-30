from typing import Optional as _Optional

from .base_actor import *


class _BaseHuman(BaseActor):
    def __init__(
            self,
            actor_type: _Optional[str] = None,
            name: _Optional[str] = None,
            role: _Optional[str] = None,
            age: _Optional[int] = None,
            *args, **kwargs
    ) -> None:
        super(_BaseHuman, self).__init__(actor_type, name, role, 'Human', age, *args, **kwargs)


class _BaseElf(BaseActor):
    def __init__(
            self,
            actor_type: _Optional[str] = None,
            name: _Optional[str] = None,
            role: _Optional[str] = None,
            age: _Optional[int] = None,
            *args, **kwargs
    ) -> None:
        super(_BaseElf, self).__init__(actor_type, name, role, 'Elf', age, *args, **kwargs)


class _BaseDwarf(BaseActor):
    def __init__(
            self,
            actor_type: _Optional[str] = None,
            name: _Optional[str] = None,
            role: _Optional[str] = None,
            age: _Optional[int] = None,
            *args, **kwargs
    ) -> None:
        super(_BaseDwarf, self).__init__(actor_type, name, role, 'Dwarf', age, *args, **kwargs)


class _BaseGnome(BaseActor):
    def __init__(
            self,
            actor_type: _Optional[str] = None,
            name: _Optional[str] = None,
            role: _Optional[str] = None,
            age: _Optional[int] = None,
            *args, **kwargs
    ) -> None:
        super(_BaseGnome, self).__init__(actor_type, name, role, 'Gnome', age, *args, **kwargs)


class _BaseHalfling(BaseActor):
    def __init__(
            self,
            actor_type: _Optional[str] = None,
            name: _Optional[str] = None,
            role: _Optional[str] = None,
            age: _Optional[int] = None,
            *args, **kwargs
    ) -> None:
        super(_BaseHalfling, self).__init__(actor_type, name, role, 'Halfling', age, *args, **kwargs)


class _BaseHalfElf(BaseActor):
    def __init__(
            self,
            actor_type: _Optional[str] = None,
            name: _Optional[str] = None,
            role: _Optional[str] = None,
            age: _Optional[int] = None,
            *args, **kwargs
    ) -> None:
        super(_BaseHalfElf, self).__init__(actor_type, name, role, 'Half-Elf', age, *args, **kwargs)


class _BaseHalfOrc(BaseActor):
    def __init__(
            self,
            actor_type: _Optional[str] = None,
            name: _Optional[str] = None,
            role: _Optional[str] = None,
            age: _Optional[int] = None,
            *args, **kwargs
    ) -> None:
        super(_BaseHalfOrc, self).__init__(actor_type, name, role, 'Half-Orc', age, *args, **kwargs)


class _BaseTiefling(BaseActor):
    def __init__(
            self,
            actor_type: _Optional[str] = None,
            name: _Optional[str] = None,
            role: _Optional[str] = None,
            age: _Optional[int] = None,
            *args, **kwargs
    ) -> None:
        super(_BaseTiefling, self).__init__(actor_type, name, role, 'Tiefling', age, *args, **kwargs)


class _BaseDragonborn(BaseActor):
    def __init__(
            self,
            actor_type: _Optional[str] = None,
            name: _Optional[str] = None,
            role: _Optional[str] = None,
            age: _Optional[int] = None,
            *args, **kwargs
    ) -> None:
        super(_BaseDragonborn, self).__init__(actor_type, name, role, 'Dragonborn', age, *args, **kwargs)
