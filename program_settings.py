import os
from dataclasses import dataclass
from typing import ClassVar

from dotenv import load_dotenv, set_key
from pathlib import Path


@dataclass(frozen = True)
class ProgramSettings:
    ENV_PATH: ClassVar[os.PathLike[str]] =  Path('.env')


    @staticmethod
    def get_setting(key: str) -> str:
        load_dotenv(dotenv_path = ProgramSettings.ENV_PATH)
        return os.environ.get(key)


    @staticmethod
    def set_setting(key: str, value: str) -> None:
        load_dotenv(dotenv_path = ProgramSettings.ENV_PATH)
        os.environ[key] = value
        set_key(ProgramSettings.ENV_PATH, key, value)
