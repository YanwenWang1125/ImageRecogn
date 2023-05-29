import random
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

        image_array = np.array(image)
        gray_image = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
        text = pytesseract.image_to_string(image, config="--psm 6")
        if counter == 1:
            # Perform binary thresholding
            _, binary = cv2.threshold(gray_image, 150, 255, cv2.THRESH_BINARY_INV)

            # step1: Detect lines
            lines = cv2.HoughLinesP(binary, rho=1, theta=np.pi / 180, threshold=100, minLineLength=100, maxLineGap=10)

            # Step 2: Line Sorting and Grouping
            horizontal_lines = []
            vertical_lines = []
            for line in lines:
                x1, y1, x2, y2 = line[0]
                if abs(x2 - x1) > abs(y2 - y1):  # Horizontal line
                    horizontal_lines.append(line)
                else:  # Vertical line
                    vertical_lines.append(line)
                red = random.randint(0, 255)
                green = random.randint(0, 255)
                blue = random.randint(0, 255)
                cv2.rectangle(image_array, (x1, y1), (x2, y2), (red, green, blue), 2)

            # Step 3: Intersection Point Detection
            intersection_points = []
            for hline in horizontal_lines:
                for vline in vertical_lines:
                    x1, y1, x2, y2 = hline[0]
                    x3, y3, x4, y4 = vline[0]
                    intersection_x = int((x1 + x2 + x3 + x4) / 4)
                    intersection_y = int((y1 + y2 + y3 + y4) / 4)
                    intersection_points.append((intersection_x, intersection_y))

            # Step 4: Cell Extraction
            # print(range(len(intersection_points) - 1))
            # for i in range(len(intersection_points) - 1):
            #
            #     x1, y1 = intersection_points[i]
            #     x2, y2 = intersection_points[i + 1]
            #     x1 = max(0, x1)
            #     y1 = max(0, y1)
            #     x2 = min(image_array.shape[1], x2)
            #     y2 = min(image_array.shape[0], y2)
            #     cell_image = image_array[y1:y2, x1:x2]
            #     print(x1,y1,x2,y2)
            #     try:
            #         cell_text = pytesseract.image_to_string(cell_image, config="--psm 6")
            #         print(cell_text)
            #     except ValueError:
            #         pass

            # Draw border around the cell

            resized_image = cv2.resize(image_array, (1080, 960))
            # Display the image with cell borders
            cv2.imshow('image', resized_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

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
