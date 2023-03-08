from dataclasses import dataclass, field
import json


@dataclass
class Config:
    path: str
    input_filepath: str = field(init=False)
    output_dir: str = field(init=False)

    def __post_init__(self):
        with open(self.path) as json_file:
            data = json.load(json_file)
        self.input_filepath = data["ConfigFile"]["input"]
        self.output_dir = data["ConfigFile"]["output"]

