from movelister.sheet import Overview


class UpdateOverview:

    @classmethod
    def update(cls, old, new):
        overview = Overview(old.new)
        overview.modifiers = new.modifiers
        return overview
