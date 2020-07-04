class Input:

    def __init__(self, name, **kwargs):
        if not isinstance(name, str):
            raise ValueError('input must have a name as string')
        self.name = name
        self.color = kwargs.get('color', -1)
