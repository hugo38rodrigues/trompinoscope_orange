import re
import requests

DIRECTORY_URL = "https://annuaire-sec.sso.infra.ftgroup"
VALIDATION_EXTERN_EMAIL = r'\.ext(?=@)'

class Person:
    _firstName: str
    _lastName: str
    _id: str
    _picture: str

    def __init__(self) -> None:
        self._firstName = ""
        self._lastName = ""
        self._picture = ""
        self._id = ""
        
    def __str__(self):
        return f"{self._firstName} {self._lastName} ({self._id})"
    
    def getLastName(self) -> str:
        return self._lastName

    def getFirstName(self) -> str:
        return self._firstName
    
    def getPicture(self) -> str:
        return f"./photos/{self._id}.jpg"
    
    def getId(self) -> str:
        return self._id
    
    def setLastName(self, lastName: str) -> None:
        self._lastName = lastName
    
    def setFirstName(self, firstName: str) -> None:
        self._firstName = firstName
    
    def setId(self, id: str) -> None:
        self._id = id

    def getPhotoUrl(self) -> str:
        return f"{DIRECTORY_URL}/persons/{self._id}/photo"
    
    def savePhoto(self) -> None:
        response = requests.get(self.getPhotoUrl(), verify=False)
        if response.status_code == 200:
            with open(f"./photos/{self._id}.jpg", "wb") as f:
                f.write(response.content)
        else:
            print(f"Failed to download photo for {self._id}, status code: {response.status_code}")
    
    @staticmethod
    def checkValidEmail(email: str) -> bool:
        return re.search(VALIDATION_EXTERN_EMAIL, email)
