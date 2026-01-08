import builtins
import configparser
import dataclasses
import os


@dataclasses.dataclass(init=False)
class NeatConfig:
    pop_size: int
    generations: int
    target_fitness: float
    inputs: int
    outputs: int
    workers: int
    speciation: bool
    save_genome: bool
    target_species: int
    elitism: int
    log_progress: bool
    parallel: bool

    prob_create_node: float
    prob_create_gene: float
    prob_remove_node: float
    prob_remove_gene: float

    weight_init_mean: float
    weight_init_stdev: float
    weight_max_value: float
    weight_min_value: float
    weight_mutate_power: float
    weight_mutate_rate: float
    weight_replace_rate: float

    bias_init_mean: float
    bias_init_stdev: float
    bias_max_value: float
    bias_min_value: float
    bias_mutate_power: float
    bias_mutate_rate: float
    bias_replace_rate: float

    def __setitem__(self, item: str, value: str | bool | float | int):
        setattr(self, item, value)


class Config:
    def __init__(self, config_file: str, object: NeatConfig) -> None:
        if not os.path.isfile(config_file):
            raise FileNotFoundError(f"File {config_file} not found.")

        self.parser = configparser.ConfigParser()
        with open(config_file) as file:
            self.parser.read_file(file)

        self._config_object = object

    def _assign(self, section: str, field: str, type: type | None):
        try:
            match type:
                case builtins.int:
                    value = self.parser.getint(section, field)
                case builtins.float:
                    value = self.parser.getfloat(section, field)
                case builtins.str:
                    value = self.parser.get(section, field)
                case builtins.bool:
                    value = self.parser.getboolean(section, field)
                case _:
                    raise ValueError("Unsupported type")
            self._config_object[field] = value
        except Exception as e:
            raise ValueError(f"Failed to parse '{field}' in section [{section}]: {e}")

    def flatten(self, list: list[list[tuple[str, str]]]) -> list[str]:
        return [x[0] for xs in list for x in xs]

    def _validate_missing(self, fields: list[str]):
        config = self.flatten([list(self.parser.items(s)) for s in self.parser.sections()])
        missing = False
        for field in fields:
            if field not in config:
                print(f"Attribute {field.lower()} missing")
                missing = True

        if missing:
            raise ValueError("Missing required configuration fields")

    def parse(self) -> NeatConfig:
        fields: dict[str, type] = NeatConfig.__dict__.get("__annotations__")  # type: ignore
        configuration_attributes = list(fields.keys())

        self._validate_missing(configuration_attributes)

        for section in self.parser.sections():
            for prop in list(self.parser.items(section)):
                if (prop[0]) not in configuration_attributes:
                    print(f"Attribute {prop[0]} unknown, ignored")
                    continue

                self._assign(section, prop[0], fields.get(prop[0]))

        return self._config_object
