YAML_EXTENSIONS = (".yaml", ".yml")

ALL_EXTENSIONS = YAML_EXTENSIONS

ENV_VARS = {
    "base_dir": ["CONFIG_BASEDIR", ""],
    "current_env": ["ENV", "local"],
    "files": ["CONFIG_FULLPATH", None],
}
