
import os
import re
from pdfminer.high_level import extract_text
from pdfminer.pdfparser import PDFSyntaxError
from pdfminer.pdfdocument import PDFDocument, PDFNoOutlines
from pdfminer.pdfparser import PDFParser


def extract_text_from_pdf(pdf_path):
    print('Check 8.2 ==============================================')
    folder = os.path.abspath('../fetched_pdfs')
    filenames = os.listdir(folder)
    outline_found = False
    tofind = ''
    print(outline_found)
    textOutput = ''

    titles = ''
    dictin = []
    for p in filenames:
        print(p)
        try:
            with open('fetched_pdfs/18582385.pdf', 'rb') as file:
                parser = PDFParser(file)
                document = PDFDocument(parser)
                try:
                    outlines = document.get_outlines()
                    print(outlines)
                    for level, title, dest, a, se in outlines:
                        print(f"Level: {level}, Title: {title}, a: {a}, se:{se}")
                        print(title)
                        titles = f"{title}"
                        if titles == "Methods":
                            outline_found = True
                            tofind = title
                            print(f'check 8.3 ==========={title} found in {p}')
                        print(outline_found)

                    if outline_found == True:
                        dictin.append({'l': level, 't': title})
                        print(dictin)
                        text = extract_text(file)
                        print('CHECK 8.3.1 =====================OUTLINE=========', outline_found)
                        print('CHECK 8.3.2 =====================TOFIND VALUE=========', tofind)
                        methods_text = re.search(rf'{tofind}(.*?)(?=^[A-Z][a-z]+\s+[A-Z][a-z]+|[^\n]+\Z)', text,
                                                 re.DOTALL | re.MULTILINE)

                        print(methods_text)
                        if methods_text:
                            print('check 8.4===============================================')
                            print(methods_text.group(1))
                            textOutput = methods_text.group(1)
                            print('check 8.5===============================================')
                except PDFNoOutlines:
                    outlines = None
                    # textOutput = GetOutline.extractMethodsFromPDF(p)


        except PDFSyntaxError:
            print(f'Error parsing PDF file : Invalid or corrupted PDF file.')

    return textOutput


pdf_path = "miappe2.pdf"
extracted_text = extract_text_from_pdf(pdf_path)
