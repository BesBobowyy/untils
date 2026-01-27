# State control

In this lesson you will learn how to change state and create context commands.

## Theory

The state - is a list of commands, which is active only if current state equals this state.

!!! note "Note"
    In this lesson we don't speak about state abilities and reserved names, because them were spoken in `01. First Project` lesson in this course.

## Practice

### Preview

Let's define states in this lesson config:

```json
{
    "version": 1,
    "states": {
        "__init__": ["c1"],
        "adventure": ["c2", "c3", "b"],
        "fight": ["c4", "b"]
    },
    "commands": {
        "b": {
            "aliases": [],
            "type": "word"
        },
        "c1": {
            "aliases": [],
            "type": "word"
        },
        "c2": {
            "aliases": [],
            "type": "word"
        },
        "c3": {
            "aliases": [],
            "type": "word"
        },
        "c4": {
            "aliases": [],
            "type": "word"
        }
    }
}
```

Here we have next data:

- `__init__`: `c1`.
- `adventure`: `c2`, `c3` and `b`,
- `fight`: `c4` and `b`.

We will define, that the command `c1` toggles the state `adventure`, the command `c3` toggles the state `fight` and the command `c4` toggles the state `adventure`, we close cycle.

Let's write script:

```py
# Written by untils v1.0.0r.

# In this code I don't use any detailed architecture for simplification.
# In real products you must use OOP style or another simplier.

import untils

from typing import List

import os

# Computing paths.
DIR: str = os.path.abspath(os.path.dirname(__file__))    # The 'Project' path.
CONFIG_PATH: str = os.path.join(DIR, "resources", "config.json")    # Hardcoded path.

# The library configuration.
settings: untils.Settings = untils.Settings()    # Context settings object.
command_system: untils.CommandSystem = untils.CommandSystem(settings)    # Command system.
command_system.load_config(CONFIG_PATH)    # Load the config.

# Others.
i: int = 10    # Iterations count.

# Commands functions
def com_b(input_str: str, input_dict: untils.utils.InputDict) -> None:
    print("Command `b`.")

def com_c1(input_str: str, input_dict: untils.utils.InputDict) -> None:
    print("Command `c1`.")
    print("Routing to the state `adventure`.")
    settings.current_state = "adventure"    # Changing to the `adventure`.

def com_c2(input_str: str, input_dict: untils.utils.InputDict) -> None:
    print("Command `c2`.")

def com_c3(input_str: str, input_dict: untils.utils.InputDict) -> None:
    print("Command `c3`.")
    print("Routing to the state `fight`.")
    settings.current_state = "fight"    # Changing to the `fight`.

def com_c4(input_str: str, input_dict: untils.utils.InputDict) -> None:
    print("Command `c4`.")
    print("Routing to the state `adventure`.")
    settings.current_state = "adventure"    # Changing to the `adventure`.

# Command adding.
command_system.register_command(("b",), com_b)    # Register `com_b`.
command_system.register_command(("c1",), com_c1)    # Register `com_c1`.
command_system.register_command(("c2",), com_c2)    # Register `com_c2`.
command_system.register_command(("c3",), com_c3)    # Register `com_c3`.
command_system.register_command(("c4",), com_c4)    # Register `com_c4`.

# Main loop.
while i > 0:
    input_str: str = input("> ")    # Reading a user input.

    is_valid: bool = False

    try:
        # If input is valid.
        input_dict: untils.utils.InputDict = command_system.process_input(input_str)    # Parsed input.
        is_valid: bool = command_system.is_input_valid(input_dict)    # Is input valid.
        normalized_path: List[str] = command_system.get_normalized_path(input_dict)    # Get normalized path.
        command_system.execute(input_str, input_dict, normalized_path)    # Execute commands.
        print(input_dict["path"])
    except untils.utils.InputError as e:
        # Unless input is valid.
        print(f"Incorrect input: {e}")
    except Exception as e:
        # Unknown exception.
        print(f"Unexpected exception: {e}")
    
    print(f"Is valid: {is_valid}")
    
    i -= 1
```

What's changed from previous?:

1. Changed config (see upper).
2. Replaced commands in code to new.
3. State changing in commands `c1`, `c3` and `c4`.

The example of output:

```txt
> b
Incorrect input: The command is not defined in the current state '__init__' or in the '__base__' state.
Is valid: False
> c1
Command `c1`.
Routing to the state `adventure`.
['c1']
Is valid: True
> c2
Command `c2`.
['c2']
Is valid: True
> c4
Incorrect input: The command is not defined in the current state 'adventure' or in the '__base__' state.
Is valid: False
> b
Command `b`.
['b']
Is valid: True
> c3
Command `c3`.
Routing to the state `fight`.
['c3']
Is valid: True
> c2
Incorrect input: The command is not defined in the current state 'fight' or in the '__base__' state.
Is valid: False
> b
Command `b`.
['b']
Is valid: True
> c4
Command `c4`.
Routing to the state `adventure`.
['c4']
Is valid: True
> c4
Incorrect input: The command is not defined in the current state 'adventure' or in the '__base__' state.
Is valid: False
```

In this output we have universal command `b` for states `adventure` and `fight`, `c1` routes to `adventure`, `c3` routes to `fight`, `c4` routes to `adventure`, but commands from other states are blocked.

!!! warning "Warning"
    Don't forget, that may be blocked only root commands, which defines in `"commands"`, not `"children"`. Also may be blocked only `Word` and `Fallback` commands.

!!! important "Important"
    Any name in config hasn't special character (exceptly internal state name and `Fallback` convention), in state name next characters [`-`, `:`, `/`] is allowed for visual separation.

### Context commands

Context commands - is a way for difficult commands, which defines hard actions, for example as player percs.

Let's define a new config:

```json
{
    "version": 1,
    "states": {
        "__init__": [
            "base",
            "player"
        ],
        "context:player": [
            "quit",
            "help",
            "name",
            "abilities",
            "advancements"
        ]
    },
    "commands": {
        // State: "__init__":
        "base": {
            "aliases": ["b"],
            "type": "word"
        },
        "player": {
            // Context command.
            "aliases": ["p"],
            "type": "word"
        },
        // State "context:player":
        "quit": {
            "aliases": ["q"],
            "type": "word"
        },
        "help": {
            "aliases": ["h"],
            "type": "word"
        },
        "name": {
            "aliases": [],
            "type": "word",
            "children": {
                "$argument": {
                    "type": "fallback",
                    "default": "Player"
                }
            }
        },
        "abilities": {
            "aliases": [],
            "type": "word"
        },
        "advancements": {
            "aliases": [],
            "type": "word"
        }
    }
}
```

Let's create script for this hard config:

```py
# Written by untils v1.0.0r.

# In this code I don't use any detailed architecture for simplification.
# In real products you must use OOP style or another simplier.

import untils

from typing import List

import os

# Computing paths.
DIR: str = os.path.abspath(os.path.dirname(__file__))    # The 'Project' path.
CONFIG_PATH: str = os.path.join(DIR, "resources", "config.json")    # Hardcoded path.

# The library configuration.
settings: untils.Settings = untils.Settings()    # Context settings object.
command_system: untils.CommandSystem = untils.CommandSystem(settings)    # Command system.
command_system.load_config(CONFIG_PATH)    # Load the config.

# Others.
i: int = 15    # Iterations count.
player_name: str = "Player"    # Player name.

# Commands functions
def com_base(input_str: str, input_dict: untils.utils.InputDict) -> None:
    print("Command `base`.")
    print("This is base command in this example.")

def com_player(input_str: str, input_dict: untils.utils.InputDict) -> None:
    print("Command `player`.")
    print("Routing to the state `context:player`.")
    settings.current_state = "context:player"    # Changing to the `context:player`.
    print("You in player settings mode. Type `help` for info.")

def com_quit(input_str: str, input_dict: untils.utils.InputDict) -> None:
    print("Command `player:quit`.")
    print("Routing to the state `__init__`.")
    settings.current_state = "__init__"    # Changing to the `__init__`.
    print("Returning to main game...")

def com_help(input_str: str, input_dict: untils.utils.InputDict) -> None:
    print("Command `player:help`.")
    print("You in player mode, you can use:")
    print("| `quit` - Return.")
    print("| `help` - View available commands in player mode.")
    print("| `name` - Set or get player name.")
    print("| `abilities` - View player abilities (placebo option).")
    print("| `advancements` - View advancements (placebo option).")

def com_name(input_str: str, input_dict: untils.utils.InputDict) -> None:
    global player_name
    
    print("Command `player:name`.")

    if command_system.access_path(normalized_path, ("name",)):
        # Get player name.
        print(player_name)
    elif command_system.access_path(normalized_path, ("name", "$argument")):
        # Set player name.
        player_name = input_dict["path"][1]
        print(f"Player name was changed to: '{player_name}'.")
    else:
        # Invalid command structure.
        print(f"Invalid command structure: {input_str}.")

def com_abilities(input_str: str, input_dict: untils.utils.InputDict) -> None:
    print("Command `player:abilities`.")
    print("This is placebo option without implementation for example.")

def com_advancements(input_str: str, input_dict: untils.utils.InputDict) -> None:
    print("Command `player:advancements`.")
    print("This is placebo option without implementation for example.")



# Command adding.
command_system.register_command(("base",), com_base)    # Register `com_base`.
command_system.register_command(("player",), com_player)    # Register `com_player`.
command_system.register_command(("quit",), com_quit)    # Register `com_quit`.
command_system.register_command(("help",), com_help)    # Register `com_help`.
command_system.register_command(("name",), com_name)    # Register `com_name`.
command_system.register_command(("abilities",), com_abilities)    # Register `com_abilities`.
command_system.register_command(("advancements",), com_advancements)    # Register `com_advancements`.

# Main loop.
while i > 0:
    input_str: str = input("> ")    # Reading a user input.

    is_valid: bool = False

    try:
        # If input is valid.
        input_dict: untils.utils.InputDict = command_system.process_input(input_str)    # Parsed input.
        is_valid: bool = command_system.is_input_valid(input_dict)    # Is input valid.
        normalized_path: List[str] = command_system.get_normalized_path(input_dict)    # Get normalized path.
        command_system.execute(input_str, input_dict, normalized_path)    # Execute commands.
        print(input_dict["path"])
    except untils.utils.InputError as e:
        # Unless input is valid.
        print(f"Incorrect input: {e}")
    except Exception as e:
        # Unknown exception.
        print(f"Unexpected exception: {e}")
    
    print(f"Is valid: {is_valid}")

    i -= 1
```

The example of output:

```txt
> player
Command `player`.
Routing to the state `context:player`.
You in player settings mode. Type `help` for info.
['player']
Is valid: True
> name
Command `player:name`.
Player
['name']
Is valid: True
> name "Hello, World!"
Command `player:name`.
Player name was changed to: 'Hello, World!'.
['name', 'Hello, World!']
Is valid: True
> name
Command `player:name`.
Hello, World!
['name']
Is valid: True
> help
Command `player:help`.
You in player mode, you can use:
| `quit` - Return.
| `help` - View available commands in player mode.
| `name` - Set or get player name.
| `abilities` - View player abilities (placebo option).
| `advancements` - View advancements (placebo option).
['help']
Is valid: True
> abilities
Command `player:abilities`.
This is placebo option without implementation for example.
['abilities']
Is valid: True
> advancements
Command `player:advancements`.
This is placebo option without implementation for example.
['advancements']
Is valid: True
> quit
Command `player:quit`.
Routing to the state `__init__`.
Returning to main game...
['quit']
Is valid: True
> base 
Command `base`.
This is base command in this example.
['base']
Is valid: True
> name
Incorrect input: The command is not defined in the current state '__init__' or in the '__base__' state.
Is valid: False
> abilities
Incorrect input: The command is not defined in the current state '__init__' or in the '__base__' state.
Is valid: False
> advancements
Incorrect input: The command is not defined in the current state '__init__' or in the '__base__' state.
Is valid: False
> base
Command `base`.
This is base command in this example.
['base']
Is valid: True
> base
Command `base`.
This is base command in this example.
['base']
Is valid: True
> base
Command `base`.
This is base command in this example.
['base']
Is valid: True
```

## Conclusion

TL;DR: States control available commands, current state defines a state from states, which currently enabled. May be blocked only root commands.

## Documentation

Next lesson: [04. Command Logic](04-command-logic.md "Next article in this course.").
