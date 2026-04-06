import re
import requests

DIRECTORY_URL = "https://annuaire-sec.sso.infra.ftgroup"
VALIDATION_EXTERN_EMAIL = r'\.ext(?=@)'

class Person:
    _gender: str
    _firstName: str
    _lastName: str
    _email: str
    _id: str
    _picture: str

    def __init__(self) -> None:
        self._gender = ""
        self._firstName = ""
        self._lastName = ""
        self._email = ""
        self._id = ""
        self._picture = ""
        
    def __str__(self):
        return f"{self._gender} {self._firstName} {self._lastName} {'EXTERNAL ' if not self.isInternal() else ''}({self._id})"
    
    def getGender(self) -> str:
        return self._gender
    
    def getLastName(self) -> str:
        return self._lastName

    def getFirstName(self) -> str:
        return self._firstName
    
    def getPicture(self) -> str:
        return f"./photos/{self._id}.jpg"
    
    def getId(self) -> str:
        return self._id
    
    def getEmail(self) -> str:
        return self._email
    
    def setGender(self, gender: str) -> None:
        self._gender = gender
        
    def setLastName(self, lastName: str) -> None:
        self._lastName = lastName
    
    def setFirstName(self, firstName: str) -> None:
        self._firstName = firstName
    
    def setId(self, id: str) -> None:
        self._id = id

    def setEmail(self, email: str) -> None:
        self._email = email

    def isInternal(self) -> bool:
        return re.search(VALIDATION_EXTERN_EMAIL, self._email) is None

    def getPhotoUrl(self) -> str:
        return f"{DIRECTORY_URL}/persons/{self._id}/photo"
    
    def savePhoto(self) -> None:
        response = requests.get(self.getPhotoUrl(), verify=False)
        if response.status_code == 200:
            with open(f"./photos/{self._id}.jpg", "wb") as f:
                f.write(response.content)
        else:
            print(f"Failed to download photo for {self._id}, status code: {response.status_code}")
