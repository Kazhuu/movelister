from movelister.sheet.sheet import MODIFIER_LIST_SHEET_NAME, MASTER_LIST_SHEET_NAME
from movelister.sheet.modifiers import Modifiers
from movelister.sheet.overview import Overview
from movelister.sheet.master import Master


class UpdateOverview:
    """
    TODO: Generate one less phase than original.
    """
    @classmethod
    def update(cls, previousOverview, name):
        """
        Create new Overview class instance with given name. Created Overview
        will use latest modifier and action data filled to by the user. New
        data is combined with existing data user filled data.
        """
        cls.newOverview = Overview(name)
        cls._updateLatestModifiers()
        cls._updateLatestActions(name)
        cls._updateActions(previousOverview)
        return cls.newOverview

    @classmethod
    def _updateActions(cls, previousOverview):
        for action in cls.newOverview.actions:
            # Find action from old overview and take modifiers from it.
            previousAction = previousOverview.findAction(action)
            if previousAction:
                action.modifiers = cls._deleteOldModifiersFromAction(previousAction)
                action.hitPhase = previousAction.hitPhase
                action.default = previousAction.default
                action.notes = previousAction.notes

    @classmethod
    def _updateLatestModifiers(cls):
        """
        Update latest modifiers from sheet which defines them to the new
        overview.
        """
        cls.newOverview.modifiers = Modifiers(MODIFIER_LIST_SHEET_NAME).getModifiers()

    @classmethod
    def _updateLatestActions(cls, viewName):
        """
        Update latest actions filtered by given view name and add them to new overview.
        """
        masterSheet = Master(MASTER_LIST_SHEET_NAME)
        cls.newOverview.actions = masterSheet.getActions(viewName)

    def _deleteOldModifiersFromAction(action):
        """
        Delete non existing modifiers from given action that doesn't exist on
        new overview anymore.
        """
        return action.modifiers
