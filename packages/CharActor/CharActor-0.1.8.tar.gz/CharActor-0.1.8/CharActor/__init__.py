from .__log__ import logger, log
from ._charactor import dicts as _dicts
from ._charactor import create, BaseCharacters as _BaseCharacters, character_bank, _Armory, _Goods
from . import _entity

class _Catalogues:
    Armory = None
    Goods = None
    def __init__(self):
        self.Armory = _Armory()
        self.Goods = _Goods()
        
Catalogues = _Catalogues()

del log, logger