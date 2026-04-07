from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import A3

# from PIL import Image, ImageDraw

import re
from person import Person

def split_text_if_needed(c, text, font, size, max_width):
    width = c.stringWidth(text, font, size)
    if width <= max_width:
        return [text]
    words = re.split(r'[ -]+', text)
    if len(words) <= 1:
        return [text]  # Can't split, return as is
    # Split into two lines as evenly as possible
    mid = (len(words) + 1) // 2
    line1 = ' '.join(words[:mid])
    line2 = ' '.join(words[mid:])
    w1 = c.stringWidth(line1, font, size)
    w2 = c.stringWidth(line2, font, size)
    if w1 <= max_width and w2 <= max_width:
        return [line1, line2]
    else:
        # If still too wide, try different split
        if len(words) > 2:
            line1 = words[0]
            line2 = ' '.join(words[1:])
            w1 = c.stringWidth(line1, font, size)
            w2 = c.stringWidth(line2, font, size)
            if w1 <= max_width and w2 <= max_width:
                return [line1, line2]
        # Otherwise, return original
        return [text]

# --- CONFIG ---
OUTPUT_PATH = "trombinoscope.pdf"
PAGE_WIDTH, PAGE_HEIGHT = A3  # 29.7 x 42 cm

# Grid: 6 columns x 5 rows
COLS = 6
ROWS = 5

# Photo dimensions 3 x 3.99 cm (to maintain 4:3 ratio) - adjusted to fit better in the card layout
PHOTO_W = 3 * cm
PHOTO_H = 3.99 * cm

# Margin (space between cards) and Padding (inner card space)
MARGIN_CARD = 0.25 * cm
PADDING_CARD = 0.25 * cm

# Page margins
MARGIN_TOP = 3.5 * cm       # For title and page numbering

# Colors
COLOR_TITLE = HexColor("#2c3e50")
COLOR_NAME = HexColor("#333333")
COLOR_LINE = HexColor("#2c3e50")

# Text
TXT_SPACE_BEFORE = 0.3 * cm
# TXT_LINE_HEIGHT = 0.3 * cm
TXT_LINE_SPACE = 0.1 * cm
TXT_FONT_HEIGHT = 10

def build_pdf(peoples):
    c = canvas.Canvas(OUTPUT_PATH, pagesize=A3)

    # Cards size : 4 cm x 5.5 cm (including margins and padding)
    #   - Card width: photo width + 2 x padding = 3 cm + 2 x 0.5 cm = 4 cm
    #   - Card height: padding + photo height + space for text (4 lines + 3 spaces) + padding = 0.5 cm + 3.99 cm + 0.2 cm + (4 x 0.3 cm) + (3 x 0.1 cm) + 0.5 cm = 5.5 cm
    card_w = PHOTO_W + 2 * PADDING_CARD
    # card_h = PADDING_CARD + PHOTO_H + TXT_SPACE_BEFORE + 4 * TXT_LINE_HEIGHT + 3 * TXT_LINE_SPACE + PADDING_CARD
    card_h = PADDING_CARD + PHOTO_H + TXT_SPACE_BEFORE + 4 * TXT_FONT_HEIGHT + 3 * TXT_LINE_SPACE + PADDING_CARD

    # Grid total width: 6 cards + 5 margins = 6 * card_w + 5 * MARGIN_CARD = 26.5 cm
    # Left margin to center the grid: (29.7 cm - 26.5 cm) / 2 = 1.6 cm
    grid_w = COLS * card_w + (COLS - 1) * MARGIN_CARD
    margin_left = (PAGE_WIDTH - grid_w) / 2

    # Available width for text inside the card (considering padding)
    # 4 cm - 2 x 0.5 cm = 3 cm
    available_width = card_w - 2 * PADDING_CARD

    # Nb of cards per page = 6 x 5 = 30
    per_page = COLS * ROWS
    # Calculate total pages needed
    total_pages = (len(peoples) + per_page - 1) // per_page

    for page_num in range(total_pages):

        # Title display
        title_y = PAGE_HEIGHT - (MARGIN_TOP / 2)
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
            photo_y = card_y + PADDING_CARD + TXT_SPACE_BEFORE + 4 * TXT_FONT_HEIGHT + 3 * TXT_LINE_SPACE
            placeholder_img = ImageReader(person.getPicture())
            c.drawImage(placeholder_img, photo_x, photo_y, PHOTO_W, PHOTO_H,
                        preserveAspectRatio=True, mask="auto")

            # Text positions
            text_start_y = photo_y - TXT_SPACE_BEFORE - TXT_FONT_HEIGHT + TXT_FONT_HEIGHT / 2
            total_line_space = TXT_FONT_HEIGHT + TXT_LINE_SPACE

            # First name
            center_x = card_x + card_w / 2
            c.setFillColor(COLOR_NAME)
            c.setFont("Helvetica", TXT_FONT_HEIGHT)
            firstnames = split_text_if_needed(c, person.getFirstName(), "Helvetica", TXT_FONT_HEIGHT, available_width)
            lastnames = split_text_if_needed(c, person.getLastName().upper(), "Helvetica-Bold", TXT_FONT_HEIGHT, available_width)

            c.drawCentredString(center_x, text_start_y, firstnames[0])
            if len(firstnames) > 1:
                text_start_y -= total_line_space
                c.drawCentredString(center_x, text_start_y, firstnames[1])

            # Last name in uppercase
            c.setFont("Helvetica-Bold", TXT_FONT_HEIGHT)
            text_start_y -= total_line_space
            c.drawCentredString(center_x, text_start_y, lastnames[0])
            if len(lastnames) > 1:
                text_start_y -= total_line_space
                c.drawCentredString(center_x, text_start_y, lastnames[1])

        # --- Footer ---
        c.setFillColor(HexColor("#aaaaaa"))
        c.setFont("Helvetica", 7)
        c.drawCentredString(PAGE_WIDTH / 2, 1 * cm, "Document interne")

        c.showPage()

    c.save()
    # if os.path.exists(placeholder_path):
    #     os.remove(placeholder_path)
    print(f"\nPDF created: {OUTPUT_PATH}")
