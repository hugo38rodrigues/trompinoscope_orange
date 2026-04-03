from bs4 import BeautifulSoup
import re
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PIL import Image, ImageDraw
import os
from reportlab.lib.pagesizes import A3
import requests
import urllib3
from person import Person
import time
from urllib.parse import urljoin
import sys

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

VALIDATION_EXTERN_EMAIL = r'\.ext(?=@)'

# --- CONFIG ---
OUTPUT_PATH = "trombinoscope.pdf"
PAGE_WIDTH, PAGE_HEIGHT = A3  # 29.7 x 42 cm

# Grid: 4 columns x 4 rows
COLS = 4
ROWS = 4

# Photo dimensions
PHOTO_W = 4.5 * cm
PHOTO_H = 6 * cm

# Margin (space between cards) and Padding (inner card space)
MARGIN_CARD = 0.5 * cm
PADDING_CARD = 0.5 * cm

# Page margins
MARGIN_TOP = 3.5 * cm

# Colors
COLOR_TITLE = HexColor("#2c3e50")
COLOR_NAME = HexColor("#333333")
COLOR_LINE = HexColor("#2c3e50")

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


def build_pdf(peoples, output_path):
    c = canvas.Canvas(output_path, pagesize=A3)

    card_w = PHOTO_W + 2 * PADDING_CARD
    card_h = PHOTO_H + 2 * PADDING_CARD + 1.8 * cm

    # Center the grid horizontally
    grid_w = COLS * card_w + (COLS - 1) * MARGIN_CARD
    margin_left = (PAGE_WIDTH - grid_w) / 2

    per_page = COLS * ROWS
    total_pages = (len(peoples) + per_page - 1) // per_page

    for page_num in range(total_pages):

        # --- Simple header ---
        title_y = PAGE_HEIGHT - 2 * cm
        c.setFillColor(COLOR_TITLE)
        c.setFont("Helvetica-Bold", 28)
        c.drawCentredString(PAGE_WIDTH / 2, title_y, "Trombinoscope")

        # Line below the title
        line_y = title_y - 0.4 * cm
        c.setStrokeColor(COLOR_LINE)
        c.setLineWidth(1.5)
        c.line(PAGE_WIDTH / 2 - 4 * cm, line_y, PAGE_WIDTH / 2 + 4 * cm, line_y)

        # Page number
        c.setFont("Helvetica", 9)
        c.setFillColor(HexColor("#999999"))
        c.drawCentredString(PAGE_WIDTH / 2, line_y - 0.6 * cm, f"Page {page_num + 1} / {total_pages}")

        # --- Grid ---
        start_idx = page_num * per_page
        page_people: list[Person] = peoples[start_idx: start_idx + per_page]

        for i, person in enumerate(page_people):
            col = i % COLS
            row = i // COLS

            card_x = margin_left + col * (card_w + MARGIN_CARD)
            card_y = PAGE_HEIGHT - MARGIN_TOP - (row + 1) * card_h - row * MARGIN_CARD

            # Thin border
            c.setStrokeColor(HexColor("#cccccc"))
            c.setLineWidth(0.5)
            c.rect(card_x, card_y, card_w, card_h, fill=0, stroke=1)

            # Photo
            photo_x = card_x + PADDING_CARD
            photo_y = card_y + PADDING_CARD + 1.8 * cm
            placeholder_img = ImageReader(person.picture)
            c.drawImage(placeholder_img, photo_x, photo_y, PHOTO_W, PHOTO_H,
                        preserveAspectRatio=True, mask="auto")

            # First name
            center_x = card_x + card_w / 2
            c.setFillColor(COLOR_NAME)
            c.setFont("Helvetica", 10)
            c.drawCentredString(center_x, card_y + PADDING_CARD + 0.8 * cm, person.firstName)

            # Last name in uppercase
            c.setFont("Helvetica-Bold", 10)
            c.drawCentredString(center_x, card_y + PADDING_CARD + 0.2 * cm, person.lastName.upper())

        # --- Footer ---
        c.setFillColor(HexColor("#aaaaaa"))
        c.setFont("Helvetica", 7)
        c.drawCentredString(PAGE_WIDTH / 2, 1 * cm, "Document interne")

        c.showPage()

    c.save()
    # if os.path.exists(placeholder_path):
    #     os.remove(placeholder_path)
    print(f"PDF created: {output_path}")


def extractDetailPageURL() -> list[str]:
    '''Extracts detail page URLs from local HTML files.'''
    urlsId: list[str] = []
    
    print("Searching for detail page URLs...")
    for filename in os.listdir("./pages"):
        if not filename.endswith(".html"):
            continue

        print(f" - Processing file: {filename}")
        filepath = os.path.join("./pages", filename)
        with open(filepath, "r", encoding="utf-8") as f:
            page = BeautifulSoup(f, "html.parser")

        # All <ul class="media-list">    
        for ul in page.find_all("ul", class_="media-list"):
            # In each ul, all <a class="pull-left">
            for a in ul.find_all("a", class_="pull-left"):
                email = a.contents[1].get("data-lync").strip()
                if re.search(VALIDATION_EXTERN_EMAIL, email):
                    pass
                else :
                    url = a.get("href")
                    print(f" - URL found: {url}")    
                    urlsId.append(url)

    return urlsId

def getPersonListFromDetailPage(urlsId: list[str]) -> list[Person]:
    personList: list[Person] = []
    person: Person
    
    for urlId in urlsId:
        response = requests.get(urlId, verify=False)
        cleanedResponse = response.text.replace("\r\n", "").replace("\t", "")

        person = extractPersonFromDetailPage(cleanedResponse, urlId)
        personList.append(person)

    return personList
        

def extractPersonFromDetailPage (detailPage: str, urlId: str) -> Person:

    person: Person   
    page = BeautifulSoup(detailPage, "html.parser")

    nom: str=""
    prenom: str=""
    for section in page.find_all("section", id="personDetails"):
        # Last name / First name
        h2 = section.find(id="pphCivilitySnGnText")
        if h2:
            # Get the last name from text and span
            nom_span = h2.find("span", class_="nameFormat")
            nom = nom_span.get_text(strip=True) if nom_span else ""

            # The first name is in the raw text before the span
            parts = h2.find(string=True, recursive=False).strip().split()
            prenom = parts[1] if len(parts) > 1 else ""
            
            photo_img = section.find("img", id="pphPhoto")

        user_id = urlId.split("/")[-1]

        if photo_img:
            photo_url = urljoin(urlId, photo_img["src"])
            response = requests.get(photo_url, verify=False)
            if response.status_code == 200:
                # Save to file
                with open(f"./photos/{user_id}.jpg", "wb") as f:
                    f.write(response.content)
                    
    time.sleep(1)
    person = Person(firstName=prenom, lastName=nom, picture=f"./photos/{user_id}.jpg")

    return person

if __name__ == "__main__":

    # List of people to include in the PDF
    personList: list[Person] = []

    print("Generating the trombinoscope...")
    if len(sys.argv) > 1:
        print("## Mode: generation from already downloaded detail pages ##")
        arg = sys.argv[1]

        if arg == "1":
            detailPagesList = []
            for filename in os.listdir("./detail_pages"):
                if not filename.endswith(".html"):
                    continue

                filepath = os.path.join("./detail_pages", filename)
                with open(filepath, "r", encoding="utf-8") as f:
                    detailPagesList.append(filepath)
            personList = getPersonListFromDetailPage(detailPagesList)
    else:
        urlsId: list[str]
        print("## Mode: generation from online detail pages ##")
        urlsId = extractDetailPageURL()
        
        personList = getPersonListFromDetailPage(urlsId)

        print("People found:")
        for person in personList:
            print(f" - {person.firstName} {person.lastName} {person.picture}")
        
    build_pdf(personList, OUTPUT_PATH)
