import pickle as _pickle

from CharActor._quiet_dict import QuietDict as _QuietDict
from ._charactor.actor._actor import _character_list, _ALIGNMENTS, _BACKGROUNDS

_char_list = _character_list._char_list


class _create(_QuietDict):
    @staticmethod
    def random_character(obj_name=None, name='Unnamed'):
        import random as _random
        alignment = _random.choice(list(_ALIGNMENTS.keys()))
        background = _random.choice(list(_BACKGROUNDS.keys()))
        return f'{obj_name} = _Create.{_char_list[_random.randint(0, len(_char_list) - 1)]}("{name}", "{background}", "{alignment}")'

    def __init__(self):
        super(_create, self).__init__()
        self.update(_character_list._base_characters)
        for item in self.items:
            setattr(self, item, self[item])

        for r, c in self.items.items():
            for k, v in c.items():
                setattr(self, f'{r}{k}', v)

        self._created_count = 0
        self._char1 = None
        self._char2 = None
        self._char3 = None
        self._char4 = None
        self._char5 = None
        self._char6 = None
        self._char7 = None
        self._char8 = None

    def __call__(self, obj_name=None, name=None, role=None, race=None, background=None,  alignment=None, grid=None):
        random = False
        for param in [obj_name, name, role, race, alignment]:
            if param is None:
                continue
            if not isinstance(param, str):
                raise TypeError(f'Expected str, got {type(param)}')
        if obj_name is None and self._created_count > 0:
            obj_name = f'char{(self._created_count%8)+1}'
        elif obj_name is not None:
            obj_name = obj_name
        else:                
            obj_name = 'char1'
        if name is None:
            name = 'Unnamed'
        if role is None and race is None and background is None and alignment is None:
            statement = self.random_character(obj_name, name)
        else:
            statement = f'{obj_name} = _Create.{race}{role}("{name}", "{background}", "{alignment}")'
        self._created_count += 1
        exec(statement, globals(), locals())
        if grid is not None:
            locals()[obj_name]._join_grid(grid)
        setattr(self, f'_{obj_name}', locals()[obj_name])
        return locals()[obj_name]
    
    def _save_character(self, character, file_name):
        with open(f'CharActor/character_bank/{file_name}.pickle', 'wb') as file:
            _pickle.dump(character, file)


_Create = _create()


for _k in _character_list.__dict__.copy().keys():
    if _k not in _char_list and _k not in  ['random_character', '_char_list']:
        delattr(_character_list, _k)
