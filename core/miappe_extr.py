import io

import nltk
import pdfminer.high_level
import pdfminer.layout
import re
import json
from nltk.corpus import stopwords
import spacy
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
class Miappe:
    #step1 load json and create a dictionary
    def loadjson(self):
        # Load MIAPPE guidelines from a JSON file
        with open('../miappe_data/miappe.json', 'r') as f:
            miappe_json = json.load(f)
        # Extract MIAPPE guidelines from JSON and store them in a dictionary
        miappe_guidelines = {}
        for category, guidelines in miappe_json.items():
            miappe_guidelines[category] = guidelines
        print(miappe_guidelines)
        return (miappe_guidelines)
    #step2 open pdf and extract clean text and process extracted text
    def extractPdf(self):
        with open('../data/miappe.pdf', 'rb') as pdf_file:
            # Parse the PDF and get a generator object for the pages
            pages = pdfminer.high_level.extract_pages(pdf_file)
            # Loop through each page and extract the text
            full_text = ''
            for page_layout in pages:
                for element in page_layout:
                    if isinstance(element, pdfminer.layout.LTTextBoxHorizontal):
                        full_text += element.get_text().strip() + ' '

            # Process the extracted text
            #text = full_text.lower()
            text = re.sub(r'[^a-zA-Z0-9\s]', '', full_text)
            #text = re.sub(r'\s+', ' ', text)
            text = re.sub(r'\s+', ' ', text.replace('\n', ' '))
            stop_words = set(stopwords.words('english'))
            tokens = nltk.word_tokenize(text)
            filtered_text = [word for word in tokens if word not in stop_words]
            # Print the processed text
            print(filtered_text)
            return filtered_text
    #step 3 Tokenize the processed text into sentences using a natural language processing library such as spaCy.
    def nlpTokenize(text):
        # Load the spaCy English language model
        nlp = spacy.load('en_core_sci_lg')
        # Tokenize the processed text into sentences
        print(text)
        text2 = ' '.join(text)
        doc = nlp(text2)
        print("PDF file text:", text2)
        if not text2:
            print("Error: Empty PDF file text!")
            return None
        sentences = [sent.text.strip() for sent in doc.sents]
        return sentences

    # Calculate the cosine similarity between each sentence and each MIAPPE guideline
    def calculate_similarity(sentences, miappe_guidelines, threshold=0.8):
        vectorizer = TfidfVectorizer()
        miappe_data = {}
        for guideline_name, guideline_sentences in miappe_guidelines.items():
            guideline_vectors = vectorizer.fit_transform(guideline_sentences)
            for sentence in sentences:
                sentence_vector = vectorizer.transform([sentence])
                similarities = cosine_similarity(sentence_vector, guideline_vectors)
                max_similarity = similarities.max()
                if max_similarity > threshold:
                    if guideline_name not in miappe_data:
                        miappe_data[guideline_name] = []
                    miappe_data[guideline_name].append(sentence)
        return miappe_data

    def save_miappe_to_csv(miappe_data, output_file):
        miappe_df = pd.DataFrame.from_dict(miappe_data, orient='index')
        miappe_df = miappe_df.transpose()
        miappe_df.to_csv(output_file, index=False)
        print(f"MIAPPE data saved to {output_file}.")
    #step end calling all the methods
    def main(self):
        jsonDict = Miappe.loadjson(self)
        pdffiletertext = Miappe.extractPdf(self)
        tokenizeNlp = Miappe.nlpTokenize(pdffiletertext)
        miappe_data = Miappe.calculate_similarity(tokenizeNlp,jsonDict)
        Miappe.save_miappe_to_csv(miappe_data, "../data/miappe_data2.csv")



