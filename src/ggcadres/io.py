"""Input/output."""

from typing import IO

import yaml

REQUIRED_KEYS = {"people", "num-groups"}
OPTIONAL_KEYS = {"preferred-groups", "forbidden-groups"}


def read_specification(handle: IO) -> dict:
    """Read a specification.

    Args:
        handle: A handle to a YAML file.

    Returns:
        The loaded specification.
    """
    res = yaml.safe_load(handle)

    # Ensure that only certain keys exist.

    for key in REQUIRED_KEYS:
        if key not in res:
            raise KeyError(f"missing key from specification: {key!r}")

    if bad_keys := set(res.keys()) - REQUIRED_KEYS - OPTIONAL_KEYS:
        raise KeyError(f"extra keys detected in specification: {bad_keys!r}")

    # Ensure that people in preferred and forbidden groupings exist.

    people = set(res["people"])

    for key in OPTIONAL_KEYS:
        for group in res.get(key, []):
            if bad_people := set(group) - people:
                raise ValueError(
                    f"non-existent people detected in {key}: {bad_people!r}"
                )

    return res
