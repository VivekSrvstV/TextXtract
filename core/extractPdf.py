from collections import defaultdict, Counter

import PyPDF2
from PyPDF2 import PdfReader
from flask import json
from pdfminer.pdfparser import PDFParser, PDFSyntaxError
from pdfminer.pdfdocument import PDFDocument
from datetime import datetime
import os
import nltk
from reportlab.lib.pagesizes import portrait, letter
from reportlab.platypus import SimpleDocTemplate, TableStyle
import os
from pdfminer.high_level import extract_text

nltk.download('punkt')
from nltk.tokenize import word_tokenize
from core.allinone import ALlSearch
import csv
import pandas as pd
import scispacy
import spacy
import requests


# Open the PDF file
class ExtPDF:
    def getDetails(self):
        filename = "data_results/data.xlsx"
        result_dict = {}
        with open(filename, "r") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")
            header = next(csv_reader)  # skip the header row
            for row in csv_reader:
                print('row value check 1 : ####', row)
                row_dict = {}
                for i, value in enumerate(row):
                    print('i value check #####', i)
                    print('value check #####', value)
                    print('row value check ####', row[i])
                    row_dict[header[i]] = value
                    # result_dict[row[i]] = row_dict
                    result_dict[row[i]] = value
        # print(result_dict)
        return result_dict

    def readCSV(self):
        file_path = os.path.join(os.path.dirname(__file__), '..', 'data_results', 'data.csv')
        with open(file_path, mode='r') as csv_file:
            # Use a CSV reader to read the file
            csv_reader = csv.reader(csv_file)
            # Get the header row
            header = next(csv_reader)
            # Create an empty list to store the dictionaries
            dict_list = []
            # Loop through the remaining rows and create a dictionary for each row
            for row in csv_reader:
                row_dict = {}
                for i in range(len(header)):
                    row_dict[header[i]] = row[i]
                dict_list.append(row_dict)
        # Print the list of dictionaries
        # print(dict_list)
        return dict_list

    def totalPubBasedOnDate(self):
        dict_list = ExtPDF.readCSV(self)
        # Count the occurrences of publication_name
        pub_count = Counter(d.get('Publication Date') for d in dict_list if d.get('Publication Date'))

        #pub_count = Counter(d['Publication Date'] for d in dict_list)
        # Convert the Counter object into a list of dictionaries with the desired format
        result = [{'date': k, 'publications': v} for k, v in pub_count.items()]
        # Print the result
        print(result)
        return result

    def totalPubBasedOnPubname(self):
        dict_list = ExtPDF.readCSV(self)
        # Count the occurrences of publication_name
        pub_count = Counter(d['Citation'] for d in dict_list)
        # Convert the Counter object into a list of dictionaries with the desired format
        result = [{'Citation': k, 'publications': v} for k, v in pub_count.items()]
        # Print the result
        print(result)
        return result

    def csvtojson(self):
        csvfilepath = 'data_results/data.csv'
        jsonfilepath = 'data.json'
        # read csv
        data = {}
        with open(csvfilepath) as csvfile:
            csvReader = csv.DictReader(csvfile)
            for rows in csvReader:
                print(rows)
                id = rows['title']
                data[id] = rows
        # create json
        with open(jsonfilepath, 'w') as jsonfile:
            jsonfile.write(json.dumps(data, indent=4))
        return data

    def readPDFTitle(file):
        base_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi'
        folder = os.path.abspath('../fetched_pdfs')
        for filename in os.listdir(folder):
            # Remove the .pdf extension
            pmid = filename[:-4]
            params = {'db': 'pubmed', 'retmode': 'json', 'id': pmid}
            response = requests.get(base_url, params=params)
            data = response.json()
            article_info = data['result'][pmid]
            title = article_info['title']

            print("===========name of publication =========", title)
            return title

    def getAuthor(file):

        base_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi'
        folder = os.path.abspath('../fetched_pdfs')
        for filename in os.listdir(folder):
            # Remove the .pdf extension
            pmid = filename[:-4]
            params = {'db': 'pubmed', 'retmode': 'json', 'id': pmid}
            response = requests.get(base_url, params=params)
            data = response.json()
            article_info = data['result'][pmid]
            authors = article_info['authors']  # Extracting author information
            author_names = ', '.join([author['name'] for author in authors])  # Concatenating author names
            print("===========name of authors =========",author_names)
            return author_names


    def getPubName(file):
        base_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi'
        folder = os.path.abspath('../fetched_pdfs')
        for filename in os.listdir(folder):
            # Remove the .pdf extension
            pmid = filename[:-4]
            params = {'db': 'pubmed', 'retmode': 'json', 'id': pmid}
            response = requests.get(base_url, params=params)
            data = response.json()
            article_info = data['result'][pmid]
            publication_name = article_info['source']

            print("===========name of publication =========", publication_name)
            return publication_name

    def getPubDate(self):
        base_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi'
        folder = os.path.abspath('../fetched_pdfs')
        for filename in os.listdir(folder):
            # Remove the .pdf extension
            pmid = filename[:-4]
            params = {'db': 'pubmed', 'retmode': 'json', 'id': pmid}
            response = requests.get(base_url, params=params)
            data = response.json()
            article_info = data['result'][pmid]
            publication_date = article_info['pubdate']

            print("===========name of publication =========", publication_date)
            return publication_date


    def getKeywords(file):
        keyword_list = []

        parser = PDFParser(file)
        document = PDFDocument(parser)
        if '/Keywords' in document.info[0]:
            keywords = document.info[0]['/Keywords']
        else:
            keywords = ''

        keyword_list.append(keywords)
        return keyword_list


    def pubdate(pdf_file):
        pb = []

        pdf_content = pdf_file.read()
        text = pdf_content.decode('utf-8', 'ignore')
        tokens = word_tokenize(text)

        publication_date = None
        for i, token in enumerate(tokens):
            if token.lower() in ['publication', 'date', 'of']:
                if tokens[i - 1].lower() == 'publication' and tokens[i + 1].lower() == 'date':
                    publication_date = tokens[i + 2]
                    break
        if publication_date:
            print(f'Publication date: {publication_date}')
        else:
            print('Publication date not found.')
        pb.append(publication_date)
        return pb


    def getResult(search_key, data):
        print(search_key)
        extracted_data = []

        for entry in data:
            extracted_entry = {}
            for key in search_key:
                if key in entry:
                    extracted_entry[key] = entry[key]
                else:
                    extracted_entry[key] = None
            extracted_data.append(extracted_entry)

        return extracted_data


    def getSpcs(file):
        print("find out species")
        nlp = spacy.load("en_ner_jnlpba_md")
        species = []
        text = extract_text(file)
        doc = nlp(text)
        for ent in doc.ents:
            if ent.label_ == "ORGANISM" or ent.label_ == "ORGANISM_SUBDIVISION" or ent.label_ == "ORGANISM_SUBSTANCE":
                species.append(ent.text)

        return species


    def getOnto(file):
        print("get onto")
        nlp = spacy.load("en_ner_jnlpba_md")
        onto = []
        text = extract_text(file)
        doc = nlp(text)
        for ent in doc.ents:
            if ent.label_ == "DNA" or ent.label_ == "CELL" or ent.label_ == "TYPE" or ent.label_ == "CELL_LINE" or ent.label_ == "RNA" or ent.label_ == "PROTEIN":
                onto.append(ent.text)

        return onto


    def getGene(file):
        print("gene")
        nlp = spacy.load("en_ner_bionlp13cg_md")
        gene = []
        text = extract_text(file)
        doc = nlp(text)
        for ent in doc.ents:
            if ent.label_ == "GENE_OR_GENE_PRODUCT":
                gene.append(ent.text)

        return gene


    def getDcs(file):
        print("disease")
        nlp = spacy.load("en_ner_bc5cdr_md")
        diseases = []
        text = extract_text(file)
        doc = nlp(text)  # Process text with spaCy
        for ent in doc.ents:
            if ent.label_ == "DISEASE":
                diseases.append(ent.text)

        return diseases


    def getPhenotype(self):
        print("phenotype")
        pheno = []
        return pheno


    def findOutput(search_key):
        print(search_key)
        folder = os.path.abspath('../fetched_pdfs')
        data = []
        for filename in os.listdir(folder):
            try:
                with open(os.path.join(folder, filename), "rb") as file:
                    # Extract text from PDF
                    #for items in search_key:
                    spc = ExtPDF.getSpcs(file)
                    onto = ExtPDF.getOnto(file)
                    gne = ExtPDF.getGene(file)
                    des = ExtPDF.getDcs(file)
                    pn = ExtPDF.getPubName(file)
                    ttl = ExtPDF.readPDFTitle(file)
                    ath = ExtPDF.getAuthor(file)
                    pd = ExtPDF.getPubDate(file)
                    phn = ExtPDF.getPhenotype(file)
                    '''if items.lower() == 'Species'.lower() or items.lower() == 'Ontology'.lower() \
                                or items.lower() == 'Gene'.lower() or  items.lower() == 'Disease'.lower() \
                                or items.lower() == 'Publication Name'.lower() or items.lower() == 'Title'.lower() \
                                or items.lower() == 'Author'.lower() or items.lower() == 'Publication Date'.lower() \
                                or items.lower() == 'Phenotype'.lower():'''
                    if spc or onto or gne or des or pn or ttl or ath or pd or phn :
                        data.append({'pmid': filename[:-4], 'spc': spc,'onto':onto,'gne':gne,'des':des,'pn':pn,'ttl':ttl,'ath':ath,'pd':pd,'phn':phn})

            except Exception as e:
                # Handle the exception
                # print("Error reading PDF file:", filename)
                print("Error message:", str(e))

        return data
