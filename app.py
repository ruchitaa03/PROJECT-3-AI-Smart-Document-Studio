import streamlit as st
import tempfile
import os
import fitz
from deep_translator import GoogleTranslator
from gtts import gTTS

from utils import (
    image_to_pdf,
    docx_to_pdf,
    merge_pdfs,
    extract_pages,
    extract_text
)

st.set_page_config(page_title="AI Smart Document Studio", layout="wide")

st.title("📄 AI Smart Document Studio")

menu = st.sidebar.selectbox(
    "Select Feature",
    [
        "Merge Files",
        "Extract Pages",
        "Translate Text",
        "Generate Audio"
    ]
)

os.makedirs("output", exist_ok=True)

# ---------------- MERGE ----------------

if menu == "Merge Files":

    uploaded_files = st.file_uploader(
        "Upload PDF, DOCX or Images",
        type=["pdf", "docx", "png", "jpg", "jpeg"],
        accept_multiple_files=True
    )

    if st.button("Merge"):

        pdf_files = []

        for file in uploaded_files:

            suffix = file.name.split(".")[-1]

            temp = tempfile.NamedTemporaryFile(delete=False, suffix="."+suffix)
            temp.write(file.read())
            temp.close()

            path = temp.name

            if suffix == "pdf":
                pdf_files.append(path)

            elif suffix in ["png", "jpg", "jpeg"]:
                pdf_files.append(image_to_pdf(path))

            elif suffix == "docx":
                pdf_files.append(docx_to_pdf(path))

        output = "output/merged.pdf"

        merge_pdfs(pdf_files, output)

        st.success("Merged Successfully")

        pdf = fitz.open(output)

        for page in pdf:
            pix = page.get_pixmap()
            st.image(pix.tobytes("png"))

        with open(output, "rb") as f:
            st.download_button(
                "Download PDF",
                f,
                "merged.pdf"
            )

# ---------------- EXTRACT ----------------

elif menu == "Extract Pages":

    pdf_file = st.file_uploader("Upload PDF", type="pdf")

    pages = st.text_input("Pages Example : 1,3,5")

    if st.button("Extract"):

        temp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")

        temp.write(pdf_file.read())

        temp.close()

        output = "output/extracted.pdf"

        extract_pages(temp.name, pages, output)

        st.success("Pages Extracted")

        with open(output, "rb") as f:

            st.download_button(
                "Download",
                f,
                "Extracted.pdf"
            )

# ---------------- TRANSLATE ----------------

elif menu == "Translate Text":

    pdf = st.file_uploader("Upload PDF", type="pdf")

    language = st.selectbox(
        "Language",
        [
            "en",
            "hi",
            "kn",
            "ta",
            "te",
            "fr",
            "de",
            "es"
        ]
    )

    if st.button("Translate"):

        temp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")

        temp.write(pdf.read())

        temp.close()

        text = extract_text(temp.name)

        translated = GoogleTranslator(
            source="auto",
            target=language
        ).translate(text)

        st.text_area(
            "Translated Text",
            translated,
            height=300
        )

# ---------------- AUDIO ----------------

elif menu == "Generate Audio":

    text = st.text_area("Enter Text")

    lang = st.selectbox(
        "Language",
        ["en", "hi", "kn", "ta", "te"]
    )

    if st.button("Generate Audio"):

        tts = gTTS(text=text, lang=lang)

        audio = "output/audio.mp3"

        tts.save(audio)

        st.audio(audio)

        with open(audio, "rb") as f:

            st.download_button(
                "Download Audio",
                f,
                "audio.mp3"
            )
