from dynaconf import Dynaconf
from importlib import resources


with resources.path("pygradus", "settings.toml") as path:
    settings = Dynaconf(
        envvar_prefix="DYNACONF",
        settings_files=[path],
    )

# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load these files in the order.
