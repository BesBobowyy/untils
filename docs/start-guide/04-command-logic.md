# Command Logic

## Philosophy

In this lesson you will take all information to create command logic.

Firstly, this library has strict separation for commands: Structure - In config by the library; Logic - In game code by you.

## Theory

You don't need to write custom behaviour for command validation, parsing and executing, you can use built-in method `CommandSystem.execute`.

Firstly, you need to register new commands to current `CommandSystem` object, not type. You have four methods to control all available in object commands. These methods always use a *command path*.

Command path - Is a universal path, that defines all possible variations of parsed input path by user. For example: `["base"]` defines only input `"base"`. The path `["base", "-any"]` defines input with root command `base`, but next command may be any, how `Fallback` type.
This path is list or tuple with nested list, tuple or string. Nested string defines a single word or special placeholder. Nested list or tuple defines multiple words or special placeholders.

### Command Path special placeholders

Command path system has special placeholders by `-` character at name beginning.

!!! note "Note"
    In the current library version we have only one special placeholder.

!!! tip "Tip"
    Don't avoid the special placeholders, because they have not overlap with words, because starts with `-` character, which in input will parsed as flag or option, but not word in input path.

#### `"-any"`

This placeholder defines any word, which wrote in path.

### `CommandSystem.get_command`

This method returns a command, which defined by a path, but may return `None` if a command not defined by the path.

### `CommandSystem.register_command`

This method registers a command by a path. You need to write a function with `CallableCommand` signature. Returns a bool value as success. You cannot register any command to the path, which already busy.

### `CommandSystem.change_command`

This method changes already defined command by a path. Returns a bool value as success. You cannot place command by empty path.

### `CommandSystem.unload_command`

This method deletes a path key with their command from commands route. Returns a bool value as success. You cannot delete an empty key.

## Practice

You can write your logic to any place, but the best way - Is OOP.

Code example:

```py
# Written by untils v1.0.0r.

# In this code I don't use any detailed architecture for simplification.
# In real products you must use OOP style or another simplier.

import untils

from typing import List, Union, Literal

import os

# Computing paths.
DIR: str = os.path.abspath(os.path.dirname(__file__))    # The 'Project' path.
CONFIG_PATH: str = os.path.join(DIR, "resources", "config.json")    # Hardcoded path.

# The library configuration.
settings: untils.Settings = untils.Settings()    # Context settings object.
command_system: untils.CommandSystem = untils.CommandSystem(settings)    # Command system.
command_system.load_config(CONFIG_PATH)    # Load the config.

# Others.
class GameLogic:
    __slots__ = ["i", "player_name"]

    i: int    # Iterations count.
    player_name: Union[Literal["Player"], str]    # Player name.

    def __init__(self) -> None:
        self.i = 1
        self.player_name = "Player"
    
# Command methods.
class CommandProcessor:
    __slots__ = ["game_logic"]

    game_logic: GameLogic

    def __init__(self, game_logic: GameLogic) -> None:
        self.game_logic = game_logic

    def com_base(self, input_str: str, input_dict: untils.utils.InputDict) -> None:
        """Path: `[\"base\"]`.

        State: `__init__`.
        """

        print("Command `base`.")

        print("This is base command in this example.")

    def com_player(self, input_str: str, input_dict: untils.utils.InputDict) -> None:
        """Path: `[\"player\"]`.
        
        State: `__init__`.
        """

        print("Command `player`.")

        print("Routing to the state `context:player`.")
        settings.current_state = "context:player"    # Changing to the `context:player`.
        print("You in player settings mode. Type `help` for info.")

    def com_quit(self, input_str: str, input_dict: untils.utils.InputDict) -> None:
        """Path: `[\"quit\"]`.
        
        State: `context:player`.
        """
        
        print("Command `player:quit`.")

        print("Routing to the state `__init__`.")
        settings.current_state = "__init__"    # Changing to the `__init__`.
        print("Returning to main game...")

    def com_help(self, input_str: str, input_dict: untils.utils.InputDict) -> None:
        """Path: `[\"help\"]`.
        
        State: `context:player`.
        """
        
        print("Command `player:help`.")

        print("You in player mode, you can use:")
        print("| `quit` - Return.")
        print("| `help` - View available commands in player mode.")
        print("| `name` - Set or get player name.")
        print("| `abilities` - View player abilities (placebo option).")
        print("| `advancements` - View advancements (placebo option).")

    def com_name(self, input_str: str, input_dict: untils.utils.InputDict) -> None:
        """Path: `[\"name\"]`.
        
        State: `context:player`.
        """
        
        global player_name
        
        print("Command `player:name`.")

        if command_system.access_path(normalized_path, ("name",)):
            # Get player name.
            print(self.game_logic.player_name)
        elif command_system.access_path(normalized_path, ("name", "$argument")):
            # Set player name.
            player_name = input_dict["path"][1]
            print(f"Player name was changed to: '{player_name}'.")
        else:
            # Invalid command structure.
            print(f"Invalid command structure: {input_str}.")

    def com_abilities(self, input_str: str, input_dict: untils.utils.InputDict) -> None:
        """Path: `[\"abilities\"]`.
        
        State: `context:player`.
        """
        
        print("Command `player:abilities`.")

        print("This is placebo option without implementation for example.")

    def com_advancements(self, input_str: str, input_dict: untils.utils.InputDict) -> None:
        """Path: `[\"advancements\"]`.
        
        State: `context:player`.
        """
        
        print("Command `player:advancements`.")

        print("This is placebo option without implementation for example.")

# Others.
game_logic: GameLogic = GameLogic()
command_processor: CommandProcessor = CommandProcessor(game_logic)

# Command adding.
command_system.register_command(("base",), command_processor.com_base)    # Register `com_base`.
command_system.register_command(("player",), command_processor.com_player)    # Register `com_player`.
command_system.register_command(("quit",), command_processor.com_quit)    # Register `com_quit`.
command_system.register_command(("help",), command_processor.com_help)    # Register `com_help`.
command_system.register_command(("name",), command_processor.com_name)    # Register `com_name`.
command_system.register_command(("abilities",), command_processor.com_abilities)    # Register `com_abilities`.
command_system.register_command(("advancements",), command_processor.com_advancements)    # Register `com_advancements`.

# Main loop.
while game_logic.i > 0:
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

    game_logic.i -= 1
```

## Conclusion

TL;DR: You need to write custom logic, but command description you write in config.

## Documentation

Next lesson: [05. Logging](05-logging.md "Final article in this course.").
