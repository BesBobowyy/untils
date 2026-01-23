# Warnings level

In this lesson you will understand the Warnings Level conception. Let's start.

## Theory

Warnings level - Is a debug level, which define warnings and exceptions behaviour.

Warnings level has three levels:

1. Ignore - Ignore all errors. It uses auto-correction, but debug breaks by magic behaviour. Use only in prototypes or if you know all issues and grab all responsibility to own.
2. Basic - Displays all errors as warnings in the console, but don't stop program. It uses auto-correction, but auto-correction type will be shown in the console.
3. Strict - Raises exceptions for all errors and mistakes. No auto-correction, breaks program. Activated by default. Should be activated in real products. But the `Strict` mode has own "exceptions" in behaviour: If you set non-standart config file extension and process it, you will view a warning. Also you will view warnings in other things, which don't change program behaviour.

But don't accept Warnings level as your enemy. Conversaly, it always help you, because for all type of errors it has different error messages. Also you can use Warnings level in code, because it raises exceptions, which you can catch and process. Also you can fix a much errors with this thing, just read a message.

!!! tip "Tip"
    Read docstrings, because mplib has docstrings in Google Style for ALL public objects, including classes, methods, functions, decorators and much more.

## What does it hadles?

It handles all errors and mistakes, which *contradict* with logic, standards and conventions.

Example:

```json
{
    "version": 2,
    "states": {
        "__base__": [
            "test",
            "argument"
        ],
        "__init__": [
            "hello"
        ]
    },
    "commands": {
        "test": {
            "type": "word"
        },
        "argument": {
            "type": "fallback",
            "default": null
        }
    }
}
```

!!! warning "Warning"
    An error may occur ANYWHERE, including config, input, some actions, incorrect usage and other. Read documentation and API Reference to prevent random errors.

There several mistakes, which breaks logic, standards and conventions:

1. The `"version"` field accessed as 2, but this is incorrect version, latest is 1. Logic error.
2. In `__init__` state the command `hello` is unknown. Logic error.
3. The `test` command hasn't `"aliases"` field, which is required *by convention*. Convention error.
4. The `argument` command defined as `Fallback` type, but hasn't the `$` character at name beginning. The standard error.

The reaction of these errors and mistakes depends by Warnings level:

- Ignore: "Oh, okay, let's do silent correct for user convenience.".
- Basic: "Hey, dude, there an error, but I will correct it!".
- Strict: "FIX THAT.".
  
If Warnings level uses auto-correction, it will auto-correct previous errors like that:

1. ConfigValuesWarning: Config version 2 is not valid. Change to the latest with migration. Auto-correcting to the latest.
2. Command name is not valid. Skipping.
3. *Obscured by 2 action*.
4. The `Fallback` command may has a single '$' character on name start by the standard, but it is not found.

## Practice

You can change Warnings level in Settings object by property.

Warnings level - Is a Enum with three fields.

```py
import mplib

settings: mplib.Settings = mplib.Settings()
settings.warnings_level = mplib.utils.WarningsLevel.Ignore    # Ignore mode.
print(settings.warnings_level)    # > WarningsLevel.Ignore
settings.warnings_level = mplib.utils.WarningsLevel.Basic    # Basic mode.
print(settings.warnings_level)    # > WarningsLevel.Basic
settings.warnings_level = mplib.utils.WarningsLevel.Strict    # Strict mode.
print(settings.warnings_level)    # > WarningsLevel.Strict
```

You can also use an alternative method, which always show you `FutureWarning`, but is not denied:

```py
import mplib

settings: mplib.Settings = mplib.Settings()
settings.set_warnings_level(mplib.utils.WarningsLevel.Ignore)    # Ignore mode.
print(settings.get_warnings_level())    # > WarningsLevel.Ignore
settings.set_warnings_level(mplib.utils.WarningsLevel.Basic)    # Basic mode.
print(settings.get_warnings_level())    # > WarningsLevel.Basic
settings.set_warnings_level(mplib.utils.WarningsLevel.Strict)    # Strict mode.
print(settings.get_warnings_level())    # > WarningsLevel.Strict
```

## Conclusion

TL;DR: Warnings level defines debug level, which you can use and gain benefit.

## Documentation

Next lesson: [03. State Control](03-state-control.md "Next article in this course.").
