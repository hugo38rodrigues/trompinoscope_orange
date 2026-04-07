from bs4 import BeautifulSoup
from person import Person

# The structure of the result search page is as follows:
# <section id="personDetails">
#   <h2 id="pphCivilitySnGnText">M. John<span class="nameFormat">Doe</span></h2>
#   <img id="pphPhoto"data-lync="email">
#   <a id="pphSignetButton" data-source="xxxxxxxxxxxx">
#   <p id="pphPosteText">Function</p>
# </section>

class DetailPage:
    _htmlCode: BeautifulSoup = None
    _personList: list[Person] = []

    def __init__(self, filepath: str):
        '''Initializes the DetailPage object by loading the detail page HTML code from a file.'''
        self._htmlCode = None
        self._personList = []
        self._loadDetailPage(filepath)
        self._searchPersons()

    def getPersonList(self) -> list[Person]:
        '''Returns the list of Person objects extracted from the detail page.'''
        return self._personList

    def _loadDetailPage(self, filepath: str):
        '''Loads the detail page HTML code from a file.'''
        with open(filepath, "r", encoding="utf-8") as file:
            self._htmlCode = BeautifulSoup(file, "html.parser")

    def _searchPersons(self) -> None:
        '''Extracts the list of Person objects from the detail page HTML code.'''
        for section in self._htmlCode.find_all("section", id="personDetails"):
            person = self._extractPersonFromDetailPage(section)
            print (f"   - {person}")
            if person.isInternal() and not person.isTPS():
                self._personList.append(person)

    def _extractPersonFromDetailPage(self, section: str) -> Person:
        '''Extracts a Person object from a detail page section.'''
        person = Person()

        # Extract email
        for img in section.find_all("img", id="pphPhoto"):
            # The email is stored in the "data-lync" attribute of the "img" tag
            person.setEmail(img.get("data-lync").strip())
    
        # Extract Gender, Firstname, Lastname
        for h2 in section.find_all("h2", id="pphCivilitySnGnText"):
        # Exemple :
        #   - Amelie <span class="nameFormat">Chabert</span>
        #   - Mme Sophie <span class="nameFormat">Zijp Rouzier</span>
            name = h2
            
            last_name = ""
            first_names = ""
            gender = ""
            
            for content in name.contents:
                if isinstance(content, str):
                    text = content.strip()
                    if not last_name:  # before the name span
                        # Split the text to separate gender and first names
                        parts = text.split()
                        if parts and parts[0] in ("M.", "Mme", "Mr", "Mrs"):
                            gender = parts[0]
                            first_names = " ".join(parts[1:])
                        else:
                            gender = ""
                            first_names = text
                    else:  # after the name span, but since only one span, shouldn't happen
                        pass
                elif content.name == 'span' and 'nameFormat' in content.get('class', []):
                    last_name = content.text.strip()
            
            # Set the values
            person.setGender(gender)
            person.setLastName(last_name)
            person.setFirstName(first_names)

        # Extract id
        for a in section.find_all("a", id="pphSignetButton"):
            # The id is stored in the "data-source" attribute of the "a" tag
            person.setId(a.get("data-source").strip())
        
        # Extract function
        for p in section.find_all("p", id="pphPosteText"):
            # The function is stored in the text of the "p" tag
            person.setFunction(p.text.strip())

        return person
