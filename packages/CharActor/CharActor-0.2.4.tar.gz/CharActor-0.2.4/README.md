# CharActor

### Description

CharActor provides a convenient collection of character-based operations. It allows you to easily create, modify and employ characters in a variety of different ways.

### Installation

```bash
pip install CharActor
```

## Usage

```python
from CharActor import character_bank, create

# Create a randomized character
character = create()

# Create a character with a specific name
character = create(name='John Doe')

# Create a character with a specific object name, character name, race, role, background and alignment
character = create('my_character', 'John Doe', 'Human', 'Fighter', 'Noble', 'Lawful Good')

# Access any of the characters
my_character = character_bank.my_character

# Access any of the characters' attributes
my_character.name # 'John Doe'
my_character.Strength # Str: 17 (+3)
```

## Characters

A character object contains a variety of attributes/methods which tend to differ from character to character.

### Attributes

* name
* _role (e.g my_character.Fighter)
* _race (e.g my_character.Human)
* _background (e.g my_character.Noble)
* _alignment (e.g my_character.LawfulGood)
* age
* Strength
* Dexterity
* Constitution
* Intelligence
* Wisdom
* Charisma
* actions
* armor_class
* character_sheet (e.g print(my_character.character_sheet))
* entity_id
* experience
* hp
* initiative
* inventory
* level
* saving_throws
* skill_points
* skillbook
* speed
* target

### Methods

* attack
* look_around
* move
* pickup
* saving_throw
* end_turn

## Character Bank

The character bank is a collection of all the characters that have been created. It is a dictionary of character objects, with the key being the name of the character. More conveniently, the character bank also allows you to access the characters as attributes. A saving system(using python's pickle) is currently under development. Until then your character's are only saved for the duration of the program.

```python
from CharActor import character_bank, create

# Create a character
character = create('my_character')

# Access the character
my_character = character_bank.my_character
print(my_character.character_sheet)
```


## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Support

If you like this project or are just feeling generous, consider buying me a coffee.

[buymeacoffee](https://www.buymeacoffee.com/primalcoder)