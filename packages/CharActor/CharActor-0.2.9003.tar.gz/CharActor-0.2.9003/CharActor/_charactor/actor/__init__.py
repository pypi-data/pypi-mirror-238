from ... import _character_bank as character_bank
from ..._character_bank import _Create
from ._actor import _character_list, _base_characters, _Armory, _Goods

from CharActor import log

# print('Welcome to the character creation module!\n\n You can create a new character by calling the create() '
#       'function.')
# print(f'Provide the necessary parameters to create a new character or leave them blank to create a random one.\n\n'
#       f'\tExample:\n\t\tcreate(name="Drog Fuerborne", role="Fighter", race="Human", alignment="chaotic_good")\n\n')
# print(f'You can also inspect the BaseCharacters attribute to create a character.\n\n\tExample:\n\t\tchar1 = '
#       f'BaseCharacters.HumanFighter(name="Drog Fuerborne", alignment="chaotic_good")\n\n')
BaseCharacters = _Create


def create(obj_name=None, name=None, role=None, race=None, background=None,  alignment=None, grid=None):
    """This is a convenience function for creating a new character. It is a wrapper for the _Create class.
    The character will be added to the character bank and can be accessed by calling character_bank.<obj_name>.
    
    :param obj_name: The name of the character object. If not provided, the name will be 'char1' if this is the first
                    character created, otherwise it will be 'charN' where N is the number of characters created. 
                    If provided, the name will be used as the name of the character object. 
                    If the name is already in use, it will be overwritten.
    :type obj_name: str or None (default)   
    
    :param name: The name of the character. If not provided, the name will be 'Unnamed'.
    :type name: str or None (default)
    
    :param role: The role of the character. If not provided, the role will be randomly selected.
    :type role: str or None (default)
    
    :param race: The race of the character. If not provided, the race will be randomly selected.
    :type race: str or None (default)
    
    :param background: The background of the character. If not provided, the background will be randomly selected.
    :type background: str or None (default)
    
    :param alignment: The alignment of the character. If not provided, the alignment will be randomly selected.
    :type alignment: str or None (default)
    
    :param grid: The grid to which the character will be added. If not provided, the character will not be added to a
        grid. 
    :type grid: Grid or None (default)
    """
    if obj_name is None and _Create._created_count > 0:
        obj_name = f'char{(_Create._created_count%8)+1}'
    elif obj_name is not None:
        obj_name = obj_name
    else:                
        obj_name = 'char1'
    log(f'Creating character: {obj_name}')
    details = []
    if name is not None:
        log(f'\tname: {name}')
        details.append(name)
    if role is not None:
        log(f'\trole: {role}')
        details.append(role)
    if race is not None:
        log(f'\trace: {race}')
        details.append(race)
    if background is not None:
        log(f'\tbackground: {background}')
        details.append(background)
    if alignment is not None:
        log(f'\talignment: {alignment}')
        details.append(alignment)
    if not details:
        log('No details provided. Creating random character.')
    setattr(character_bank, f'{obj_name}', _Create(obj_name, name, role, race, background, alignment))
    log(f'{obj_name} created.')
    if grid is not None:
        getattr(character_bank, f'{obj_name}')._join_grid(grid)
