import re
import yaml


class YAMLDumper(yaml.Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super(YAMLDumper, self).increase_indent(flow, False)


def snake_to_camel(word: str) -> str:
    return "".join(x.capitalize() or "_" for x in word.split("_"))


def camel_to_snake(name: str) -> str:
    name = re.sub("@", "", name)
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()


def check_numeric(value):
    # Checks whether the given value is of special type

    if value.lower() == "none":
        return value

    if value.lower() in ["false", "true"]:
        return value

    try:
        int(value)
        float(value)
        bool(value)
        return value
    except ValueError:
        return f'"{value}"'
