"""Generate GG prayer cadres."""

from typing import IO

import click
import yaml
from ggcadres.cadres import CadreGenerator
from ggcadres.io import read_specification


@click.command("gg-cadres", help=__doc__, context_settings=dict(show_default=True))
@click.option(
    "--input",
    "-i",
    "input_",
    required=True,
    type=click.File("r"),
    help="The YAML file to read specifications from.",
)
@click.option(
    "--output",
    "-o",
    type=click.File("w"),
    default="-",
    help="The YAML file to output prayer cadres to; "
    "use '-' to output to the command line.",
)
@click.option(
    "--seed",
    "-s",
    type=click.IntRange(0),
    default=12,
    help="The seed to use for random number generation.",
)
def main(input_: IO, output: IO, seed: int):
    spec = read_specification(input_)
    cadres = CadreGenerator(
        spec["people"],
        preferred_groups=spec.get("preferred-groups"),
        forbidden_groups=spec.get("forbidden-groups"),
        num_groups=spec["num-groups"],
        seed=seed,
    ).generate()
    yaml.safe_dump([list(cadre) for cadre in cadres], output)
