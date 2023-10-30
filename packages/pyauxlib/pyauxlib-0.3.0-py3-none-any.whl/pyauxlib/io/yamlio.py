"""Yaml-related functions."""
import logging
import re
from pathlib import Path
from typing import Any

import yaml
from yaml.parser import ParserError

logger = logging.getLogger(__name__)


def _loader_scientific_notation() -> type[yaml.FullLoader]:
    """Yaml loader with scientific notation.

    Returns a yaml loader that can parse numbers in scientific notation as numbers
    instead of string. This is because library 'pyyaml' uses YAML 1.1 spec instead of
    YAML 1.2 spec. See:
    # REFERENCE https://github.com/yaml/pyyaml/issues/173
    # REFERENCE https://stackoverflow.com/a/30462009
    """
    loader = yaml.FullLoader
    loader.add_implicit_resolver(  # type: ignore[no-untyped-call]
        "tag:yaml.org,2002:float",
        re.compile(
            """^(?:
     [-+]?(?:[0-9][0-9_]*)\\.[0-9_]*(?:[eE][-+]?[0-9]+)?
    |[-+]?(?:[0-9][0-9_]*)(?:[eE][-+]?[0-9]+)
    |\\.[0-9_]+(?:[eE][-+][0-9]+)?
    |[-+]?[0-9][0-9_]*(?::[0-5]?[0-9])+\\.[0-9_]*
    |[-+]?\\.(?:inf|Inf|INF)
    |\\.(?:nan|NaN|NAN))$""",
            re.X,
        ),
        list("-+0123456789."),
    )
    return loader


def load_yaml(file: Path, safe_load: bool = False) -> Any:
    """Load a yaml file and returns its contents.

     Returns an empty dictionary if the file is not found.

    Parameters
    ----------
    file : Path
        file
    safe_load : bool
        use safe load for the yaml

    Returns
    -------
    Any
        The contents of the yaml file.
    """
    try:
        with Path.open(file) as f:
            if safe_load:
                conf = yaml.safe_load(f)
            else:
                logger.warning(
                    "Probable use of unsafe `yaml.load` on file '%s'. Consider `yaml.safe_load` if the use of scientific notation is not necessary.",
                    file,
                )
                conf = yaml.load(f, Loader=_loader_scientific_notation())  # noqa: S506
            if conf is None:
                return {}
    except ParserError:
        logger.warning("Error loading the file '%s'", file)
        raise
    except FileNotFoundError:
        logger.warning("File '%s' was not found", file)
        raise

    return conf
