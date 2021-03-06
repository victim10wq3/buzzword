"""
Random utilities this app needs
"""
import os

from explore.models import Corpus
from .models import OCRUpdate
from django.core.exceptions import ObjectDoesNotExist


def markdown_to_buzz_input(markdown):
    """
    User can use markdown when correcting OCR
    We need to parse out headers and bulletpoints into <meta> features
    """
    return markdown


def get_raw_text_for_ocr(slug, pdf):
    this_pdf = OCRUpdate.objects.filter(pdf=pdf)
    if this_pdf:
        latest = this_pdf.latest("timestamp")
        return latest.text
    # todo: transfer raw to OCRUpdate on load?
    # corpath = corpus.path.rsplit("-parsed")[0]
    corpath = os.path.join("static", "plaintexts", slug)
    text_version = os.path.basename(pdf.path.replace(".pdf", ".txt"))
    corfile = os.path.join(corpath, text_version)
    with open(corfile, "r") as fo:
        data = fo.read()
    return data


def _get_pdf_paths(slug):
    pdfs_path = os.path.join("static", "pdfs", slug + "-pdfs")
    pdfs = [
        os.path.join(pdfs_path, i) for i in os.listdir(pdfs_path) if i.endswith(".pdf")
    ]
    return list(sorted(pdfs))
