"""
Preprocessing utilities:
- Extract text from uploaded files (PDF, TXT, DOCX [optional], images [optional OCR])
- Clean and normalize text
"""

from io import BytesIO
from pathlib import Path
from typing import Optional


def _extract_text_pdf(data: bytes) -> str:
	try:
		from pdfminer.high_level import extract_text
	except Exception:
		raise RuntimeError("pdfminer.six is required for PDF extraction. Add it to requirements and install.")
	with BytesIO(data) as bio:
		return extract_text(bio) or ""


def _extract_text_txt(data: bytes, encoding: str = "utf-8") -> str:
	try:
		return data.decode(encoding, errors="ignore")
	except Exception:
		return data.decode("latin-1", errors="ignore")


def _extract_text_docx(data: bytes) -> str:
	try:
		import docx  # python-docx
	except Exception:
		raise RuntimeError("python-docx not installed. Install it to enable DOCX support.")
	with BytesIO(data) as bio:
		doc = docx.Document(bio)
		return "\n".join(p.text for p in doc.paragraphs)


def _extract_text_image(data: bytes) -> str:
	# Optional OCR path using pytesseract if available
	try:
		from PIL import Image
		import pytesseract
	except Exception:
		raise RuntimeError("pytesseract and pillow are required for OCR. Install them to enable image OCR.")
	with BytesIO(data) as bio:
		img = Image.open(bio)
		return pytesseract.image_to_string(img)


def extract_text_from_file(data: bytes, filename: Optional[str]) -> str:
	"""
	Extract text based on file extension.
	Supported: .pdf, .txt, .docx (optional), common image formats (optional)
	"""
	suffix = (Path(filename).suffix.lower() if filename else "")
	if suffix == ".pdf":
		return _extract_text_pdf(data)
	if suffix == ".txt":
		return _extract_text_txt(data)
	if suffix == ".docx":
		return _extract_text_docx(data)
	if suffix in {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp"}:
		return _extract_text_image(data)
	# Fallback: try text decode
	return _extract_text_txt(data)


def clean_text(text: str) -> str:
	"""Basic normalization: strip, collapse whitespace, remove control chars."""
	import re
	text = text.replace("\r", " ")
	text = text.replace("\t", " ")
	text = re.sub(r"\s+", " ", text)
	return text.strip()

