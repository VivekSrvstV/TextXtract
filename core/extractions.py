import os
import io
import csv

import en_core_sci_lg
import pandas as pd
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
import spacy
import re
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import spacy
import en_core_sci_lg
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import concurrent.futures

class Extr:

    def extract_text_from_pdf(pdf_path):
        print("extract from pdf")
        resource_manager = PDFResourceManager()
        fake_file_handle = io.StringIO()
        converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
        page_interpreter = PDFPageInterpreter(resource_manager, converter)

        with open(pdf_path, 'rb') as fh:
            for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
                page_interpreter.process_page(page)

        converter.close()
        text = fake_file_handle.getvalue()
        fake_file_handle.close()

        print("test is :")
        # print(text)
        if text:
            return text

    def process_chunk(pages, page_interpreter):
        for page in pages:
            page_interpreter.process_page(page)

    def preprocess_text(text):
        print("removing line break and spaces")
        # Remove line breaks and extra white space
        text = re.sub(r'\s+', ' ', text.replace('\n', ' '))
        print("after removing ")
        print(text)
        return text

    def get_miappe_checklist(self):
        '''miappe_checklist_path = 'miappe.txt'
        with open(miappe_checklist_path, 'r', encoding='latin-1') as f:
            reader = csv.reader(f, delimiter='\t')
            miappe_checklist = {rows[0]: rows[1:] for rows in reader}'''
        print("the miappe checklist is ")
        miappe_guidelines = {
            'Experimental design': ['Plant material', 'Growing conditions', 'Experimental design'],
            'Phenotyping methods': ['Imaging methods', 'Data extraction and analysis', 'Trait ontology'],
            'Environmental conditions': ['Climate data', 'Soil data', 'Nutrient data'],
            'Metadata': ['Experiment metadata', 'Plant metadata', 'Imaging metadata'],
            'Data availability': ['Data sharing', 'Data archiving'],
            'Standards compliance': ['MIAPPE compliance', 'Ontology compliance', 'Standards compliance']
        }
        print (miappe_guidelines)
        return miappe_guidelines

    def get_miappe_data(text, miappe_checklist):
        print("get miappe data")
        nlp = spacy.load("en_core_sci_lg")
        doc = nlp(text)
        sentences = list(doc.sents)
        # Create a dictionary to store the MIAPPE data
        miappe_data = {key: [] for key in miappe_checklist.keys()}

        # Create a function to calculate cosine similarity between sentences and MIAPPE checklist items
        def calculate_cosine_similarity(sentence, item):
            vectorizer = TfidfVectorizer(stop_words='english', min_df=1, max_df=0.5)
            vectors = vectorizer.fit_transform([sentence, item]).toarray()
            return cosine_similarity(vectors)[0][1]

        # Loop through the sentences in the text
        print("check 4.1")
        for sentence in sentences:
            # Loop through the MIAPPE checklist items
            for item, values in miappe_checklist.items():
                # Loop through the values for each item
                for value in values:
                    # Calculate cosine similarity between sentence and item value
                    similarity = calculate_cosine_similarity(str(sentence), value)
                    #print(similarity)
                    # If similarity is above a certain threshold, add the sentence to the MIAPPE data for that item
                    if similarity > 0.7:
                        miappe_checklist[item].append(str(sentence))

        return miappe_data
    def main(self):
        # Define the PDF file to extract text from
        pdf_path = '../data/miappe.pdf'
        print("inside main")
        # Extract text from PDF file
        print("check 1")
        text = Extr.extract_text_from_pdf(pdf_path)
        print ("check 2")
        # Preprocess the text
        text = Extr.preprocess_text(text)
        print("check 3")
        # Get the MIAPPE checklist
        miappe_checklist = Extr.get_miappe_checklist(self)
        print("check 4")
        # Get the MIAPPE data from the text
        print(text)
        miappe_data = Extr.get_miappe_data(text, miappe_checklist)
        print("check 5")
        # Convert the MIAPPE data to a pandas dataframe
        miappe_df = pd.DataFrame(miappe_data)
        print("check 6")
        # Save the MIAPPE data to a CSV file
        miappe_df.to_csv('miappe_data1.csv', index=False)
        print("check 7")
        # Print the MIAPPE data
        print(miappe_df)
