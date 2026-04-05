from bs4 import BeautifulSoup
from person import Person

# Structure of the page:
# <div class="div-infos-details">
# 	<img class="pull-left" data-lync="khalid.zaida@orange.com">
# 	<a class="pull-left" href="https://annuaire-sec.sso.infra.ftgroup/persons/iRafdcYFeFUDjHYH_9OurA%3D%3D">
# 	    <img class="media-object" data-original="/persons/iRafdcYFeFUDjHYH_9OurA%3D%3D/photo" data-lync="khalid.zaida@orange.com" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsQAAA7EAZUrDhsAAAANSURBVBhXYzh8+PB/AAffA0nNPuCLAAAAAElFTkSuQmCC">
# 	</a>
# 	<div class="media-body">
# 		<h3 class="media-heading">
# 			<a href="https://annuaire-sec.sso.infra.ftgroup/persons/iRafdcYFeFUDjHYH_9OurA%3D%3D">
# 				M. <span class="nameFormat">Zaida</span> Khalid <span style="color: #cd5e00"></span>
# 			</a>
# 		</h3>
# 		<p class="poste">Ingénieur d'étude confirmé</p>
# 		<div class="list-entities list-inline">
# 			<a class="entityclass" href="https://annuaire-sec.sso.infra.ftgroup/entities/ou=Orange,ou=entities" data-hasqtip="0">Orange</a>/<a class="entityclass" href="https://annuaire-sec.sso.infra.ftgroup/entities/ou=OF,ou=Orange,ou=entities" data-hasqtip="1">OF</a>/<a class="entityclass" href="https://annuaire-sec.sso.infra.ftgroup/entities/ou=DSI,ou=OF,ou=Orange,ou=entities" data-hasqtip="2">DSI</a>/<a class="entityclass" href="https://annuaire-sec.sso.infra.ftgroup/entities/ou=DB2B,ou=DSI,ou=OF,ou=Orange,ou=entities" data-hasqtip="3">DB2B</a>/<a class="entityclass" href="https://annuaire-sec.sso.infra.ftgroup/entities/ou=MOBILITE,ou=DB2B,ou=DSI,ou=OF,ou=Orange,ou=entities" data-hasqtip="4">MOBILITE</a>/<a class="entityclass" href="https://annuaire-sec.sso.infra.ftgroup/entities/ou=CCM,ou=MOBILITE,ou=DB2B,ou=DSI,ou=OF,ou=Orange,ou=entities" data-hasqtip="5">CCM</a>
# 		</div>
# 	</div>
# </div>

class SearchPage:
    _htmlCode: BeautifulSoup
    _personList: list[Person] = []

    def __init__(self, filepath: str):
        '''Initializes the SearchPage object by loading the search page HTML code from a file.'''
        self._loadSearchPage(filepath)
        self._searchPersons()

    def getPersonList(self) -> list[Person]:
        '''Returns the list of Person objects extracted from the search page.'''
        return self._personList

    def _loadSearchPage(self, filepath: str):
        '''Loads the search page HTML code from a file.'''
        with open(filepath, "r", encoding="utf-8") as file:
            self._htmlCode = BeautifulSoup(file, "html.parser")

    def _searchPersons(self) -> None:
        '''Extracts the list of Person objects from the search page HTML code.'''
        for div in self._htmlCode.find_all("div", class_="div-infos-details"):
            person = self._extractPersonFromResultSearchPage(div)
            print (f" - Person extracted: {person}")
            if person.isInternal():
                self._personList.append(person)

    def _extractPersonFromResultSearchPage(self, div: str) -> Person:
        '''Extracts a Person object from a search result div.'''
        person = Person()

        # Extract email, id
        for a in div.find_all("a", class_="pull-left"):
            # The email is stored in the "data-lync" attribute of the "img" tag inside the "a" tag
            person.setEmail(a.find("img").get("data-lync").strip())
            # The id is stored in the "href" attribute of the "a" tag
            person.setId(a.get("href").split("/")[-1])
    
        # Extract Firstname, Lastname
        for h3 in div.find_all("h3", class_="media-heading"):
            # The firstname and lastname are stored in the "a" tag inside the "h3" tag
            name = h3.find("a").text.strip().split(" ")
            person.setGender(name[0])
            person.setFirstName(name[1])
            person.setLastName(name[2])
        
        return person
