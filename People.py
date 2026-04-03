class People:
    firstName: str
    lastName: int
    picture: str

    def __init__(self, firstName: str, lastName: int, picture: str ) -> None:
        self.firstName = firstName
        self.lastName = lastName
        self.picture = picture