import os
import urllib3
from person import Person
import trombinoscope as trombi
from search_page import SearchPage
from detail_page import DetailPage

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def extractPersonsFromSearchPages() -> list[Person]:
    '''Extracts Persons from local Search Page results stored in ./pages.'''
    personList: list[Person] = []
    
    print("\nLooking into search pages...")
    for filename in sorted(os.listdir("./pages")):
        if not filename.endswith(".html"):
            continue

        print(f"\n - Processing file: {filename}")
        filepath = os.path.join("./pages", filename)
        searchPage = SearchPage(filepath)

        personList.extend(searchPage.getPersonList())
    return personList

def extractPersonsFromDetailedPages() -> list[Person]:
    '''Extracts Persons from local detail pages stored in ./detail_pages.'''
    personList: list[Person] = []

    print("\nLooking into detail pages...")
    for filename in sorted(os.listdir("./detail_pages")):
        if not filename.endswith(".html"):
            continue
            
        print(f"\n - Processing file: {filename}")
        filepath = os.path.join("./detail_pages", filename)
        detailPage = DetailPage(filepath)

        personList.extend(detailPage.getPersonList())
    return personList
  
if __name__ == "__main__":
    '''Main function to generate the trombinoscope PDF.'''
    
    # List of people to include in the PDF
    personList: list[Person] = []

    print("Extractin people from Directory...")
    personList.extend(extractPersonsFromSearchPages())
    personList.extend(extractPersonsFromDetailedPages())

    print("\nGet photos:")
    for person in personList:
        print(f" - {person}")
        person.savePhoto()
        
    trombi.build_pdf(personList)
