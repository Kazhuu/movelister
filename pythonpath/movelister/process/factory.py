from movelister.sheet.sheet import MODIFIER_LIST_SHEET_NAME
from movelister.sheet.modifiers import Modifiers
from movelister.sheet.overview import Overview
from movelister.model.action import Action


class OverviewFactory:

    @staticmethod
    def createOverview(masterSheet, viewName):
        """
        Factory to build Overview class instance from Master sheet instance and
        from given view name. Modifiers from Modifier sheet will also be used.
        """
        modifiers = Modifiers(MODIFIER_LIST_SHEET_NAME)
        actions = masterSheet.getActions(viewName)
        overview = Overview(viewName)
        overview.modifiers = modifiers.getModifiers()
        for action in actions:
            overview.addAction(Action(action.name, color=action.color, phases=action.phases))
        return overview
