class Person:
    firstName: str
    lastName: str
    picture: str

    def __init__(self, firstName: str, lastName: str, picture: str ) -> None:
        self.firstName = firstName
        self.lastName = lastName
        self.picture = picture