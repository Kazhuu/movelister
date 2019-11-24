from movelister.sheet import MODIFIER_LIST_SHEET_NAME, Modifiers, Overview, Master, MASTER_LIST_SHEET_NAME


class UpdateOverview:
    """
    TODO: Generate one less phase than original.
    """
    @classmethod
    def update(cls, previousOverview, name):
        """
        """
        cls.newOverview = Overview(name)
        cls._updateLatestModifiers()
        cls._updateLatestModifiedActions(name)
        cls._updateModifiedActions(previousOverview)
        return cls.newOverview

    @classmethod
    def _updateModifiedActions(cls, previousOverview):
        for modAction in cls.newOverview.modifiedActions:
            # Find modifiedAction from old overview and take modifiers from it.
            previousModAction = previousOverview.findModifiedAction(modAction)
            if previousModAction:
                modAction.modifiers = cls._deleteOldModifiersFromAction(previousModAction)
                modAction.hitPhase = previousModAction.hitPhase
                modAction.default = previousModAction.default

    @classmethod
    def _updateLatestModifiers(cls):
        """
        Update latest modifiers from sheet which defines them to the new
        overview.
        """
        cls.newOverview.modifiers = Modifiers(MODIFIER_LIST_SHEET_NAME).getModifiers()

    @classmethod
    def _updateLatestModifiedActions(cls, viewName):
        """
        Update latest modified actions filtered by given view name and add them
        to new overview.
        """
        masterSheet = Master(MASTER_LIST_SHEET_NAME)
        cls.newOverview.modifiedActions = masterSheet.getModifiedActions(viewName)

    def _deleteOldModifiersFromAction(action):
        """
        Delete non existing modifiers from given action that doesn't exist on
        new overview anymore.
        """
        return action.modifiers
