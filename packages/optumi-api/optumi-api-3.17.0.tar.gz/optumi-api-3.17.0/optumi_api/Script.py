##
## Copyright (C) Optumi Inc - All rights reserved.
##
## You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
## To receive a copy of the licensing terms please write to contact@optumi.com or visit us at https://www.optumi.com.
##

from .Executable import Executable


class Script(Executable):
    """A class for executing Python scripts. Extends Executable."""

    def __init__(self, path: str):
        """Constructor for a Script object.

        Args:
            path (str): The file path to the script.
        """
        super().__init__(path, "python script")

    def __str__(self):
        return super().__str__()
