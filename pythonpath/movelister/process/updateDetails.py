from movelister.sheet.details import Details
from movelister.core.iterator import DetailsIterator


class UpdateDetails:

    @classmethod
    def update(cls, modifiersSheet, parentOverview, previousDetails, name):
        newDetails = Details(name)
        actions = parentOverview.actions
        newDetails.details = list(filter(lambda detail: modifiersSheet.isValidDetail(detail), DetailsIterator(actions)))
        # TODO: Copy data from previous details to the new one.
        # newDetails.details = previousDetails.details
        return newDetails

