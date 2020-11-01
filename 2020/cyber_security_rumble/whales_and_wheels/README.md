# Whales and wheels

Points: 100

This is the vulnerable code:
```python
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
```

Using a similar approach describe
[here](https://www.kevinlondon.com/2015/08/15/dangerous-python-functions-pt2.html),
I wrote an exploit in [yoink.py](yoink.py).
