class ResultFormatter:

    @classmethod
    def format(cls, result):
        return [result.result, result.action, result.modifiers]
