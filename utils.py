import os
import img2pdf
import fitz

from PyPDF2 import PdfMerger
from PyPDF2 import PdfReader
from PyPDF2 import PdfWriter

from docx import Document

from reportlab.pdfgen import canvas


def image_to_pdf(image):

    pdf = os.path.splitext(image)[0] + ".pdf"

    with open(pdf, "wb") as f:
        f.write(img2pdf.convert(image))

    return pdf


def docx_to_pdf(doc):

    pdf = os.path.splitext(doc)[0] + ".pdf"

    document = Document(doc)

    c = canvas.Canvas(pdf)

    y = 800

    for para in document.paragraphs:

        c.drawString(40, y, para.text)

        y -= 20

        if y < 40:

            c.showPage()

            y = 800

    c.save()

    return pdf


def merge_pdfs(files, output):

    merger = PdfMerger()

    for pdf in files:

        merger.append(pdf)

    merger.write(output)

    merger.close()


def extract_pages(pdf, pages, output):

    reader = PdfReader(pdf)

    writer = PdfWriter()

    nums = [int(i)-1 for i in pages.split(",")]

    for n in nums:

        writer.add_page(reader.pages[n])

    with open(output, "wb") as f:

        writer.write(f)


def extract_text(pdf):

    doc = fitz.open(pdf)

    text = ""

    for page in doc:

        text += page.get_text()

    return text
