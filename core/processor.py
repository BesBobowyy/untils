from core.utils.type_aliases import UnknownConfigType, ConfigType

from core.ioreader import IOReader
from core.config_validator import ConfigValidator
from core.parser import Parser
from core.commands_config import CommandsConfig
from core.settings import Settings

class Processor:
    """Class for config processing."""

    @staticmethod
    def load_config(settings: Settings, file_path: str, debug: bool=False) -> CommandsConfig:
        if debug: print(f"--- Load config by path: {repr(file_path)} ---")

        ### 1. IOReader ###
        if debug: print("--- Reading the file ---")
        CONTENT: UnknownConfigType = IOReader.read_file(settings, file_path)
        if debug: print(f"Content: {CONTENT}")

        ### 2. ConfigValidator ###
        if debug: print("--- Validating the config ---")
        RAW_CONFIG: ConfigType = ConfigValidator.validate_config(settings, CONTENT)
        if debug: print(f"Intermediate config: {RAW_CONFIG}")

        ### 3. Parser ###
        if debug: print("--- Parsing ---")
        CONFIG: CommandsConfig = Parser.parse_config(RAW_CONFIG)
        if debug: print("Parsed config: <TODO>")

        return CONFIG



if __name__ == "__main__":
    from core.utils.enums import WarningsLevel    # pyright: ignore[reportUnusedImport]

    import os

    FILE_PATH: str = os.path.join(
        os.path.abspath(os.path.dirname(os.path.dirname(__file__))),
        "code_tests", "resources", "commands_2.json"
    )
    SETTINGS: Settings = Settings()
    SETTINGS.warnings_level = WarningsLevel.Basic

    CONFIG: CommandsConfig = Processor.load_config(SETTINGS, FILE_PATH)
    print(CONFIG)