import os
from spacy.matcher import Matcher

from core.get_outline  import GetOutline
from textblob import TextBlob
import re
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize


class MStudy:
    pdfFiles = []
    nlp = spacy.load("en_core_sci_lg")
    def listPdfFiles(miappePDF):
        print('check 4=========================================', miappePDF)
        print('pdf files', miappePDF)
        folder = os.path.abspath('../fetched_pdfs')
        filenames = os.listdir(folder)
        matching_files = []
        for f in filenames:
            if f[:-4] in [elem for elem in miappePDF]:
                matching_files.append(f)
                #print('matching file:', f)
        return matching_files
    @staticmethod
    def createPatterns():
        matcher = Matcher(MStudy.nlp.vocab)
        method_pattern = [{"LOWER": "methods"}, {"OP": "?"}]
        material_pattern = [{"LOWER": "materials"}, {"OP": "?"}]
        mm_pattern = [{"LOWER": "methods"}, {"LOWER": "and"}, {"LOWER": "materials"}]
        methodology_pattern = [{"LOWER": "methodology"}]
        am_pattern = [{"LOWER": "materials"}, {"LOWER": "and"}, {"LOWER": "methods"}]
        m_pattern = [{"LOWER": "material"}, {"LOWER": "and"}, {"LOWER": "method"}]
        ms_pattern = [{"LOWER": "materials"}, {"LOWER": "and"}, {"LOWER": "methods"}]
        pattern_list = [method_pattern, material_pattern, mm_pattern, methodology_pattern, am_pattern, m_pattern,
                        ms_pattern]
        for pattern in pattern_list:
            matcher.add("MaterialMethods", [pattern])
        return matcher

    def study_values(pdfFiles,categories):
        studyMiappe = []
        print(categories)
        print('check 6==========================================================')
        for p in pdfFiles:
            #print(p)

            findMethod = GetOutline.getOutLineAndText(p)


            if'Study title' in categories:study_title = MStudy.study_title(findMethod)
            else:study_title=''

            if'Study description' in categories:study_desc = MStudy.extractDescription(findMethod)
            else:study_desc = ''

            if 'Start date of study' in categories:start_date = MStudy.start_date(findMethod)
            else:start_date=''

            if 'End date of study' in categories:end_date = MStudy.end_date(findMethod)
            else:end_date=''

            if 'Contact institution' in categories:org_name = MStudy.org_name(findMethod)
            else:org_name=''

            if 'Geographic location (country)' in categories:locat = MStudy.locat(findMethod)
            else:locat=''

            if 'Type of experimental design' in categories:experiment_map_design = MStudy.emd(findMethod)
            else:experiment_map_design=''

            if 'Type of growth facility' in categories:typeofgrowth= MStudy.onto(findMethod)
            else:typeofgrowth=''

            if 'Geographic location (latitude)' in categories:geo_loc_lat = MStudy.findLat(findMethod)
            else:geo_loc_lat=''

            if 'Geographic location (longitude)' in categories:geo_loc_long = MStudy.findLong(findMethod)
            else:geo_loc_long=''

            if 'Geographic location (altitude)' in categories:geo_loc_alt = MStudy.findAlt(findMethod)
            else:geo_loc_alt=''
            if study_title or study_desc or end_date or start_date or org_name or locat or experiment_map_design or typeofgrowth or geo_loc_alt or geo_loc_long or geo_loc_lat:
                studyMiappe.append({
                    'PMID_stud': p, 'study_description': study_desc,'study_title':study_title,'end_date':end_date,
                    'start_date':start_date,'org_name':org_name,'location':locat,'emd':experiment_map_design,'ontology':typeofgrowth,
                    'latitude':geo_loc_lat,'longitude':geo_loc_long,'altitude':geo_loc_alt
                })
        #print('data from study',studyMiappe)
        return studyMiappe
    def start_date(p):
        doc = MStudy.nlp(p)
        entities = []
        for ent in doc.ents:
            if ent.label_ in ["DATE"]:
                entities.append(ent.text)
        return entities
        '''
        a = ['Methods', 'Methodology', 'Methods', 'Materials', 'Material and Method', 'Materials and Methods']
        try:

            pdf_text = extract_text("fetched_pdfs/" + p)
            for method in a:
                index = pdf_text.find(method)
                if index != -1:
                    whitespace_len = 0
                    for char in pdf_text[index + len(method):]:
                        if char == "\n":
                            whitespace_len += 1
                        else:
                            break
                    start_index = index + len(method) + whitespace_len
                    end_index = pdf_text.find("\n" * (whitespace_len + 1), start_index)
                    paragraph = pdf_text[start_index:end_index]
                    doc = MStudy.nlp(paragraph)
                    # Extract named entities
                    entities = []
                    for ent in doc.ents:
                        if ent.label_ in ["DATE"]:
                            entities.append((ent.text, ent.label_))
        except PDFSyntaxError:
            #print(f'Error parsing PDF file : Invalid or corrupted PDF file.')
        return entities
'''
    def end_date(p):
        doc = MStudy.nlp(p)
        # Extract named entities
        entities = []
        for ent in doc.ents:
            if ent.label_ in ["DATE"]:
                entities.append(ent.text)
        return entities
        '''
        entities = []
        a = ['Methods', 'Methodology', 'Methods', 'Materials', 'Material and Method', 'Materials and Methods']
        try:

            pdf_text = extract_text("fetched_pdfs/" + p)
            for method in a:
                index = pdf_text.find(method)
                if index != -1:
                    whitespace_len = 0
                    for char in pdf_text[index + len(method):]:
                        if char == "\n":
                            whitespace_len += 1
                        else:
                            break
                    start_index = index + len(method) + whitespace_len
                    end_index = pdf_text.find("\n" * (whitespace_len + 1), start_index)
                    paragraph = pdf_text[start_index:end_index]
                    doc = MStudy.nlp(paragraph)
                    # Extract named entities
                    entities = []
                    for ent in doc.ents:
                        if ent.label_ in ["DATE"]:
                            entities.append((ent.text, ent.label_))
        except PDFSyntaxError:
            #print(f'Error parsing PDF file : Invalid or corrupted PDF file.')
        return entities'''

    def org_name(p):
        entities = []
        doc = MStudy.nlp(p)
        for ent in doc.ents:
            if ent.label_ in ["ORG"]:
                entities.append(ent.text)
        return entities
        '''
        entities = []
        a = ['Methods', 'Methodology', 'Methods', 'Materials', 'Material and Method', 'Materials and Methods']
        try:

            pdf_text = extract_text("fetched_pdfs/" + p)
            for method in a:
                index = pdf_text.find(method)
                if index != -1:
                    whitespace_len = 0
                    for char in pdf_text[index + len(method):]:
                        if char == "\n":
                            whitespace_len += 1
                        else:
                            break
                    start_index = index + len(method) + whitespace_len
                    end_index = pdf_text.find("\n" * (whitespace_len + 1), start_index)
                    paragraph = pdf_text[start_index:end_index]
                    doc = MStudy.nlp(paragraph)
                    # Extract named entities
                    entities = []
                    for ent in doc.ents:
                        if ent.label_ in ["ORG"]:
                            entities.append((ent.text, ent.label_))
        except PDFSyntaxError:
            #print(f'Error parsing PDF file : Invalid or corrupted PDF file.')
        return entities
        '''
    def locat(p):
        doc = MStudy.nlp(p)
        countries = []
        for ent in doc.ents:
            if ent.label_ == "GPE" and ent.text not in countries:
                countries.append(ent.text)
        return countries
        '''
        countries = []
        a = ['Methods', 'Methodology', 'Methods', 'Materials', 'Material and Method', 'Materials and Methods']
        try:

            pdf_text = extract_text("fetched_pdfs/" + p)
            for method in a:
                index = pdf_text.find(method)
                if index != -1:
                    whitespace_len = 0
                    for char in pdf_text[index + len(method):]:
                        if char == "\n":
                            whitespace_len += 1
                        else:
                            break
                    start_index = index + len(method) + whitespace_len
                    end_index = pdf_text.find("\n" * (whitespace_len + 1), start_index)
                    paragraph = pdf_text[start_index:end_index]
                    doc = MStudy.nlp(paragraph)
                    countries = []
                    for ent in doc.ents:
                        if ent.label_ == "GPE" and ent.text not in countries:
                            countries.append(ent.text)
        except PDFSyntaxError:
            #print(f'Error parsing PDF file : Invalid or corrupted PDF file.')
        return countries
        '''

    def emd(p):
        urls = ""
        url_pattern = re.compile(r'https?://\S+')
        urls = re.findall(url_pattern, p)
        return urls
        '''
        a = ['Methods', 'Methodology', 'Methods', 'Materials', 'Material and Method', 'Materials and Methods']
        try:

            pdf_text = extract_text("fetched_pdfs/" + p)
            for method in a:
                index = pdf_text.find(method)
                if index != -1:
                    whitespace_len = 0
                    for char in pdf_text[index + len(method):]:
                        if char == "\n":
                            whitespace_len += 1
                        else:
                            break
                    start_index = index + len(method) + whitespace_len
                    end_index = pdf_text.find("\n" * (whitespace_len + 1), start_index)
                    paragraph = pdf_text[start_index:end_index]
                    url_pattern = re.compile(r'https?://\S+')
                    urls = re.findall(url_pattern, paragraph)

        except PDFSyntaxError:
            #print(f'Error parsing PDF file : Invalid or corrupted PDF file.')
        return urls '''

    def onto(p):

        accession_numbers = ""
        pattern = r"\bCO_\d{6}\b"
        accession_numbers = re.findall(pattern, p)
        return accession_numbers
        '''
        a = ['Methods', 'Methodology', 'Methods', 'Materials', 'Material and Method', 'Materials and Methods']
        try:
            pdf_text = extract_text("fetched_pdfs/" + p)
            for method in a:
                index = pdf_text.find(method)
                if index != -1:
                    whitespace_len = 0
                    for char in pdf_text[index + len(method):]:
                        if char == "\n":
                            whitespace_len += 1
                        else:
                            break
                    start_index = index + len(method) + whitespace_len
                    end_index = pdf_text.find("\n" * (whitespace_len + 1), start_index)
                    paragraph = pdf_text[start_index:end_index]
                    pattern = r"\bCO_\d{6}\b"
                    accession_numbers = re.findall(pattern, paragraph)

        except PDFSyntaxError:
            #print(f'Error parsing PDF file : Invalid or corrupted PDF file.')
        return accession_numbers '''
    def findLong(p):
        longitude = ""
        pattern = r"\b\d{1,3}\.\d{1,6}\b°?\s?[WwEe]\b"
        longitude = re.findall(pattern, p)
        return longitude
        '''
        a = ['Methods', 'Methodology', 'Methods', 'Materials', 'Material and Method', 'Materials and Methods']
        try:
            pdf_text = extract_text("fetched_pdfs/" + p)
            for method in a:
                index = pdf_text.find(method)
                if index != -1:
                    whitespace_len = 0
                    for char in pdf_text[index + len(method):]:
                        if char == "\n":
                            whitespace_len += 1
                        else:
                            break
                    start_index = index + len(method) + whitespace_len
                    end_index = pdf_text.find("\n" * (whitespace_len + 1), start_index)
                    paragraph = pdf_text[start_index:end_index]
                    pattern = r"\b\d{1,3}\.\d{1,6}\b°?\s?[WwEe]\b"
                    longitude = re.findall(pattern, paragraph)

        except PDFSyntaxError:
            #print(f'Error parsing PDF file : Invalid or corrupted PDF file.')
        return longitude '''

    def findLat(p):
        lat = ""
        pattern = r"\b\d{1,3}\.\d{1,6}\b°?\s?[NnSs]\b"
        lat = re.findall(pattern, p)
        return lat
        '''
        a = ['Methods', 'Methodology', 'Methods', 'Materials', 'Material and Method', 'Materials and Methods']
        try:
            pdf_text = extract_text("fetched_pdfs/" + p)
            for method in a:
                index = pdf_text.find(method)
                if index != -1:
                    whitespace_len = 0
                    for char in pdf_text[index + len(method):]:
                        if char == "\n":
                            whitespace_len += 1
                        else:
                            break
                    start_index = index + len(method) + whitespace_len
                    end_index = pdf_text.find("\n" * (whitespace_len + 1), start_index)
                    paragraph = pdf_text[start_index:end_index]
                    pattern  = r"\b\d{1,3}\.\d{1,6}\b°?\s?[NnSs]\b"
                    lat = re.findall(pattern, paragraph)

        except PDFSyntaxError:
            #print(f'Error parsing PDF file : Invalid or corrupted PDF file.')
        return lat'''

    def findAlt(p):
        alt = ""
        pattern = r"\b\d{1,5}(\.\d+)?\s?(meters?|m)\b"
        alt = re.findall(pattern, p)
        return alt
        '''
        a = ['Methods', 'Methodology', 'Methods', 'Materials', 'Material and Method', 'Materials and Methods']
        try:
            pdf_text = extract_text("fetched_pdfs/" + p)
            for method in a:
                index = pdf_text.find(method)
                if index != -1:
                    whitespace_len = 0
                    for char in pdf_text[index + len(method):]:
                        if char == "\n":
                            whitespace_len += 1
                        else:
                            break
                    start_index = index + len(method) + whitespace_len
                    end_index = pdf_text.find("\n" * (whitespace_len + 1), start_index)
                    paragraph = pdf_text[start_index:end_index]
                    pattern = r"\b\d{1,5}(\.\d+)?\s?(meters?|m)\b"
                    alt = re.findall(pattern, paragraph)

        except PDFSyntaxError:
            #print(f'Error parsing PDF file : Invalid or corrupted PDF file.')
        return alt '''
    def extractDescription(pdfFiles):
        #print("=====================",pdfFiles)
        ''' from summarizer import Summarizer
        model = Summarizer()
        result = model(pdfFiles, min_length=60)
        sums = ''.join(result)
        return sums '''
        blob = TextBlob(pdfFiles)
        # Split the text into sentences
        sentences = blob.sentences

        # Calculate the polarity (sentiment) of each sentence
        # You can use sentiment analysis to identify important sentences
        sentence_scores = [(sentence, sentence.sentiment.polarity) for sentence in sentences]

        # Sort sentences by polarity in descending order (most positive first)
        sorted_sentences = sorted(sentence_scores, key=lambda x: x[1], reverse=True)

        # Extract the top N sentences as the summary
        N = 3  # You can adjust N based on your desired summary length
        summary_sentences = [sentence[0] for sentence in sorted_sentences[:N]]

        # Combine the summary sentences into a summary text
        summary_text = " ".join(str(sentence) for sentence in summary_sentences)

        # Print or use the generated summary
        print(summary_text)

        return summary_text
        # Tokenizing the text
        '''stopWords = set(stopwords.words("english"))
        words = word_tokenize(pdfFiles)

        # Creating a frequency table to keep the
        # score of each word

        freqTable = dict()
        for word in words:
            word = word.lower()
            if word in stopWords:
                continue
            if word in freqTable:
                freqTable[word] += 1
            else:
                freqTable[word] = 1

        # Creating a dictionary to keep the score
        # of each sentence
        sentences = sent_tokenize(pdfFiles)
        sentenceValue = dict()

        for sentence in sentences:
            for word, freq in freqTable.items():
                if word in sentence.lower():
                    if sentence in sentenceValue:
                        sentenceValue[sentence] += freq
                    else:
                        sentenceValue[sentence] = freq

        sumValues = 0
        for sentence in sentenceValue:
            sumValues += sentenceValue[sentence]

        # Average value of a sentence from the original text
        print("8889((((((((((((((((((((((((((((((((((((((((((((((((((((",sentenceValue)
        print("***************************************",len(sentenceValue))
        average = int(sumValues / len(sentenceValue))
        # Storing sentences into our summary.
        summary = ''
        for sentence in sentences:
            if (sentence in sentenceValue) and (sentenceValue[sentence] > (1.2 * average)):
                summary += " " + sentence
        print(summary) '''

    def study_title(p):

        #model = Summarizer()
        #summary = model(p)
        #keywords = re.findall(r'\b\w+\b', summary.lower())
        #title_keywords = sorted(set(keywords), key=keywords.count, reverse=True)[:15]
        #title = ' '.join(title_keywords).capitalize() + '.'

        blob = TextBlob(p)
        noun_phrases = blob.noun_phrases
        top_noun_phrases = sorted(set(noun_phrases), key=noun_phrases.count, reverse=True)[:25]

        # Create a title by joining the most important noun phrases with appropriate punctuation
        title = ' '.join([phrase.capitalize() for phrase in top_noun_phrases]) + '.'

        '''
        a = ['Methods', 'Methodology', 'Methods', 'Materials', 'Material and Method', 'Materials and Methods']
        try:
            pdf_text = extract_text("fetched_pdfs/" + p)
            for method in a:
                index = pdf_text.find(method)
                if index != -1:
                    whitespace_len = 0
                    for char in pdf_text[index + len(method):]:
                        if char == "\n":
                            whitespace_len += 1
                        else:
                            break
                    start_index = index + len(method) + whitespace_len
                    end_index = pdf_text.find("\n" * (whitespace_len + 1), start_index)
                    paragraph = pdf_text[start_index:end_index]
                    text = paragraph.lower()
                    stop_words = ['the', 'of', 'and', 'a', 'in', 'to', 'for', 'on', 'with', 'is', 'that', 'by', 'at']
                    words = text.split()
                    filtered_words = [word for word in words if word not in stop_words]
                    title = " ".join(filtered_words)
                    title = title.title()
        except PDFSyntaxError:
            print(f'Error parsing PDF file : Invalid or corrupted PDF file.')'''
        return title



''' def extractMethodsFromPDF(pdfFiles):
        matcher = MStudy.createPatterns()
        studyMiappe = []
        model = Summarizer()
        for p in pdfFiles:
            #print('name of pdf file is ', p)
            try:
                with open('fetched_pdfs/' + p, 'rb') as file:
                    resource_manager = PDFResourceManager()
                    out_text = io.StringIO()
                    device = TextConverter(resource_manager, out_text, laparams=LAParams())
                    interpreter = PDFPageInterpreter(resource_manager, device)
                    for page in PDFPage.get_pages(file, caching=True, check_extractable=True):
                        interpreter.process_page(page)
                    page_text = out_text.getvalue()
                    doc = MStudy.nlp(page_text)
                    #print('the doc is ', doc)
                    matches = matcher(doc)
                    #print('the matches are ', matches)
                    for match_id, start, end in matches:
                        #print(match_id)
                        #print(end)
                        #print(start)
                        mm_text = doc[start:end].text
                        #print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
                        #print(mm_text)
                        for sent in doc.sents:
                            #print('************************************')
                            #print(sent)
                            if mm_text in sent.text:
                                #print('/////////////////////////////////////////////')
                                #print(mm_text)
                                body = sent
                                result = model(body, min_length=10,max_length=15)
                                sums = ''.join(result)
                                #print('=========================================')
                                #print(sums)
                    studyMiappe.append({
                       'PMID_stud': p, 'study_title': sums
                    })
            except PDFSyntaxError:
                #print(f'Error parsing PDF file {p}: Invalid or corrupted PDF file.')
                continue
            except Exception as e:
                #print(f'Error parsing PDF file {p}: {e}')
                continue
        return studyMiappe
'''


