class Modifier:

    def __init__(self, name, **kwargs):
        if not isinstance(name, str):
            raise ValueError('modifier must have a name as string')
        self.name = name
        self.color = kwargs.get('color', -1)
        self.phases = kwargs.get('phases', 1)
