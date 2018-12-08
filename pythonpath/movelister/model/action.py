class Action:

    def __init__(self, name, **kwargs):
        self.name = name
        self.inputs = kwargs.get('inputs', 'Default')
        self.color = kwargs.get('color', -1)
        self.phases = kwargs.get('phases', 1)
