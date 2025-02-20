import io
import os
from typing import Any

import jinja2
from yaml import safe_load  # type: ignore


def load_settings(filename: str) -> dict[str, Any]:
    """Load the application settings."""

    def load_jinja_template(jinja_filepath: str) -> str:
        """Load a jinja template file."""
        with open(
            file=os.path.realpath(jinja_filepath), mode="r", encoding="utf-8"
        ) as fd:
            data = fd.read()
            template = jinja2.Environment(loader=jinja2.BaseLoader()).from_string(data)
            return template.render(env=os.environ)

    # Load yaml configuration into variable
    return safe_load(io.StringIO(load_jinja_template(filename)))  # type: ignore


def get_config() -> dict[str, Any]:
    """Get the application configuration."""
    config_filename = os.getenv("CONFIG_FILENAME", "src/config/config.yaml")
    config = load_settings(config_filename)
    return config


APP_CONFIG = get_config()
