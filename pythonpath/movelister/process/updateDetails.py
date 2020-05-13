from movelister.sheet.details import Details


class UpdateDetails:
    @classmethod
    def update(cls, previousDetails, name):
        cls.newDetails = Details(name)
        # TODO: Copy data from previous details to the new one.
        cls.newDetails.details = previousDetails.details
        return cls.newDetails

