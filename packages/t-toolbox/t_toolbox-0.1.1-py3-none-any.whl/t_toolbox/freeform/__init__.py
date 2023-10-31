class Freeform:
    """
    Class that can have any fields the user wants.
    """

    def __init__(self, **fields) -> None:
        for field, value in fields.items():
            self.__setattr__(field, value)
