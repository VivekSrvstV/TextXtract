import nltk
import spacy
import json
from io import StringIO

from nltk.corpus import stopwords
from pdfminer.high_level import extract_text
import csv
class MM:
    def runModel(self):
        # Load pre-trained English NER model
        nlp = spacy.load('en_core_sci_lg')
        # Define the path to the PDF file
        pdf_path = '../data/miappe.pdf'
        # Extract text content from the PDF file
        text = extract_text(pdf_path)
        doc = nlp(text)
        sentences = nltk.sent_tokenize(doc)
        print('Text in a list :',sentences)
        stop_words = set(stopwords.words('english'))
        print('Stop word in the text : ',stop_words)

        print(sentences)


def main():
    MM.runModel('hello')


if __name__ == "__main__":
    main()