# CharActor

## Description

CharActor provides a convenient collection of character-based operations. It allows you to easily create, modify and employ characters in a variety of different ways. 

## Installation

```bash
pip install CharActor
```

## Usage

```python
import CharActor

# Create a character
CharActor.create() # Creates a random character and assigns it to the character bank as char1
CharActor.character_bank.char1 # Access the character via the character bank

# Reassign the character for implicit access
char1 = CharActor.character_bank.char1

# Modify the character
char1.name = "Bob"

# Print char1's character_sheet
print(char1.character_sheet)
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)