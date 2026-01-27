# First project

## Preparing

Firstly, you need to know some useful information, before we start.

In this project we will use next folder structure:

```txt
[Project]
| [resources]
| | config.json
| main.py
```

!!! tip "Tip"
    You can contain your config everywhere, but control names and context, that don't mistake with `untils` config and others in future.

## Config

Configs contain three required fields: `version`, `states` and `commands`:

- `version` - Config version.
- `states` - All available command states. States define, which root commands can be used in this state. All states are divided into two groups: Internal and Custom:
- - Internal state - Reserved state, which used by state system by default. Has custom format: `__{name}__`.
- - Custom state - User defined state.
- `commands` - Defined commands.

### Version

A config version define, which config structure and abilities are available. Config version always an integer.

Сurrent version of `untils` has only 1 version: 1, in the future version may be changed.

!!! warning "Warning"
    The documentation will change with version changing and may be deprecated in future.

### States

State system - is a system, which has a set of states, which defines commands execution environment.

For example, you have state `__base__`, `explore` and state `fight`. In `explore` state you have commands: `look`, `go ("1"|"2"|"3"|"4")`. In `fight` state you have commands: `hit`, `defend` and `run`. In `__base__` state you have commands: `inventory`, but this state is internal, so you have commands in this state everywhere.

States syntax:

```txt
{
    "states": {
        "__base__": [...],    // Internal state.
        "__init__": [...],    // Internal state.
        "<name>": [
            "<command_0>",
            "<command_1>",
            ...
            "<command_n>
        ]
    }
}
```

!!! important "Important"
    Use correct order in states and commands, because the correct order is important for parser, unless bugs may occured.

    For states: [`"__base__"`, `"__init__"`, ...], for commands: [..., `"<fallback command>"`].

#### Internal state: `__base__`

This internal state define, which commands are available in any state.

Commands in this state are available everywhere anywhere.

#### Internal state: `__init__`

This internal state define, which commands are available by default.

This state always sets by default, when script ran, and their commands available from start, but state was changed to other, you cannot use these commands.

### Commands

Commands - Main things in this library, and you can write them!

Commands syntax:

```txt
{
    "commands": CommandList
}



CommandList {
    "<command_0>": Command,
    "<command_1>": Command,
    ...
    "<command_n>": Command
}

Command {
    "aliases": [
        "<alias_0>",
        "<alias_1>",
        ...
        "<alias_n>"
    ],
    "type": "<type>",
    "default": Any,
    "children": CommandList
}
```

!!! important "Important"
    You can use Unicode latest version character, but only an alphabetic and numeric symbols. You can use the Python's `str.isalnum()` for tests.

    Exceptions:

    1. In `Fallback` command name `$` character is allowed only at name beginning by standard.
    2. In internal state name character `_` is allowed only in `__{name}__` signature.
    3. In state name next characters [`-`, `:`, `/`] is allowed for visual separation.

!!! warning "Warning"
    Everywhere use original names, not aliases.

!!! warning "Warning"
    In real products, please, use the library standart, because the `Strict` warnings level will raise exceptions for all mistakes.
    With this standart you can write only 1 `$` character at name beginning for `Fallback` type, but in any other you will get an exception.

#### Explanation

Explanation:

- `"aliases"` (Type: [`Word`, `Flag`, `Option`]) - Alias list. Alias - is alternative name of current command. Aliases may have any names, but it's not overlaps with original name, another names and between self.
- `"type"` - Command type. Current library version has only 4 command type: `Word`, `Fallback`, `Flag` and `Option`:
  - `Word` - A simple word command type. This type make a path from commands, which defines game logic.
  - `Fallback` - Any word for this position. For example, if you write `base Aaa` and `base Bbb`, `Fallback` command eat `Aaa`, `Bbb` and other sequences.
  - `Flag` - Non positional keyword, which contain a bool value: `false` or `true`, but it contains `null` if it not set in current input.
  - `Option` - Non positional keyword, which contain any string value after it. By default is `null`.
- `"default"` (Type: [`Fallback`, `Flag`, `Option`]) - Default value if unset.
- `"children"` (Type: [`Word`, `Fallback`]) - Nested commands.

!!! important "Important"
    `Fallback` commands has `"default"` field, but it's always casting to string by commands path specific. For example: `{"default": null}` -> `'None'`, `{"default": 5.2}` -> `'5.2'` and others.

### Examples

This is the minimal valid config template:

```json
{
    "version": 1,
    "states": [],
    "commands": {}
}
```

This is an example of config for small exploring game:

```json
{
    "version": 1,
    "states": {
        "__base__": [
            "review"
        ],
        "__init__": [
            "start"
        ],
        "explore": [
            "look",
            "go"
        ],
        "fight": [
            "hit",
            "defend",
            "run"
        ]
    },
    "commands": {
        "review": {
            // Get all available commands.
            "aliases": [],
            "type": "word"
        },
        "start": {
            // Launch game.
            "aliases": [],
            "type": "word"
        },
        "look": {
            // Look around in current position.
            "aliases": ["l"],
            "type": "word"
        },
        "go": {
            // Select an option to go after exploring.
            "aliases": [
                "g",
                "идти"    // State, command and alias name may be any alphabetic or numeric character in Unicode.
            ],
            "type": "word",
            "children": {
                "1": {
                    // First choice.
                    "aliases": ["one", "first", "f"],
                    "type": "word"
                },
                "2": {
                    // Second choice.
                    "aliases": ["two", "second", "s"],
                    "type": "word"
                },
                "3": {
                    // Third choice.
                    "aliases": ["three", "third", "t"],
                    "type": "word"
                },
                "4": {
                    // Fourth choice.
                    "aliases": ["four", "fourth", "fo"],
                    "type": "word"
                },
                "$argument": {    // Only `Fallback` type has `$` character in name!
                    // Any other choice.
                    "type": "fallback",
                    "default": null
                }
            }
        },
        "hit": {
            // Try to hit an opponent.
            "aliases": ["h"],
            "type": "word"
        },
        "defend": {
            // Try to defend from an opponent.
            "aliases": ["d"],
            "type": "word"
        },
        "run": {
            // Try to escape from an opponent.
            "aliases": ["r"],
            "type": "word"
        }
    }
}
```

## User input

User input has simple unique syntax, which can be telled for several minutes.

Every command has own syntax by it's type.

Command syntax:

```txt
Word: `<name>`.
Fallback: `<any>`.
Flag: `-<operator><name>`.
Option: `--<name> <value>`.
```

Explanation:

- `Word`: Only command name in one word. For example: `hello` - 1 word, `hello world` - 2 words (`hello`, `world`).
- `Fallback`: Only one any word.
- `Flag`: Has single `Minus` separator (`-`) and name. By default this construction sets a flag to `True`, but if you put in `<operator>` the `!` character, you sets the flag to `False`. For example: `-T` sets the flag `T` to `True`, but `-!T` sets the flag `T` to `False`.
- `Option`: Has double `Minus` separator (`--`), name and value. You cannot write `Option` without value. For example: `--file hello` sets the option `file` to the value `hello`.

!!! warning "Warning"
    You need to watch for command condition, because if you write flag or option earlier than them defined, you get error.

Also this syntax has some features under.

### Strings

You can write strings with any character as one entity.

Strings syntax:

```txt
"<string>"
```

In `<string>` you can write any sequence of the characters. Strings are supported in all constructions with several tokens for a one entity.

For example: `character name "Hello, World!"`  will be split to the `["character", "name", "Hello, World!"]`.

!!! warning "Warning"
    You need to control border characters in string, because if you set different quotes in name, parser will break this sequence. First quote, which starts a string, always will end the string.

Also you can use special characters for quotes. For example: `name "Hello, \"World\"!"` will be parsed correctly to the: `["name", "Hello, \"World\"!"]`

### Name tokens concatenation

!!! danger "Danger"
    This feature is experimental and has a set of bugs. This feature was written here only because it has in code. Don't use it, while this feature wasn't fixed or changed.

You can write several tokens with `Word` and `String` types in single construction and them will concatenated.

For example: `name Hello"World!"` will be split to the: `["name", "helloWorld!"]`

## First script

Let's define first config file for this course in `"Project/resources/config.json"`:

```json
{
    "version": 1,
    "states": {
        "__base__": [
            "message",
            "python"
        ]
    },
    "commands": {
        "message": {
            "aliases": ["m", "msg"],
            "type": "word",
            "children": {
                "$argument": {
                    "type": "fallback",
                    "default": "Hello, World!"
                }
            }
        },
        "python": {
            "aliases": [],
            "type": "word"
        }
    }
}
```

This is a first script, which you can run with this library:

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
def com_message(input_str: str, input_dict: untils.utils.InputDict) -> None:
    print(":", input_dict["path"][1])
    print(":", input_dict["path"][1])
    
def com_python(input_str: str, input_dict: untils.utils.InputDict) -> None:
    print("untils was created on Python!")

# Command adding.
command_system.register_command(("message",), com_message)    # Register `com_message`.
command_system.register_command(("python",), com_python)    # Register `com_python`.

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
        print(input_dict)
        print(input_dict)
    except untils.utils.InputError as e:
        # Unless input is valid.
        print(f"Incorrect input: {e}")
    except Exception as e:
        # Unknown exception.
        print(f"Unexpected exception: {e}")
    
    print(f"Is valid: {is_valid}")
    
    i -= 1
```

### Explanation

Let's view all lines in this code and understand it.

```py
# Computing paths.
DIR: str = os.path.abspath(os.path.dirname(__file__))    # The 'Project' path.
CONFIG_PATH: str = os.path.join(DIR, "resources", "config.json")    # Hardcoded path.
```

This snippet defines a path to the config in `"Project/resources/config.json"`.

```py
# The library configuration.
settings: untils.Settings = untils.Settings()    # Context settings object.
command_system: untils.CommandSystem = untils.CommandSystem(settings)    # Command system.
command_system.load_config(CONFIG_PATH)    # Load the config.
```

This snippet defines a small, but required boilerplate.
By steps:

1. We create settings. Settings - Is a universal object, where contained all important fields, like current state or warnings level.
2. We create command system. Command system - Is a main object, where contained the settings, a parsed config and commands.
3. We load config through public API in method `load_config`.

```py
# Commands functions
def com_message(input_str: str, input_dict: untils.utils.InputDict) -> None:
    print(input_dict["path"][1] if len(input_dict["path"]) == 2 else None)
    
def com_python(input_str: str, input_dict: untils.utils.InputDict) -> None:
    print("untils was created on Python!")
```

In this snippet we create two functions with `CommandCallable` signatrure.

!!! note "Note"
    The `CommandCallable` type alias defines all command with next signature:

    ```py
    def name(input_str: str, input_dict: untils.utils.InputDict) -> None:
        ...
    ```

```py
# Command adding.
command_system.register_command(("message",), com_message)    # Register `com_message`.
command_system.register_command(("python",), com_python)    # Register `com_python`.
```

Here we are registering to a route in `command_system` the new commands.

```py
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
    except untils.utils.InputError as e:
        # Unless input is valid.
        print(f"Incorrect input: {e}")
    except Exception as e:
        # Unknown exception.
        print(f"Unexpected exception: {e}")
    
    print(f"Is valid: {is_valid}")
    
    i -= 1
```

There we parse and validate a raw input. When you use `process_input` or `is_input_valid` methods, an exception may raised. There we catch `InputError` exception, which is main exception for all input exceptions. Also we need to normalize the path, because an original path uses aliases and fallbacks, but normalize convert all to keys. After all operations we execute input.

Well done!

## Conclusion

TL;DR: Config as file defines command structure, but for all command you need to write own behaviour via untils's API.

## Documentation

Next lesson: [02. Warnings Level](02-warnings-level.md "Next article in this course.").
