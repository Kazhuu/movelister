from movelister.model.result import Result


class ResultFormatter:

    @classmethod
    def format(cls, result):
        return [result.result, result.action, result.modifiers]


class EndResultFormatter:

    @classmethod
    def format(cls):
        return [Result.END_MARKER, '', '']


class EmptyResultFormatter:

    @classmethod
    def format(cls):
        return ['', '', '']
