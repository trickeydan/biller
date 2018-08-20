from ruamel.yaml import YAML

yaml = YAML(typ='safe')


class YamlObject:

    def __init__(self, file):

        with open(file) as stream:
            self.data = yaml.load(stream)