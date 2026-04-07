import re
from time import time
import requests
import os

DIRECTORY_URL = "https://annuaire-sec.sso.infra.ftgroup"
VALIDATION_EXTERN_EMAIL = r'\.ext(?=@)'

class Person:
    _gender: str
    _firstName: str
    _lastName: str
    _email: str
    _id: str
    _picture: str
    _function: str

    def __init__(self) -> None:
        self._gender = ""
        self._firstName = ""
        self._lastName = ""
        self._email = ""
        self._id = ""
        self._picture = ""
        self._function = ""
        
    def __str__(self):
        display:str = f"{self.getGender()} {self.getFirstName()} {self.getLastName()}"
        display += f", {self.getFunction()}"
        if self.isInternal():
            display += f" ({self.getId()})"
        if self.isTPS():
            display += " (TPS)"
        if not self.isInternal():
            display += " (Externe)"

        return display
    
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
    
    def getFunction(self) -> str:
        return self._function if self._function else "Non renseigné"
    
    def setGender(self, gender: str) -> None:
        if gender=="":
            self._gender = "M./Mme"
        else:
            self._gender = gender

    def setLastName(self, lastName: str) -> None:
        self._lastName = lastName
    
    def setFirstName(self, firstName: str) -> None:
        self._firstName = firstName
    
    def setId(self, id: str) -> None:
        self._id = id

    def setEmail(self, email: str) -> None:
        self._email = email

    def setFunction(self, function: str) -> None:
        self._function = function

    def isInternal(self) -> bool:
        return re.search(VALIDATION_EXTERN_EMAIL, self._email) is None
    
    def isTPS(self) -> bool:
        return self._function in ("TPS Temps libéré", "TPS Mécénat de compétences")
    
    def getPhotoUrl(self) -> str:
        return f"{DIRECTORY_URL}/persons/{self._id}/photo"
    
    def savePhoto(self) -> None:
        photo_path = f"./photos/{self._id}.jpg"
        if not os.path.exists(photo_path):
            time.sleep(0.5)         # Limit API calls
            response = requests.get(self.getPhotoUrl(), verify=False)
            if response.status_code == 200:
                with open(photo_path, "wb") as f:
                    print (f"   - Downloading photo for {self._firstName} {self._lastName}...")
                    f.write(response.content)
            else:
                print(f"Failed to download photo for {self._id}, status code: {response.status_code}")
