import builtins
import yaml
import toml

from anytree import LevelOrderIter
from typing import Union
from typing_utils import get_origin

from sdRDM.linking.nodes import AttributeNode, ClassNode
from sdRDM.tools.utils import YAMLDumper

DEFAULT_MAPPINGS = {"list": list, "dict": dict}
BUILTIN_TYPES = tuple(
    getattr(builtins, t)
    for t in dir(builtins)
    if isinstance(getattr(builtins, t), type)
)


def build_guide_tree(obj, parent=None, outer=None, constants={}):
    """Creates a binary tree representation from the underlying data model.

    Args:
        obj (Callable): Object from which the tree is constructed.
        parent (Node, optional): Parent node to which the node will be added if provided. Defaults to None.
        outer (Any, optional): Data structure into which the actual data type is wrapped. Defaults to None.

    Returns:
        Node: Tree representation of the data model.
    """

    if parent is None:
        parent = ClassNode(
            obj.__name__,
            parent=parent,
            module=obj.__module__,
            class_name=obj.__name__,
            outer_type=outer,
            constants=constants,
        )

    if outer == list:
        parent = AttributeNode(name="0", parent=parent)

    for name, field in obj.__fields__.items():
        inner_type = field.type_
        outer_type = field.outer_type_

        if outer_type and _is_iterable(outer_type):
            value = get_origin(outer_type)()
            outer_type = get_origin(outer_type)
        else:
            value = None
            outer_type = None

        current_parent = AttributeNode(
            name, parent=parent, outer_type=outer_type, value=value
        )

        if get_origin(inner_type) is Union:
            # Adress Union types
            inner_type = list(inner_type.__args__)
        else:
            # If not, put the single type in a list
            inner_type = [inner_type]

        for dtype in inner_type:
            if hasattr(dtype, "__fields__"):
                build_guide_tree(
                    dtype, current_parent, outer=outer_type, constants=constants
                )

    return parent


def _is_iterable(data_type):
    """Checks whether the given typing.XYZ is of type List or Dict"""

    origin = get_origin(data_type)

    if origin is None:
        return False
    elif origin.__name__ == "Union":
        return False

    return True


def generate_template(obj, out: str, simple: bool = True) -> None:
    """Generates a template for linking two datasets."""

    template = {
        "__model__": obj.__name__,
        "__sources__": {
            "LibName": "URL to the library",
        },
    }

    # Add attributes of root objects
    template[obj.__name__] = {
        n.name: "Enter target"
        for n in obj.create_tree()[0].children
        if isinstance(n, AttributeNode) and len(n.children) == 0
    }

    for node in LevelOrderIter(obj.create_tree()[0]):
        path = _get_path(node.node_path)

        if node.children and path:
            attr_template = {
                n.name: "Enter target" for n in node.children if len(n.children) == 0
            }

            if simple:
                template[path] = attr_template
            else:
                template[path] = [
                    {
                        "attribute": "Name of the target to check for",
                        "pattern": r".*",
                        "targets": attr_template,
                    }
                ]

    with open(out, "w") as f:
        if not simple:
            f.write(yaml.dump(template, Dumper=YAMLDumper, sort_keys=False))
            return

        f.write(toml.dumps(template))


def _get_path(path):
    """Parses a tree path to a symbolic path through the data model"""
    return ".".join([node.name for node in path if node.name[0].islower()])
