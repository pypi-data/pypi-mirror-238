from typing import Tuple, List, Dict, Union
import mystring
from pnostic.structure import Logger, RepoResultObject, RepoObject, RepoSifting
import pnostic.utils as utils

class app(Logger):
    def __init__(self):
        super().__init__()

    def initialize(self) -> bool:
        return True

    def name(self) -> mystring.string:
        return mystring.string.of("Raw Save")

    def clean(self) -> bool:
        return True

    def message(self, msg: str) -> bool:
        return True

    def emergency(self, msg:str)->bool:
        utils.custom_msg(msg, utils.bcolors.FAIL)
        return True

    def parameter(self, parameter: RepoObject) -> bool:
        parameter.frame.to_pickle(
            self.file_name(parameter, parameter.filename, suffix=".pkl")
        )
        return True

    def result(self, result: RepoResultObject) -> bool:
        result.frame.to_pickle(
            self.file_name(result, result.tool_name, suffix=".pkl")
        )
        return True
