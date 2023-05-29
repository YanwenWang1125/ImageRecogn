from pathlib import Path

import cv2
import numpy as np
from pdf2image import convert_from_path
import pytesseract
import stat
import os

#1. cut the pdf only half tha page, (boxes only)
# https://www.i2tutorials.com/python-program-to-read-the-pdf-files/
# trimming and modify the pdf, PyPdf2

testFile = "example.pdf"
os.chmod(testFile,stat.S_IRUSR|stat.S_IRGRP|stat.S_IROTH|stat.S_IXUSR|stat.S_IRUSR|stat.S_IWUSR|stat.S_IWGRP|stat.S_IXGRP)


# Set the tesseract executable path
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Yanwe\Desktop\Dr.Dippel\tesseractEngine\tesseract.exe'


def pdf_to_images(pdf_file, poppler_path):
    return convert_from_path(pdf_file,dpi=300, poppler_path=poppler_path)


def ocr_handwriting(images):
    text = ""
    counter = 0
    for image in images:
        # Convert the image to grayscale

        gray_image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)

        # Apply OCR
        text = pytesseract.image_to_string(gray_image, config="--psm 6")
        if counter == 1:
            print("\n\n")
            print("paging...")
            for i in text.split("\n"):
                print(i+"\n")
        counter+=1
    return text


def main():
    pdf_file = testFile
    poppler_path = Path(r"C:\Users\Yanwe\Desktop\Dr.Dippel\popper\poppler-0.68.0\bin")

    # Convert PDF to images
    images = pdf_to_images(pdf_file, poppler_path)

    # Extract handwritten text using OCR
    extracted_text = ocr_handwriting(images)

    print("Extracted Text:")
    print(extracted_text)


if __name__ == "__main__":
    main()
