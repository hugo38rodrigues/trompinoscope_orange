import os
import requests
import urllib3
from person import Person
import time
from urllib.parse import urljoin
import trombinoscope as trombi
from search_page import SearchPage

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# def create_placeholder(width_px, height_px):
#     """Simple placeholder with silhouette."""
#     img = Image.new("RGB", (width_px, height_px), color=(230, 230, 230))
#     draw = ImageDraw.Draw(img)
#     cx, cy = width_px // 2, height_px // 2
#     r = int(width_px * 0.17)
#     head_y = cy - int(height_px * 0.1)
#     draw.ellipse([cx - r, head_y - r, cx + r, head_y + r], fill=(180, 180, 180))
#     bw = int(width_px * 0.32)
#     bt = head_y + r + int(height_px * 0.02)
#     bb = cy + int(height_px * 0.35)
#     draw.ellipse([cx - bw, bt, cx + bw, bb], fill=(180, 180, 180))
#     path = "/tmp/placeholder.png"
#     img.save(path)
#     return path


def extractURLIDFromResultSearchPage(detailPage: str) -> list[str]:
    urlsIdList: list[str] = []

    # Structure of the page:
    # <ul class="media-list">
    #   <li class="media">
    #     <a class="pull-left" href="https://example.com/detail/123">
    #       <img src="photo.jpg" data-lync="
    #       <span class="nameFormat">Doe</span> John">
    #     </a>

    # All <ul class="media-list">    
    for ul in detailPage.find_all("ul", class_="media-list"):
        # In each ul, all <a class="pull-left">
        for a in ul.find_all("a", class_="pull-left"):
            email = a.contents[1].get("data-lync").strip()
            if (Person.checkValidEmail(email)):
                print (f" - Ignore external email: {email}")
                pass
            else :
                urlId = a.get("href")
                print (f" - Valid email found: {email}, {urlId}")
                urlsIdList.append(urlId)

    return urlsIdList

def extractPersonsFromSearchPages() -> list[Person]:
    '''Extracts Persons from local HTML files.'''
    personList: list[Person] = []
    
    print("Looking into search pages...")
    for filename in os.listdir("./pages"):
        if not filename.endswith(".html"):
            continue

        print(f" - Processing file: {filename}")
        filepath = os.path.join("./pages", filename)
        searchPage = SearchPage(filepath)

        personList.extend(searchPage.getPersonList())
    return personList

def getPersonListFromDetailPageUrls(urlsId: list[str]) -> list[Person]:
    personList: list[Person] = []
    person: Person
    
    for urlId in urlsId:
        response = requests.get(urlId, verify=False)
        cleanedResponse = response.text.replace("\r\n", "").replace("\t", "")

        person = extractPersonFromDetailPage(cleanedResponse)
        personList.append(person)

    return personList
        
def getPersonListFromDetailPages() -> list[Person]:
    personList: list[Person] = []
    person: Person

    detailPagesList = []
    for filename in os.listdir("./detail_pages"):
        if not filename.endswith(".html"):
            continue
            
        print(f" - Processing file: {filename}")
        filepath = os.path.join("./detail_pages", filename)
        with open(filepath, "r", encoding="utf-8") as f:
            detailPagesList.append(filepath)

    if detailPagesList:
        print("Detail pages found, processing them...")

        for detailPage in detailPagesList:  
            with open(detailPage, "r", encoding="utf-8") as f:
                cleanedResponse = f.read().replace("\r\n", "").replace("\t", "")

            person = extractPersonFromDetailPage(cleanedResponse)
            personList.append(person)

    return personList

def extractPersonFromDetailPage (detailPage: str) -> Person:

    person: Person = Person()
    page = BeautifulSoup(detailPage, "html.parser")

    # The structure of the result search page is as follows:
    # <section id="personDetails">
    #   <h2 id="pphCivilitySnGnText">M. John
    #     <span class="nameFormat">Doe</span>
    #   </h2>
    #   <img id="pphPhoto" src="/persons/xxxxxx/photo;jsessionid=xxxxxxxxxxx"/>
    for section in page.find_all("section", id="personDetails"):
        # Last name / First name / Id
        h2 = section.find(id="pphCivilitySnGnText")
        if h2:
            # Get the last name from text and span
            nom_span = h2.find("span", class_="nameFormat")
            person.setLastName(nom_span.get_text(strip=True))

            # The first name is in the raw text before the span
            # parts[0]=Gender parts[1]=FirstName
            parts = h2.find(string=True, recursive=False).strip().split()
            person.setFirstName(parts[1])
            
            # ID is in the img src
            # example: src="/persons/xxxxxx/photo;jsessionid=xxxxxxxxxxxxxxx"/>
            src=section.find("img", id="pphPhoto").get("src")
            # The ID is the part between "/persons/" and "/photo"
            person.setId(src.split("/")[2])

    person.savePhoto()
                    
    time.sleep(1)

    return person

if __name__ == "__main__":
    '''Main function to generate the trombinoscope PDF.'''
    
    # List of people to include in the PDF
    personList: list[Person] = []

    print("Generating the trombinoscope...")
    personList.extend(extractPersonsFromSearchPages())

    # print("Check for provided detail pages...")
    # personList.extend(getPersonListFromDetailPages())

    print("People found:")
    for person in personList:
        print(f" - {person}")
        time.sleep(0.5)         # Limit API calls
        person.savePhoto()
        
    trombi.build_pdf(personList)
