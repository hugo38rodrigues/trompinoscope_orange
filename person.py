class Person:
    firstName: str
    lastName: str
    id: str
    picture: str

    def __init__(self, firstName: str, lastName: str, picture: str, id: str) -> None:
        self.firstName = firstName
        self.lastName = lastName
        self.picture = picture
        self.id = id

    def __str__(self):
        return f"{self.firstName} {self.lastName} ({self.id})"
