import re
import os

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List

from sdRDM.generator.codegen import DataTypes
from sdRDM.generator.abstractparser import SchemaParser

MODULE_PATTERN = r"^#{1} "
OBJECT_PATTERN = r"^#{2,3}"
ATTRIBUTE_PATTERN = r"- __([A-Za-z\_]*)(\*?)__"
OPTION_PATTERN = r"([A-Za-z\_]*)\s?\:\s(.*)?"
SUPER_PATTERN = r"\[\_([A-Za-z0-9]*)\_\]"
OBJECT_NAME_PATTERN = r"^\#{2,3}\s*([A-Za-z]*)\s*"

MANDATORY_OPTIONS = ["description", "type"]


class ValidatorState(Enum):

    NEW_MODULE = auto()
    INSIDE_MODULE = auto()
    NEW_OBJECT = auto()
    INSIDE_OBJECT = auto()
    INSIDE_ATTRIBUTE = auto()
    NEW_ATTRIBUTE = auto()
    END_OF_FILE = auto()
    IDLE = auto()


@dataclass
class MarkdownParser(SchemaParser):

    module_name: str = ""
    state: ValidatorState = ValidatorState.IDLE
    attr: Dict = field(default_factory=dict)
    obj: Dict = field(default_factory=dict)
    objs: List = field(default_factory=list)
    inherits: List = field(default_factory=list)
    compositions: List = field(default_factory=list)

    @classmethod
    def parse(cls, path: str):

        if not os.path.exists(path):
            raise FileNotFoundError(
                f"File '{path}' does not exist. Please specify a valid file."
            )

        # Open the markdown file, clean it and set up the parser
        markdown_f = open(path).readlines()
        lines = [line.rstrip() for line in markdown_f if line.rstrip()]
        parser = cls()

        # Perform parsing
        for index, line in enumerate(lines):
            if bool(re.match(MODULE_PATTERN, line)):
                parser.state = ValidatorState.NEW_MODULE

            elif bool(re.match(OBJECT_PATTERN, line)):
                parser.state = ValidatorState.NEW_OBJECT

            elif bool(re.match(ATTRIBUTE_PATTERN, line)):
                parser.state = ValidatorState.NEW_ATTRIBUTE

            elif re.findall(OPTION_PATTERN, line):
                parser.state = ValidatorState.INSIDE_ATTRIBUTE

            parser.parse_line(line, index)

            if index == len(lines) - 1:
                parser.state = ValidatorState.END_OF_FILE

        return parser

    def parse_line(self, line: str, index: int):

        if self.state is ValidatorState.NEW_MODULE:
            # Parses name whenever a new module is encountered
            # Sets state to INSIDE_MODULE to catch the docstring

            self.module_name = line.replace("#", "").strip()
            self.state = ValidatorState.INSIDE_MODULE

        elif self.state is ValidatorState.INSIDE_MODULE:
            # Catches the docstring of the module

            self.module_docstring = line.strip()

        elif self.state is ValidatorState.NEW_OBJECT:
            # New objects will trigger the following workflow
            #
            # (0) Finalize previous objects for intermediate ones
            # (1) Reset object an attributes
            # (2) Gather the object name
            # (3) Set Parser state to INSIDE_OBJECT

            # Add the last attribute and object
            self._add_attribute_to_obj()
            if self.obj:
                self.objs.append(self.obj.copy())

            # Reset object and attributes
            self.obj = {"attributes": []}
            self.attr = {}

            # Parse new object
            self._parse_object_name(line, index)

            # Set state to inside an object
            self.state = ValidatorState.INSIDE_OBJECT

        elif self.state is ValidatorState.INSIDE_OBJECT:
            # Catches the docstring of the object

            if line.strip() and self.obj:
                self.obj["docstring"] = line.strip()

        elif self.state is ValidatorState.INSIDE_ATTRIBUTE:
            # Parses a line containing attribute options
            # Example: 'Type: string' or 'xml: attribute'

            self._parse_attribute_part(line)

        elif self.state is ValidatorState.NEW_ATTRIBUTE:
            # Whenever a new atribute is encountered the
            # following steps are executed
            #
            # (1) Parse possible compositions and foreign types
            # (2) Add the attribute to the object --> Triggers checks for mandatory options
            # (3) Sets up a new attribute that will be filled with options

            self._check_compositions()
            self._add_attribute_to_obj()
            self._set_up_new_attribute(line)

        elif self.state is ValidatorState.END_OF_FILE:
            # When the file has ende, usually there will be a "leftover"
            # attribute. This will be addd here and the object put into
            # the list of all objects from the module

            self.obj["attributes"].append(self.attr.copy())
            self.objs.append(self.obj.copy())

    def _parse_object_name(self, line: str, index: int):
        """Checks and parses the object (### ObjectName) for a name and possible inheritance."""

        name = re.findall(OBJECT_NAME_PATTERN, line)[0]
        parent = re.findall(SUPER_PATTERN, line)

        if not name:
            raise ValueError(
                "".join(
                    [
                        f"No object name avalaible at \033[1mline {index}\033[0m. ",
                        f"Please make sure to enter objects by using the following: \033[1m### ObjectName\033[0m",
                    ]
                )
            )
        else:
            self.obj["name"] = name

        if parent:
            self.inherits.append({"parent": parent[0], "child": self.obj["name"]})

    def _parse_attribute_part(self, line):
        """Extracts the key value relation of an attribute option (e.g. 'Type : string')"""
        key, value = re.findall(OPTION_PATTERN, line)[0]
        self.attr[key.lower()] = value

    def _check_compositions(self):
        """Checks for composition patterns and non-native types"""
        if not self.attr.get("type"):
            return None

        dtype = self.attr["type"]
        if dtype not in DataTypes.__members__:
            self.compositions.append({"module": dtype, "container": self.obj["name"]})

    def _add_attribute_to_obj(self):
        """Adds an attribute to an object only IF the mandatory fields are given.

        This method will perform a content checkup that includes all mandatory
        fields such as 'Type' and 'Description' without which a code generation
        is infeasible. Raises an error with report if tests fail.
        """

        if self._check_mandatory_options() and self.attr:
            self.obj["attributes"].append(self.attr.copy())
        elif self.attr:
            missing_fields = list(
                filter(lambda option: option not in self.attr.keys(), MANDATORY_OPTIONS)
            )
            raise ValueError(
                "".join(
                    [
                        f"Missing mandatory fields for attribute \033[1m{self.attr['name']}\033[0m ",
                        f"in object \033[1m{self.obj['name']}\033[0m: {missing_fields}",
                    ]
                )
            )

        self.attr = {}

    def _check_mandatory_options(self) -> bool:
        """Checks if an attribute covers all mandatory fields/options"""
        return (
            all(option in self.attr.keys() for option in MANDATORY_OPTIONS)
            if self.attr
            else False
        )

    def _set_up_new_attribute(self, line):
        """Sets up a new attribute based on the Markdown definition '- __Name__'."""
        name, required = re.findall(ATTRIBUTE_PATTERN, line)[0]
        self.attr["name"] = name
        self.attr["required"] = required

    def __setattr__(self, key, value):
        """Overload of the set attribute method to signalize the end of the file"""
        if value is ValidatorState.END_OF_FILE:
            self._add_attribute_to_obj()
            self.objs.append(self.obj.copy())

        super().__setattr__(key, value)