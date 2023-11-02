from os import PathLike
from pathlib import Path
from typing import TextIO, Union
from harp.model import Model, Registers
from pydantic_yaml import parse_yaml_raw_as

_common_yaml_path = Path(__file__).absolute().parent.joinpath("common.yml")


def _read_common_registers(file: Union[str, PathLike, TextIO]) -> Registers:
    try:
        with open(file) as fileIO:
            return _read_common_registers(fileIO)
    except TypeError:
        return parse_yaml_raw_as(Registers, file.read())


def read_schema(
    file: Union[str, PathLike, TextIO], include_common_registers: bool = True
) -> Model:
    try:
        with open(file) as fileIO:
            return read_schema(fileIO, include_common_registers)
    except TypeError:
        schema = parse_yaml_raw_as(Model, file.read())
        if not "WhoAmI" in schema.registers and include_common_registers:
            common = _read_common_registers(_common_yaml_path)
            schema.registers = dict(common.registers, **schema.registers)
            schema.bitMasks = dict(common.bitMasks, **schema.bitMasks)
            schema.groupMasks = dict(common.groupMasks, **schema.groupMasks)
        return schema
