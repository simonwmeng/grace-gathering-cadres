# Grace Gathering cadre generator

## ?!

This repository contains a CLI, `gg-cadres`, to generate cadres (subgroups) for things
such as Grace Gatherings.

## Installation

### With *conda*

In a terminal, type

```bash
conda env create -f environment.yaml
```

### Without *conda*

TODO: Add this section

## Generating cadres

Create a YAML file matching the following specification:

```yaml
people: (list[str]) the people to divide into cadres
num-groups: (int) the number of desired groups
preferred-groups: (list[list[str]]) people to always group together
forbidden-groups: (list[list[str]]) people to avoid grouping together
```

The generator may not always be able to avoid generating forbidden groups depending on
what preferred and forbidden groups you specify.

To generate cadres, activate the enviroment (e.g., `conda activate gg-cadres`) and run
the following:

```bash
gg-cadres -i <specification.yaml> [-o <output.yaml>] [-s <seed>]
```

If you do not specify `--output/-o`, output will be printed to stdout.
