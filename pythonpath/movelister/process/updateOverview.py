class UpdateOverview:
    """
    Class which takes care of updating two overview class instances to one
    instance. This is used when existing overview and new overview need to be
    synced and data updated.
    """

    @classmethod
    def update(cls, old, new):
        """
        TODO: Implement this update order.
        update:
            modifiedActions user data from old to new
            add user content from old to new
        """
        cls. _updateModifiedActions(old, new)
        return new

    def _updateModifiedActions(old, new):
        for modAction in new.modifiedActions:
            # Find modifiedAction from old overview and take modifiers from it.
            oldModAction = old.findModifiedAction(modAction)
            if oldModAction:
                modAction.modifiers = oldModAction.modifiers
                modAction.hitPhase = oldModAction.hitPhase
                modAction.default = oldModAction.default
