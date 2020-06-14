from movelister.sheet.details import Details
from movelister.core.iterator import DetailsIterator


class UpdateDetails:

    @classmethod
    def update(cls, modifiersSheet, parentOverview, previousDetails, name):
        newDetails = Details(name)
        cls._generateNewDetails(newDetails, parentOverview, modifiersSheet)
        cls._updateFromPreviousDetails(newDetails, previousDetails)
        return newDetails

    @classmethod
    def _generateNewDetails(cls, newDetails, parentOverview, modifiersSheet):
        actions = parentOverview.actions
        newDetails.details = list(filter(lambda detail: modifiersSheet.isValidDetail(detail), DetailsIterator(actions)))

    @classmethod
    def _updateFromPreviousDetails(cls, newDetails, previousDetails):
        for detail in newDetails.details:
            oldDetail = previousDetails.findDetail(detail)
            if oldDetail:
                cls._updateDetail(detail, oldDetail)

    @classmethod
    def _updateDetail(cls, newDetail, previousDetail):
        newDetail.action = previousDetail.action
        newDetail.inputs = previousDetail.inputs
        newDetail.phases = previousDetail.phases
        newDetail.notes = previousDetail.notes
        newDetail.modifiers = previousDetail.modifiers
