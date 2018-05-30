class Singleton(object):
    """
    Singleton metaclass fot creating singleton objects.
    """
    instances = {}

    def __new__(cls, *args, **kwargs):
        if cls not in cls.instances:
            cls.instances[cls] = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls.instances[cls]
