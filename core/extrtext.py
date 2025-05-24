import io
import spacy
import json
from io import StringIO
from pdfminer.high_level import extract_text
import csv
import scispacy
import nltk
from nltk import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from core.calculateTFIDF import TFIDF
from core.text_classify import ClassifyText
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from core.textcls import Tc
import pandas as pd
nltk.download("stopwords")
nltk.download('wordnet') #for lemmatizing



class NLPProject:
    def __init__(self, text):
        #print('################### Processing text ########################')
        self.text = text
        self.sentences = nltk.sent_tokenize(self.text) # Use the NLTK sent_tokenize function to segment the text into sentences
        self.stop_words = set(stopwords.words('english'))
        self.stemmer = PorterStemmer()


    def tokenize_words(self, sentence):
        #print('################### Processing tokenization ########################')
        words = nltk.word_tokenize(sentence)
        return words

    def remove_stop_words(self, words):
        #print('################### Removing stop words  ########################')
        filtered_words = [word for word in words if word.lower() not in self.stop_words]
        return filtered_words



    def perform_lemmatizing(self,words):
        #print('################### Performing lemmatization  ########################')
        lemmatizer = WordNetLemmatizer()
        lemmatized_words = [lemmatizer.lemmatize(words) for words in words]
        return lemmatized_words


    def process_text(self):
        processed_sentences = []
        tokenized = []
        remStop = []
        for sentence in self.sentences:
            words = self.tokenize_words(sentence)
            tokenized.append(words)
            words = self.remove_stop_words(words)
            remStop.append(words)
            lemmatizing = self.perform_lemmatizing(words)
            processed_sentences.append(lemmatizing)

        return processed_sentences

    def calculate_similarity(self, sentences, miappe_guidelines, threshold=0.1):
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


    def save_miappe_to_csv(self, miappe_data, output_file):
        miappe_df = pd.DataFrame.from_dict(miappe_data, orient='index')
        miappe_df = miappe_df.transpose()
        miappe_df.to_csv(output_file, index=False)
        print(f"MIAPPE data saved to {output_file}.")


def extract_text_from_pdf(pdf_path):
    print("Extracting text from PDF...")
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

    if text:
        return text

def main():
    pdf_path = 'miappe2.pdf'
    text = extract_text_from_pdf(pdf_path)
    # Create an instance of the NLPProject class
    project = NLPProject(text)
    # Call the process_text() method to process the input text
    processed_text = project.process_text()
    document = ""
    print('#################Processed sentences ######################')
    # Join the list of sentences into a single string
    text = [' '.join(sent) for sent in processed_text]
    print(text)

    #miappe_data = project.calculate_similarity(text, miappe_guidelines)
    #project.save_miappe_to_csv(miappe_data, "miappe_data34.csv")
    print('===============================0end =================================================================')
    nlp = spacy.load("en_core_sci_lg")
    x = " , ".join(text)
    #print(x)
    doc = nlp(x)
    for ent in doc.ents:
        print('text:',ent.text)
        print('label:',ent.label_)

    Person = []
    Organisation = []

    LOC = []
    DATE = []
    NORP = []
    WORK_OF_ART = []
    CARDINAL = []
    PRODUCT = []
    PERCENT = []
    MONEY = []
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            Person.append(ent.text)
        elif ent.label_ =="ORG":
            Organisation.append(ent.text)
        elif ent.label_ =="GPE" or ent.label_ =="LOC":
            LOC.append(ent.text)
        elif ent.label_ =="DATE":
            DATE.append(ent.text)
        elif ent.label_ =="NORP":
            NORP.append(ent.text)
        elif ent.label_ =="WORK_OF_ART":
            WORK_OF_ART.append(ent.text)
        elif ent.label_ =="CARDINAL" or ent.label_=='ORDINAL':
            CARDINAL.append(ent.text)
        elif ent.label_ =="PRODUCT":
            PRODUCT.append(ent.text)
        elif ent.label_ =="PERCENT":
            PERCENT.append(ent.text)
        elif ent.label_ =="MONEY":
            MONEY.append(ent.text)
        elif ent.label_ =="FACT":
            MONEY.append(ent.text)
        elif ent.label_ =="LAW":
            MONEY.append(ent.text)
    #tfresults = TFIDF.calc('hello', processed_text)
    # Write data to CSV file
    '''   
    with open('tfidf_result.csv', mode='w', newline='') as file:
        fieldnames = ['Sentence', 'Topic scores', 'Assigned topic']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for data in tfresults:
            writer.writerow(data)
    '''

    #call text classifier
    #text_classification = ClassifyText.classify('values')
    #text_classification = Tc.textCl('test')
    print('****************************************scores *********************************************************')

    #print(tfresults)
    print('#################################text classification ##################################################')
    #print(text_classification)


if __name__ == "__main__":
    main()

