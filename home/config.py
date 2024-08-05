import toml
import pathlib

CONF = toml.load(pathlib.Path(__file__).parent / 'config.toml')

