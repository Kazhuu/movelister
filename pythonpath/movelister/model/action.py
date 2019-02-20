class Action:

    def __init__(self, name, **kwargs):
        if not isinstance(name, str):
            raise ValueError('action must have a name as string')
        self.name = name
        self.inputs = kwargs.get('inputs', 'Default')
        self.color = kwargs.get('color', -1)
        self.phases = kwargs.get('phases', 1)

    def __eq__(self, other):
        """
        Test object equality.
        """
        return self.name == other.name

    def __ne__(self, other):
        """
        Test object nonequality.
        """
        return not self == other
